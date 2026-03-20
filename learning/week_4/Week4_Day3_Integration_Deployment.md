# Həftə 4 - Gün 3: İnteqrasiya və Yerləşdirmə (Deployment)

`learning/week_4/Week4_Day3_Integration_Deployment.md`

---

## 1. Verilənlər Bazası İnteqrasiyası

### 1.1 Niyə Verilənlər Bazası?

İndiyə qədər məlumatları fayllarda (CSV, JSON) saxladıq. Bu, kiçik layihələr üçün kafi olsa da, böyük həcmli data, eyni vaxtlı müraciət və mürəkkəb sorğular üçün **verilənlər bazası (database)** lazımdır.

| Xüsusiyyət | Fayl (CSV/JSON) | Verilənlər Bazası |
|---|---|---|
| **Axtarış** | O(n) — bütün faylı oxumaq lazım | O(log n) — indeks ilə sürətli |
| **Eynivaxtlı müraciət** | Çətin, data korrupsiyası riski | Daxili lock/transaction mexanizmi |
| **Mürəkkəb sorğular** | Əl ilə filtrasiya/qruplaşdırma | SQL ilə güclü sorğu dili |
| **Data bütövlüyü** | Heç bir zəmanət | Constraints, foreign keys |
| **Ölçek** | Kiçik data (MB) | Kiçikdən çox böyüyə (TB) |

### 1.2 SQLite — Python-un Daxili Verilənlər Bazası

**SQLite** — server tələb etməyən, faylda saxlanan, yüngül relational verilənlər bazasıdır. Python-un standart kitabxanasında `sqlite3` modulu ilə gəlir — əlavə qurulum lazım deyil.

```python
import sqlite3
from pathlib import Path

# === Verilənlər bazasını yaratmaq / bağlanmaq ===
# Fayl yoxdursa avtomatik yaradılır
db_path = "school.db"
connection = sqlite3.connect(db_path)

# Cursor — SQL sorğularını icra etmək üçün vasitə
cursor = connection.cursor()

# === Cədvəl yaratmaq (CREATE TABLE) ===
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        grade TEXT CHECK(grade IN ('A', 'B', 'C', 'D', 'F')),
        score REAL CHECK(score >= 0 AND score <= 100),
        enrollment_date TEXT DEFAULT (date('now'))
    )
""")

# === Məlumat əlavə etmək (INSERT) ===
# Parametrli sorğu — SQL injection-dan qoruyur
cursor.execute(
    "INSERT INTO students (name, surname, grade, score) VALUES (?, ?, ?, ?)",
    ("Əli", "Həsənov", "A", 92.5)
)

# Birdən çox sətir əlavə etmək
students_data = [
    ("Vəli", "Məmmədov", "B", 85.0),
    ("Leyla", "Əliyeva", "A", 95.5),
    ("Nigar", "Quliyeva", "C", 72.0),
    ("Rəşad", "İsmayılov", "B", 81.3),
    ("Günel", "Hüseynova", "D", 58.7),
]
cursor.executemany(
    "INSERT INTO students (name, surname, grade, score) VALUES (?, ?, ?, ?)",
    students_data
)

# Dəyişiklikləri saxlamaq — commit olmadan dəyişikliklər itir!
connection.commit()
```

> [!warning] **Diqqət — SQL Injection**
> Heç vaxt f-string və ya string birləşdirmə ilə SQL sorğusu yazmayın:
> ```python
> # ❌ TƏHLÜKƏLİ — SQL injection
> cursor.execute(f"SELECT * FROM students WHERE name = '{user_input}'")
>
> # ✅ TƏHLÜKƏSİZ — parametrli sorğu
> cursor.execute("SELECT * FROM students WHERE name = ?", (user_input,))
> ```
> Parametrli sorğular zərərli SQL kodunun icrasının qarşısını alır.

### 1.3 Məlumat Sorğulama (SELECT)

