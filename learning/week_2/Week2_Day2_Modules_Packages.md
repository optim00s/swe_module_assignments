# Həftə 2 - Gün 2: Modullar, Paketlər və Standart Kitabxana

`learning/week_2/Week2_Day2_Modules_Packages.md`

---

## 1. Modullar (Modules)

### 1.1 Modul Nədir?

**Modul** — Python kodunu ehtiva edən tək bir `.py` faylıdır. Hər bir Python faylı avtomatik olaraq bir moduldur. Modullar kodun **təkrar istifadə edilməsini**, **məntiqi bölünməsini** və **ad çakışmalarının qarşısının alınmasını** (namespacing) təmin edir.

Modulların mövcudluğu olmadan bütün kod tək bir faylda olmalı idi — bu, böyük layihələrdə idarəolunmaz xaosa gətirib çıxardı. Modullar sayəsində hər bir funksional hissə öz faylında yaşayır və lazım olduqda digər fayllar tərəfindən istifadə edilir.

### 1.2 Modul Yaratmaq

Modul yaratmaq üçün sadəcə `.py` faylı yaratmaq kifayətdir:

```python
# ===== math_utils.py =====
# Bu fayl özü bir moduldur — adı "math_utils"

"""Riyazi əməliyyatlar üçün yardımçı funksiyalar."""

PI = 3.14159265358979          # Modul səviyyəsində sabit

def circle_area(radius):
    """Dairənin sahəsini hesablayır: π × r²"""
    if radius < 0:
        raise ValueError("Radius mənfi ola bilməz")
    return PI * radius ** 2

def circle_circumference(radius):
    """Dairənin çevrəsini hesablayır: 2 × π × r"""
    if radius < 0:
        raise ValueError("Radius mənfi ola bilməz")
    return 2 * PI * radius

def factorial(n):
    """n! (n faktorial) hesablayır — rekursiv."""
    if not isinstance(n, int) or n < 0:
        raise ValueError("n mənfi olmayan tam ədəd olmalıdır")
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

### 1.3 Modul İdxal Etmək (Import)

Python-da modulu istifadə etmək üçün `import` ifadəsindən istifadə olunur. Bir neçə fərqli import üsulu var:

```python
# === 1. Tam modul import ===
import math_utils

area = math_utils.circle_area(5)       # Modul adı ilə müraciət
print(math_utils.PI)                    # 3.14159...

# === 2. Konkret elementləri import etmək ===
from math_utils import circle_area, PI

area = circle_area(5)                   # Birbaşa ad ilə müraciət (modul adı lazım deyil)
print(PI)

# === 3. Bütün elementləri import etmək (tövsiyə OLUNMUR) ===
from math_utils import *

# Bu, modulun bütün public adlarını cari namespace-ə gətirir
# Hansı adın haradan gəldiyini izləmək çətinləşir — ad çakışmaları yaranır

# === 4. Alias (ləqəb) ilə import ===
import math_utils as mu

area = mu.circle_area(5)               # Qısa ad ilə müraciət
```

**Import Üsullarının Müqayisəsi:**

| Üsul | Sintaksis | Üstünlük | Çatışmazlıq |
|---|---|---|---|
| `import module` | `module.func()` | Ad mənbəyi aydın | Uzun yazılış |
| `from module import func` | `func()` | Qısa yazılış | Çox import olsa çaşqınlıq |
| `from module import *` | `func()` | Ən qısa | ❌ Ad çakışması, mənbə naməlum |
| `import module as alias` | `alias.func()` | Qısa + aydın mənbə | Standart alias-lar var |

> [!tip] **Best Practice — Import Sıralaması (PEP 8)**
> Import-ları faylın əvvəlində, bu sıra ilə yazın:
> 1. **Standart kitabxana** modulları (`os`, `sys`, `json`)
> 2. **Üçüncü tərəf** kitabxanalar (`requests`, `flask`)
> 3. **Yerli (local)** modullar (`from . import utils`)
>
> Hər qrup arasında boş sətir qoyun. `isort` aləti bunu avtomatik edir.

### 1.4 `__name__` və `__main__`

Hər Python modulunun `__name__` adlı xüsusi atributu var. Əgər modul **birbaşa** icra olunursa, `__name__` dəyəri `"__main__"` olur. Əgər başqa modul tərəfindən **import edilərsə**, `__name__` dəyəri modulun adı olur.

Bu mexanizm modulun həm müstəqil proqram, həm də import edilə bilən kitabxana kimi işləməsinə imkan verir.

```python
# ===== math_utils.py =====

