# Həftə 1 - Gün 1: Python Əsasları — Giriş, İdarəetmə Strukturları, Funksiyalar

`learning/week_1/Week1_Day1_Python_Basics.md`

---

## 1. Python Dilinə Giriş

### 1.1 Python Nədir?

Python, 1991-ci ildə **Guido van Rossum** tərəfindən yaradılmış, yüksək səviyyəli (**high-level**), interpretasiya olunan (**interpreted**), ümumi təyinatlı (**general-purpose**) proqramlaşdırma dilidir. Python-un dizayn fəlsəfəsi **kodun oxunaqlılığını** (readability) ön plana çıxarır və bu məqsədlə **məcburi indentasiya** (forced indentation) sistemindən istifadə edir.

Python **dinamik tipli** (dynamically typed) bir dildir — bu o deməkdir ki, dəyişənin tipi proqramın icrası zamanı (runtime) müəyyən edilir, kompilyasiya zamanı deyil. Bu xüsusiyyət inkişaf sürətini artırır, lakin böyük layihələrdə **type hint** istifadəsini vacib edir.

Python həmçinin **çoxparadigmalı** (multi-paradigm) bir dildir: prosedural, obyektyönümlü və funksional proqramlaşdırma üslublarının hamısını dəstəkləyir.

### 1.2 Niyə Python?

Python-un AI Engineering və Software Engineering sahələrində dominant olmasının əsas səbəbləri:

| Xüsusiyyət | İzah |
|---|---|
| **Sadə sintaksis** | Pseudocode-a yaxın, öyrənmə əyrisi aşağıdır |
| **Geniş ekosistem** | NumPy, Pandas, TensorFlow, PyTorch, scikit-learn kimi kitabxanalar |
| **İcma dəstəyi** | Dünyanın ən böyük proqramlaşdırma icmalarından birinə sahib |
| **Cross-platform** | Windows, macOS, Linux-da eyni şəkildə işləyir |
| **Rapid prototyping** | İdeyanı sürətlə prototipə çevirmək üçün ideal |
| **Glue language** | C, C++, Rust kimi dillərlə asanlıqla inteqrasiya olunur |

> [!tip] **Best Practice — Niyə Python AI üçün standartdır?**
> Python-un AI sahəsində dominant olmasının əsl səbəbi dilin özü deyil, **ekosistemdir**. TensorFlow, PyTorch kimi framework-lərin backend-i C++/CUDA ilə yazılıb, lakin Python onlara **yüksək səviyyəli interfeys** (high-level API) təqdim edir. Bu, mühəndislərin hardware optimallaşdırması ilə məşğul olmadan model arxitekturasına fokuslanmasına imkan verir. Bu pattern "**Python as glue language**" adlanır.

### 1.3 Python Versiyaları: Python 2 vs Python 3

Python 2 rəsmi olaraq **1 Yanvar 2020**-ci ildə dəstəkdən çıxarılıb (EOL — End of Life). Bütün yeni layihələr **Python 3.10+** ilə başlamalıdır.

| Xüsusiyyət | Python 2 | Python 3 |
|---|---|---|
| `print` | `print "hello"` (statement) | `print("hello")` (function) |
| Integer division | `5/2 = 2` | `5/2 = 2.5` |
| Strings | Default ASCII | Default Unicode (UTF-8) |
| `range()` | List qaytarır | Iterator qaytarır (memory-efficient) |
| Dəstək | ❌ EOL (2020) | ✅ Aktiv inkişafda |

---

## 2. Python Sintaksisi və İndentasiya

### 2.1 İndentasiya (Indentation)

Python-da indentasiya **sintaktik məcburiyyətdir**, estetik seçim deyil. Digər dillərdə (C, Java, JavaScript) kod bloklarını müəyyən etmək üçün `{}` mötərizələr istifadə olunur, Python-da isə bu rolu **indentasiya** (boşluq/tab) oynayır.

Python interpretatoru kod blokunun hansı `if`, `for`, `def` və ya `class` ifadəsinə aid olduğunu məhz indentasiya səviyyəsinə görə müəyyən edir. İndentasiyanın pozulması `IndentationError` xətasına səbəb olur.

```python
# Düzgün indentasiya — hər blok 4 boşluqla (space) iç-içədir
def greet(name):
    if name:                    # 4 boşluq — funksiya blokunun içindədir
        message = f"Salam, {name}!"  # 8 boşluq — if blokunun içindədir
        return message          # 8 boşluq — hələ də if blokunun içindədir
    return "Salam, naməlum!"   # 4 boşluq — if blokun xaricindədir, amma funksiyanın içindədir
```

```python
# Səhv indentasiya — IndentationError verəcək
def greet(name):
if name:           # XƏTA! Funksiya blokunun içində olmalıdır (4 boşluq lazımdır)
    return name
```

> [!tip] **Best Practice — Tab vs Space**
> PEP 8 standartına görə **4 boşluq (space)** istifadə edin, **tab** deyil. Müasir IDE-lər (VS Code, PyCharm, Cursor) Tab düyməsini avtomatik olaraq 4 space-ə çevirir. Tab və space-in qarışdırılması `TabError` xətasına gətirib çıxarır. Layihənizin `.editorconfig` faylında bunu konfiqurasiya edin.

### 2.2 Şərhlər (Comments)

Python-da şərhlər kodun oxunaqlılığını artırmaq üçün istifadə olunur və interpretator tərəfindən nəzərə alınmır.

