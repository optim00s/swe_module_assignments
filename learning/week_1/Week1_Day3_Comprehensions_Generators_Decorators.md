# List Comprehensions, Generators, Decorators

---

## 1. List Comprehensions

### 1.1 Tərif

List comprehension — mövcud bir ardıcıllıqdan (iterable) yeni list yaratmağın **qısa, oxunaqlı və Pythonic** üsuludur. Adi `for` dövrü ilə yaradılan list-lə eyni nəticəni verir, lakin daha az kodla.

---

### 1.2 Əsas Sintaksis

```
[ifadə  for  element  in  ardıcıllıq]
```

```python
# Adi for dövrü ilə:
kvadratlar = []
for i in range(1, 6):
    kvadratlar.append(i ** 2)
print(kvadratlar)   # [1, 4, 9, 16, 25]

# List comprehension ilə — EYNI nəticə:
kvadratlar = [i ** 2 for i in range(1, 6)]
print(kvadratlar)   # [1, 4, 9, 16, 25]
```

---

### 1.3 Şərtli List Comprehension (`if`)

**Filtrasiya** — yalnız şərti ödəyən elementləri götürmək:

```
[ifadə  for  element  in  ardıcıllıq  if  şərt]
```

```python
# Cüt ədədlər
cütlər = [i for i in range(10) if i % 2 == 0]
print(cütlər)   # [0, 2, 4, 6, 8]

# 5-dən böyük olanlar
siyahı = [3, 7, 1, 9, 4, 6, 2, 8]
böyüklər = [x for x in siyahı if x > 5]
print(böyüklər)   # [7, 9, 6, 8]

# Yalnız string olanlar
qarışıq = [1, "salam", 3.14, "dünya", True, "Python"]
sözlər = [x for x in qarışıq if isinstance(x, str)]
print(sözlər)   # ['salam', 'dünya', 'Python']
```

---

### 1.4 `if-else` ilə List Comprehension (Ternary)

Hər elementə **transformasiya** tətbiq etmək — `if-else` ifadənin **əvvəlindədir**:

```
[doğru_dəyər  if  şərt  else  yanlış_dəyər  for  element  in  ardıcıllıq]
```

```python
# Müsbət isə özü, mənfi isə 0
ədədlər = [-2, 5, -1, 8, -4, 3]
nəticə = [x if x > 0 else 0 for x in ədədlər]
print(nəticə)   # [0, 5, 0, 8, 0, 3]

# Cüt isə "cüt", tək isə "tək"
etiket = ["cüt" if x % 2 == 0 else "tək" for x in range(6)]
print(etiket)   # ['cüt', 'tək', 'cüt', 'tək', 'cüt', 'tək']
```

> ⚠️ **Fərq:**
> - `[x for x in s if şərt]` → **filtrasiya** (bəzi elementlər atılır)
> - `[x if şərt else y for x in s]` → **transformasiya** (bütün elementlər qalır, dəyişdirilir)

---

### 1.5 İç-içə List Comprehension (Nested)

```python
# İç-içə for dövrü → düzləşdirmə (flatten)
matris = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
düz = [element for sətir in matris for element in sətir]
print(düz)   # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# 3x3 matris yaratmaq
matris = [[i * j for j in range(1, 4)] for i in range(1, 4)]
print(matris)
# [[1,2,3], [2,4,6], [3,6,9]]
```

---

### 1.6 Dict, Set və Tuple Comprehension

Eyni sintaksis digər strukturlar üçün də işlədilir:

```python
# Dict comprehension
kvadratlar = {x: x**2 for x in range(1, 6)}
print(kvadratlar)   # {1:1, 2:4, 3:9, 4:16, 5:25}

# Şərtli dict comprehension
cüt_kvadratlar = {x: x**2 for x in range(10) if x % 2 == 0}
print(cüt_kvadratlar)   # {0:0, 2:4, 4:16, 6:36, 8:64}

# Set comprehension
unikal_uzunluqlar = {len(söz) for söz in ["alma", "armud", "kivi", "gilas"]}
print(unikal_uzunluqlar)   # {4, 5} — sırasız, unikal

# Generator expression (tuple deyil!)
gen = (x**2 for x in range(5))
print(type(gen))   # <class 'generator'>
```

