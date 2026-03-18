# Python-a Giriş, Kontrol Strukturları və Funksiyalar

---

## 1. Python-a Giriş

Python 1991-ci ildə Guido van Rossum tərəfindən yaradılmış, oxunaqlılığı və sadəliyi ilə seçilən yüksək səviyyəli proqramlaşdırma dilidir. Python **interpreted** dildir — yəni kod birbaşa maşın koduna çevrilmədən, **interpreter** vasitəsilə sətir-sətir icra olunur.

**Python-un istifadə sahələri:**

- Veb backend inkişafı (Django, FastAPI, Flask)
- Məlumat elmi və analitika (Pandas, NumPy)
- Maşın öyrənməsi və süni intellekt (TensorFlow, PyTorch, Scikit-learn)
- Avtomatlaşdırma və skript yazımı
- API inteqrasiyası və veb scraping
- Kibertəhlükəsizlik alətləri

---

## 2. Python Sintaksisi və İndentasiya

### 2.1 Sintaksis

Python kodu aydın və oxunaqlı olmaq üçün dizayn edilib. Digər dillərdən (C, Java) fərqli olaraq Python-da əksər hallarda `{}` mötərizə istifadə olunmur.

```python
# Bu bir şərh sətridir
print("Salam, Dünya!")  # Bu da sətir sonu şərhidir
```

### 2.2 İndentasiya (Girintilər)

Python-da indentasiya sintaktik məcburiyyətdir — yalnız vizual nizamlılıq üçün deyil. Kod bloklarını müəyyən etmək üçün istifadə olunur.

**Standart:** 4 boşluq (space). Tab da işləyir, lakin hər ikisini qarışdırmaq `IndentationError` verir.

```python
# DOĞRU
if True:
    print("Bu blok içərisindədir")
    print("Bu da blok içərisindədir")

print("Bu blok xaricindədir")

# YANLIŞ — IndentationError
if True:
print("Xəta!")
```

---

## 3. Dəyişənlər (Variables) və Məlumat Tipləri (Data Types)

### 3.1 Dəyişənlər

Dəyişən — məlumatı yadda saxlamaq üçün istifadə olunan ad-etiketdir. Python-da dəyişəni əvvəlcədən elan etməyə ehtiyac yoxdur — sadəcə dəyər mənimsədin.

```python
ad = "Əli"
yas = 25
boy = 1.75
aktiv = True
```

**Dəyişən adlandırma qaydaları:**

- Hərf və ya `_` ilə başlamalıdır (rəqəmlə başlaya bilməz)
- Yalnız hərf, rəqəm və `_` istifadə oluna bilər
- Böyük/kiçik hərfə həssasdır: `Ad` və `ad` fərqli dəyişənlərdir
- Python açar sözləri (keywords) istifadə edilə bilməz: `for`, `if`, `class` və s.

```python
# Etibarlı adlar
_deyishen = 1
deyishen2 = 2
birinci_ad = "Leyla"

# Etibarsız adlar
2deyishen = 1    # SyntaxError
for = 5          # SyntaxError (keyword)
```

**Çoxlu mənimsətmə:**

```python
x = y = z = 0          # üçü də 0 olur
a, b, c = 1, 2, 3      # a=1, b=2, c=3
ad, yas = "Kamran", 30
```

### 3.2 Əsas Məlumat Tipləri

Python-da hər şey bir **obyektdir** — dəyişənlər isə bu obyektlərə işarə edən etiketlərdir.

---

#### `int` — Tam ədəd

Onluq nöqtəsiz tam ədədlər.

```python
a = 10
b = -5
c = 0
böyük = 1_000_000   # oxunaqlılıq üçün _ istifadə edilə bilər

# Digər say sistemlərindən
ikilik  = 0b1010      # binary  → 10
səkkizlik = 0o12      # octal   → 10
onaltılıq = 0xA       # hex     → 10
```


| Xüsusiyyət     | Dəyər                                |
| -------------- | ------------------------------------ |
| Minimum dəyər  | Limitsiz (Python-da int limitsizdir) |
| Maksimum dəyər | Limitsiz                             |
| Tip yoxlaması  | `type(x) == int`                     |


