# Həftə 1 - Gün 3: List Comprehensions, Generators, Decorators

`learning/week_1/Week1_Day3_Comprehensions_Generators_Decorators.md`

---

## 1. Comprehensions (Anlama İfadələri)

### 1.1 Comprehension Nədir?

Comprehension — Python-a xas olan, **bir iterable üzərindən yeni kolleksiya yaratmaq** üçün kompakt və oxunaqlı sintaksis formalarıdır. Əsasən `for` dövrü + şərt + transformasiya əməliyyatını **tək sətirdə** ifadə etməyə imkan verir.

Comprehension-ların üç əsas növü var:
- **List comprehension** — `[ifadə for element in iterable if şərt]`
- **Dict comprehension** — `{key: value for element in iterable if şərt}`
- **Set comprehension** — `{ifadə for element in iterable if şərt}`

Comprehension-lar yalnız qısaltma deyil — eyni zamanda adi `for` dövründən **daha sürətli** işləyir, çünki Python interpretatoru onları xüsusi bytecode ilə optimallaşdırır.

### 1.2 List Comprehension

#### Əsas Sintaksis

```
[ifadə for element in iterable]
[ifadə for element in iterable if şərt]
```

Bunu belə oxuyun: "iterable-dəki hər element üçün (əgər şərt doğrudursa) ifadəni hesabla və nəticəni yeni list-ə əlavə et."

#### Ekvivalent `for` Dövrü ilə Müqayisə

```python
# === Məqsəd: 0-dan 9-a qədər ədədlərin kvadratlarını tapmaq ===

# Ənənəvi for dövrü ilə
squares_loop = []
for x in range(10):
    squares_loop.append(x ** 2)

# List comprehension ilə — eyni nəticə, daha kompakt
squares_comp = [x ** 2 for x in range(10)]

# Hər ikisi eyni nəticəni verir:
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

#### Filtrasiya ilə List Comprehension

```python
# Şərtli comprehension — yalnız şərtə uyğun elementlər daxil edilir
raw_data = [12, -5, 0, 7.5, None, "", 42, -3, "noise", 99]

# Yalnız müsbət ədədləri seçmək
# isinstance() ilə tip yoxlaması — yalnız int və float tipləri qəbul edilir
positive_numbers = [
    x for x in raw_data
    if isinstance(x, (int, float))  # Əvvəlcə tipi yoxla
    and x is not None               # None-u kənarlaşdır (None da isinstance keçə bilər)
    and x > 0                       # Yalnız müsbət ədədlər
]
print(positive_numbers)  # [12, 7.5, 42, 99]

# if-else ilə comprehension — transformasiya + şərt
# DİQQƏT: if-else ifadənin ÖNÜNdə, filter isə ARXASINda yazılır
scores = [85, 42, 91, 67, 73, 55, 98]
results = [
    "pass" if score >= 70 else "fail"   # if-else — transformasiya hissəsi (ifadənin özü)
    for score in scores                  # iterasiya
]
# ['pass', 'fail', 'pass', 'fail', 'pass', 'fail', 'pass']
```

> [!tip] **Best Practice — Comprehension-da if vs if-else Mövqeyi**
> Bu, tez-tez qarışdırılan bir xüsusiyyətdir:
> - **Filtrasiya** (`if` alone): `for`-dan **sonra** yazılır → `[x for x in data if x > 0]`
> - **Transformasiya** (`if-else`): `for`-dan **əvvəl** yazılır → `["yes" if x > 0 else "no" for x in data]`
>
> Məntiqi: filtrasiya "hansı elementləri götürəcəyimizi" seçir, transformasiya isə "elementlə nə edəcəyimizi" müəyyən edir.

#### İç-içə (Nested) Comprehension

```python
# 2D matris yaratmaq (3x4 matris)
matrix = [
    [row * 4 + col for col in range(4)]   # Daxili list — hər sətir
    for row in range(3)                     # Xarici list — sətirlərin siyahısı
]
# [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]]