```python
# Bu tək sətirli şərhdir (single-line comment)
# Hash (#) işarəsindən sonra gələn hər şey şərhdir

"""
Bu çoxsətirli string-dir (multi-line string).
Texniki olaraq şərh deyil — Python bunu string literal kimi saxlayır,
lakin heç bir dəyişənə təyin edilmədikdə garbage collector tərəfindən silinir.
Adətən docstring kimi istifadə olunur.
"""

x = 42  # Inline şərh — kodla eyni sətirdə, amma 2 boşluq sonra yazılır
```

### 2.3 PEP 8 — Python Stil Təlimatı

**PEP 8** (Python Enhancement Proposal 8) Python kodunun yazılma stilinə dair rəsmi təlimatdır. Bu, "düzgün işləyən" kodla "düzgün yazılmış" kod arasındakı fərqi müəyyən edir.

Əsas qaydalar:

| Qayda | Nümunə |
|---|---|
| Sətir uzunluğu: max 79 simvol | Uzun sətirləri `\` və ya mötərizə ilə bölün |
| Funksiya/dəyişən adları: `snake_case` | `calculate_total_price` |
| Sinif adları: `PascalCase` | `NeuralNetwork` |
| Sabitlər: `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| İmportlar: faylın əvvəlində | Standart → Third-party → Local sıra ilə |
| Operatorların ətrafında boşluq | `x = 5 + 3` (✅) `x=5+3` (❌) |

---

## 3. Dəyişənlər və Məlumat Tipləri

### 3.1 Dəyişənlər (Variables)

Python-da dəyişən — **yaddaşdakı bir obyektə istinad edən addır** (reference/label). C/C++ kimi dillərdən fərqli olaraq, dəyişən bir "qutu" deyil ki, dəyəri içində saxlayır — o, sadəcə yaddaşdakı bir obyektə **işarə edir** (points to).

Bu, Python-un **"everything is an object"** fəlsəfəsinin nəticəsidir — ədədlər, stringlər, funksiyalar, hətta modullar belə obyektdir.

```python
# Dəyişən yaratmaq — tip bəyannaməsi lazım deyil
age = 25                # 'age' adı int obyektinə (25) istinad edir
name = "Arrakis"        # 'name' adı str obyektinə istirad edir
pi = 3.14159            # 'pi' adı float obyektinə istinad edir
is_active = True        # 'is_active' adı bool obyektinə istinad edir

# Eyni anda birdən çox dəyişən təyin etmək (multiple assignment)
x, y, z = 10, 20, 30   # Hər bir dəyişən müvafiq dəyərə bağlanır

# Eyni dəyəri birdən çox dəyişənə təyin etmək
a = b = c = 0           # Hər üçü eyni 0 obyektinə istinad edir
```

```python
# id() funksiyası ilə obyektin yaddaşdakı ünvanını yoxlamaq
x = 256
y = 256
print(id(x) == id(y))  # True — Python kiçik ədədləri cache-ləyir (integer interning: -5 to 256)

x = 257
y = 257
print(id(x) == id(y))  # False (və ya True — CPython implementasiyasından asılıdır)
```

> [!tip] **Best Practice — Integer Interning**
> CPython (Python-un standart implementasiyası) `-5`-dən `256`-ya qədər olan integer-ləri əvvəlcədən yaradıb cache-ləyir. Bu, performans optimallaşdırmasıdır, çünki bu aralıqdakı ədədlər çox tez-tez istifadə olunur. Buna görə `is` operatoru ilə ədədləri müqayisə etməyin — həmişə `==` istifadə edin.

### 3.2 Məlumat Tipləri (Data Types)

Python-da hər şey obyektdir və hər obyektin bir **tipi** var. Bu tip, obyektin hansı əməliyyatları dəstəklədiyini və yaddaşda necə saxlandığını müəyyən edir.

#### 3.2.1 Ədədi Tiplər (Numeric Types)

**`int` (Integer — Tam ədəd)**

Python 3-də `int` tipinin **ölçü limiti yoxdur** — yaddaş icazə verdiyi qədər böyük ədədlərlə işləyə bilərsiniz. Bu, kriptografiya və böyük ədəd hesablamaları üçün çox əlverişlidir.

```python
# Integer nümunələri
regular_int = 42
negative_int = -17
big_int = 10**100               # Googol — 1-in ardınca 100 sıfır
binary = 0b1010                 # İkili say sistemi — 10-a bərabərdir
octal = 0o17                    # Səkkizli say sistemi — 15-ə bərabərdir
hexadecimal = 0xFF              # Onaltılıq say sistemi — 255-ə bərabərdir
readable_number = 1_000_000     # Alt xətt (underscore) oxunaqlılıq üçündür, dəyərə təsir etmir
```

**`float` (Floating-point — Kəsr ədəd)**

Float tiplər IEEE 754 standartına əsasən **64-bit ikili kəsr** (double precision) olaraq saxlanılır. Bu, **təxmini təmsil** deməkdir — bəzi ondalık ədədlər dəqiq saxlanıla bilmir.

```python
# Float nümunələri
temperature = 36.6
scientific = 2.5e10             # Elmi notasiya: 2.5 × 10^10 = 25000000000.0
tiny = 1.5e-4                   # 0.00015

# Float-un dəqiqlik problemi — IEEE 754-ün təbiətindən qaynaqlanır
print(0.1 + 0.2)               # 0.30000000000000004 (0.3 deyil!)
print(0.1 + 0.2 == 0.3)        # False!

# Həll yolu: math.isclose() və ya decimal modulu
import math
print(math.isclose(0.1 + 0.2, 0.3))  # True — tolerans daxilində müqayisə edir

from decimal import Decimal
print(Decimal('0.1') + Decimal('0.2'))  # 0.3 — dəqiq arifmetika
```

