# Həftə 5 - Gün 2: Unit Testing və TDD

`learning/week_5/Week5_Day2_Testing.md`

---

## 1. Niyə Test Yazmaq Lazımdır?

### 1.1 Testlərin Faydaları

**Unit test** — kodun kiçik, müstəqil hissəsinin (funksiya, metod, sinif) gözlənildiyi kimi işlədiyini yoxlayan avtomatik testdir.

| Fayda | İzah |
|---|---|
| **Bug-ların erkən aşkarlanması** | Kodun davranışını dəyişiklikdən sonra avtomatik yoxlayır |
| **Refactoring əminliyi** | Kodu dəyişəndə testlər pozulmadıqca düzgün işlədiyini bilirsiniz |
| **Canlı sənədləmə** | Testlər funksiyaların necə istifadə olunacağını göstərir |
| **Dizayn keyfiyyəti** | Test yazmaq çətin olan kod — adətən pis dizayn edilmiş koddur |
| **Deployment əminliyi** | CI/CD-də testlər keçməlidir ki, kod production-a getsin |

### 1.2 Test Piramidası

```
          /\
         /  \       E2E Tests (az — yavaş, bahalı)
        /    \      Sistem testləri, browser testləri
       /------\
      /        \    Integration Tests (orta)
     /          \   Komponentlər arası əlaqə testləri
    /------------\
   /              \  Unit Tests (çox — sürətli, ucuz)
  /________________\ Tək funksiya/sinif testləri
```

| Səviyyə | Nə Test Edir | Sürət | Say |
|---|---|---|---|
| **Unit** | Tək funksiya/sinif | Çox sürətli (ms) | Çox |
| **Integration** | Komponentlər arası əlaqə | Orta | Orta |
| **E2E** | Bütün sistem | Yavaş (saniyələr) | Az |

---

## 2. `unittest` — Python-un Daxili Test Framework-ü

### 2.1 Əsas Struktur

```python
# test_calculator.py
import unittest

# Test ediləcək kod (adətən ayrı moduldadır)
def add(a, b):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Yalnız ədədlər qəbul edilir")
    return a + b

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Sıfıra bölmək olmaz")
    return a / b


class TestCalculator(unittest.TestCase):
    """
    unittest.TestCase-dən miras alan test sinifi.
    Hər test metodu 'test_' prefiksi ilə başlamalıdır.
    """

    def test_add_positive_numbers(self):
        """İki müsbət ədədin cəmini yoxlayır."""
        result = add(3, 5)
        self.assertEqual(result, 8)    # result == 8 olmalıdır

    def test_add_negative_numbers(self):
        """Mənfi ədədlərlə cəm."""
        self.assertEqual(add(-3, -5), -8)

    def test_add_mixed_numbers(self):
        """Müsbət və mənfi ədədlərin cəmi."""
        self.assertEqual(add(-3, 5), 2)

    def test_add_floats(self):
        """Float ədədlərlə cəm."""
        result = add(0.1, 0.2)
        self.assertAlmostEqual(result, 0.3, places=7)   # Float dəqiqlik

    def test_add_type_error(self):
        """Ədəd olmayan giriş — TypeError gözlənilir."""
        with self.assertRaises(TypeError):
            add("hello", 5)

    def test_divide_normal(self):
        """Normal bölmə."""
        self.assertEqual(divide(10, 2), 5.0)

    def test_divide_by_zero(self):
        """Sıfıra bölmə — ZeroDivisionError gözlənilir."""
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)


if __name__ == "__main__":
    unittest.main()
```

### 2.2 Assert Metodları

| Metod | Yoxlayır | Nümunə |
|---|---|---|
| `assertEqual(a, b)` | `a == b` | `assertEqual(4, 4)` |
| `assertNotEqual(a, b)` | `a != b` | `assertNotEqual(4, 5)` |
| `assertTrue(x)` | `bool(x) is True` | `assertTrue(is_valid)` |
| `assertFalse(x)` | `bool(x) is False` | `assertFalse(is_empty)` |
| `assertIsNone(x)` | `x is None` | `assertIsNone(result)` |
| `assertIsNotNone(x)` | `x is not None` | `assertIsNotNone(data)` |
| `assertIn(a, b)` | `a in b` | `assertIn("key", dict)` |
| `assertRaises(Error)` | Exception qaldırılır | `with assertRaises(ValueError):` |
| `assertAlmostEqual(a, b)` | Float müqayisəsi | `assertAlmostEqual(0.3, 0.3)` |
| `assertIsInstance(a, T)` | `isinstance(a, T)` | `assertIsInstance(obj, list)` |
| `assertGreater(a, b)` | `a > b` | `assertGreater(10, 5)` |

### 2.3 setUp və tearDown