# Matrisi düzləşdirmək (flatten) — 2D → 1D
flat = [
    element
    for row in matrix         # Əvvəl xarici dövr — hər sətir üçün
    for element in row        # Sonra daxili dövr — sətirdəki hər element üçün
]
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

# Dekart hasili (Cartesian product) — bütün kombinasiyalar
models = ["BERT", "GPT"]
sizes = ["base", "large"]
combinations = [
    f"{model}-{size}"
    for model in models
    for size in sizes
]
# ['BERT-base', 'BERT-large', 'GPT-base', 'GPT-large']
```

> [!warning] **Diqqət — Comprehension Oxunaqlılığı**
> İç-içə comprehension-lar 2 səviyyədən çox olmamalıdır. Əgər comprehension tək sətirdə rahat oxunmursa, adi `for` dövrünə çevirin. **Qısa kod ≠ yaxşı kod** — oxunaqlılıq həmişə qısalıqdan önəmlidir.

### 1.3 Dictionary Comprehension

```python
# Sadə dict comprehension
words = ["transformer", "attention", "embedding", "tokenizer"]
word_lengths = {word: len(word) for word in words}
# {'transformer': 11, 'attention': 9, 'embedding': 9, 'tokenizer': 9}

# Mövcud dict-i filtrasiya etmək
model_scores = {
    "GPT-4": 92.5,
    "GPT-3.5": 81.2,
    "BERT": 76.8,
    "Claude": 91.0,
    "T5": 68.4,
}

# Yalnız 80+ bal alan modelləri saxlamaq
top_models = {
    name: score
    for name, score in model_scores.items()
    if score >= 80
}
# {'GPT-4': 92.5, 'GPT-3.5': 81.2, 'Claude': 91.0}

# Key və value-nu dəyişmək (inversion)
inverted = {score: name for name, score in model_scores.items()}
# {92.5: 'GPT-4', 81.2: 'GPT-3.5', 76.8: 'BERT', 91.0: 'Claude', 68.4: 'T5'}

# Enumerate ilə indeks əsaslı dict
features = ["price", "area", "rooms", "floor"]
feature_index = {feature: idx for idx, feature in enumerate(features)}
# {'price': 0, 'area': 1, 'rooms': 2, 'floor': 3}
```

### 1.4 Set Comprehension

```python
# Set comprehension — dublikatlar avtomatik silinir
text = "machine learning is a subset of artificial intelligence"
unique_lengths = {len(word) for word in text.split()}
# {1, 2, 7, 8, 12} — sözlərin unikal uzunluqları (sırasız)

# Data cleaning — unikal, normallaşdırılmış dəyərlər
raw_tags = ["Python", "python", "PYTHON", "Java", "java", "JAVA", "Rust"]
clean_tags = {tag.lower() for tag in raw_tags}
# {'python', 'java', 'rust'}
```

### 1.5 Comprehension Performance Müqayisəsi

```python
import timeit

# 1 milyonluq list yaratmaq — müxtəlif üsullar
n = 1_000_000

# for dövrü + append
def with_loop():
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result

# List comprehension
def with_comprehension():
    return [i ** 2 for i in range(n)]

# map() funksiyası
def with_map():
    return list(map(lambda i: i ** 2, range(n)))

