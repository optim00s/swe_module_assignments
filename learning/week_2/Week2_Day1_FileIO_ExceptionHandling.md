# Həftə 2 - Gün 1: Fayl Əməliyyatları (File I/O) və Xətaların İdarə Edilməsi (Exception Handling)

`learning/week_2/Week2_Day1_FileIO_ExceptionHandling.md`

---

## 1. Fayl Əməliyyatları (File I/O)

### 1.1 Fayl I/O Nədir?

**File I/O (Input/Output)** — proqramın xarici fayllarla əlaqə qurma mexanizmidir. **Input** fayldan məlumat oxumaq, **Output** isə fayla məlumat yazmaq deməkdir. Proqramlar yalnız yaddaşda (RAM) işləyir — proqram bağlandıqda yaddaşdakı bütün məlumatlar itirilir. Məlumatları **davamlı** (persistent) saxlamaq üçün onları diskdəki fayllara yazmaq lazımdır.

Fayl əməliyyatlarının əsas addımları:
1. **Açmaq** (open) — fayla bağlantı yaratmaq
2. **Oxumaq/Yazmaq** (read/write) — əməliyyat icra etmək
3. **Bağlamaq** (close) — bağlantını kəsmək və resursları azad etmək

### 1.2 `open()` Funksiyası və Fayl Rejimləri

`open()` — Python-un daxili (built-in) funksiyasıdır və fayl obyekti (file object / file handle) qaytarır. Bu obyekt vasitəsilə faylla əməliyyatlar aparılır.

```python
# open() funksiyasının əsas sintaksisi
# file_object = open(file_path, mode, encoding)

# Sadə fayl açma
file = open("data.txt", "r", encoding="utf-8")
content = file.read()
file.close()   # Faylı MÜTLƏQ bağlamaq lazımdır
```

**Fayl Rejimləri (Modes):**

| Rejim | Ad | İzah |
|---|---|---|
| `"r"` | Read | Yalnız oxumaq (default). Fayl yoxdursa `FileNotFoundError` |
| `"w"` | Write | Yazmaq. Fayl varsa **məzmunu silinir**, yoxdursa yaradılır |
| `"a"` | Append | Əlavə etmək. Faylın sonuna yazır, mövcud məzmun qorunur |
| `"x"` | Exclusive Create | Yeni fayl yaradır. Fayl artıq varsa `FileExistsError` |
| `"r+"` | Read+Write | Oxumaq və yazmaq. Fayl yoxdursa xəta |
| `"w+"` | Write+Read | Yazmaq və oxumaq. Fayl varsa məzmunu silinir |
| `"b"` | Binary | İkili rejim. Digər rejimlərlə birləşdirilir: `"rb"`, `"wb"` |

| Rejim | Fayl varsa | Fayl yoxdursa | Oxumaq | Yazmaq |
|---|---|---|---|---|
| `"r"` | Açır | ❌ Xəta | ✅ | ❌ |
| `"w"` | Silir, açır | Yaradır | ❌ | ✅ |
| `"a"` | Sona əlavə | Yaradır | ❌ | ✅ (sona) |
| `"x"` | ❌ Xəta | Yaradır | ❌ | ✅ |
| `"r+"` | Açır | ❌ Xəta | ✅ | ✅ |

> [!warning] **Diqqət — `"w"` rejimi təhlükəlidir**
> `"w"` rejimi faylı açdığı anda **bütün mövcud məzmunu silir** — hətta siz heç nə yazmamış olsanız belə. Mövcud fayla əlavə etmək üçün həmişə `"a"` rejimini istifadə edin. Əgər faylın üzərinə yazmaq istəyirsinizsə, əvvəlcə ehtiyat nüsxə (backup) yaratmaq yaxşı praktikadır.

### 1.3 Kontekst Meneceri — `with` İfadəsi

`with` ifadəsi faylı avtomatik olaraq bağlayır — hətta xəta baş versə belə. Bu, **resurs idarəetməsinin** ən təhlükəsiz və Pythonic üsuludur.

`with` ifadəsi Python-un **context manager protocol**-unu (`__enter__` və `__exit__` metodları) istifadə edir. Blokdan çıxıldıqda (normal və ya xəta ilə) `__exit__` metodu avtomatik çağırılır.