def circle_area(radius):
    return 3.14159 * radius ** 2

# Bu blok YALNIZ fayl birbaşa icra olunduqda işləyir
# Import edildikdə işləmir
if __name__ == "__main__":
    # Test / demo kodu buraya yazılır
    print("math_utils modulu test edilir...")
    print(f"r=5 üçün sahə: {circle_area(5)}")
    print(f"r=10 üçün sahə: {circle_area(10)}")
    print("Bütün testlər keçdi!")

# Əgər bu fayl birbaşa çalışdırılsa:
#   python math_utils.py → __name__ == "__main__" → test kodu işləyir
#
# Əgər başqa fayldan import edilsə:
#   import math_utils → __name__ == "math_utils" → test kodu işləmir
```

> [!tip] **Best Practice — `if __name__ == "__main__"` Həmişə İstifadə Edin**
> Hər modula bu bloku əlavə etmək yaxşı vərdişdir. Bu:
> 1. Modulu həm kitabxana, həm müstəqil skript kimi istifadəyə uyğun edir
> 2. Test/demo kodunu production koddan ayırır
> 3. Import zamanı yan effektlərin (side effects) qarşısını alır

### 1.5 `__all__` — Eksport Nəzarəti

`__all__` — moduldan `from module import *` ilə import ediləcək adları müəyyən edən list-dir.

```python
# ===== utils.py =====
__all__ = ["public_function", "PublicClass"]  # Yalnız bunlar export olunacaq

def public_function():
    """Bu funksiya import * ilə gələcək."""
    return "public"

def _private_helper():
    """Alt xətt ilə başlayan — konvensiyaya görə private."""
    return "private"

class PublicClass:
    pass

class _InternalClass:
    pass
```

---

## 2. Paketlər (Packages)

### 2.1 Paket Nədir?

**Paket** — modulları məntiqi qruplara təşkil edən **qovluqdur**. Python-da paket bir qovluqdan və (əvvəlki versiyalarda) `__init__.py` faylından ibarətdir. Paketlər modulları iyerarxik şəkildə strukturlaşdırmağa imkan verir — böyük layihələrdə bu mütləqdir.

### 2.2 Paket Strukturu

```
my_project/                      # Layihənin kök qovluğu
├── main.py                      # Giriş nöqtəsi (entry point)
├── config.py                    # Konfiqurasiya
├── utils/                       # "utils" paketi (qovluq)
│   ├── __init__.py              # Paketi Python paketi kimi tanıdır
│   ├── file_utils.py            # Fayl əməliyyatları modulu
│   ├── string_utils.py          # String əməliyyatları modulu
│   └── validation.py            # Yoxlama funksiyaları modulu
├── data/                        # "data" paketi
│   ├── __init__.py
│   ├── readers.py               # Data oxuma modulları
│   └── writers.py               # Data yazma modulları
└── tests/                       # Test paketi
    ├── __init__.py
    ├── test_file_utils.py
    └── test_validation.py
```

### 2.3 `__init__.py` Faylı

`__init__.py` — paket qovluğunun Python paketi olaraq tanınmasını təmin edən xüsusi fayldır. Python 3.3+-da "namespace packages" üçün bu fayl məcburi deyil, lakin onu istifadə etmək **tövsiyə olunur**, çünki paket başlangıcı (initialization) və interfeys təyini üçün istifadə edilir.

```python
# ===== utils/__init__.py =====

"""Utils paketi — ümumi yardımçı funksiyalar."""