> [!tip] **Best Practice — Floating-Point Arifmetikası**
> Maliyyə hesablamalarında **heç vaxt** `float` istifadə etməyin. Əvəzinə `decimal.Decimal` modulundan istifadə edin. AI/ML sahəsində isə bu problem adətən nəzərə alınmır, çünki modelin öyrənmə prosesində kiçik yuvarlama xətaları əhəmiyyətsizdir. Lakin loss function-ların çox kiçik dəyərlərə yaxınlaşdığı hallarda `float32` vs `float64` seçimi kritik ola bilər.

**`complex` (Kompleks ədəd)**

Kompleks ədədlər real və xəyali hissədən ibarətdir. Riyazi hesablamalar, siqnal emalı və kvant hesablamalarında istifadə olunur.

```python
# Kompleks ədəd yaratmaq — j xəyali vahidi təmsil edir
z = 3 + 4j
print(z.real)        # 3.0 — real hissə
print(z.imag)        # 4.0 — xəyali hissə
print(abs(z))        # 5.0 — modul (Pifaqor teoremi: √(3² + 4²))
```

#### 3.2.2 String (Mətn tipi)

String — simvolların ardıcıl toplusudur (**sequence of characters**). Python-da stringlər **dəyişilməzdir** (immutable) — yaradıldıqdan sonra daxili simvollarını dəyişmək mümkün deyil. Hər "dəyişiklik" əslində yeni bir string obyekti yaradır.

```python
# String yaratmanın müxtəlif yolları
single_quotes = 'Salam'                # Tək dırnaq
double_quotes = "Dünya"                # Qoşa dırnaq — fərqi yoxdur
multiline = """Bu çox
sətirli bir
stringdir."""                           # Üç dırnaq — çoxsətirli
raw_string = r"C:\new\folder"          # Raw string — escape simvolları emal olunmur

# f-string (Formatted String Literal) — Python 3.6+
planet = "Arrakis"
spice_output = 1_500_000
report = f"{planet} planetinin illik spice hasilatı: {spice_output:,} ton"
# Nəticə: "Arrakis planetinin illik spice hasilatı: 1,500,000 ton"

# String metodları
text = "  Python Engineering  "
print(text.strip())          # "Python Engineering" — əvvəl/sondakı boşluqları silir
print(text.lower())          # "  python engineering  " — kiçik hərflərə çevirir
print(text.upper())          # "  PYTHON ENGINEERING  " — böyük hərflərə çevirir
print(text.replace("Python", "AI"))  # "  AI Engineering  " — əvəzetmə
print(text.split())          # ['Python', 'Engineering'] — boşluqlara görə bölür
print("-".join(["2024", "01", "15"]))  # "2024-01-15" — birləşdirmə
```

```python
# String slicing — indekslər vasitəsilə alt-string almaq
# İndekslər 0-dan başlayır, son indeks daxil deyil
word = "PYTHON"
#        P  Y  T  H  O  N
#        0  1  2  3  4  5   (müsbət indeks)
#       -6 -5 -4 -3 -2 -1   (mənfi indeks)

print(word[0])       # 'P' — birinci simvol
print(word[-1])      # 'N' — sonuncu simvol
print(word[0:3])     # 'PYT' — 0-dan 3-ə qədər (3 daxil deyil)
print(word[::2])     # 'PTO' — hər ikinci simvol (step=2)
print(word[::-1])    # 'NOHTYP' — tərsinə çevirmə
```

> [!tip] **Best Practice — String Immutability və Performans**
> Çoxlu string birləşdirmə (`+` operatoru) əməliyyatı lazım olduqda **`str.join()`** istifadə edin. Hər `+` əməliyyatı yeni string obyekti yaratdığı üçün loop içində `+=` istifadə etmək **O(n²)** mürəkkəbliyə malikdir. `"".join(list_of_strings)` isə **O(n)** mürəkkəbliklə işləyir, çünki bütün string-ləri bir dəfə birləşdirir.

#### 3.2.3 Boolean Tipi

Boolean tipi yalnız iki dəyər alır: `True` (1) və `False` (0). Şərt ifadələrinin və məntiqi əməliyyatların əsasını təşkil edir. Python-da `bool` tipi əslində `int` tipinin alt sinifidir (`True == 1`, `False == 0`).

```python
# Boolean dəyərlər
is_trained = True
has_errors = False

# Boolean kontekstdə "truthy" və "falsy" dəyərlər
# Aşağıdakılar False hesab olunur (falsy):
#   - None, False, 0, 0.0, 0j
#   - Boş kolleksiyalar: '', [], (), {}, set(), frozenset()
#   - __bool__() metodu False qaytaran obyektlər

# Nümunə: boş siyahı falsy-dir
data = []
if not data:
    print("Məlumat yoxdur")  # Bu sətir çap olunacaq

# bool() funksiyası ilə truthy/falsy yoxlamaq
print(bool(0))        # False
print(bool(42))       # True — sıfırdan fərqli hər ədəd truthy-dir
print(bool(""))       # False — boş string
print(bool("hello"))  # True — dolu string
print(bool(None))     # False
```

#### 3.2.4 NoneType