```python
# ❌ SƏHV YANAŞMA — faylı əl ilə bağlamaq
file = open("data.txt", "r")
content = file.read()
# Əgər burada xəta baş versə, file.close() heç vaxt çağırılmayacaq!
# Bu, resurs sızıntısına (resource leak) səbəb olur
file.close()

# ✅ DÜZGÜN YANAŞMA — with kontekst meneceri
with open("data.txt", "r", encoding="utf-8") as file:
    content = file.read()
    # 'with' bloku bitdikdə fayl avtomatik bağlanır
    # Hətta xəta baş versə belə!

# Burada file artıq bağlıdır
print(file.closed)  # True
```

> [!tip] **Best Practice — Həmişə `with` İstifadə Edin**
> Fayl əməliyyatlarında **həmişə** `with` ifadəsini istifadə edin. Bu qayda istisnasızdır. `with` olmadan fayl bağlanmaya bilər — bu, yaddaş sızıntısına, data itkisinə və ya faylın kilidlənməsinə gətirib çıxara bilər. Əməliyyat sistemi prosesə verilən fayl handle sayını məhdudlaşdırır — bağlanmamış fayllar bu limiti aşa bilər.

### 1.4 Fayldan Oxumaq

```python
# Nümunə fayl yaradırıq (sonrakı nümunələr üçün)
with open("students.txt", "w", encoding="utf-8") as f:
    f.write("Əli:85\n")
    f.write("Vəli:92\n")
    f.write("Leyla:78\n")
    f.write("Nigar:95\n")
    f.write("Rəşad:67\n")

# === read() — Bütün faylı bir dəfəyə oxuyur ===
with open("students.txt", "r", encoding="utf-8") as f:
    full_content = f.read()   # Bütün məzmun tək string olaraq
    print(full_content)
    # Əli:85
    # Vəli:92
    # ...

# === readline() — Tək sətir oxuyur ===
with open("students.txt", "r", encoding="utf-8") as f:
    first_line = f.readline()    # "Əli:85\n" — sətir sonu (\n) daxildir
    second_line = f.readline()   # "Vəli:92\n"
    print(first_line.strip())    # "Əli:85" — strip() \n-i silir

# === readlines() — Bütün sətirləri list olaraq oxuyur ===
with open("students.txt", "r", encoding="utf-8") as f:
    all_lines = f.readlines()    # ['Əli:85\n', 'Vəli:92\n', ...]
    # Hər sətirin sonunda \n var — strip() ilə təmizləmək lazımdır

# === Ən yaxşı üsul: for dövrü ilə sətir-sətir oxumaq ===
# Fayl obyekti özü iterable-dır — hər iterasiyada bir sətir qaytarır
# Böyük fayllar üçün ən yaddaş-effektiv üsul budur
with open("students.txt", "r", encoding="utf-8") as f:
    for line in f:
        name, score = line.strip().split(":")
        print(f"Tələbə: {name}, Bal: {score}")
```

**Oxuma Metodlarının Müqayisəsi:**

| Metod | Qaytarır | Yaddaş | İstifadə halı |
|---|---|---|---|
| `read()` | Tək string | Bütün fayl yaddaşda | Kiçik fayllar |
| `read(n)` | n simvol | Yalnız n simvol | Chunk-larla oxumaq |
| `readline()` | Tək sətir (string) | Yalnız 1 sətir | Sətir-sətir emal |
| `readlines()` | List of strings | Bütün fayl yaddaşda | Bütün sətirlərə indekslə müraciət |
| `for line in f` | Hər iterasiyada 1 sətir | Yalnız 1 sətir | Böyük fayllar (tövsiyə olunan) |

### 1.5 Fayla Yazmaq

```python
# === write() — String yazır ===
with open("report.txt", "w", encoding="utf-8") as f:
    f.write("Hesabat Başlığı\n")          # \n — yeni sətir
    f.write("=" * 30 + "\n")              # separator xətti
    f.write("Tarix: 2026-03-19\n")

# === writelines() — Sətirlərin siyahısını yazır ===
# DİQQƏT: writelines() avtomatik \n əlavə etmir!
lines = ["Birinci sətir\n", "İkinci sətir\n", "Üçüncü sətir\n"]
with open("output.txt", "w", encoding="utf-8") as f:
    f.writelines(lines)

# === print() funksiyası ilə fayla yazmaq ===
with open("formatted.txt", "w", encoding="utf-8") as f:
    students = [("Əli", 85), ("Vəli", 92), ("Leyla", 78)]
    for name, score in students:
        # print() avtomatik \n əlavə edir və formatlamanı asanlaşdırır
        print(f"{name:<10} {score:>5}", file=f)

# === Fayla əlavə etmək (append) ===
with open("log.txt", "a", encoding="utf-8") as f:
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    f.write(f"[{timestamp}] Yeni qeyd əlavə edildi\n")
```