```python
import sqlite3

connection = sqlite3.connect("school.db")
# Row factory — nəticəni dict-ə bənzər formatda qaytarır
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

# === Bütün tələbələr ===
cursor.execute("SELECT * FROM students")
all_students = cursor.fetchall()
for student in all_students:
    print(f"{student['name']} {student['surname']}: {student['score']}")

# === Filtrasiya (WHERE) ===
cursor.execute(
    "SELECT name, surname, score FROM students WHERE score >= ? ORDER BY score DESC",
    (80,)
)
top_students = cursor.fetchall()
print("\n80+ bal alan tələbələr:")
for s in top_students:
    print(f"  {s['name']} {s['surname']}: {s['score']}")

# === Aqreqat funksiyalar ===
cursor.execute("""
    SELECT
        grade,
        COUNT(*) as student_count,
        ROUND(AVG(score), 2) as avg_score,
        MAX(score) as max_score,
        MIN(score) as min_score
    FROM students
    GROUP BY grade
    ORDER BY avg_score DESC
""")
print("\nQrup statistikası:")
for row in cursor.fetchall():
    print(f"  Qrup {row['grade']}: {row['student_count']} tələbə, "
          f"ortalama: {row['avg_score']}, maks: {row['max_score']}")

# === Yeniləmə (UPDATE) ===
cursor.execute(
    "UPDATE students SET score = ?, grade = ? WHERE name = ? AND surname = ?",
    (95.0, "A", "Vəli", "Məmmədov")
)

# === Silmə (DELETE) ===
cursor.execute("DELETE FROM students WHERE score < ?", (60,))

connection.commit()
connection.close()
```

### 1.4 Kontekst Meneceri ilə Verilənlər Bazası

```python
import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db_connection(db_path):
    """
    Verilənlər bazası bağlantısı üçün kontekst meneceri.
    Bağlantını avtomatik commit edir (uğurlu) və ya rollback edir (xəta).
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()        # Xəta olmadıqda commit
    except Exception:
        conn.rollback()      # Xəta olduqda geri al
        raise
    finally:
        conn.close()         # Həmişə bağla

# İstifadə
with get_db_connection("school.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE grade = 'A'")
    a_students = cursor.fetchall()
    for s in a_students:
        print(f"{s['name']} {s['surname']}: {s['score']}")
```

### 1.5 Repository Pattern — Data Girişinin Strukturlaşdırılması

```python
import sqlite3
from contextlib import contextmanager

class StudentRepository:
    """
    Tələbə data girişi üçün repository (ambar) sinifi.

    Bütün SQL sorğuları burada cəmləşir — qalan kod SQL bilmir.
    Bu, Separation of Concerns prinsipinin tətbiqidir.
    """

    def __init__(self, db_path):
        self.db_path = db_path

    @contextmanager
    def _get_cursor(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_all(self):
        """Bütün tələbələri qaytarır."""
        with self._get_cursor() as cur:
            cur.execute("SELECT * FROM students ORDER BY name")
            return [dict(row) for row in cur.fetchall()]

    def get_by_id(self, student_id):
        """ID ilə tək tələbəni qaytarır."""
        with self._get_cursor() as cur:
            cur.execute("SELECT * FROM students WHERE id = ?", (student_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def search(self, name_query):
        """Ad ilə axtarış (qismən uyğunluq)."""
        with self._get_cursor() as cur:
            cur.execute(
                "SELECT * FROM students WHERE name LIKE ? OR surname LIKE ?",
                (f"%{name_query}%", f"%{name_query}%")
            )
            return [dict(row) for row in cur.fetchall()]

    def add(self, name, surname, grade, score):
        """Yeni tələbə əlavə edir və ID-ni qaytarır."""
        with self._get_cursor() as cur:
            cur.execute(
                "INSERT INTO students (name, surname, grade, score) VALUES (?, ?, ?, ?)",
                (name, surname, grade, score)
            )
            return cur.lastrowid

    def update_score(self, student_id, new_score):
        """Tələbənin balını yeniləyir."""
        with self._get_cursor() as cur:
            cur.execute(
                "UPDATE students SET score = ? WHERE id = ?",
                (new_score, student_id)
            )
            return cur.rowcount > 0

    def delete(self, student_id):
        """Tələbəni silir."""
        with self._get_cursor() as cur:
            cur.execute("DELETE FROM students WHERE id = ?", (student_id,))
            return cur.rowcount > 0

    def get_statistics(self):
        """Ümumi statistika."""
        with self._get_cursor() as cur:
            cur.execute("""
                SELECT
                    COUNT(*) as total,
                    ROUND(AVG(score), 2) as avg_score,
                    MAX(score) as max_score,
                    MIN(score) as min_score
                FROM students
            """)
            return dict(cur.fetchone())


# İstifadə — SQL kodundan tamamilə təcrid olunmuş
repo = StudentRepository("school.db")

# all_students = repo.get_all()
# student = repo.get_by_id(1)
# new_id = repo.add("Kamran", "Əhmədov", "B", 83.5)
# repo.update_score(new_id, 88.0)
# stats = repo.get_statistics()
```