`None` — Python-da "heç nə" və ya "dəyər yoxdur" anlayışını ifadə edən xüsusi singleton obyektdir. Digər dillərdəki `null`, `nil` konseptinin analoqu kimi düşünə bilərsiniz.

```python
# None istifadəsi
result = None                      # Hələ dəyər təyin edilməyib

# None yoxlamaq üçün 'is' operatoru istifadə edin, '==' yox
if result is None:                 # ✅ Düzgün — identity yoxlaması
    print("Nəticə yoxdur")

if result == None:                 # ❌ Səhv — equality yoxlaması (override oluna bilər)
    print("Bunu etməyin")
```

### 3.3 Tip Çevirmələri (Type Conversion)

Python-da tip çevirmələri iki kateqoriyaya bölünür:

**İmplisit (Implicit/Automatic)** — Python özü avtomatik çevirir:

```python
# int + float = float (Python avtomatik genişləndirir)
result = 5 + 3.14    # 8.14 — int avtomatik float-a çevrildi
print(type(result))  # <class 'float'>

# bool → int (True=1, False=0)
total = True + True + False  # 2
```

**Eksplisit (Explicit/Manual)** — proqramçı özü çevirir:

```python
# Tip çevirmə funksiyaları
age_str = "25"
age_int = int(age_str)        # str → int
age_float = float(age_str)    # str → float: 25.0
back_to_str = str(age_int)    # int → str: "25"

# Diqqət: etibarsız çevirmə ValueError verir
# int("hello")  # ValueError: invalid literal for int() with base 10: 'hello'
```

### 3.4 Məlumat Tipləri Müqayisə Cədvəli

| Tip | Dəyişən? (Mutable) | Nümunə | İstifadə sahəsi |
|---|---|---|---|
| `int` | ❌ Immutable | `42` | Sayğaclar, indekslər |
| `float` | ❌ Immutable | `3.14` | Elmi hesablamalar |
| `complex` | ❌ Immutable | `3+4j` | Siqnal emalı |
| `str` | ❌ Immutable | `"hello"` | Mətn əməliyyatları |
| `bool` | ❌ Immutable | `True` | Şərt ifadələri |
| `NoneType` | ❌ Immutable | `None` | Dəyərin olmaması |
| `list` | ✅ Mutable | `[1, 2, 3]` | Dinamik kolleksiyalar |
| `tuple` | ❌ Immutable | `(1, 2, 3)` | Sabit kolleksiyalar |
| `dict` | ✅ Mutable | `{"a": 1}` | Key-value xəritələmə |
| `set` | ✅ Mutable | `{1, 2, 3}` | Unikal dəyərlər toplusu |

---

## 4. İdarəetmə Strukturları (Control Structures)

İdarəetmə strukturları proqramın icra axınını (execution flow) yönləndirən konstruksiyalardır. Onlar olmadan proqram yalnız yuxarıdan aşağıya, ardıcıl şəkildə işləyərdi. Bu strukturlar proqrama **qərar vermə** və **təkrarlama** qabiliyyəti verir.

### 4.1 Şərt İfadələri: `if`, `elif`, `else`

Şərt ifadəsi — verilmiş şərtin doğruluğuna (True/False) əsasən müəyyən kod blokunun icra edilib-edilməyəcəyinə qərar verən konstruksiyadır.

**Sintaksis:**

```python
if şərt_1:
    # şərt_1 True olduqda icra olunan blok
elif şərt_2:
    # şərt_1 False, şərt_2 True olduqda icra olunan blok
else:
    # yuxarıdakı heç bir şərt True olmadıqda icra olunan blok
```

**Ətraflı nümunə:**

```python
# Model performansını qiymətləndirmə sistemi
# accuracy dəyərinə görə müxtəlif hərəkətlər yerinə yetiririk
model_accuracy = 0.87

if model_accuracy >= 0.95:
    # 95% və yuxarı — istehsala hazırdır
    status = "Production-ready"
    action = "Deploy to production"
elif model_accuracy >= 0.85:
    # 85%-95% arası — yaxşıdır, amma fine-tuning lazımdır
    status = "Good"
    action = "Fine-tune hyperparameters"
elif model_accuracy >= 0.70:
    # 70%-85% arası — əlavə data və ya arxitektura dəyişikliyi lazımdır
    status = "Needs improvement"
    action = "Collect more training data"
else:
    # 70%-dən aşağı — ciddi problem var
    status = "Poor"
    action = "Review model architecture and data quality"

print(f"Model status: {status}")    # "Good"
print(f"Next step: {action}")       # "Fine-tune hyperparameters"
```

**Ternary (şərti) ifadə — tək sətirlik if/else:**

```python
# Standart forma:  dəyər_1 if şərt else dəyər_2
age = 20
category = "adult" if age >= 18 else "minor"

# Nested ternary (oxunaqlılığı azalda bilər, ehtiyatla istifadə edin)
score = 85
grade = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "F"
```

### 4.2 `match-case` İfadəsi (Python 3.10+)

Python 3.10 ilə təqdim olunan **structural pattern matching** — digər dillərdəki `switch-case`-in daha güclü versiyasıdır. Sadəcə dəyər müqayisəsi deyil, həm də **data strukturlarının formasına** görə matching edə bilir.

```python
# HTTP status code-larını emal etmək
def handle_response(status_code):
    match status_code:
        case 200:
            return "Success — Sorğu uğurla tamamlandı"
        case 301:
            return "Moved Permanently — Resurs köçürülüb"
        case 404:
            return "Not Found — Resurs tapılmadı"
        case 500:
            return "Internal Server Error — Server xətası"
        case _:
            # '_' wildcard pattern-dir — yuxarıdakıların heç birinə uyğun gəlmədikdə işləyir
            return f"Unknown status: {status_code}"

print(handle_response(404))  # "Not Found — Resurs tapılmadı"
```