> 💡 `(x for x in ...)` — bu **tuple** deyil, **generator expression**-dır. Tuple üçün: `tuple(x for x in ...)`

---

### 1.7 List Comprehension vs `map()`/`filter()`

```python
ədədlər = [1, 2, 3, 4, 5]

# map() — funksiya tətbiq et
map_nəticəsi    = list(map(lambda x: x**2, ədədlər))
# List comprehension ilə ekvivalent:
lc_nəticəsi     = [x**2 for x in ədədlər]

# filter() — filtrasiya et
filter_nəticəsi = list(filter(lambda x: x % 2 == 0, ədədlər))
# List comprehension ilə ekvivalent:
lc_filtr        = [x for x in ədədlər if x % 2 == 0]
```

Üstünlük: List comprehension adətən daha oxunaqlıdır.

---

### 1.8 Nə Zaman İstifadə Etməli, Nə Zaman Etməməli?

```python
# ✅ Uyğun — sadə, bir sətirdə oxunaqlı
[x**2 for x in range(10) if x % 2 == 0]

# ❌ Uyğun deyil — çox mürəkkəb, ayrı funksiya yaz
[f(x) for x in data if g(x) and h(x) or k(x) if len(x) > 3]
```

**Qayda:** Bir sətirdə rahat oxunmursa — adi `for` dövrü daha aydındır.

---

## 2. Generators (Generatorlar)

### 2.1 Tərif — "Tənbəl" Hesablama

Generator — elementləri **hamısını birdən yaddaşda saxlamayan**, onları yalnız **tələb olunduqda** (lazım olan anda) hesablayan xüsusi bir iterable-dır.

**Adi list vs generator:**

```python
import sys

# List — hamısını yaddaşda saxlayır
adi_list = [x**2 for x in range(1_000_000)]
print(sys.getsizeof(adi_list))    # ~8 MB!

# Generator — yalnız bir element saxlayır
gen = (x**2 for x in range(1_000_000))
print(sys.getsizeof(gen))         # ~120 bytes
```

---

### 2.2 `yield` Açar Sözü

`yield` — funksiyanı **generator funksiyasına** çevirir. `return`-dən fərqi:
- `return` funksiyanı bitirər, dəyər qaytarır
- `yield` funksiyanı **dayandırır**, dəyər verir, sonra **davam etdirilə bilər**

```python
def sayac():
    print("Birinci yield-dən əvvəl")
    yield 1
    print("İkinci yield-dən əvvəl")
    yield 2
    print("Üçüncü yield-dən əvvəl")
    yield 3
    print("Funksiya bitdi")

gen = sayac()           # Funksiya ÇALIŞMIR — sadəcə generator yaradılır
print(type(gen))        # <class 'generator'>

print(next(gen))        # "Birinci yield-dən əvvəl" → 1
print(next(gen))        # "İkinci yield-dən əvvəl"  → 2
print(next(gen))        # "Üçüncü yield-dən əvvəl" → 3
print(next(gen))        # "Funksiya bitdi" → StopIteration xətası
```

---

### 2.3 Generator Funksiyaları Yaratmaq

#### Nümunə 1: Sonsuz ardıcıllıq

```python
def sonsuz_sayac(başlanğıc=0):
    n = başlanğıc
    while True:           # Sonsuz dövr — amma yaddaş problemi yoxdur!
        yield n
        n += 1

gen = sonsuz_sayac(10)
print(next(gen))   # 10
print(next(gen))   # 11
print(next(gen))   # 12

# for dövrü ilə (break lazımdır, əks halda sonsuz çalışar)
for n in sonsuz_sayac():
    if n > 5:
        break
    print(n)
# 0 1 2 3 4 5
```