# Nəticələr (təxmini):
# for loop:        ~0.12 saniyə
# comprehension:   ~0.08 saniyə (~33% daha sürətli)
# map():           ~0.10 saniyə
```

---

## 2. Generators (Generatorlar)

### 2.1 Generator Nədir?

Generator — dəyərləri **hamısını bir anda yaddaşda saxlamaq əvəzinə**, **lazım olduqda tək-tək yaradıb qaytaran** xüsusi iterator növüdür. Bu konsept **lazy evaluation** (tənbəl qiymətləndirmə) adlanır.

Bu fərqi başa düşmək üçün bir analoji düşünün: list — bütün yeməklərin eyni anda masaya qoyulduğu bufet; generator isə hər yemək tələb olunduqda hazırlanan restoran menyusu. Bufet çox yer tutur (yaddaş), restoran isə yalnız sifariş verildikdə hazırlayır (lazy evaluation).

**List vs Generator — Yaddaş Fərqi:**

| Xüsusiyyət | List | Generator |
|---|---|---|
| **Yaddaş** | Bütün elementlər eyni anda yaddaşda | Yalnız cari element yaddaşda |
| **1M element yaddaşı** | ~8 MB (int list) | ~120 bytes (generator obyekti) |
| **Sürət (ilk element)** | Bütün list yaradılana qədər gözləyir | Dərhal ilk elementi qaytarır |
| **Təkrar istifadə** | İstənilən qədər iterate oluna bilər | Yalnız bir dəfə iterate oluna bilər |
| **İndekslə müraciət** | ✅ `list[5]` | ❌ Mümkün deyil |

### 2.2 `yield` Açar Sözü

`yield` — funksiyanı generatora çevirən açar sözdür. `return` kimi dəyər qaytarır, lakin funksiyanın icrasını **dayandırır** (pause) və sonrakı çağırışda **davam etdirir** (resume).

Bu davranış funksiya kontekstinin "dondurulması" və "açılması" kimi düşünülə bilər — funksiyanın lokal dəyişənləri, icra nöqtəsi və stack frame-i qorunur.

```python
# Sadə generator funksiyası
def countdown(n):
    """n-dən 1-ə qədər geri sayma generatoru."""
    print(f"Generator başladı: {n}-dən geri sayma")
    while n > 0:
        yield n          # Dəyəri qaytarır və burada DAYANIR
        n -= 1           # Növbəti next() çağırışında BURADAN davam edir
    print("Generator tamamlandı!")

# Generator obyektini yaratmaq — funksiya hələ İCRA OLUNMUR
gen = countdown(5)
print(type(gen))  # <class 'generator'>

# next() ilə dəyərləri tək-tək almaq
print(next(gen))  # "Generator başladı: 5-dən geri sayma" və 5 qaytarır
print(next(gen))  # 4
print(next(gen))  # 3

# for dövrü qalan dəyərləri avtomatik alır
for value in gen:
    print(value)
# 2
# 1
# "Generator tamamlandı!"

# Generator tükəndikdən sonra next() çağırmaq StopIteration verir
# next(gen)  # StopIteration exception
```

```python
# Praktik nümunə: Böyük fayl oxuma generatoru
def read_large_file(file_path, chunk_size=1024):
    """
    Böyük faylı chunk-larla (hissə-hissə) oxuyan generator.

    Faylı tamamilə yaddaşa yükləmək əvəzinə, chunk_size bayt hissələrlə
    oxuyur. 10GB fayl üçün belə yalnız chunk_size qədər yaddaş istifadə edir.
    """
    with open(file_path, 'r') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break       # Fayl sona çatdı
            yield chunk     # Chunk-u qaytarır, sonrakı istəyə qədər gözləyir

# İstifadə:
# for chunk in read_large_file("training_data.csv"):
#     process(chunk)   # Hər chunk ayrıca emal olunur
```

### 2.3 Generator Expressions (Generator İfadələri)

Generator expression — list comprehension-ın lazy versiyasıdır. Kvadrat mötərizə `[]` əvəzinə adi mötərizə `()` istifadə olunur.

```python
# List comprehension — bütün nəticələri dərhal yaddaşda yaradır
squares_list = [x ** 2 for x in range(1_000_000)]
# ~8MB yaddaş istifadə edir

# Generator expression — dəyərləri lazım olduqda yaradır
squares_gen = (x ** 2 for x in range(1_000_000))
# ~120 bytes yaddaş istifadə edir!

# Generator expression-ı funksiyalara birbaşa ötürmək
# (Əlavə mötərizə lazım deyil — funksiya mötərizəsi kifayətdir)
total = sum(x ** 2 for x in range(1_000_000))
max_square = max(x ** 2 for x in range(100))
has_negative = any(x < 0 for x in [1, -2, 3])  # True