```python
import unittest
import sqlite3
import os

class TestStudentDatabase(unittest.TestCase):

    def setUp(self):
        """
        Hər test metodundan ƏVVƏL çağırılır.
        Test üçün təmiz mühit yaradır.
        """
        self.db_path = "test_students.db"
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                score REAL
            )
        """)
        # Test datası
        self.cursor.executemany(
            "INSERT INTO students (name, score) VALUES (?, ?)",
            [("Əli", 85.0), ("Vəli", 72.5), ("Leyla", 93.0)]
        )
        self.conn.commit()

    def tearDown(self):
        """
        Hər test metodundan SONRA çağırılır.
        Test resurslarını təmizləyir.
        """
        self.conn.close()
        os.remove(self.db_path)

    def test_student_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM students")
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 3)

    def test_highest_score(self):
        self.cursor.execute("SELECT MAX(score) FROM students")
        max_score = self.cursor.fetchone()[0]
        self.assertEqual(max_score, 93.0)

    def test_insert_student(self):
        self.cursor.execute(
            "INSERT INTO students (name, score) VALUES (?, ?)",
            ("Nigar", 88.5)
        )
        self.conn.commit()
        self.cursor.execute("SELECT COUNT(*) FROM students")
        self.assertEqual(self.cursor.fetchone()[0], 4)
```

---

## 3. `pytest` — Müasir Test Framework

### 3.1 Niyə pytest?

`pytest` — Python ekosistemində ən populyar test framework-üdür. `unittest`-dən daha sadə sintaksis, güclü xüsusiyyətlər və geniş plugin ekosistemi təqdim edir.

| Xüsusiyyət | unittest | pytest |
|---|---|---|
| **Test yazma** | Sinif + metod lazımdır | Sadə funksiya kifayətdir |
| **Assert** | `self.assertEqual(a, b)` | `assert a == b` |
| **Fixtures** | `setUp` / `tearDown` | `@pytest.fixture` — daha elastik |
| **Parametrize** | Yoxdur (əl ilə) | `@pytest.mark.parametrize` |
| **Xəta mesajı** | Ümumi | Çox ətraflı diff göstərir |
| **Plugin-lər** | Məhdud | 1000+ plugin |

### 3.2 Sadə pytest Testləri

```python
# test_math_utils.py
import pytest

# Test ediləcək funksiyalar
def factorial(n):
    """n! hesablayır."""
    if not isinstance(n, int):
        raise TypeError("Tam ədəd lazımdır")
    if n < 0:
        raise ValueError("Mənfi ədədin faktorialı yoxdur")
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def is_prime(n):
    """Ədədin sadə (prime) olub-olmadığını yoxlayır."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


# === pytest testləri — sadə funksiyalar, 'assert' ifadəsi ===

def test_factorial_zero():
    """0! = 1"""
    assert factorial(0) == 1

def test_factorial_one():
    """1! = 1"""
    assert factorial(1) == 1

def test_factorial_five():
    """5! = 120"""
    assert factorial(5) == 120

def test_factorial_negative_raises():
    """Mənfi ədəd — ValueError gözlənilir."""
    with pytest.raises(ValueError, match="Mənfi"):
        factorial(-1)

def test_factorial_float_raises():
    """Float — TypeError gözlənilir."""
    with pytest.raises(TypeError):
        factorial(3.5)

def test_is_prime_basic():
    assert is_prime(2) is True
    assert is_prime(3) is True
    assert is_prime(17) is True

def test_is_not_prime():
    assert is_prime(0) is False
    assert is_prime(1) is False
    assert is_prime(4) is False
    assert is_prime(15) is False
```

```bash
# Testləri icra etmək
pytest                          # Bütün testlər
pytest test_math_utils.py       # Xüsusi fayl
pytest -v                       # Verbose — hər testin adını göstərir
pytest -k "factorial"           # Yalnız adında "factorial" olan testlər
pytest --tb=short               # Qısa traceback
```

### 3.3 Fixtures — Test Mühiti İdarəetməsi

**Fixture** — test üçün lazım olan data və ya resursu təmin edən funksiadır. `setUp`/`tearDown`-dan daha elastik və təkrar istifadə edilə biləndir.