#### Nümunə 2: Böyük fayl oxuma

```python
def fayl_oxu(fayl_adı):
    with open(fayl_adı) as f:
        for sətir in f:
            yield sətir.strip()   # Hər dəfə bir sətir — yaddaşda tam fayl saxlanmır

for sətir in fayl_oxu("böyük_fayl.txt"):
    print(sətir)
```

#### Nümunə 3: Pipeline (Zəncir)

```python
def oxu(data):
    for element in data:
        yield element

def filtr(data, şərt):
    for element in data:
        if şərt(element):
            yield element

def çevir(data, f):
    for element in data:
        yield f(element)

# Zəncir: oxu → filtr → çevir (hamısı lazy!)
siyahı = range(1, 20)
nəticə = çevir(
    filtr(oxu(siyahı), lambda x: x % 2 == 0),
    lambda x: x ** 2
)

for x in nəticə:
    print(x)   # 4, 16, 36, 64, 100, 144, 196, 256, 324
```

---

### 2.4 `yield from` — Generator Delegasiyası

```python
def generator_a():
    yield 1
    yield 2

def generator_b():
    yield 3
    yield 4

def birləşdirilmiş():
    yield from generator_a()   # a-nın hər elementini yield et
    yield from generator_b()   # b-nin hər elementini yield et
    yield from [5, 6, 7]       # iterable-dan yield et

print(list(birləşdirilmiş()))   # [1, 2, 3, 4, 5, 6, 7]
```

---

### 2.5 Generator Metodları

```python
def gen_func():
    dəyər = yield 1
    print(f"Daxil olan dəyər: {dəyər}")
    yield 2

gen = gen_func()

# .send() — generatora dəyər göndər
print(next(gen))       # 1 — ilk next() ilə başla
print(gen.send(42))    # "Daxil olan dəyər: 42" → 2

# .throw() — generatora xəta göndər
# .close() — generatoru bağla
```

---

### 2.6 `next()` və `for` ilə İstifadə

```python
def üçlər():
    yield 3
    yield 6
    yield 9

gen = üçlər()

# next() ilə manual
print(next(gen))   # 3
print(next(gen))   # 6

# for dövrü ilə (StopIteration-ı avtomatik tutur)
gen2 = üçlər()
for x in gen2:
    print(x)   # 3 6 9

# Default dəyər ilə next()
gen3 = üçlər()
print(next(gen3, "Bitti"))   # 3
print(next(gen3, "Bitti"))   # 6
print(next(gen3, "Bitti"))   # 9
print(next(gen3, "Bitti"))   # "Bitti" — StopIteration əvəzinə
```

---

### 2.7 Generator-un Əsas Xüsusiyyətləri

```python
gen = (x for x in range(5))

# ⚠️ Generator bir dəfəlik istifadə olunur!
print(list(gen))    # [0, 1, 2, 3, 4]
print(list(gen))    # [] — tükənib, yenidən başlamır!

# Yenidən istifadə üçün generator funksiyasını yenidən çağır:
def yenilənə_bilən():
    yield from range(5)

print(list(yenilənə_bilən()))   # [0, 1, 2, 3, 4]
print(list(yenilənə_bilən()))   # [0, 1, 2, 3, 4] — hər dəfə təzə
```

---

### 2.8 List vs Generator — Nə Zaman Hansını?

| Vəziyyət | Seç |
|---|---|
| Elementlər dəfələrlə lazımdır | `list` |
| İndeksləmə, slicing lazımdır | `list` |
| `len()` lazımdır | `list` |
| Çox böyük və ya sonsuz ardıcıllıq | `generator` |
| Yalnız bir dəfə keçiləcək | `generator` |
| Yaddaş optimallaşdırması kritikdir | `generator` |
| Pipeline (bir-birinin ardınca işlem) | `generator` |

---

## 3. Decorators (Dekoratorlar)

### 3.1 Tərif — "Funksiya Sarğısı"