```python
print(type(42))   # <class 'int'>
```

---

#### `float` — Onluq ədəd

IEEE 754 standartına əsaslanan 64-bit (double precision) onluq ədədlər.

```python
x = 3.14
y = -0.001
z = 2.5e3    # elmi notation → 2500.0
w = 1.5e-2   # → 0.015

print(type(3.14))  # <class 'float'>
```


| Xüsusiyyət      | Dəyər                                           |
| --------------- | ----------------------------------------------- |
| Dəqiqlik        | ~15-17 əhəmiyyətli rəqəm                        |
| Maksimum        | ~1.8 × 10³⁰⁸                                    |
| Xüsusi dəyərlər | `float('inf')`, `float('-inf')`, `float('nan')` |


```python
# Üzən nöqtə dəqiqliyi xəbərdarlığı
print(0.1 + 0.2)   # 0.30000000000000004 — bu normaldır!
```

---

#### `str` — Mətn (String)

Simvollar ardıcıllığı. Dəyişməzdir (immutable).

```python
s1 = "Salam"
s2 = 'Dünya'
s3 = """Bu
çox sətirli
mətndir"""
s4 = f"Adım {ad}, yaşım {yas}"   # f-string (format string)
```

**Əsas əməliyyatlar:**

```python
s = "Python"
print(len(s))       # 6 — uzunluq
print(s[0])         # 'P' — indeksləmə
print(s[-1])        # 'n' — sondan indeksləmə
print(s[1:4])       # 'yth' — dilimleme (slicing)
print(s.upper())    # 'PYTHON'
print(s.lower())    # 'python'
print(s.replace("Py", "My"))  # 'Mython'
print("on" in s)    # True — axtarış
```

---

#### `bool` — Məntiqi tip

Yalnız iki dəyər alır: `True` və `False`. `int`-dən törənir (`True == 1`, `False == 0`).

```python
aktiv = True
bağlıdır = False

print(type(True))   # <class 'bool'>
print(True + True)  # 2 (int kimi)
```

**Falsy (False kimi qiymətlənən) dəyərlər:**

```python
bool(0)      # False
bool(0.0)    # False
bool("")     # False
bool([])     # False
bool(None)   # False
# Bunlar xaricindəki hər şey True-dur
```

---

#### `NoneType` — Boş dəyər

`None` — dəyərin olmadığını bildirir. Java-dakı `null`-a bənzər.

```python
netice = None
print(type(None))     # <class 'NoneType'>
print(netice is None) # True — None yoxlaması üçün == deyil, is istifadə et
```

---

#### Tip Çevirmələri (Type Casting)

```python
int("42")       # 42
int(3.9)        # 3 (yuvarlaqlaşdırmır, kəsir)
float("3.14")   # 3.14
float(5)        # 5.0
str(100)        # "100"
bool(0)         # False
bool("salam")   # True

# Xəta baş verir:
int("salam")    # ValueError
```

---

### 3.3 `type()` və `isinstance()`

```python
x = 42
print(type(x))             # <class 'int'>
print(isinstance(x, int))  # True
print(isinstance(x, (int, float)))  # True — birdən çox tip yoxlaması
```

---

## 4. Kontrol Strukturları

### 4.1 Şərt Operatoru: `if`, `elif`, `else`

Şərt doğru (`True`) olduqda müəyyən kod bloku icra olunur.

```python
yas = 20

if yas < 18:
    print("Yetkinlik yaşına çatmayıb")
elif yas == 18:
    print("Tam 18 yaşındadır")
else:
    print("Yetkindir")
```

**Müqayisə operatorları:**


| Operator | Mənası           |
| -------- | ---------------- |
| `==`     | Bərabərdir       |
| `!=`     | Bərabər deyil    |
| `>`      | Böyükdür         |
| `<`      | Kiçikdir         |
| `>=`     | Böyük bərabərdir |
| `<=`     | Kiçik bərabərdir |
| `is`     | Eyni obyektdir   |
| `in`     | Daxilindədir     |


**Məntiqi operatorlar:**