# Yaddaş müqayisəsi
import sys
list_size = sys.getsizeof([x ** 2 for x in range(10000)])
gen_size = sys.getsizeof(x ** 2 for x in range(10000))
print(f"List: {list_size:,} bytes")   # ~87,624 bytes
print(f"Generator: {gen_size:,} bytes")  # ~200 bytes
```

> [!tip] **Best Practice — Nə Vaxt Generator, Nə Vaxt List?**
> - **Generator istifadə edin** əgər: data çox böyükdür, yalnız bir dəfə iterate edəcəksiniz, bütün nəticələrə eyni anda ehtiyac yoxdur, pipeline processing edirsiniz.
> - **List istifadə edin** əgər: elementlərə indekslə müraciət lazımdır, `len()` lazımdır, birdən çox dəfə iterate etmək lazımdır, data kiçikdir.
> - **Qızıl qayda**: `sum()`, `max()`, `min()`, `any()`, `all()` kimi funksiyalara ötürərkən HƏMİŞƏ generator expression istifadə edin — list yaratmağa ehtiyac yoxdur.

### 2.4 Generator Pipeline (Boru Xətti)

Generator-ların ən güclü istifadə hallarından biri — bir neçə generatoru zəncirvari bağlayaraq **data processing pipeline** yaratmaqdır. Hər generator yalnız özünə lazım olan minimum yaddaşı istifadə edir.

```python
def read_sensor_data(filepath):
    """Sensor datasını sətir-sətir oxuyur (mərhələ 1)."""
    with open(filepath) as f:
        for line in f:
            yield line.strip()

def parse_readings(lines):
    """Hər sətiri float-a çevirir, xətalıları atlayır (mərhələ 2)."""
    for line in lines:
        try:
            yield float(line)
        except ValueError:
            continue    # Etibarsız sətirləri atlayır

def filter_anomalies(readings, threshold=100.0):
    """Anomaliyaları (həddi aşan dəyərləri) süzür (mərhələ 3)."""
    for reading in readings:
        if reading <= threshold:
            yield reading

def compute_moving_average(readings, window=5):
    """Hərəkətli ortalama hesablayır (mərhələ 4)."""
    buffer = []
    for reading in readings:
        buffer.append(reading)
        if len(buffer) > window:
            buffer.pop(0)
        yield sum(buffer) / len(buffer)

# Pipeline qurulması — hər generator əvvəlkindən data alır
# Heç bir mərhələdə bütün data yaddaşa yüklənmir!
# raw_lines = read_sensor_data("sensors.txt")     # Lazy — heç nə oxumur hələ
# parsed = parse_readings(raw_lines)               # Lazy — gözləyir
# clean = filter_anomalies(parsed)                 # Lazy — gözləyir
# averages = compute_moving_average(clean)          # Lazy — gözləyir
#
# for avg in averages:                             # İndi hamısı işə düşür!
#     print(f"Moving avg: {avg:.2f}")
```

### 2.5 `yield from` — Delegasiya

`yield from` — bir generatorun başqa bir iterable-ın və ya generatorun bütün elementlərini öz adından qaytarmasına imkan verir. Bu, iç-içə generator-ları sadələşdirir.

```python
# yield from olmadan — əl ilə iterasiya
def flatten_manual(nested_list):
    for sublist in nested_list:
        for item in sublist:
            yield item

# yield from ilə — daha təmiz
def flatten(nested_list):
    for sublist in nested_list:
        yield from sublist    # sublist-in bütün elementlərini qaytarır

data = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
print(list(flatten(data)))   # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Rekursiv flatten — istənilən dərinlikdəki nested strukturu düzləşdirir
def deep_flatten(iterable):
    for item in iterable:
        if isinstance(item, (list, tuple)):
            yield from deep_flatten(item)   # Rekursiv çağırış
        else:
            yield item