Decorator — **başqa bir funksiyaya əlavə davranış qatan**, **həmin funksiyanı dəyişdirmədən** onu genişləndirən bir funksiya növüdür. Öz işləmə mexanizmi anlamaq üçün əvvəlcə Python-da funksiyaların "birinci dərəcəli vətəndaş" (first-class citizen) olduğunu bilmək lazımdır.

---

### 3.2 Funksiyalar First-Class Citizen-dır

Python-da funksiyalar dəyər kimi işlənir — dəyişənlərə mənimsədilə, arqument kimi ötürülə, başqa funksiyadan qaytarıla bilər.

```python
# 1. Funksiya dəyişənə mənimsədilə bilər
def salam():
    return "Salam!"

f = salam           # Funksiya çağırılmır — sadəcə istinad kopyalanır
print(f())          # "Salam!" — f, salam-ın istinadıdır

# 2. Funksiya arqument kimi ötürülə bilər
def tətbiq_et(funksiya, dəyər):
    return funksiya(dəyər)

print(tətbiq_et(len, "Python"))   # 6
print(tətbiq_et(str.upper, "salam"))   # "SALAM"

# 3. Funksiya başqa funksiyadan qaytarıla bilər
def xarici():
    def daxili():
        return "Mən daxili funksiyayam"
    return daxili   # Funksiya qaytarılır, çağırılmır

f = xarici()
print(f())   # "Mən daxili funksiyayam"
```

---

### 3.3 Closure (Qapalı Ətraf)

Decorator-u anlamaq üçün closure anlayışı vacibdir.

**Closure** — daxili funksiyanın, xarici funksiyanın dəyişənlərini "yadda saxlaması"dır — xarici funksiya bitdikdən sonra belə.

```python
def əmsal_yaradan(əmsal):
    def vurucu(x):
        return x * əmsal   # 'əmsal' xarici funksiyadan götürülür
    return vurucu

ikiqat = əmsal_yaradan(2)   # əmsal=2 olan closure
üçqat  = əmsal_yaradan(3)   # əmsal=3 olan closure

print(ikiqat(5))    # 10
print(üçqat(5))     # 15
print(ikiqat(7))    # 14

# Closure-un yadda saxladığı dəyəri görmək:
print(ikiqat.__closure__[0].cell_contents)   # 2
```

---

### 3.4 Decorator — Əl ilə Yazılışı

```python
def dekorator(funksiya):
    def sarğı(*args, **kwargs):
        print("Funksiyadan ƏVVƏL")
        nəticə = funksiya(*args, **kwargs)   # orijinal funksiyanı çağır
        print("Funksiyadan SONRA")
        return nəticə
    return sarğı

def salamla(ad):
    print(f"Salam, {ad}!")

# Decorator-u əl ilə tətbiq etmək:
salamla = dekorator(salamla)

salamla("Leyla")
# Funksiyadan ƏVVƏL
# Salam, Leyla!
# Funksiyadan SONRA
```

---

### 3.5 `@` Sintaksisi — Şəkər Sintaksis (Syntactic Sugar)

`@dekorator` yazmaq — `funksiya = dekorator(funksiya)` yazmaqla **tamamilə eynidir**:

```python
def dekorator(funksiya):
    def sarğı(*args, **kwargs):
        print("Əvvəl")
        nəticə = funksiya(*args, **kwargs)
        print("Sonra")
        return nəticə
    return sarğı

@dekorator   # ← Bu sətir: salamla = dekorator(salamla) ilə eynidir
def salamla(ad):
    print(f"Salam, {ad}!")

salamla("Murad")
# Əvvəl
# Salam, Murad!
# Sonra
```

---

### 3.6 Praktiki Nümunələr

#### Zamanlama Dekoratoru