```python
import pytest
import sqlite3
import os

@pytest.fixture
def sample_students():
    """Nümunə tələbə datası təmin edir."""
    return [
        {"name": "Əli", "surname": "Həsənov", "score": 85.0},
        {"name": "Vəli", "surname": "Məmmədov", "score": 72.5},
        {"name": "Leyla", "surname": "Əliyeva", "score": 93.0},
        {"name": "Nigar", "surname": "Quliyeva", "score": 45.0},
    ]

@pytest.fixture
def db_connection():
    """
    Test verilənlər bazası yaradır.
    yield-dən əvvəl — setUp (hazırlıq)
    yield-dən sonra — tearDown (təmizlik)
    """
    db_path = "test_temp.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE students (
            id INTEGER PRIMARY KEY,
            name TEXT,
            score REAL
        )
    """)
    conn.commit()

    yield conn         # Test bu bağlantını istifadə edir

    # Təmizlik — test bitdikdən sonra
    conn.close()
    os.remove(db_path)


def test_passing_students(sample_students):
    """Keçən tələbələrin sayını yoxlayır."""
    passing = [s for s in sample_students if s["score"] >= 50]
    assert len(passing) == 3

def test_average_score(sample_students):
    """Ortalama balı yoxlayır."""
    avg = sum(s["score"] for s in sample_students) / len(sample_students)
    assert round(avg, 2) == 73.88

def test_database_insert(db_connection):
    """Verilənlər bazasına əlavə etməni yoxlayır."""
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO students (name, score) VALUES (?, ?)", ("Test", 90.0))
    db_connection.commit()

    cursor.execute("SELECT COUNT(*) FROM students")
    assert cursor.fetchone()[0] == 1
```

### 3.4 Parametrize — Çoxlu Giriş ilə Test

`@pytest.mark.parametrize` — eyni test funksiyasını müxtəlif giriş dəyərləri ilə avtomatik icra edir. Bu, çoxlu oxşar test metodları yazmaq əvəzinə çox rahatdır.

```python
import pytest

def calculate_grade(score):
    """Bala görə qiymət təyin edir."""
    if not isinstance(score, (int, float)):
        raise TypeError("Bal ədəd olmalıdır")
    if score < 0 or score > 100:
        raise ValueError("Bal 0-100 arasında olmalıdır")
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


# Parametrize — hər tuple bir test halı
@pytest.mark.parametrize("score, expected_grade", [
    (95, "A"),
    (90, "A"),      # Sərhəd dəyəri (boundary)
    (89, "B"),      # Sərhəddən bir az aşağı
    (80, "B"),
    (75, "C"),
    (70, "C"),
    (65, "D"),
    (60, "D"),
    (59, "F"),
    (0, "F"),
    (100, "A"),
])
def test_calculate_grade(score, expected_grade):
    """Müxtəlif ballar üçün düzgün qiyməti yoxlayır."""
    assert calculate_grade(score) == expected_grade


@pytest.mark.parametrize("invalid_score", [-1, 101, -50, 200])
def test_grade_invalid_score(invalid_score):
    """Etibarsız ballar üçün ValueError gözlənilir."""
    with pytest.raises(ValueError):
        calculate_grade(invalid_score)


@pytest.mark.parametrize("invalid_type", ["hello", None, [90], {"score": 90}])
def test_grade_invalid_type(invalid_type):
    """Ədəd olmayan giriş üçün TypeError gözlənilir."""
    with pytest.raises(TypeError):
        calculate_grade(invalid_type)
```

### 3.5 Testlərin Təşkili

```
tests/
├── conftest.py              # Paylaşılan fixture-lar (pytest avtomatik tapır)
├── test_calculator.py       # Hesablama testləri
├── test_file_utils.py       # Fayl əməliyyatları testləri
├── test_database.py         # DB testləri
└── test_api/                # API testləri alt-qovluğu
    ├── __init__.py
    ├── test_endpoints.py
    └── test_auth.py
```

```python
# conftest.py — bütün testlər üçün ortaq fixture-lar
import pytest

@pytest.fixture
def temp_directory(tmp_path):
    """Müvəqqəti test qovluğu yaradır (pytest built-in tmp_path istifadə edir)."""
    test_dir = tmp_path / "test_data"
    test_dir.mkdir()
    return test_dir

@pytest.fixture
def sample_config():
    """Nümunə konfiqurasiya dict-i."""
    return {
        "max_students": 100,
        "passing_score": 50,
        "grading_scale": {"A": 90, "B": 80, "C": 70, "D": 60},
    }
```

---

## 4. Test-Driven Development (TDD)

### 4.1 TDD Nədir?

**TDD (Test-Driven Development)** — əvvəlcə **test yazıb**, sonra testi keçirəcək **kodu yazmaq** metodologiyasıdır. Bu, ənənəvi "əvvəlcə kod, sonra test" yanaşmasının tam əksidir.

### 4.2 TDD Dövrü: Red → Green → Refactor

```
1. RED    — Əvvəlcə test yaz. Test uğursuz olacaq (çünki kod hələ yoxdur).
2. GREEN  — Testi keçirəcək MİNİMAL kodu yaz. Gözəllik vacib deyil, yalnız keçməlidir.
3. REFACTOR — Kodu təmizlə, optimallaşdır. Testlər hələ də keçməlidir.

Təkrarla.
```

### 4.3 TDD Nümunəsi: Parola Yoxlayıcı