# Alt modullardan vacib funksiyaları paketin özünə gətirmək
# Bu sayədə istifadəçi utils.validate() yaza bilər,
# utils.validation.validate() yazmaq əvəzinə
from .validation import validate_email, validate_score
from .string_utils import clean_text, truncate
from .file_utils import read_lines, write_lines

# Paketin versiyası
__version__ = "1.0.0"

# __all__ — 'from utils import *' nəzarəti
__all__ = [
    "validate_email",
    "validate_score",
    "clean_text",
    "truncate",
    "read_lines",
    "write_lines",
]
```

```python
# ===== utils/validation.py =====

"""Giriş məlumatlarının yoxlanması funksiyaları."""

def validate_email(email):
    """Sadə email format yoxlaması."""
    if not isinstance(email, str):
        raise TypeError("Email string olmalıdır")
    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValueError(f"Etibarsız email formatı: {email}")
    return True

def validate_score(score, min_val=0, max_val=100):
    """Balın icazə verilən aralıqda olduğunu yoxlayır."""
    if not isinstance(score, (int, float)):
        raise TypeError(f"Bal ədəd olmalıdır, {type(score).__name__} verildi")
    if not (min_val <= score <= max_val):
        raise ValueError(f"Bal {min_val}-{max_val} aralığında olmalıdır, {score} verildi")
    return True
```

### 2.4 Nisbi və Mütləq Import

```python
# ===== Mütləq import (Absolute Import) — tam yol göstərilir =====
# Layihənin kökündən başlayaraq tam modul yolu
from utils.validation import validate_email
from utils.file_utils import read_lines
import utils.string_utils

# ===== Nisbi import (Relative Import) — cari mövqeyə görə =====
# Yalnız paket daxilində istifadə olunur
# '.' — cari paket, '..' — üst paket

# utils/validation.py daxilindən eyni paketdəki digər modula müraciət:
from .string_utils import clean_text       # Eyni paketdə (utils/)
from .file_utils import read_lines         # Eyni paketdə (utils/)
from ..config import DATABASE_URL          # Üst paketdə (my_project/)
```

| Import Növü | Sintaksis | Üstünlük | Çatışmazlıq |
|---|---|---|---|
| **Mütləq** | `from utils.validation import ...` | Aydın, refactor-a davamlı | Uzun yollar |
| **Nisbi** | `from .validation import ...` | Qısa, paket daxilində rahat | Paket kənarında işləmir |

> [!tip] **Best Practice — Mütləq Import Üstünlük Verilir**
> PEP 8 mütləq import-u tövsiyə edir, çünki daha aydındır və refactoring zamanı daha az sınır. Nisbi import yalnız çox böyük paketlərdə və ya paket daxili modullar arasında qısa müraciət lazım olduqda istifadə olunmalıdır.

---

## 3. Python Standart Kitabxanası

Python-un **"batteries included"** (batareyalar daxildir) fəlsəfəsi — əlavə kitabxana yükləmədən çox sayda tapşırığı yerinə yetirə biləcəyiniz deməkdir. Standart kitabxana 200-dən çox modul ehtiva edir.

### 3.1 `os` — Əməliyyat Sistemi İnterfeisi

```python
import os

# Cari işçi qovluq (Current Working Directory)
cwd = os.getcwd()
print(cwd)  # C:\Users\Sharaf\Desktop\project

# Qovluq mövcudluğunu yoxlamaq
print(os.path.exists("data"))          # True/False
print(os.path.isfile("config.json"))   # Fayldır?
print(os.path.isdir("data"))           # Qovluqdur?

# Qovluq yaratmaq
os.makedirs("output/reports/2026", exist_ok=True)
# exist_ok=True — artıq varsa xəta vermir

# Qovluqdakı faylları siyahılamaq
entries = os.listdir(".")              # Cari qovluqdakı bütün elementlər
print(entries)  # ['main.py', 'data', 'config.json', ...]