### 1.6 Praktik Nümunə: Tələbə Balları Sistemi

Bu nümunə yalnız indiyə qədər öyrənilmiş konseptləri istifadə edir: fayllar, funksiyalar, list, dict, dövrülər, şərt ifadələri.

```python
def read_student_scores(filepath):
    """Fayldan tələbə adlarını və ballarını oxuyur."""
    students = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:            # Boş sətirləri atlayır
                continue
            parts = line.split(":")
            if len(parts) == 2:     # Düzgün formatda olduğunu yoxlayır
                name = parts[0].strip()
                score = int(parts[1].strip())
                students[name] = score
    return students


def calculate_statistics(scores):
    """Balların statistikasını hesablayır."""
    values = list(scores.values())
    total = sum(values)
    count = len(values)
    average = total / count if count > 0 else 0
    highest = max(values)
    lowest = min(values)

    return {
        "count": count,
        "average": round(average, 2),
        "highest": highest,
        "lowest": lowest,
        "passed": sum(1 for v in values if v >= 50),
        "failed": sum(1 for v in values if v < 50),
    }


def write_report(filepath, students, stats):
    """Hesabatı fayla yazır."""
    with open(filepath, "w", encoding="utf-8") as f:
        print("TƏLƏBƏ BALLARI HESABATI", file=f)
        print("=" * 40, file=f)
        print(f"Ümumi tələbə sayı: {stats['count']}", file=f)
        print(f"Ortalama bal:      {stats['average']}", file=f)
        print(f"Ən yüksək bal:     {stats['highest']}", file=f)
        print(f"Ən aşağı bal:      {stats['lowest']}", file=f)
        print(f"Keçənlər:          {stats['passed']}", file=f)
        print(f"Kəsilənlər:        {stats['failed']}", file=f)
        print("=" * 40, file=f)
        print(f"\n{'Ad':<15} {'Bal':>5} {'Status':>10}", file=f)
        print("-" * 32, file=f)
        for name, score in sorted(students.items(), key=lambda x: x[1], reverse=True):
            status = "Keçdi" if score >= 50 else "Kəsildi"
            print(f"{name:<15} {score:>5} {status:>10}", file=f)


# İstifadə:
# students = read_student_scores("students.txt")
# stats = calculate_statistics(students)
# write_report("report.txt", students, stats)
```

### 1.7 CSV Faylları ilə İşləmək

```python
import csv

# === CSV Yazmaq ===
headers = ["Ad", "Soyad", "Bal", "Status"]
rows = [
    ["Əli", "Həsənov", 85, "Keçdi"],
    ["Vəli", "Məmmədov", 42, "Kəsildi"],
    ["Leyla", "Əliyeva", 91, "Keçdi"],
]

with open("students.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers)     # Başlıq sətri
    writer.writerows(rows)       # Bütün sətirləri yazır

# === CSV Oxumaq ===
with open("students.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)        # İlk sətir — başlıqlar
    for row in reader:
        name, surname, score, status = row
        print(f"{name} {surname}: {score} ({status})")

# === DictReader — hər sətir dict olaraq ===
with open("students.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)   # Başlıqları avtomatik key olaraq istifadə edir
    for row in reader:
        print(f"{row['Ad']} {row['Soyad']}: {row['Bal']}")
```

### 1.8 JSON Faylları ilə İşləmək