deeply_nested = [1, [2, [3, [4, [5]]]], 6]
print(list(deep_flatten(deeply_nested)))  # [1, 2, 3, 4, 5, 6]
```

### 2.6 Iterators vs Generators Müqayisəsi

| Xüsusiyyət | Iterator (Manual) | Generator |
|---|---|---|
| **Yaratma** | Class ilə (`__iter__`, `__next__`) | `yield` ilə (funksiya) və ya generator expression |
| **Kod uzunluğu** | Çox (class boilerplate) | Az (funksiya + yield) |
| **State management** | Əl ilə (instance dəyişənləri) | Avtomatik (Python saxlayır) |
| **StopIteration** | Əl ilə `raise` etmək lazım | Avtomatik (`return` və ya funksiya sonu) |
| **İstifadə halı** | Kompleks iterasiya məntiqi | Sadə ardıcıllıq generasiyası |

```python
# Manual iterator — çox kod lazımdır
class CountDown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

# Eyni funksionallıq generator ilə — cəmi 4 sətir
def countdown(start):
    while start > 0:
        yield start
        start -= 1
```

---

## 3. Decorators (Dekoratorlar)

### 3.1 Əvvəlki Konseptlər: First-Class Functions

Dekoratorları başa düşmək üçün əvvəlcə Python-da funksiyaların **birinci sinif vətəndaş** (first-class citizen) olduğunu bilmək lazımdır. Bu o deməkdir ki, funksiyalar:

1. **Dəyişənə təyin edilə bilər** — digər dəyərlər kimi
2. **Başqa funksiyaya parametr olaraq ötürülə bilər** — callback kimi
3. **Başqa funksiyadan qaytarıla bilər** — factory pattern
4. **Data strukturlarında saxlanıla bilər** — list, dict elementləri kimi

```python
# 1. Funksiya dəyişənə təyin oluna bilər
def greet(name):
    return f"Salam, {name}!"

say_hello = greet              # Funksiya obyektini dəyişənə təyin edirik (çağırmırıq!)
print(say_hello("Arrakis"))   # "Salam, Arrakis!" — eyni funksiya, fərqli ad

# 2. Funksiya başqa funksiyaya parametr olaraq ötürülə bilər
def apply_operation(func, value):
    """Verilmiş funksiyanı verilmiş dəyərə tətbiq edir."""
    return func(value)

result = apply_operation(len, "Transformer")   # len funksiyasını ötürürük
print(result)  # 11

# 3. Funksiya başqa funksiyadan qaytarıla bilər
def create_multiplier(factor):
    """Verilmiş əmsala görə vurma funksiyası yaradıb qaytarır."""
    def multiplier(x):
        return x * factor   # 'factor' enclosing scope-dan gəlir (closure)
    return multiplier        # Funksiyanı çağırmadan qaytarırıq

double = create_multiplier(2)
triple = create_multiplier(3)
print(double(5))    # 10
print(triple(5))    # 15
```

### 3.2 Closures (Bağlama)

Closure — **xarici funksiyası artıq icrasını bitirdikdən sonra da** xarici funksiyanın dəyişənlərinə müraciət edə bilən iç-içə (nested) funksiyadır. Dekoratorların texniki əsasını closures təşkil edir.

```python
def create_counter(start=0):
    """
    Hər çağırışda artan sayğac funksiyası yaradır.
    'count' dəyişəni closure vasitəsilə "yadda saxlanılır".
    """
    count = start     # Bu dəyişən closure-da "tutulacaq"

    def increment():
        nonlocal count    # Enclosing scope-dakı 'count'-u dəyişdirmək üçün
        count += 1
        return count

    return increment     # increment funksiyası count-a istinadını saxlayır

# create_counter() artıq icrasını bitirib, amma...
counter_a = create_counter(0)
counter_b = create_counter(100)

print(counter_a())  # 1  — hər çağırış count-u artırır
print(counter_a())  # 2
print(counter_a())  # 3
print(counter_b())  # 101 — müstəqil closure, öz count-u var
print(counter_b())  # 102
```

### 3.3 Decorator Nədir?

Decorator — **başqa bir funksiyanı alıb, onun davranışını dəyişdirən/genişləndirən** və yeni funksiyanı qaytaran funksiya/callable-dır. Orijinal funksiyanın kodunu dəyişdirmədən ona əlavə funksionallıq "sarımaq" (wrap) üçün istifadə olunur.

Bu, **Open/Closed Principle**-in (açıq-qapalı prinsip) praktik tətbiqidir: kod genişləndirməyə açıq, dəyişikliyə qapalı olmalıdır.

**Decorator-un iş prinsipi:**

```
@decorator          my_func = decorator(my_func)
def my_func():  →   # Bu iki yazılış tamamilə ekvivalentdir
    ...