```python
# Addım 1: RED — Əvvəlcə testləri yazırıq (funksiya hələ yoxdur)

# test_password_validator.py
import pytest

def test_valid_password():
    """Güclü parol qəbul edilir."""
    assert validate_password("Str0ng!Pass") is True

def test_too_short():
    """8-dən qısa parol rədd edilir."""
    assert validate_password("Ab1!") is False

def test_no_uppercase():
    """Böyük hərf olmayan parol rədd edilir."""
    assert validate_password("weak1!pass") is False

def test_no_lowercase():
    """Kiçik hərf olmayan parol rədd edilir."""
    assert validate_password("WEAK1!PASS") is False

def test_no_digit():
    """Rəqəm olmayan parol rədd edilir."""
    assert validate_password("Weak!Pass") is False

def test_no_special_char():
    """Xüsusi simvol olmayan parol rədd edilir."""
    assert validate_password("Weak1Pass") is False

def test_empty_password():
    """Boş parol rədd edilir."""
    assert validate_password("") is False


# Addım 2: GREEN — Testləri keçirəcək minimum kodu yazırıq

def validate_password(password):
    """
    Parolun güclülüyünü yoxlayır.

    Tələblər:
    - Minimum 8 simvol
    - Ən azı 1 böyük hərf
    - Ən azı 1 kiçik hərf
    - Ən azı 1 rəqəm
    - Ən azı 1 xüsusi simvol
    """
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(c in special_chars for c in password):
        return False
    return True


# Addım 3: REFACTOR — Kodu təmizləyirik (testlər hələ keçməlidir)

def validate_password_v2(password):
    """Refactored versiya — daha təmiz."""
    checks = [
        (len(password) >= 8, "Minimum 8 simvol"),
        (any(c.isupper() for c in password), "Böyük hərf lazımdır"),
        (any(c.islower() for c in password), "Kiçik hərf lazımdır"),
        (any(c.isdigit() for c in password), "Rəqəm lazımdır"),
        (any(not c.isalnum() for c in password), "Xüsusi simvol lazımdır"),
    ]
    return all(passed for passed, _ in checks)
```

> [!tip] **Best Practice — Test Adlandırma**
> Test adları **nəyin test edildiyini** aydın ifadə etməlidir. Bəzi populyar konvensiyalar:
> - `test_<method>_<scenario>_<expected>` — məs. `test_divide_by_zero_raises_error`
> - `test_should_<behavior>_when_<condition>` — məs. `test_should_reject_when_password_too_short`
>
> Uzun ad > qısa amma anlaşılmaz ad

---

## 5. Test Coverage (Örtük)

### 5.1 Coverage Nədir?

**Test coverage** — testlərin kodun neçə faizini "örtdüyünü" (icra etdiyini) ölçən metrikdir. 100% coverage kodun xətasız olması demək deyil, amma aşağı coverage testlərin kifayət etmədiyi deməkdir.

```bash
# pytest-cov plugin-i yükləmək
pip install pytest-cov

# Coverage ilə testləri icra etmək
pytest --cov=src --cov-report=term-missing

# HTML hesabat yaratmaq
pytest --cov=src --cov-report=html
# htmlcov/index.html faylını brauzerdə açın
```

```
# Nümunə coverage hesabatı:
Name                    Stmts   Miss  Cover   Missing
------------------------------------------------------
src/calculator.py          25      3    88%   42-44
src/validator.py           18      0   100%
src/file_utils.py          35      8    77%   28-35
------------------------------------------------------
TOTAL                      78     11    86%
```

> [!tip] **Best Practice — Coverage Hədəfi**
> - **80%+** — yaxşı başlanğıc nöqtəsi
> - **90%+** — yetkin layihələr üçün hədəf
> - **100%** — hər yerdə lazım deyil; bəzi kod (error handling, edge cases) test etmək çətindir
>
> Coverage rəqəminə deyil, **kritik iş məntiqinin** test olunmasına fokuslanın.

---

## 6. Gün 2 — Xülasə

| Mövzu | Əsas Nöqtə |
|---|---|
| **Unit test** | Kodun kiçik hissəsinin düzgünlüyünü yoxlayır |
| **unittest** | Python-un daxili framework-ü; TestCase sinfi, assert metodları |
| **pytest** | Daha sadə sintaksis; `assert`, fixture, parametrize |
| **Fixtures** | Test mühitini hazırlayan/təmizləyən yardımçı funksiyalar |
| **Parametrize** | Eyni testi müxtəlif dəyərlərlə icra etmək |
| **TDD** | Red → Green → Refactor dövrü |
| **Coverage** | Testlərin kodun neçə faizini örtdüyünü ölçür |

---

> [!note] **Növbəti Gün**
> **Gün 3**-də debugging texnikalarını və alətlərini — `pdb`, IDE debugger, logging modulu və sistemli bug axtarma strategiyalarını öyrənəcəyik.