# Fayl yolunu birləşdirmək — OS-a uyğun separator istifadə edir
filepath = os.path.join("data", "students", "scores.csv")
# Windows: "data\\students\\scores.csv"
# Linux:   "data/students/scores.csv"

# Fayl adı və qovluğunu ayırmaq
directory = os.path.dirname("/home/user/data/file.txt")  # "/home/user/data"
filename = os.path.basename("/home/user/data/file.txt")  # "file.txt"
name, ext = os.path.splitext("report.csv")               # ("report", ".csv")

# Mühit dəyişənləri (Environment Variables)
home = os.environ.get("HOME", "Tapılmadı")
path = os.environ.get("PATH", "")
```

### 3.2 `pathlib` — Müasir Yol İdarəetməsi (Python 3.4+)

`pathlib` — `os.path`-in müasir, obyektyönümlü alternatividir. Yol əməliyyatlarını daha oxunaqlı və intuitiv edir.

```python
from pathlib import Path

# Yol yaratmaq
current = Path(".")                        # Cari qovluq
home = Path.home()                         # İstifadəçinin ev qovluğu
data_dir = Path("data") / "students"       # '/' operatoru ilə birləşdirmə!

# Fayl/qovluq əməliyyatları
config = Path("config.json")
print(config.exists())                     # Mövcuddur?
print(config.is_file())                    # Fayldır?
print(config.suffix)                       # ".json" — uzantı
print(config.stem)                         # "config" — adsız uzantı
print(config.parent)                       # "." — ana qovluq
print(config.resolve())                    # Tam (absolute) yol

# Qovluq yaratmaq
output = Path("output") / "reports"
output.mkdir(parents=True, exist_ok=True)  # İç-içə qovluqları yaradır

# Faylları siyahılamaq
for py_file in Path(".").glob("**/*.py"):  # Rekursiv axtarış
    print(py_file)

# Fayl oxumaq/yazmaq — with open() əvəzinə qısa yol
content = Path("data.txt").read_text(encoding="utf-8")       # Oxumaq
Path("output.txt").write_text("Salam Dünya", encoding="utf-8")  # Yazmaq
```

> [!tip] **Best Practice — `pathlib` istifadə edin, `os.path` deyil**
> Yeni kodda **həmişə** `pathlib.Path` istifadə edin. `os.path` funksional üslubdadır (`os.path.join(a, b)`), `pathlib` isə obyektyönümlüdür (`a / b`). `pathlib` daha oxunaqlı, daha az xətaya meyilli və cross-platform-dur. Köhnə kod ilə uyğunluq lazım olduqda `str(path)` ilə string-ə çevirə bilərsiniz.

### 3.3 `sys` — Python Interpretatoru ilə Əlaqə

```python
import sys

# Python versiyası
print(sys.version)          # "3.12.0 (main, Oct 2 2023, ...)"
print(sys.version_info)     # sys.version_info(major=3, minor=12, micro=0, ...)

# Komanda sətri arqumentləri
# python script.py arg1 arg2
print(sys.argv)             # ['script.py', 'arg1', 'arg2']

# Modul axtarış yolları
print(sys.path)             # Python-un modul axtardığı qovluqlar siyahısı

# Platformaya aid məlumatlar
print(sys.platform)         # "win32", "linux", "darwin" (macOS)

# Proqramdan çıxmaq
# sys.exit(0)               # Normal çıxış (0 = uğurlu)
# sys.exit(1)               # Xəta ilə çıxış (0-dan fərqli = xəta)

# Rekursiya limiti
print(sys.getrecursionlimit())  # Default: 1000
# sys.setrecursionlimit(5000)   # Limiti artırmaq (ehtiyatla!)
```

### 3.4 `datetime` — Tarix və Vaxt

```python
from datetime import datetime, date, time, timedelta

# Cari tarix və vaxt
now = datetime.now()
print(now)                           # 2026-03-19 14:30:45.123456

# Ayrı-ayrı komponentlər
print(now.year)                      # 2026
print(now.month)                     # 3
print(now.day)                       # 19
print(now.hour)                      # 14
print(now.weekday())                 # 3 (0=Bazar ertəsi, 6=Bazar)