```

### 3.4 Sadə Decorator Yaratmaq

```python
import time
import functools

def timer(func):
    """
    Funksiyanın icra müddətini ölçən decorator.

    Bu decorator:
    1. Orijinal funksiyanı parametr olaraq alır
    2. Wrapper funksiya yaradır — orijinal funksiyanı əhatə edir
    3. Wrapper-i qaytarır — orijinal funksiyanın yerinə keçir
    """
    @functools.wraps(func)   # Orijinal funksiyanın __name__, __doc__ və s. atributlarını qoruyur
    def wrapper(*args, **kwargs):
        # ÖNCƏKİ davranış — funksiyanın icrasından əvvəl
        start_time = time.perf_counter()

        # Orijinal funksiyanı çağırmaq
        result = func(*args, **kwargs)

        # SONRAKİ davranış — funksiyanın icrasından sonra
        elapsed = time.perf_counter() - start_time
        print(f"⏱ {func.__name__}() {elapsed:.4f} saniyədə tamamlandı")

        return result    # Orijinal funksiyanın nəticəsini qaytarır

    return wrapper       # Wrapper funksiyasını qaytarır

# Decorator-u tətbiq etmək — @ sintaksisi ilə
@timer
def train_model(epochs):
    """Model treninqi simulyasiyası."""
    total = 0
    for i in range(epochs * 100000):
        total += i
    return total

# Artıq train_model() çağırılanda wrapper() çağırılacaq
result = train_model(10)
# ⏱ train_model() 0.0523 saniyədə tamamlandı
```

> [!tip] **Best Practice — `functools.wraps` Həmişə İstifadə Edin**
> `@functools.wraps(func)` olmadan, wrapper funksiyası orijinal funksiyanın `__name__`, `__doc__`, `__module__` kimi atributlarını itirər. Bu, debugging və documentation alətlərini pozar. **Hər decorator-da** `@functools.wraps` istifadə etmək qızıl qaydadır.

### 3.5 Parametrli Decorator

Əgər decorator-un özünə parametr ötürmək lazımdırsa, **üç qat iç-içə funksiya** lazımdır: xarici funksiya parametrləri alır, ortadakı funksiyanı (dekoratoru) qaytarır, daxili wrapper isə orijinal funksiyanı əhatə edir.

```python
import functools

def retry(max_attempts=3, delay=1.0):
    """
    Uğursuz funksiyanı verilmiş sayda təkrar cəhd edən decorator.

    Args:
        max_attempts: Maksimum cəhd sayı (default: 3)
        delay: Cəhdlər arası gözləmə müddəti, saniyə (default: 1.0)
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"⚠ {func.__name__}() — Cəhd {attempt}/{max_attempts} uğursuz: {e}")
                    if attempt < max_attempts:
                        import time
                        time.sleep(delay)
            # Bütün cəhdlər uğursuz oldu
            raise last_exception
        return wrapper
    return decorator

# İstifadə — parametrlərlə
@retry(max_attempts=5, delay=0.5)
def fetch_api_data(url):
    """API-dan data alır — şəbəkə xətası ola bilər."""
    import random
    if random.random() < 0.7:    # 70% ehtimalla xəta simulyasiyası
        raise ConnectionError(f"Əlaqə uğursuz: {url}")
    return {"status": "success", "data": [1, 2, 3]}

# result = fetch_api_data("https://api.example.com/data")
```

### 3.6 Birdən Çox Decorator Tətbiqi (Stacking)

Bir funksiyaya birdən çox decorator tətbiq etmək mümkündür. Dekoratorlar **aşağıdan yuxarıya** tətbiq olunur, amma **yuxarıdan aşağıya** icra olunur.

```python
import functools
import time

def timer(func):
    """İcra müddətini ölçür."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"⏱ {func.__name__}: {elapsed:.4f}s")
        return result
    return wrapper