```python
x = 5
if x > 0 and x < 10:
    print("0 ilə 10 arasındadır")

if x < 0 or x > 3:
    print("0-dan kiçik ya da 3-dən böyükdür")

if not (x == 5):
    print("5 deyil")
```

**Bir sətirlik if (Ternary Operator):**

```python
netice = "böyük" if x > 0 else "kiçik"
```

---

### 4.2 `for` Dövrü

`for` dövrü bir ardıcıllıq (sequence) üzərindən keçmək üçün istifadə olunur. Neçə dəfə dövrün icra olunacağı əvvəlcədən məlumdur.

```python
# String üzərindən
for hərf in "Python":
    print(hərf)

# List üzərindən
rənglər = ["qırmızı", "yaşıl", "mavi"]
for rəng in rənglər:
    print(rəng)

# range() ilə
for i in range(5):        # 0, 1, 2, 3, 4
    print(i)

for i in range(1, 6):     # 1, 2, 3, 4, 5
    print(i)

for i in range(0, 10, 2): # 0, 2, 4, 6, 8 (addım = 2)
    print(i)

for i in range(5, 0, -1): # 5, 4, 3, 2, 1 (geri sayım)
    print(i)
```

`**enumerate()` — indeks ilə birlikdə:**

```python
meyvələr = ["alma", "armud", "gilas"]
for i, meyvə in enumerate(meyvələr):
    print(f"{i}: {meyvə}")
# 0: alma
# 1: armud
# 2: gilas
```

---

### 4.3 `while` Dövrü

`while` dövrü şərt doğru olduğu müddətcə çalışmağa davam edir. Dövrün neçə dəfə çalışacağı əvvəlcədən bilinmir.

```python
sayac = 0
while sayac < 5:
    print(sayac)
    sayac += 1

# İstifadəçi daxiletməsi ilə klassik nümunə
cavab = ""
while cavab != "çıx":
    cavab = input("Komanda daxil et: ")
    print(f"Daxil etdin: {cavab}")
```

> ⚠️ **Diqqət:** `while` dövrünü yazarkən şərtin nə vaxtsa `False` olacağına əmin ol, əks halda **sonsuz dövr** (infinite loop) yaranar.

---

### 4.4 `for` vs `while` — Nə zaman hangisini istifadə etməli?


| Vəziyyət                                          | İstifadə et   |
| ------------------------------------------------- | ------------- |
| Ardıcıllıq üzərindən keçmək (list, string, range) | `for`         |
| Dövrün sayı əvvəlcədən məlumdur                   | `for`         |
| Şərtə əsasən dövr etmək lazımdır                  | `while`       |
| Dövrün sayı əvvəlcədən bilinmir                   | `while`       |
| Sonsuz dövr (server loop)                         | `while True:` |


---

### 4.5 `break` — Dövrü Dayandırmaq

`break` — dövrü dərhal dayandırır və dövrün xaricinə çıxır.

```python
for i in range(10):
    if i == 5:
        break        # i 5-ə çatanda dövr dayanır
    print(i)
# Çıxış: 0 1 2 3 4

# while ilə
while True:
    girdi = input("Çıxmaq üçün 'q' yaz: ")
    if girdi == "q":
        break
    print(f"Daxil etdin: {girdi}")
```

---

### 4.6 `continue` — Dövrün Cari İterasiyasını Atlamaq

`continue` — cari iterasiyanın qalan hissəsini atlayır və növbəti iterasiyaya keçir.

```python
for i in range(10):
    if i % 2 == 0:
        continue     # cüt ədədləri atla
    print(i)
# Çıxış: 1 3 5 7 9
```

---

### 4.7 `pass` — Boş Blok Tutucusu

`pass` — heç bir iş görmür, lakin sintaktik olaraq boş blok buraxmamaq üçün istifadə olunur.

```python
for i in range(5):
    pass   # hələlik boş, sonra dolduracağam

if şərt:
    pass   # TODO: sonra əlavə et
else:
    print("Şərt yanlışdır")
```

---

### 4.8 `else` bloku dövrlərdə

Python-da `for` və `while` dövrləri `else` blokuna sahib ola bilər. Bu blok dövr **normal** tamamlandıqda (yəni `break` ilə dayandırılmadıqda) icra olunur.