# Xüsusi tarix yaratmaq
birthday = date(1990, 5, 15)
meeting = datetime(2026, 4, 1, 10, 30)  # 1 Aprel 2026, saat 10:30

# Formatlaşdırma (datetime → string)
formatted = now.strftime("%d/%m/%Y %H:%M")   # "19/03/2026 14:30"
formatted_2 = now.strftime("%B %d, %Y")      # "March 19, 2026"

# Parsing (string → datetime)
parsed = datetime.strptime("2026-03-19", "%Y-%m-%d")

# Tarixlər arası fərq (timedelta)
future = now + timedelta(days=30, hours=5)    # 30 gün 5 saat sonra
difference = datetime(2026, 12, 31) - now     # İki tarix arasındakı fərq
print(difference.days)                        # Qalan gün sayı

# Tarixləri müqayisə etmək
deadline = datetime(2026, 4, 1)
if now < deadline:
    print("Vaxt var!")
```

### 3.5 `collections` — Xüsusi Data Strukturları

```python
from collections import Counter, defaultdict, OrderedDict, deque, namedtuple

# === Counter — Elementləri sayır ===
text = "proqramlaşdırma"
letter_count = Counter(text)
print(letter_count.most_common(3))   # Ən çox rast gələn 3 hərf

inventory = Counter({"alma": 5, "armud": 3})
sold = Counter({"alma": 2, "armud": 1})
remaining = inventory - sold         # Counter({'alma': 3, 'armud': 2})

# === defaultdict — Mövcud olmayan key üçün default dəyər ===
grouped = defaultdict(list)
students = [("A", "Əli"), ("B", "Vəli"), ("A", "Leyla"), ("B", "Nigar")]
for grade, name in students:
    grouped[grade].append(name)
# {'A': ['Əli', 'Leyla'], 'B': ['Vəli', 'Nigar']}

# === deque — İki tərəfli növbə (Double-Ended Queue) ===
# List-dən fərqli olaraq, əvvəldən əlavə/silmə O(1)-dir
task_queue = deque(["task_1", "task_2", "task_3"])
task_queue.appendleft("urgent_task")  # Əvvələ əlavə: O(1)
task_queue.append("task_4")            # Sona əlavə: O(1)
first = task_queue.popleft()           # Əvvəldən silmə: O(1)

# maxlen ilə sabit ölçülü bufer (köhnə elementlər avtomatik atılır)
recent_logs = deque(maxlen=5)
for i in range(10):
    recent_logs.append(f"log_{i}")
print(list(recent_logs))  # ['log_5', 'log_6', 'log_7', 'log_8', 'log_9']
```

### 3.6 `itertools` — İterasiya Alətləri

```python
import itertools

# === chain() — Bir neçə iterable-ı ardıcıl birləşdirir ===
list_a = [1, 2, 3]
list_b = [4, 5, 6]
list_c = [7, 8, 9]
combined = list(itertools.chain(list_a, list_b, list_c))
# [1, 2, 3, 4, 5, 6, 7, 8, 9]

# === product() — Dekart hasili (bütün kombinasiyalar) ===
colors = ["red", "blue"]
sizes = ["S", "M", "L"]
variants = list(itertools.product(colors, sizes))
# [('red', 'S'), ('red', 'M'), ('red', 'L'), ('blue', 'S'), ...]

# === combinations() — Kombinasiyalar (sıra nəzərə alınmır) ===
team_members = ["Əli", "Vəli", "Leyla", "Nigar"]
pairs = list(itertools.combinations(team_members, 2))
# [('Əli', 'Vəli'), ('Əli', 'Leyla'), ..., ('Leyla', 'Nigar')]

# === groupby() — Ardıcıl eyni elementləri qruplaşdırır ===
data = sorted([("A", 85), ("B", 72), ("A", 91), ("B", 68)], key=lambda x: x[0])
for grade, students in itertools.groupby(data, key=lambda x: x[0]):
    print(f"Qrup {grade}: {list(students)}")