def log_call(func):
    """Funksiya çağırışını log edir."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"📋 {func.__name__}() çağırıldı — args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"✅ {func.__name__}() nəticə qaytardı: {result}")
        return result
    return wrapper

def validate_positive(func):
    """Bütün ədədi arqumentlərin müsbət olduğunu yoxlayır."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg < 0:
                raise ValueError(f"Mənfi dəyər icazə verilmir: {arg}")
        return func(*args, **kwargs)
    return wrapper

# Stacking — dekoratorlar aşağıdan yuxarıya tətbiq olunur:
# 1. validate_positive(calculate_loss) → wrapped_1
# 2. log_call(wrapped_1) → wrapped_2
# 3. timer(wrapped_2) → wrapped_3 (final)
@timer               # 3-cü (ən xarici) — əvvəl icra olunur
@log_call            # 2-ci (ortada)
@validate_positive   # 1-ci (ən daxili) — orijinala ən yaxın
def calculate_loss(predictions, targets):
    """MSE loss hesablayır."""
    n = len(predictions)
    return sum((p - t) ** 2 for p, t in zip(predictions, targets)) / n

loss = calculate_loss([2.5, 0.0, 2.1], [3.0, -0.5, 2.0])
# ⏱ calculate_loss: 0.0001s
# 📋 calculate_loss() çağırıldı — args=([2.5, 0.0, 2.1], [3.0, -0.5, 2.0]), kwargs={}
# ✅ calculate_loss() nəticə qaytardı: 0.17333333333333334
```

### 3.7 Praktik Decorator Nümunələri

#### Cache / Memoization Decorator

```python
import functools

def memoize(func):
    """
    Funksiyanın nəticələrini cache-ləyən decorator (memoization).

    Eyni arqumentlərlə təkrar çağırışlarda hesablama əvəzinə
    cache-dən nəticəni qaytarır. Rekursiv funksiyalarda dramatik
    performans artımı təmin edir.
    """
    cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args in cache:
            print(f"  Cache hit: {func.__name__}{args}")
            return cache[args]
        print(f"  Computing: {func.__name__}{args}")
        result = func(*args)
        cache[args] = result
        return result

    wrapper.cache = cache         # Cache-ə xaricdən müraciət imkanı
    wrapper.clear_cache = cache.clear  # Cache-i təmizləmə funksiyası
    return wrapper