```python
# Structural pattern matching — data strukturlarına görə matching
def process_command(command):
    match command.split():
        case ["quit"]:
            # Tək "quit" sözü
            return "Exiting..."
        case ["train", model_name]:
            # "train" + model adı: ["train", "gpt4"] kimi
            return f"Training model: {model_name}"
        case ["train", model_name, *hyperparams]:
            # "train" + model adı + istənilən sayda əlavə parametr
            return f"Training {model_name} with params: {hyperparams}"
        case _:
            return "Unknown command"

print(process_command("train gpt4"))             # "Training model: gpt4"
print(process_command("train gpt4 lr=0.01 epochs=10"))  # "Training gpt4 with params: ['lr=0.01', 'epochs=10']"
```

### 4.3 Dövrlər (Loops)

Dövrlər — müəyyən kod blokunun təkrar-təkrar icra edilməsini təmin edən konstruksiyalardır. Python-da iki əsas dövr növü var: `for` və `while`.

#### 4.3.1 `for` Dövrü

`for` dövrü **iterasiya edilə bilən** (iterable) obyektin hər bir elementi üzərindən keçir. Iterable — ardıcıl olaraq elementlərini tək-tək qaytara bilən hər hansı obyektdir (list, tuple, string, dict, set, range, file və s.).

```python
# Sadə for dövrü — siyahı üzərində iterasiya
frameworks = ["TensorFlow", "PyTorch", "JAX", "scikit-learn"]
for framework in frameworks:
    # Hər iterasiyada 'framework' dəyişəni siyahının növbəti elementini alır
    print(f"Framework: {framework}")

# range() funksiyası — ədəd ardıcıllığı generasiya edir
# range(start, stop, step) — stop daxil deyil
for i in range(5):
    # 0, 1, 2, 3, 4 — default olaraq 0-dan başlayır
    print(i)

for i in range(2, 10, 3):
    # 2, 5, 8 — 2-dən başlayır, 3 addımla, 10-a qədər (10 daxil deyil)
    print(i)

# enumerate() — həm indeksi, həm elementi almaq üçün
layers = ["Input", "Hidden_1", "Hidden_2", "Output"]
for index, layer in enumerate(layers):
    # enumerate() hər element üçün (indeks, dəyər) cütü qaytarır
    print(f"Layer {index}: {layer}")

# zip() — paralel iterasiya (eyni anda iki və ya daha çox iterable üzərindən)
models = ["GPT-4", "Claude", "Gemini"]
scores = [92.5, 91.8, 90.3]
for model, score in zip(models, scores):
    print(f"{model}: {score}%")
```

> [!tip] **Best Practice — `enumerate()` vs Manual Counter**
> Heç vaxt loop içində manual sayğac (`i = 0; i += 1`) istifadə etməyin. `enumerate()` daha Pythonic, oxunaqlı və xətaya daha az meyillidir. `start` parametri ilə indeksi istənilən rəqəmdən başlada bilərsiniz: `enumerate(items, start=1)`.

#### 4.3.2 `while` Dövrü

`while` dövrü — verilmiş şərt `True` olduğu müddətcə icra olunan dövrüdür. `for` dövründən fərqli olaraq, iterasiya sayı əvvəlcədən bilinməyə bilər.

```python
# Sadə while dövrü — model training simulation
epoch = 0
loss = 1.0         # Başlanğıc loss dəyəri
target_loss = 0.01 # Hədəf loss dəyəri

while loss > target_loss:
    # Hər iterasiyada loss azalır (simulyasiya)
    loss *= 0.7     # Loss-u 30% azaldırıq
    epoch += 1
    print(f"Epoch {epoch}: Loss = {loss:.6f}")

print(f"Training tamamlandı! {epoch} epoch lazım oldu.")
```

```python
# while True ilə sonsuz dövr — user input loop
while True:
    user_input = input("Əmr daxil edin ('quit' — çıxış): ")
    if user_input.lower() == 'quit':
        print("Proqramdan çıxılır...")
        break   # Dövrü dayandırır
    print(f"Əmr qəbul edildi: {user_input}")
```

> [!warning] **Diqqət — Sonsuz Dövrlər**
> `while True` istifadə edərkən **mütləq** `break` şərti olmalıdır, əks halda proqram sonsuza qədər işləyəcək. Production kodda timeout mexanizmi əlavə etmək tövsiyə olunur.

#### 4.3.3 Dövr İdarəetmə Açar Sözləri: `break`, `continue`, `pass`

```python
# break — dövrü tamamilə dayandırır
print("=== break nümunəsi ===")
for num in range(1, 100):
    if num % 17 == 0:
        # 17-yə bölünən ilk ədədi tapdıqda dövrü dayandır
        print(f"17-yə bölünən ilk ədəd: {num}")
        break

# continue — cari iterasiyanı atlayır, növbəti iterasiyaya keçir
print("\n=== continue nümunəsi ===")
for num in range(10):
    if num % 2 == 0:
        # Cüt ədədləri atlayırıq
        continue
    # Bu sətir yalnız tək ədədlər üçün icra olunur
    print(f"Tək ədəd: {num}")

# pass — heç nə etmir (placeholder kimi istifadə olunur)
print("\n=== pass nümunəsi ===")
for item in range(5):
    if item < 3:
        pass    # TODO: Bu hissəni sonra implementasiya edəcəyik
    else:
        print(f"İşlənir: {item}")
```