---

## 2. Python Tətbiqlərinin Paketlənməsi

### 2.1 Layihə Strukturu

Peşəkar bir Python layihəsinin standart strukturu:

```
my_project/
├── src/                         # Mənbə kodu (source code)
│   └── my_project/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── student.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
├── tests/                       # Testlər
│   ├── __init__.py
│   ├── test_main.py
│   └── test_helpers.py
├── docs/                        # Sənədlər
├── pyproject.toml               # Layihə konfiqurasiyası (müasir standart)
├── requirements.txt             # Asılılıqlar siyahısı
├── README.md                    # Layihə təsviri
├── .gitignore                   # Git-in nəzərə almayacağı fayllar
└── LICENSE                      # Lisenziya
```

### 2.2 `pyproject.toml` — Müasir Layihə Konfiqurasiyası

`pyproject.toml` — PEP 621 ilə standartlaşdırılmış layihə konfiqurasiya faylıdır. Köhnə `setup.py` və `setup.cfg`-nin yerinə gəlir.

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "student-tracker"
version = "1.0.0"
description = "Tələbə idarəetmə sistemi"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.10"
authors = [
    {name = "Şəraf", email = "sharaf@example.com"},
]

dependencies = [
    "requests>=2.28.0",
    "click>=8.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "mypy>=1.0.0",
    "ruff>=0.1.0",
]

[project.scripts]
student-tracker = "my_project.main:cli"
```

### 2.3 `requirements.txt` — Asılılıqlar

```txt
# requirements.txt — pip install -r requirements.txt
requests==2.31.0
click==8.1.7
python-dotenv==1.0.0

# requirements-dev.txt — development asılılıqları
# pip install -r requirements-dev.txt
pytest==7.4.3
mypy==1.7.1
ruff==0.1.8
```

### 2.4 Virtual Environment (Mühit)

**Virtual environment** — hər layihə üçün müstəqil Python mühiti yaradır. Bu, fərqli layihələrdə fərqli versiyalı kitabxanaların istifadəsinə imkan verir.

```bash
# Virtual environment yaratmaq
python -m venv .venv

# Aktivləşdirmək
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Asılılıqları yükləmək
pip install -r requirements.txt

# Cari mühitdəki paketləri görmək
pip list

# Mühiti söndürmək
deactivate
```

> [!tip] **Best Practice — Virtual Environment Həmişə İstifadə Edin**
> Hər layihə üçün **mütləq** ayrı virtual environment yaradın. Sistem Python-una birbaşa paket yükləmək:
> 1. Fərqli layihələr arasında versiya konfliktinə səbəb olur
> 2. Layihənin hansı paketlərə ehtiyacı olduğunu müəyyənləşdirməyi çətinləşdirir
> 3. Sistemi stabil saxlamaq üçün vacibdir

---

## 3. Docker ilə Konteynerləşdirmə

### 3.1 Docker Nədir?

**Docker** — tətbiqləri **konteyner** adlanan izolə olunmuş mühitlərdə işlətmək üçün platformdır. Konteyner, tətbiqin işləməsi üçün lazım olan hər şeyi (kod, kitabxanalar, sistem alətləri, konfiqurasiya) bir yerdə paketləyir.

| Konsept | Tərif | Analoji |
|---|---|---|
| **Image** | Konteynerin şablonu (read-only) | Tort resepti |
| **Container** | Image-dən yaradılmış işlək instans | Reseptdən hazırlanmış tort |
| **Dockerfile** | Image-in necə qurulacağını təsvir edən fayl | Reseptin addımları |
| **Registry** | Image-lərin saxlanıldığı mərkəz | Docker Hub — onlayn resept kitabı |

### 3.2 Docker-in Faydaları

| Problem | Docker-siz | Docker ilə |
|---|---|---|
| "Mənim kompüterimdə işləyir" | Ətraf mühit fərqlər | Eyni konteyner hər yerdə |
| Asılılıq konflikti | Versiya uyğunsuzluğu | İzolə olunmuş mühitlər |
| Deployment | Mürəkkəb qurulum | `docker run` — bir komanda |
| Ölçekləmə | Əl ilə server konfiqurasiyası | Konteyner klonlanması |

### 3.3 Dockerfile Yazmaq

```dockerfile
# ===== Dockerfile =====