# === islice() — Generator-dan slice almaq ===
numbers = itertools.count(1)           # 1, 2, 3, ... (sonsuz)
first_ten = list(itertools.islice(numbers, 10))   # İlk 10 element
# [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

### 3.7 `functools` — Funksional Proqramlaşdırma Alətləri

```python
import functools

# === lru_cache — Funksiyanın nəticələrini cache-ləyir ===
@functools.lru_cache(maxsize=128)
def fibonacci(n):
    """Fibonacci ədədi — cache ilə O(n) mürəkkəblik."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(100))  # Dərhal cavab verir (cache sayəsində)
print(fibonacci.cache_info())  # Cache statistikası

# === partial — Funksiyanın bəzi parametrlərini əvvəlcədən təyin etmək ===
def power(base, exponent):
    return base ** exponent

square = functools.partial(power, exponent=2)   # exponent=2 sabitlənir
cube = functools.partial(power, exponent=3)

print(square(5))   # 25
print(cube(3))     # 27

# === reduce — Siyahını tək dəyərə azaltmaq ===
numbers = [1, 2, 3, 4, 5]
product = functools.reduce(lambda a, b: a * b, numbers)
# ((((1*2)*3)*4)*5) = 120
```

### 3.8 Digər Faydalı Standart Kitabxana Modulları

| Modul | Təyinat | Nümunə İstifadə |
|---|---|---|
| `math` | Riyazi funksiyalar | `math.sqrt(16)`, `math.log(100)` |
| `random` | Təsadüfi ədədlər | `random.randint(1, 100)`, `random.choice(list)` |
| `string` | String sabitləri | `string.ascii_letters`, `string.digits` |
| `re` | Regulyar ifadələr | `re.findall(r"\d+", text)` |
| `hashlib` | Kriptoqrafik hash | `hashlib.sha256(b"data").hexdigest()` |
| `copy` | Obyekt kopyalama | `copy.deepcopy(nested_list)` |
| `pprint` | Gözəl çap | `pprint.pprint(complex_dict)` |
| `argparse` | CLI arqumentləri | Komanda sətri interfeysi yaratmaq |
| `logging` | Log sistemi | Strukturlaşdırılmış log mesajları |
| `typing` | Tip göstəriciləri | `List[int]`, `Optional[str]`, `Dict[str, Any]` |
| `dataclasses` | Data sinifləri | Boilerplate-siz sinif təyini |
| `enum` | Nömrələmələr | Sabit dəyərlər toplusu |
| `abc` | Abstract siniflər | İnterfeys təyini |
| `sqlite3` | SQLite verilənlər bazası | Yerli DB əməliyyatları |
| `urllib` | URL əməliyyatları | URL parsing, encoding |
| `shutil` | Fayl əməliyyatları | Kopyalama, silmə, arxivləşdirmə |
| `tempfile` | Müvəqqəti fayllar | Müvəqqəti fayl/qovluq yaratmaq |
| `glob` | Fayl pattern matching | `glob.glob("*.csv")` |

---

## 4. Gün 2 — Xülasə

| Mövzu | Əsas Nöqtə |
|---|---|
| **Modul** | Hər `.py` faylı bir moduldur; `import` ilə istifadə olunur |
| **Import üsulları** | `import x`, `from x import y`, `import x as z` |
| **`__name__`** | Birbaşa icrada `"__main__"`, importda modul adı |
| **Paket** | Modulları qruplaşdıran qovluq + `__init__.py` |
| **Nisbi/Mütləq import** | Mütləq (`from pkg.mod import`) üstünlük verilir |
| **Standart kitabxana** | `os`, `pathlib`, `sys`, `datetime`, `collections`, `itertools`, `functools` |

---

> [!note] **Növbəti Gün**
> **Gün 3**-də API-lərlə işləmək (HTTP sorğuları, JSON emalı) və web scraping əsaslarını öyrənəcəyik.