```python
import time

def zamanlayıcı(funksiya):
    def sarğı(*args, **kwargs):
        başlanğıc = time.time()
        nəticə = funksiya(*args, **kwargs)
        son = time.time()
        print(f"{funksiya.__name__} {son - başlanğıc:.4f} saniyəyə çalışdı")
        return nəticə
    return sarğı

@zamanlayıcı
def yavaş_funksiya():
    time.sleep(1)
    return "Bitdi"

yavaş_funksiya()
# yavaş_funksiya 1.0012 saniyəyə çalışdı
```

---

#### Logging (Qeyd etmə) Dekoratoru

```python
def loglayan(funksiya):
    def sarğı(*args, **kwargs):
        print(f"[LOG] {funksiya.__name__} çağırıldı. Args: {args}, Kwargs: {kwargs}")
        nəticə = funksiya(*args, **kwargs)
        print(f"[LOG] {funksiya.__name__} nəticə qaytardı: {nəticə}")
        return nəticə
    return sarğı

@loglayan
def cəm(a, b):
    return a + b

cəm(3, 5)
# [LOG] cəm çağırıldı. Args: (3, 5), Kwargs: {}
# [LOG] cəm nəticə qaytardı: 8
```

---

#### Giriş Yoxlama Dekoratoru

```python
def giriş_tələb_et(funksiya):
    def sarğı(istifadəçi, *args, **kwargs):
        if not istifadəçi.get("aktiv"):
            raise PermissionError("Giriş qadağandır!")
        return funksiya(istifadəçi, *args, **kwargs)
    return sarğı

@giriş_tələb_et
def profil_göstər(istifadəçi):
    print(f"Profil: {istifadəçi['ad']}")

aktiv_user   = {"ad": "Anar", "aktiv": True}
qeyri_aktiv  = {"ad": "Zəhra", "aktiv": False}

profil_göstər(aktiv_user)    # Profil: Anar
profil_göstər(qeyri_aktiv)   # PermissionError: Giriş qadağandır!
```

---

#### Cəhd Sayı Dekoratoru (Retry)

```python
import random

def yenidən_cəhd(cəhd_sayı=3):
    def dekorator(funksiya):
        def sarğı(*args, **kwargs):
            for i in range(cəhd_sayı):
                try:
                    return funksiya(*args, **kwargs)
                except Exception as e:
                    print(f"Cəhd {i+1}/{cəhd_sayı} uğursuz: {e}")
            raise Exception("Bütün cəhdlər uğursuz oldu!")
        return sarğı
    return dekorator

@yenidən_cəhd(cəhd_sayı=3)
def etibarsız_funksiya():
    if random.random() < 0.7:
        raise ConnectionError("Server cavab vermir")
    return "Uğurlu!"

print(etibarsız_funksiya())
```

---

### 3.7 `functools.wraps` — Metadata-nı Qorumaq

Decorator tətbiq edildikdə funksiyanın adı və docstring-i **itirilir** — bunu `functools.wraps` ilə həll etmək olar:

```python
def dekorator(funksiya):
    def sarğı(*args, **kwargs):   # Adı "sarğı"dır!
        return funksiya(*args, **kwargs)
    return sarğı

@dekorator
def mənim_funksiyam():
    """Bu mənim funksiyamdır."""
    pass

print(mənim_funksiyam.__name__)   # "sarğı" ← yanlış!
print(mənim_funksiyam.__doc__)    # None    ← itib!
```

```python
from functools import wraps

def dekorator(funksiya):
    @wraps(funksiya)              # ← Metadata qorunur
    def sarğı(*args, **kwargs):
        return funksiya(*args, **kwargs)
    return sarğı

@dekorator
def mənim_funksiyam():
    """Bu mənim funksiyamdır."""
    pass

print(mənim_funksiyam.__name__)   # "mənim_funksiyam" ✅
print(mənim_funksiyam.__doc__)    # "Bu mənim funksiyamdır." ✅
```

> 💡 **Praktiki qayda:** Real layihələrdə həmişə `@wraps` istifadə et.

---

### 3.8 Arqumentli Dekoratorlar

Dekoratorun özü də parametr qəbul edə bilər — bu zaman **üç qat iç-içə funksiya** lazımdır:

```python
from functools import wraps

def təkrarla(dəfə):           # ← Dekorator fabrikası (parametr qəbul edir)
    def dekorator(funksiya):  # ← Əsl dekorator
        @wraps(funksiya)
        def sarğı(*args, **kwargs):   # ← Sarğı funksiya
            for _ in range(dəfə):
                nəticə = funksiya(*args, **kwargs)
            return nəticə
        return sarğı
    return dekorator

@təkrarla(dəfə=3)
def salam():
    print("Salam!")

salam()
# Salam!
# Salam!
# Salam!
```

---

### 3.9 Çoxlu Dekoratorların Tətbiqi

Bir funksiyaya birdən çox dekorator tətbiq oluna bilər. **Sıra önəmlidir** — aşağıdan yuxarı tətbiq edilir, yuxarıdan aşağı çalışır.

```python
from functools import wraps

def dekorator_A(f):
    @wraps(f)
    def sarğı(*a, **kw):
        print("A — əvvəl")
        nəticə = f(*a, **kw)
        print("A — sonra")
        return nəticə
    return sarğı

def dekorator_B(f):
    @wraps(f)
    def sarğı(*a, **kw):
        print("B — əvvəl")
        nəticə = f(*a, **kw)
        print("B — sonra")
        return nəticə
    return sarğı

@dekorator_A      # ← ikinci tətbiq olunan
@dekorator_B      # ← birinci tətbiq olunan
def funksiya():
    print("Əsl funksiya")

funksiya()
# A — əvvəl      ← A xarici sarğı
# B — əvvəl      ← B daxili sarğı
# Əsl funksiya
# B — sonra
# A — sonra
```

**Tətbiq sırası:**
```
@A         →    funksiya = A(B(funksiya))
@B
def funksiya
```

---

### 3.10 Sinif ilə Decorator

Funksiya əvəzinə sinif istifadə edərək da decorator yaratmaq mümkündür — `__call__` metodunu tətbiq etməklə:

```python
from functools import wraps

class zamanlayıcı:
    def __init__(self, funksiya):
        self.funksiya = funksiya
        wraps(funksiya)(self)

    def __call__(self, *args, **kwargs):
        import time
        başlanğıc = time.time()
        nəticə = self.funksiya(*args, **kwargs)
        print(f"Vaxt: {time.time() - başlanğıc:.4f}s")
        return nəticə

@zamanlayıcı
def hesabla():
    return sum(range(1_000_000))

hesabla()   # Vaxt: 0.0412s
```

---

## Ümumi Müqayisə Cədvəli

| Xüsusiyyət | List Comprehension | Generator | Decorator |
|---|---|---|---|
| Məqsəd | Yeni list yaratmaq | Lazy ardıcıllıq | Funksiyaya davranış əlavə etmək |
| Yaddaş | Hamısı birdən | Bir-bir, tələbdə | Funksiyayla eyni |
| Sintaksis | `[x for x in ...]` | `(x for x in ...)` / `yield` | `@funksiya_adı` |
| Bir dəfəlik? | ❌ (təkrar istifadə olar) | ✅ (tükənir) | — |
| İstifadə sahəsi | Filtrasiya, çevirmə | Böyük data, pipeline | Logging, auth, cache, timing |

---

## Xülasə

```python
# List Comprehension — Bir sətirdə list yarat
kvadratlar = [x**2 for x in range(10) if x % 2 == 0]

# Generator — Tənbəl, yaddaş-effektiv ardıcıllıq
def sonsuz():
    n = 0
    while True:
        yield n
        n += 1

# Decorator — Funksiyaya toxunmadan davranış əlavə et
from functools import wraps

def loglayan(f):
    @wraps(f)
    def sarğı(*args, **kwargs):
        print(f"{f.__name__} çağırıldı")
        return f(*args, **kwargs)
    return sarğı

@loglayan
def hesabla(x, y):
    return x + y
```