# Əsas image — Python 3.12 (slim versiya — yalnız lazımi komponentlər)
FROM python:3.12-slim

# Mühit dəyişənləri
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# İşçi qovluğu təyin etmək
WORKDIR /app

# Əvvəlcə yalnız asılılıqları kopyalamaq (cache optimallaşdırması)
# Asılılıqlar dəyişmədikcə bu qat yenidən qurulmayacaq
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sonra mənbə kodunu kopyalamaq
COPY src/ ./src/
COPY config/ ./config/

# Tətbiqin dinlədiyi port
EXPOSE 8000

# Tətbiqi başlatmaq
CMD ["python", "-m", "src.my_project.main"]
```

### 3.4 `.dockerignore`

```
# .dockerignore — Docker kontekstinə daxil edilməyəcək fayllar
__pycache__
*.pyc
.venv/
.env
.git/
.gitignore
*.md
tests/
docs/
.mypy_cache/
.pytest_cache/
```

### 3.5 Docker Əmrləri

```bash
# Image qurmaq
docker build -t student-tracker:1.0 .

# Konteyneri başlatmaq
docker run -d --name my-app -p 8000:8000 student-tracker:1.0

# Çalışan konteynerləri görmək
docker ps

# Konteyner log-larını görmək
docker logs my-app

# Konteynerə daxil olmaq
docker exec -it my-app /bin/bash

# Konteyneri dayandırmaq və silmək
docker stop my-app
docker rm my-app
```

### 3.6 Docker Compose — Çoxlu Xidmət

`docker-compose.yml` — birdən çox konteynerin birlikdə idarə edilməsi üçün konfiqurasiya faylıdır.

```yaml
# docker-compose.yml
version: "3.9"

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/school
    depends_on:
      - db
    volumes:
      - ./data:/app/data

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: school
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

```bash
# Bütün xidmətləri başlatmaq
docker compose up -d

# Log-ları izləmək
docker compose logs -f

# Dayandırmaq
docker compose down
```

> [!tip] **Best Practice — Docker Image Optimallaşdırması**
> 1. **Slim/Alpine image** istifadə edin — ölçünü kəskin azaldır
> 2. **Multi-stage build** — qurulum alətlərini final image-ə daxil etməyin
> 3. **Layer caching** — tez-tez dəyişən faylları Dockerfile-ın sonuna qoyun
> 4. **Non-root user** — təhlükəsizlik üçün root istifadəçi ilə işləməyin
> 5. **`.dockerignore`** — lazımsız faylları kontekstdən çıxarın

---

## 4. Gün 3 — Xülasə

| Mövzu | Əsas Nöqtə |
|---|---|
| **SQLite** | `sqlite3` modulu; SQL ilə CRUD əməliyyatları; parametrli sorğular |
| **SQL Injection** | `?` placeholder istifadə edin, f-string istifadə etməyin |
| **Repository Pattern** | SQL-i business logic-dən ayırmaq |
| **Layihə strukturu** | `src/`, `tests/`, `pyproject.toml`, `requirements.txt` |
| **Virtual Environment** | `python -m venv .venv`; hər layihə üçün ayrı mühit |
| **Docker** | Konteynerləşdirmə; Dockerfile, docker-compose |

---

> [!note] **Növbəti Həftə**
> **Həftə 5, Gün 1**-də kod keyfiyyəti prinsipləri — təmiz kod (clean code), kod review-lar və linting alətlərini öyrənəcəyik.