```python
for i in range(5):
    if i == 10:
        break
else:
    print("Dövr break olmadan tamamlandı")
# Çıxış: Dövr break olmadan tamamlandı

for i in range(5):
    if i == 3:
        break
else:
    print("Bu çap olunmayacaq")
# Çıxış: (heç nə)
```

---

## 5. Funksiyalar (Functions)

Funksiya — müəyyən bir işi yerinə yetirən, təkrar istifadə edilə bilən kod blokudur.

### 5.1 Funksiya Tərifi

```python
def salam_ver():
    print("Salam!")

salam_ver()   # Çağırmaq üçün
```

`**def**` açar sözü (keyword) ilə başlayır, ardından funksiya adı, mötərizə, iki nöqtə gəlir.

---

### 5.2 Parameterlər (Parameters) vs Arqumentlər (Arguments)

Bu iki termin tez-tez qarışdırılır — aralarındakı fərq aydındır:


| Termin       | Nədir?                                          | Nə zaman?             |
| ------------ | ----------------------------------------------- | --------------------- |
| **Parametr** | Funksiyanın **tərif**indəki dəyişən adı         | Funksiya yazılarkən   |
| **Arqument** | Funksiyanı **çağırarkən** ötürülən həqiqi dəyər | Funksiya çağırılarkən |


```python
def cəm_hesabla(x, y):   # x və y — PARAMETRLƏR
    return x + y

cəm_hesabla(3, 5)        # 3 və 5 — ARQUMENTlər
```

---

### 5.3 Arqument Növləri

#### Mövqe Arqumentləri (Positional Arguments)

Sıraya görə ötürülür. Sıra vacibdir.

```python
def tanış_ol(ad, yas):
    print(f"Adım {ad}, yaşım {yas}")

tanış_ol("Aytən", 22)   # Doğru
tanış_ol(22, "Aytən")   # Yanlış məntiqi nəticə
```

---

#### Açar Söz Arqumentləri (Keyword Arguments)

Ad ilə ötürülür. Sıra fərq etmir.

```python
tanış_ol(yas=22, ad="Aytən")  # Sıra dəyişib, lakin düzgün işləyir
```

---

#### Standart/Default Parametrlər

Parametrə əvvəlcədən dəyər təyin edilir. Arqument ötürülmədikdə bu dəyər istifadə olunur.

```python
def salam_ver(ad, dil="Azərbaycan"):
    if dil == "Azərbaycan":
        print(f"Salam, {ad}!")
    elif dil == "İngilis":
        print(f"Hello, {ad}!")

salam_ver("Kamran")              # Salam, Kamran!
salam_ver("John", "İngilis")    # Hello, John!
```

> ⚠️ Default parametrlər həmişə sonunda olmalıdır:
>
> ```python
> def f(a, b=5, c):  # SyntaxError!
> def f(a, b, c=5):  # Doğru
> ```

---

#### `*args` — Dəyişən Sayda Mövqe Arqumentləri

Neçə arqumentin ötürüləcəyi məlum olmadıqda istifadə olunur. Daxilən **tuple** kimi saxlanılır.

```python
def cəm(*ədədlər):
    print(type(ədədlər))   # <class 'tuple'>
    return sum(ədədlər)

print(cəm(1, 2, 3))        # 6
print(cəm(1, 2, 3, 4, 5))  # 15
print(cəm())               # 0
```

---

#### `**kwargs` — Dəyişən Sayda Açar Söz Arqumentləri

Ad-dəyər cütlüyü kimi ötürülür. Daxilən **dict** kimi saxlanılır.

```python
def məlumat_göstər(**detallar):
    print(type(detallar))   # <class 'dict'>
    for açar, dəyər in detallar.items():
        print(f"{açar}: {dəyər}")

məlumat_göstər(ad="Lalə", yas=25, şəhər="Bakı")
```

---

#### Parametrlərin Sırası

Funksiyada bütün parametr növlərini birlikdə istifadə edərkən sıra belədir:

```
def f(mövqe, /, standart=dəyər, *args, açar_söz_only, **kwargs)
```

Praktiki nümunə:

```python
def tam_nümunə(a, b, c=10, *args, **kwargs):
    print(a, b, c, args, kwargs)

tam_nümunə(1, 2, 3, 4, 5, x=6, y=7)
# a=1, b=2, c=3, args=(4,5), kwargs={'x':6,'y':7}
```

---

### 5.4 `return` — Nəticəni Qaytarmaq

`return` — funksiyadan çıxır və dəyər qaytarır. `return` yoxdursa funksiya `None` qaytarır.

```python
def kv(x):
    return x ** 2

netice = kv(5)
print(netice)   # 25
```

**Çoxlu dəyər qaytarmaq (tuple kimi):**

```python
def min_max(siyahı):
    return min(siyahı), max(siyahı)

kiçik, böyük = min_max([3, 1, 7, 2, 9])
print(kiçik, böyük)   # 1 9
```

`**return` olmayan funksiya:**

```python
def çap_et(mətn):
    print(mətn)
    # Return yoxdur

netice = çap_et("Salam")
print(netice)   # None
```

`**return` ilə erkən çıxış:**

```python
def mütləq_dəyər(x):
    if x >= 0:
        return x
    return -x   # Mənfi olduqda burada dayanır
```

---

### 5.5 Dəyişənin Görünüş Sahəsi (Scope)

Python-da dəyişənin harda görünə biləcəyini **LEGB** qaydası müəyyən edir:


| Hərif             | Sahə                                 |
| ----------------- | ------------------------------------ |
| **L** — Local     | Funksiya daxili                      |
| **E** — Enclosing | İç-içə funksiyalarda xarici funksiya |
| **G** — Global    | Modul səviyyəsi                      |
| **B** — Built-in  | Python-un daxili adlar fəzası        |


```python
x = "qlobal"

def test():
    x = "lokal"    # Bu yeni, lokal x-dir
    print(x)       # lokal

test()
print(x)           # qlobal
```

`**global` açar sözü:**

```python
sayac = 0

def artır():
    global sayac
    sayac += 1

artır()
artır()
print(sayac)   # 2
```

---

### 5.6 Lambda Funksiyaları (Anonim Funksiyalar)

Kiçik, bir sətirlik funksiyalar üçün `lambda` istifadə olunur.

```python
# Adi funksiya
def ikiqat(x):
    return x * 2

# Ekvivalent lambda
ikiqat = lambda x: x * 2

print(ikiqat(5))   # 10

# Çox parametrli lambda
cəm = lambda x, y: x + y
print(cəm(3, 4))   # 7

# Siyahı sıralamaqda lambda
tələbələr = [("Anar", 85), ("Zəhra", 92), ("Murad", 78)]
sıralanmış = sorted(tələbələr, key=lambda t: t[1], reverse=True)
print(sıralanmış)
# [('Zəhra', 92), ('Anar', 85), ('Murad', 78)]
```

---

## Xülasə Cədvəli


| Mövzu          | Əsas yadda saxlanılacaq məqam       |
| -------------- | ----------------------------------- |
| Sintaksis      | `{}` yoxdur, indentasiya məcburidir |
| `int`          | Limitsiz tam ədəd                   |
| `float`        | 64-bit, ~15 rəqəm dəqiqliyi         |
| `str`          | Dəyişməz, indekslənə bilər          |
| `bool`         | `True`/`False`, `int`-dən törənir   |
| `None`         | Dəyər yoxluğu, `is None` ilə yoxla  |
| `if/elif/else` | Şərtin doğruluğuna görə icra        |
| `for`          | Ardıcıllıq üzərindən keçmək         |
| `while`        | Şərt doğru olduqca dövr             |
| `break`        | Dövrü tamamilə dayandır             |
| `continue`     | Cari iterasiyanı atla               |
| `pass`         | Boş blok tutucusu                   |
| Parametr       | Funksiyanın tərif sütunundakı ad    |
| Arqument       | Çağırma zamanı ötürülən dəyər       |
| `*args`        | Dəyişən sayda mövqe arg → tuple     |
| `**kwargs`     | Dəyişən sayda açar söz arg → dict   |
| `return`       | Dəyər qaytar + funksiyadan çıx      |