```python
import json

# === Python obyektini JSON fayla yazmaq ===
config = {
    "app_name": "StudentTracker",
    "version": "1.0",
    "settings": {
        "max_students": 100,
        "passing_score": 50,
        "grading_scale": ["A", "B", "C", "D", "F"],
    },
    "active": True,
}

with open("config.json", "w", encoding="utf-8") as f:
    json.dump(
        config, f,
        indent=4,               # 4 boşluq indentasiya — oxunaqlılıq üçün
        ensure_ascii=False,     # Unicode simvollarını qoruyur (Azərbaycan hərfləri)
    )

# === JSON fayldan Python obyektinə oxumaq ===
with open("config.json", "r", encoding="utf-8") as f:
    loaded_config = json.load(f)   # dict olaraq qaytarır

print(loaded_config["settings"]["passing_score"])  # 50

# === String ↔ JSON (fayl olmadan) ===
json_string = json.dumps(config, indent=2, ensure_ascii=False)  # dict → JSON string
parsed = json.loads(json_string)                                 # JSON string → dict
```

> [!tip] **Best Practice — Encoding Həmişə Göstərin**
> Fayl açarkən **həmişə** `encoding="utf-8"` parametrini göstərin. Default encoding əməliyyat sisteminə görə dəyişir — Windows-da `cp1252`, Linux-da `utf-8`. Encoding göstərilmədikdə eyni kod müxtəlif sistemlərdə fərqli nəticə verə bilər. Bu, xüsusilə Azərbaycan hərfləri (ə, ö, ü, ş, ç, ğ, ı) olan mətnlər üçün kritikdir.

---

## 2. Xətaların İdarə Edilməsi (Exception Handling)

### 2.1 Xəta (Exception) Nədir?

**Exception** — proqramın icrası zamanı baş verən xəta hadisəsidir. Exception baş verdikdə, proqram normal icra axınını dayandırır. Əgər exception tutulmazsa (handle edilməzsə), proqram tamamilə dayanır və **traceback** (xəta izləmə) mesajı göstərilir.

Exception-lar iki kateqoriyaya bölünür:
- **Syntax Error** — kodun strukturunda olan xəta. Python kodu icra etməzdən əvvəl aşkar edir. Tutula bilməz.
- **Runtime Exception** — kodun icrası zamanı yaranan xəta. `try/except` ilə tutula bilər.

### 2.2 Ümumi Exception Tipləri

| Exception | Nə Zaman Yaranır | Nümunə |
|---|---|---|
| `ValueError` | Dəyər tipi düzgün, amma dəyər etibarsız | `int("abc")` |
| `TypeError` | Əməliyyat tipi uyğun deyil | `"5" + 3` |
| `KeyError` | Dict-də mövcud olmayan key | `d = {}; d["x"]` |
| `IndexError` | List/tuple indeksi hüduddan kənar | `[1,2][5]` |
| `FileNotFoundError` | Fayl mövcud deyil | `open("yoxdur.txt")` |
| `ZeroDivisionError` | Sıfıra bölmə | `10 / 0` |
| `AttributeError` | Obyektdə mövcud olmayan atribut | `"text".append("x")` |
| `NameError` | Təyin edilməmiş dəyişən | `print(x)` (x təyin olunmayıb) |
| `ImportError` | Modul tapılmadı | `import nonexistent` |
| `PermissionError` | Fayl icazəsi yoxdur | İcazəsiz fayla yazmaq |
| `StopIteration` | Iterator tükənib | Generatorda daha element yoxdur |
| `RecursionError` | Rekursiya limiti aşılıb | Sonsuz rekursiya |

### 2.3 Exception Hierarchy (İyerarxiyası)

Python-da bütün exception-lar bir sinif iyerarxiyasına malikdir. Bunu bilmək vacibdir, çünki `except` bloku göstərilən exception-un **bütün alt siniflərini** də tutur.

```
BaseException
├── SystemExit
├── KeyboardInterrupt
├── GeneratorExit
└── Exception
    ├── ArithmeticError
    │   ├── ZeroDivisionError
    │   ├── OverflowError
    │   └── FloatingPointError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── OSError
    │   ├── FileNotFoundError
    │   ├── PermissionError
    │   └── FileExistsError
    ├── ValueError
    ├── TypeError
    ├── AttributeError
    ├── ImportError
    │   └── ModuleNotFoundError
    └── RuntimeError
        └── RecursionError
```

### 2.4 `try/except/else/finally` Bloku

Bu, Python-da exception handling-in əsas mexanizmidir. Hər bir hissənin konkret rolu var:

```python
try:
    # Xəta yarana biləcək kod buraya yazılır
    # Python bu bloku icra etməyə cəhd edir
    pass
except SpecificError as e:
    # Yalnız SpecificError (və onun alt sinifləri) baş verdikdə icra olunur
    # 'e' — exception obyektidir, xəta haqqında məlumat verir
    pass
except (TypeError, ValueError) as e:
    # Birdən çox exception tipini tək blokda tutmaq
    pass
except Exception as e:
    # Bütün "adi" exception-ları tutur (tövsiyə olunmayan geniş tutma)
    pass
else:
    # Heç bir exception baş VERMƏDİKDƏ icra olunur
    # try bloku uğurlu tamamlandıqda
    pass
finally:
    # HƏMİŞƏ icra olunur — exception olsa da, olmasa da
    # Resurs təmizləmə (cleanup) üçün istifadə olunur
    pass
```

**Ətraflı nümunə:**

```python
def read_config_value(filepath, key):
    """Konfiqurasiya faylından müəyyən key-in dəyərini oxuyur."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "=" in line:
                    k, v = line.split("=", maxsplit=1)
                    if k.strip() == key:
                        return v.strip()
    except FileNotFoundError:
        print(f"Xəta: '{filepath}' faylı tapılmadı.")
        return None
    except PermissionError:
        print(f"Xəta: '{filepath}' faylını oxumaq üçün icazə yoxdur.")
        return None
    except ValueError:
        print(f"Xəta: Faylda düzgün formatda olmayan sətir var.")
        return None

    # Key tapılmadı
    print(f"Xəbərdarlıq: '{key}' açarı '{filepath}' faylında tapılmadı.")
    return None


# else və finally ilə fayl emalı
def process_data_file(input_path, output_path):
    """Faylı oxuyur, emal edir və nəticəni yazır."""
    processed_count = 0
    try:
        with open(input_path, "r", encoding="utf-8") as infile:
            lines = infile.readlines()
    except FileNotFoundError:
        print(f"Xəta: '{input_path}' tapılmadı!")
        return 0
    else:
        # try uğurlu olduqda — nəticəni yazırıq
        with open(output_path, "w", encoding="utf-8") as outfile:
            for line in lines:
                cleaned = line.strip().upper()
                if cleaned:
                    outfile.write(cleaned + "\n")
                    processed_count += 1
        print(f"Uğurlu: {processed_count} sətir emal edildi.")
    finally:
        # Həmişə icra olunur — log yazırıq
        print(f"Əməliyyat tamamlandı. İşlənmiş: {processed_count}")

    return processed_count
```

> [!tip] **Best Practice — Exception Handling Qaydaları**
> 1. **Spesifik olun**: `except Exception` əvəzinə `except ValueError` kimi konkret tip yazın. Geniş tutma real bug-ları gizləyir.
> 2. **`else` istifadə edin**: Uğurlu icra kodunu `try` blokundan `else`-ə köçürün. Bu, `try` blokunu minimal saxlayır.
> 3. **`finally` resurs təmizləməsi üçündür**: Fayl bağlama, şəbəkə bağlantısını kəsmə kimi əməliyyatlar.
> 4. **Exception-u udmayın**: `except: pass` heç vaxt yazmayın — xətanı ən azı log edin.

### 2.5 Exception Qaldırmaq (`raise`)

`raise` açar sözü ilə proqramçı özü exception yarada bilər. Bu, funksiyaya ötürülən arqumentlərin etibarlılığını yoxlamaq (input validation) üçün çox istifadə olunur.

```python
def calculate_average(numbers):
    """
    Verilmiş ədədlərin ortalamasını hesablayır.

    Raises:
        TypeError: numbers list deyilsə
        ValueError: list boşdursa
        TypeError: list-də ədəd olmayan element varsa
    """
    if not isinstance(numbers, list):
        raise TypeError(f"list gözlənilir, {type(numbers).__name__} verildi")

    if len(numbers) == 0:
        raise ValueError("Boş list ilə ortalama hesablamaq mümkün deyil")

    for i, num in enumerate(numbers):
        if not isinstance(num, (int, float)):
            raise TypeError(
                f"İndeks {i}-də ədəd gözlənilir, "
                f"{type(num).__name__} ('{num}') tapıldı"
            )

    return sum(numbers) / len(numbers)


# İstifadə
try:
    result = calculate_average([10, 20, "otuz", 40])
except TypeError as e:
    print(f"Tip xətası: {e}")
    # Tip xətası: İndeks 2-də ədəd gözlənilir, str ('otuz') tapıldı
```