#### 4.3.4 `for...else` və `while...else`

Python-a xas unikal bir xüsusiyyət: dövrlərə `else` bloku əlavə etmək mümkündür. `else` bloku **yalnız dövr `break` ilə dayandırılmadıqda** icra olunur.

```python
# Siyahıda mənfi ədəd axtarmaq
dataset = [4.2, 7.1, 2.8, 9.5, 1.3]

for value in dataset:
    if value < 0:
        print(f"Mənfi dəyər tapıldı: {value}")
        break
else:
    # Bu blok yalnız 'break' işləmədikdə (heç bir mənfi dəyər tapılmadıqda) icra olunur
    print("Dataset-də mənfi dəyər yoxdur — data validation uğurludur!")

# Nəticə: "Dataset-də mənfi dəyər yoxdur — data validation uğurludur!"
```

---

## 5. Funksiyalar (Functions)

### 5.1 Funksiya Nədir?

Funksiya — **müəyyən bir tapşırığı yerinə yetirmək üçün adlandırılmış, təkrar istifadə edilə bilən kod blokudur**. Funksiyalar kodun modullara bölünməsini, təkrar istifadəsini və test edilməsini asanlaşdırır. Bu, proqram mühəndisliyinin ən fundamental abstraksiya mexanizmlərindən biridir.