@memoize
def fibonacci(n):
    """N-ci Fibonacci ədədini hesablayır (rekursiv)."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(10))
# İlk çağırış: hər dəyər hesablanır
# Sonrakı çağırışlar: cache-dən alınır
# Memoize olmadan: O(2^n) — eksponensial
# Memoize ilə: O(n) — xətti

# Python-un daxili cache decorator-u (daha effektiv):
# @functools.lru_cache(maxsize=128)
```

> [!tip] **Best Practice — `functools.lru_cache`**
> Öz memoize decorator-unuzu yazmaq əvəzinə, Python-un daxili `@functools.lru_cache(maxsize=128)` dekoratorunu istifadə edin. Bu, **LRU (Least Recently Used)** strategiyası ilə cache idarəsi, thread-safety və `cache_info()` kimi əlavə funksionallıq təqdim edir. Python 3.9+-da `@functools.cache` (limitsiz cache) də mövcuddur.

#### Type Checking Decorator

```python
import functools
from typing import get_type_hints

def enforce_types(func):
    """
    Type hint-ləri runtime-da yoxlayan decorator.

    Python-un type hint-ləri default olaraq runtime-da icra olunmur.
    Bu decorator onları aktiv yoxlamaya çevirir — development
    və testing mərhələlərində faydalıdır.
    """
    hints = get_type_hints(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Parametr adları ilə dəyərləri eşlə
        import inspect
        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        # Hər parametrin tipini yoxla
        for param_name, value in bound.arguments.items():
            if param_name in hints:
                expected_type = hints[param_name]
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"'{param_name}' parametri {expected_type.__name__} tipli olmalıdır, "
                        f"lakin {type(value).__name__} verildi"
                    )

        result = func(*args, **kwargs)

        # Return tipini yoxla
        if 'return' in hints and not isinstance(result, hints['return']):
            raise TypeError(
                f"Qaytarma dəyəri {hints['return'].__name__} tipli olmalıdır, "
                f"lakin {type(result).__name__} qaytarıldı"
            )

        return result

    return wrapper

@enforce_types
def add_numbers(a: int, b: int) -> int:
    return a + b

print(add_numbers(5, 3))       # 8 — düzgün tiplər
# add_numbers("5", 3)          # TypeError: 'a' parametri int tipli olmalıdır
```

### 3.8 Dekoratorların Tətbiq Sahələri

| İstifadə Sahəsi | Nümunə | İzah |
|---|---|---|
| **Logging** | `@log_call` | Funksiya çağırışlarını qeyd edir |
| **Timing** | `@timer` | İcra müddətini ölçür |
| **Caching** | `@lru_cache` | Nəticələri cache-ləyir |
| **Retry** | `@retry(max=3)` | Uğursuz əməliyyatı təkrarlayır |
| **Authentication** | `@login_required` | Web framework-lərdə giriş yoxlaması |
| **Rate Limiting** | `@rate_limit(calls=100)` | API çağırış sayını məhdudlaşdırır |
| **Validation** | `@validate_input` | Giriş məlumatlarını yoxlayır |
| **Deprecation** | `@deprecated("Use X instead")` | Köhnəlmiş funksiyalar üçün xəbərdarlıq |

---

## 4. Comprehensions vs Generators vs Regular Loops Müqayisəsi

| Xüsusiyyət | `for` Loop | List Comprehension | Generator Expression |
|---|---|---|---|
| **Sintaksis** | Çox sətirli | Tək sətirli `[...]` | Tək sətirli `(...)` |
| **Nəticə** | Dəyişənə əl ilə əlavə | Yeni list | Lazy iterator |
| **Yaddaş** | List yaransa — O(n) | O(n) | O(1) |
| **Sürət** | Normal | ~30% daha sürətli | Bütün nəticə lazımdırsa — eyni |
| **Oxunaqlılıq** | Ən aydın | Qısa, amma complex-ləşə bilər | Qısa |
| **Reusability** | — | İstənilən qədər | Yalnız bir dəfə |
| **İstifadə halı** | Mürəkkəb məntiq, side effects | Transformasiya + filtrasiya | Böyük data, pipeline |

---

## 5. Gün 3 — Xülasə

| Mövzu | Əsas Nöqtə |
|---|---|
| **List Comprehension** | `for` loop-un kompakt, sürətli alternativi; list, dict, set versiyaları var |
| **Generator** | Lazy evaluation — yaddaş effektiv; `yield` ilə yaradılır |
| **Generator Expression** | Comprehension-ın lazy versiyası; `()` mötərizə ilə |
| **Generator Pipeline** | Generatorları zəncirləyərək data processing pipeline yaratmaq |
| **First-Class Functions** | Funksiyalar dəyişənə təyin oluna, parametr olaraq ötürülə bilər |
| **Closures** | Daxili funksiyanın xarici funksiyanın dəyişənlərini "yadda saxlaması" |
| **Decorators** | Funksiyanın davranışını kodunu dəyişmədən genişləndirmək; `@` sintaksisi |
| **functools.wraps** | Decorator-da həmişə istifadə edin — orijinal atributları qoruyur |

---

> [!note] **Növbəti Həftə**
> **Həftə 2, Gün 1**-də Python-un fayl əməliyyatları (File I/O) və xətaların idarə edilməsi (Exception Handling) mövzularına keçəcəyik — faylları oxuma/yazma, kontekst menecerləri (`with` ifadəsi) və try/except/finally blokları ilə.