### 2.6 Xüsusi Exception Sinifləri (Custom Exceptions)

Öz exception siniflərinizi yaratmaq — xətaları daha mənalı və strukturlaşdırılmış şəkildə idarə etməyə imkan verir. Custom exception-lar `Exception` sinifindən miras alınır.

```python
# Xüsusi exception sinifləri
class ValidationError(Exception):
    """Giriş məlumatlarının yoxlanması zamanı yaranan xəta."""
    pass

class ScoreOutOfRangeError(ValidationError):
    """Bal icazə verilən hüduddan kənardadır."""
    def __init__(self, score, min_val=0, max_val=100):
        self.score = score
        self.min_val = min_val
        self.max_val = max_val
        super().__init__(
            f"Bal {score} hüduddan kənardır. "
            f"İcazə verilən aralıq: [{min_val}, {max_val}]"
        )

class EmptyNameError(ValidationError):
    """Ad boş ola bilməz."""
    pass


def register_student(name, score):
    """Tələbəni qeydiyyatdan keçirir — giriş yoxlanması ilə."""
    if not name or not name.strip():
        raise EmptyNameError("Tələbə adı boş ola bilməz")

    if not isinstance(score, (int, float)):
        raise TypeError(f"Bal ədəd olmalıdır, {type(score).__name__} verildi")

    if not (0 <= score <= 100):
        raise ScoreOutOfRangeError(score)

    return {"name": name.strip(), "score": score}


# İstifadə
try:
    student = register_student("Əli", 150)
except EmptyNameError as e:
    print(f"Ad xətası: {e}")
except ScoreOutOfRangeError as e:
    print(f"Bal xətası: {e}")
    print(f"  Verilən bal: {e.score}")
    print(f"  İcazə verilən: [{e.min_val}, {e.max_val}]")
except ValidationError as e:
    print(f"Ümumi yoxlama xətası: {e}")
```

> [!tip] **Best Practice — Custom Exception İyerarxiyası**
> Layihəniz üçün bir əsas exception sinifi yaradın (məs. `AppError(Exception)`) və bütün digər custom exception-ları ondan miras alın. Bu, çağıran kodun istəsə spesifik xətanı, istəsə bütün layihə xətalarını tuta bilməsinə imkan verir. Bu pattern bütün böyük Python kitabxanalarında istifadə olunur (məs. `requests.RequestException`).

### 2.7 Exception Chaining — `raise ... from`

Bir exception başqa bir exception-dan qaynaqlandıqda, `raise ... from` ilə səbəb-nəticə əlaqəsini aydın göstərmək olar.

```python
def parse_score(raw_value):
    """String dəyəri ədədə çevirir."""
    try:
        return int(raw_value)
    except ValueError as original_error:
        raise ValidationError(
            f"'{raw_value}' düzgün bal dəyəri deyil"
        ) from original_error
        # Traceback-də həm yeni, həm orijinal xəta göstəriləcək:
        # ValueError → ValidationError

# raise ... from None  — orijinal xətanı gizlətmək üçün
# (istifadəçiyə texniki detalları göstərmək istəmədikdə)
```

---

## 3. Gün 1 — Xülasə

| Mövzu | Əsas Nöqtə |
|---|---|
| **File I/O** | `open()` ilə fayl açmaq; `r`, `w`, `a`, `x` rejimləri |
| **`with` ifadəsi** | Faylı avtomatik bağlayır — həmişə istifadə edin |
| **Oxumaq** | `read()`, `readline()`, `readlines()`, `for line in f` |
| **Yazmaq** | `write()`, `writelines()`, `print(file=f)` |
| **CSV/JSON** | `csv` modulu, `json.dump()`/`json.load()` |
| **Exception handling** | `try/except/else/finally` — xətanı tutmaq və idarə etmək |
| **`raise`** | Proqramçının özü exception qaldırması |
| **Custom Exceptions** | `Exception`-dan miras alan xüsusi xəta sinifləri |

---

> [!note] **Növbəti Gün**
> **Gün 2**-də Python modulları və paketlərini, import sistemini və standart kitabxananın ən vacib modullarını öyrənəcəyik.