Funksiyalar **DRY (Don't Repeat Yourself)** prinsipinin praktik tətbiqidir — eyni kodu bir neçə yerdə yazmaq əvəzinə, bir dəfə funksiya kimi təyin edib, lazım olan yerdən çağırırsınız.

### 5.2 Funksiya Təyini və Çağırışı

```python
# Funksiya təyini (definition) — 'def' açar sözü ilə
def calculate_bmi(weight_kg, height_m):
    """
    Bədən Kütlə İndeksini (BMI) hesablayır.

    Args:
        weight_kg (float): Çəki, kiloqramla
        height_m (float): Boy, metrlə

    Returns:
        float: BMI dəyəri (weight / height²)
    """
    # Giriş məlumatlarının yoxlanması (input validation)
    if height_m <= 0:
        raise ValueError("Boy müsbət ədəd olmalıdır")
    if weight_kg <= 0:
        raise ValueError("Çəki müsbət ədəd olmalıdır")

    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)   # 2 ondalık rəqəmə yuvarlaqlaşdır

# Funksiya çağırışı (call)
result = calculate_bmi(75, 1.80)
print(f"BMI: {result}")    # BMI: 23.15
```

### 5.3 Parametrlər və Arqumentlər

**Parametr** — funksiya təyinindəki dəyişən adıdır. **Arqument** — funksiya çağırışında parametrə ötürülən konkret dəyərdir.

```python
def create_model_config(
    model_name,                          # Positional (mövqeli) parametr — mütləq verilməlidir
    learning_rate=0.001,                 # Default dəyərli parametr — verilməsə 0.001 olacaq
    epochs=100,                          # Default dəyərli parametr
    *layers,                             # *args — istənilən sayda əlavə positional arqument tuple olaraq yığır
    optimizer="adam",                    # Keyword-only parametr (*-dən sonra gəldiyi üçün)
    **hyperparams                        # **kwargs — istənilən sayda keyword arqument dict olaraq yığır
):
    """
    ML model konfiqurasiyası yaradır.

    *layers — gizli qatların neuron saylarını tuple olaraq toplayır.
    **hyperparams — əlavə hiperparametrləri dict olaraq toplayır.
    """
    config = {
        "model_name": model_name,
        "learning_rate": learning_rate,
        "epochs": epochs,
        "layers": layers,                # Tuple olacaq: (256, 128, 64)
        "optimizer": optimizer,
        "extra": hyperparams             # Dict olacaq: {"dropout": 0.3, "batch_size": 32}
    }
    return config

# Funksiya çağırışı — müxtəlif arqument ötürmə üsulları
config = create_model_config(
    "Transformer",          # model_name (positional)
    0.0001,                 # learning_rate (positional, default-u override edir)
    50,                     # epochs (positional, default-u override edir)
    256, 128, 64,           # *layers — tuple olaraq yığılacaq: (256, 128, 64)
    optimizer="adamw",      # keyword-only parametr
    dropout=0.3,            # **hyperparams dict-ə düşəcək
    batch_size=32           # **hyperparams dict-ə düşəcək
)

print(config)
# {
#   'model_name': 'Transformer',
#   'learning_rate': 0.0001,
#   'epochs': 50,
#   'layers': (256, 128, 64),
#   'optimizer': 'adamw',
#   'extra': {'dropout': 0.3, 'batch_size': 32}
# }
```

### 5.4 Parametr Növləri Müqayisəsi

| Parametr Növü | Sintaksis | Məcburidirmi? | Nümunə |
|---|---|---|---|
| Positional | `def f(x)` | ✅ Bəli | `f(5)` |
| Default | `def f(x=10)` | ❌ Xeyr | `f()` → x=10, `f(5)` → x=5 |
| `*args` | `def f(*args)` | ❌ Xeyr | `f(1, 2, 3)` → args=(1, 2, 3) |
| Keyword-only | `def f(*, key)` | ✅ Bəli (keyword olaraq) | `f(key=5)` |
| `**kwargs` | `def f(**kwargs)` | ❌ Xeyr | `f(a=1, b=2)` → kwargs={"a":1, "b":2} |

> [!tip] **Best Practice — Mutable Default Argument Tələsi**
> **Heç vaxt** mutable obyekti (list, dict, set) default parametr kimi istifadə etməyin. Python default dəyəri funksiya təyinində **bir dəfə** yaradır və hər çağırışda eyni obyekti istifadə edir — bu, gözlənilməz davranışa səbəb olur.
>
> ```python
> # ❌ SƏHV — Hər çağırışda eyni list istifadə olunur
> def add_item(item, items=[]):
>     items.append(item)
>     return items
>
> print(add_item("a"))  # ['a']
> print(add_item("b"))  # ['a', 'b'] — Gözlənilən: ['b']!
>
> # ✅ DÜZGÜN — None istifadə edin və funksiyanın içində yaradın
> def add_item(item, items=None):
>     if items is None:
>         items = []
>     items.append(item)
>     return items
> ```

### 5.5 Scope (Əhatə Dairəsi) — LEGB Qaydası

Python-da dəyişənlərin axtarışı **LEGB** qaydasına əsasən aparılır. Bu, interpretatonun bir dəyişən adını tapmaq üçün hansı ardıcıllıqla axtarış etdiyini müəyyən edir:

| Səviyyə | Ad | İzah | Nümunə |
|---|---|---|---|
| **L** | Local | Funksiyanın daxili | Funksiya parametrləri, lokal dəyişənlər |
| **E** | Enclosing | Əhatə edən funksiyanın daxili | İç-içə funksiyalarda xarici funksiyanın dəyişənləri |
| **G** | Global | Modul səviyyəsi | Faylın ən üst səviyyəsindəki dəyişənlər |
| **B** | Built-in | Python-un daxili | `print`, `len`, `range` və s. |

```python
# LEGB nümunəsi
built_in_example = len  # B — Built-in: Python ilə gələn funksiya

global_var = "Global"   # G — Global: modul səviyyəsində

def outer_function():
    enclosing_var = "Enclosing"  # E — Enclosing: xarici funksiyanın dəyişəni

    def inner_function():
        local_var = "Local"       # L — Local: daxili funksiyanın dəyişəni

        # Python axtarış ardıcıllığı: L → E → G → B
        print(local_var)          # L-dən tapır: "Local"
        print(enclosing_var)      # E-dən tapır: "Enclosing"
        print(global_var)         # G-dən tapır: "Global"

    inner_function()

outer_function()
```

```python
# global və nonlocal açar sözləri
counter = 0  # Global dəyişən

def increment():
    global counter      # 'global' — global dəyişəni dəyişmək üçün lazımdır
    counter += 1

def outer():
    count = 0

    def inner():
        nonlocal count  # 'nonlocal' — enclosing scope-dakı dəyişəni dəyişmək üçün
        count += 1

    inner()
    print(count)  # 1

increment()
print(counter)    # 1
```

> [!tip] **Best Practice — Global Dəyişənlərdən Qaçının**
> `global` açar sözünün istifadəsi demək olar ki, həmişə pis dizayn əlamətidir. Global state kodun test edilməsini, debug edilməsini və parallelləşdirilməsini çətinləşdirir. Əvəzinə dəyərləri **parametr olaraq ötürün** və **return ilə qaytarın**. Əgər paylaşılan state lazımdırsa, siniflərdən istifadə edin.

### 5.6 Lambda Funksiyaları

Lambda — tək ifadədən ibarət, anonim (adsız) funksiyadır. `def` ilə yaradılan funksiyalardan fərqli olaraq, lambda yalnız **bir ifadə** (expression) ehtiva edə bilər, **ifadə bloku** (statement block) deyil.

Lambda-lar əsasən `sorted()`, `map()`, `filter()` kimi yüksək səviyyəli funksiyalara qısa callback ötürmək üçün istifadə olunur.

```python
# Lambda sintaksisi: lambda parametrlər: ifadə
square = lambda x: x ** 2
print(square(5))  # 25

# Praktik istifadə — sıralama meyarı olaraq
models = [
    {"name": "GPT-4", "accuracy": 92.5, "latency_ms": 850},
    {"name": "Claude", "accuracy": 91.8, "latency_ms": 620},
    {"name": "Gemini", "accuracy": 90.3, "latency_ms": 480},
]

# accuracy-yə görə azalan sıra ilə sıralamaq
sorted_by_accuracy = sorted(models, key=lambda m: m["accuracy"], reverse=True)

# latency-yə görə artan sıra ilə sıralamaq
sorted_by_speed = sorted(models, key=lambda m: m["latency_ms"])

# map() — hər elementə funksiya tətbiq etmək
names = list(map(lambda m: m["name"], models))
# ['GPT-4', 'Claude', 'Gemini']

# filter() — şərtə uyğun elementləri süzmək
fast_models = list(filter(lambda m: m["latency_ms"] < 700, models))
# [{"name": "Claude", ...}, {"name": "Gemini", ...}]
```

> [!tip] **Best Practice — Lambda vs `def`**
> Lambda-nı dəyişənə təyin etmək (`square = lambda x: x**2`) PEP 8-ə görə tövsiyə olunmur. Əgər funksiyaya ad vermək lazımdırsa, `def` istifadə edin. Lambda-lar yalnız inline, birdəfəlik istifadə üçün nəzərdə tutulub. Mürəkkəb məntiqi lambda ilə yazmağa çalışmaq kodun oxunaqlılığını ciddi şəkildə azaldır.

### 5.7 Type Hints (Tip Göstəriciləri)

Python 3.5+ ilə təqdim olunan type hints, funksiya parametrlərinin və qaytarma dəyərinin gözlənilən tipini sənədləşdirmək üçün istifadə olunur. Python runtime-da bunları **icra etmir** (enforce), lakin `mypy`, `pyright` kimi alətlər onları statik analiz üçün istifadə edir.

```python
# Type hints ilə funksiya təyini
def train_model(
    model_name: str,                          # str tipli parametr
    epochs: int = 100,                        # int tipli, default dəyərli
    learning_rate: float = 0.001,             # float tipli, default dəyərli
    layers: list[int] | None = None,          # int list-i və ya None (Python 3.10+)
    verbose: bool = False                     # bool tipli
) -> dict[str, float]:                        # Qaytarma tipi: str key və float dəyərli dict
    """Model treninqi aparır və nəticələri qaytarır."""
    if layers is None:
        layers = [128, 64, 32]

    # Simulyasiya
    final_loss = 0.05 * (1 / learning_rate) / epochs
    return {
        "final_loss": round(final_loss, 6),
        "accuracy": round(1 - final_loss, 4)
    }

# Type hints IDE-nin autocomplete və xəta aşkarlama qabiliyyətini artırır
result: dict[str, float] = train_model("ResNet", epochs=50, layers=[256, 128])
```

> [!tip] **Best Practice — Type Hints Hər Yerdə İstifadə Edin**
> Production kodda **bütün** funksiyalara type hint əlavə edin. Bu:
> 1. Kodu özünü sənədləşdirən (self-documenting) edir
> 2. IDE-nin daha dəqiq autocomplete verməsini təmin edir
> 3. `mypy` ilə birlikdə bir çox bug-u runtime-dan əvvəl tutur
> 4. Komanda üzvlərinin kodu daha tez anlamasına kömək edir
>
> CI/CD pipeline-ınıza `mypy --strict` əlavə edin.

### 5.8 Docstrings

Docstring — funksiyanın, sinifin və ya modulun birinci sətirində yerləşən **string literal**-dir. `help()` funksiyası və IDE-lər tərəfindən oxunur. Google, NumPy və Sphinx stilləri mövcuddur.

```python
def normalize_data(
    data: list[float],
    method: str = "min-max"
) -> list[float]:
    """
    Verilmiş data-nı normalizasiya edir.

    Normalizasiya, müxtəlif miqyaslı xüsusiyyətləri (features) eyni miqyasa
    gətirmək üçün istifadə olunan məlumat emalı texnikasıdır. Bu, ML modellərinin
    daha effektiv öyrənməsi üçün kritikdir.

    Args:
        data: Normalizasiya ediləcək ədədi dəyərlər siyahısı.
              Boş siyahı ötürüldükdə boş siyahı qaytarır.
        method: Normalizasiya metodu. Mövcud seçimlər:
                - "min-max": Dəyərləri [0, 1] aralığına gətirir
                - "z-score": Ortalama=0, standart kənarlaşma=1

    Returns:
        Normalizasiya edilmiş dəyərlər siyahısı.

    Raises:
        ValueError: Naməlum method daxil edildikdə.
        ValueError: Bütün dəyərlər eyni olduqda (bölmə sıfıra).

    Examples:
        >>> normalize_data([1, 2, 3, 4, 5])
        [0.0, 0.25, 0.5, 0.75, 1.0]

        >>> normalize_data([10, 20, 30], method="min-max")
        [0.0, 0.5, 1.0]
    """
    if not data:
        return []

    if method == "min-max":
        min_val, max_val = min(data), max(data)
        if min_val == max_val:
            raise ValueError("Bütün dəyərlər eynidir — normalizasiya mümkün deyil")
        return [(x - min_val) / (max_val - min_val) for x in data]
    elif method == "z-score":
        mean = sum(data) / len(data)
        std = (sum((x - mean) ** 2 for x in data) / len(data)) ** 0.5
        if std == 0:
            raise ValueError("Standart kənarlaşma 0-dır — normalizasiya mümkün deyil")
        return [(x - mean) / std for x in data]
    else:
        raise ValueError(f"Naməlum metod: {method}. 'min-max' və ya 'z-score' istifadə edin.")
```

---

## 6. Gün 1 — Xülasə

Bu gün Python-un əsas tikinti bloklarını öyrəndik:

| Mövzu | Əsas Nöqtə |
|---|---|
| Python-a Giriş | High-level, interpreted, multi-paradigm dil; AI ekosisteminin əsası |
| Sintaksis/İndentasiya | İndentasiya sintaktik qaydadır; PEP 8 standartına əməl edin |
| Dəyişənlər | Dəyişənlər obyektlərə istinadlardır (references), qutular deyil |
| Məlumat Tipləri | int, float, complex, str, bool, NoneType; mutable vs immutable |
| if/elif/else | Şərt əsaslı icra axını; match-case (3.10+) |
| for/while | Iterasiya; enumerate(), zip(), break/continue/pass |
| Funksiyalar | DRY prinsipi; *args/**kwargs; LEGB scope; type hints |

---

> [!note] **Növbəti Gün**
> **Gün 2**-də Python-un əsas data strukturlarını (Lists, Tuples, Dictionaries, Sets) dərindən öyrənəcəyik — hər birinin performans xüsusiyyətləri, istifadə sahələri və bir-birindən fərqləri ilə birlikdə.
