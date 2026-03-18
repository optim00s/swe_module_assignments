# Lists, Tuples, Dictionaries, Sets

---

## Mutable vs Immutable — Əsas Konsept

Daha əvvəl data strukturları haqqında danışmazdan əvvəl Python-da ən fundamental fərqi anlamaq lazımdır: **dəyişə bilən** (mutable) və **dəyişə bilməyən** (immutable) obyektlər.

### Immutable (Dəyişməz) Obyektlər

Yaradıldıqdan sonra dəyəri **dəyişdirilə bilməyən** obyektlər. Dəyişdirmək istədikdə Python yaddaqda **yeni obyekt** yaradır, köhnəsi dəyişmir.

```python
s = "Salam"
print(id(s))      # məsələn: 140234567890

s = s + " Dünya"  # Bu s-i dəyişdirmir, YENİ string yaradır
print(id(s))      # FƏRQLI id — başqa obyektdir

# Birbaşa dəyişdirmə cəhdi:
s[0] = "s"        # TypeError: 'str' object does not support item assignment
```

**Immutable tiplər:** `int`, `float`, `str`, `bool`, `tuple`, `frozenset`

---

### Mutable (Dəyişən) Obyektlər

Yaradıldıqdan sonra **mövcud obyekt üzərində** dəyişiklik edilə bilən tiplər. Yeni obyekt yaradılmır.

```python
siyahı = [1, 2, 3]
print(id(siyahı))     # məsələn: 140234567999

siyahı.append(4)      # EYNI obyekt dəyişdirilir
print(id(siyahı))     # EYNI id — yeni obyekt yoxdur
print(siyahı)         # [1, 2, 3, 4]
```

**Mutable tiplər:** `list`, `dict`, `set`, (sonrakı mövzularda: sinif instansları)

---

### Niyə Bu Fərq Vacibdir?

```python
# ❌ Mutable-ın gözlənilməz davranışı — alias problemi
a = [1, 2, 3]
b = a            # b, a-nın KOPYASI deyil, EYNI obyektə işarə edir

b.append(4)
print(a)         # [1, 2, 3, 4] — a da dəyişdi!
print(b)         # [1, 2, 3, 4]

# ✅ Düzgün kopya
b = a.copy()     # Səthi kopya (shallow copy)
import copy
b = copy.deepcopy(a)  # Dərin kopya (nested strukturlar üçün)
```

```python
# Immutable-ın təhlükəsiz paylaşımı
x = "salam"
y = x
y = y + "!"      # x dəyişmir, y yeni string olur
print(x)         # "salam" — toxunulmaz
```

```python
# ❌ Mutable-ı default parametr kimi istifadə etmə
def siyahıya_əlavə_et(element, siyahı=[]):   # YANLIŞDIR!
    siyahı.append(element)
    return siyahı

print(siyahıya_əlavə_et(1))   # [1]
print(siyahıya_əlavə_et(2))   # [1, 2] — gözlənilən: [2]!

# ✅ Düzgün yol
def siyahıya_əlavə_et(element, siyahı=None):
    if siyahı is None:
        siyahı = []
    siyahı.append(element)
    return siyahı
```

---

### Mutable vs Immutable Müqayisə Cədvəli

| Xüsusiyyət | Mutable | Immutable |
|---|---|---|
| Yaradıldıqdan sonra dəyişdirilə bilər | ✅ Bəli | ❌ Xeyr |
| Dəyişiklikdə yeni obyekt yaranır | ❌ Xeyr | ✅ Bəli |
| Dictionary açarı ola bilər | ❌ Xeyr | ✅ Bəli |
| Set elementi ola bilər | ❌ Xeyr | ✅ Bəli |
| Thread-safe (paylaşımda təhlükəsiz) | ❌ Xeyr | ✅ Bəli |
| Nümunələr | `list`, `dict`, `set` | `str`, `int`, `tuple` |

> 💡 **Qayda:** Bir dəyər dəyişməməlidirsə → immutable tip seç. Dəyişəcəksə → mutable.

---

## 1. List (Siyahı)

### 1.1 Tərif

List — **sıralı** (ordered), **mutable** (dəyişən), **dublikat icazə verən**, müxtəlif tipli elementləri saxlaya bilən ardıcıllıqdır (sequence).

```python
boş_list     = []
ədədlər      = [1, 2, 3, 4, 5]
mətns        = ["alma", "armud", "gilas"]
qarışıq      = [1, "salam", 3.14, True, None]
iç_içə       = [[1, 2], [3, 4], [5, 6]]   # nested list

print(type([]))   # <class 'list'>
```

---

### 1.2 İndeksləmə (Indexing)

List-də hər elementin bir indeksi var. Python-da indekslər `0`-dan başlayır.

```python
meyvələr = ["alma", "armud", "gilas", "ərik", "limon"]
#             0        1        2        3       4
#            -5       -4       -3       -2      -1

print(meyvələr[0])    # "alma"    — birinci element
print(meyvələr[2])    # "gilas"   — üçüncü element
print(meyvələr[-1])   # "limon"   — sonuncu element
print(meyvələr[-2])   # "ərik"    — sondan ikinci

# Mövcud olmayan indeks:
print(meyvələr[10])   # IndexError: list index out of range
```

---

### 1.3 Dilimlənmə (Slicing)

Slicing — list-in bir hissəsini götürməyə imkan verir. **Orijinal list dəyişmir.**

```python
# Sintaksis: siyahı[başlanğıc : son : addım]
# son indeks DAXİL DEYİL

ədədlər = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(ədədlər[2:6])     # [2, 3, 4, 5]      — 2-dən 5-ə qədər
print(ədədlər[:4])      # [0, 1, 2, 3]      — əvvəldən 3-ə qədər
print(ədədlər[6:])      # [6, 7, 8, 9]      — 6-dan sonuna qədər
print(ədədlər[:])       # [0,1,2,...,9]      — tam surət (shallow copy)
print(ədədlər[::2])     # [0, 2, 4, 6, 8]   — hər 2-ci element
print(ədədlər[1::2])    # [1, 3, 5, 7, 9]   — 1-dən hər 2-ci
print(ədədlər[::-1])    # [9,8,7,...,0]      — tərsinə

# Mənfi addım ilə:
print(ədədlər[8:2:-1])  # [8, 7, 6, 5, 4, 3]
```

---

### 1.4 Dəyişdirmə

```python
rənglər = ["qırmızı", "yaşıl", "mavi"]

rənglər[1] = "sarı"       # tək element
print(rənglər)             # ["qırmızı", "sarı", "mavi"]

rənglər[0:2] = ["ağ", "qara"]   # dilim dəyişdirmə
print(rənglər)             # ["ağ", "qara", "mavi"]
```

---

### 1.5 Metodlar

#### Əlavə etmək

```python
s = [1, 2, 3]

s.append(4)           # Sona bir element əlavə et → [1,2,3,4]
s.insert(1, 99)       # 1-ci indeksə 99 əlavə et → [1,99,2,3,4]
s.extend([5, 6, 7])   # Başqa list-i sona birləşdir → [1,99,2,3,4,5,6,7]
s += [8, 9]           # extend ilə ekvivalent
```

#### Silmək

```python
s = [10, 20, 30, 20, 40]

s.remove(20)      # İlk tapılan 20-ni sil → [10,30,20,40]
s.pop()           # Sonuncu elementi sil VƏ qaytar → 40, siyahı: [10,30,20]
s.pop(0)          # 0-cı indeksi sil VƏ qaytar → 10, siyahı: [30,20]
del s[0]          # 0-cı indeksi sil (dəyər qaytarmır)
del s[1:3]        # dilimi sil
s.clear()         # Bütün elementləri sil → []
```

#### Axtarış və Məlumat

```python
s = [3, 1, 4, 1, 5, 9, 2, 6, 5]

print(s.index(5))     # 4 — ilk 5-in indeksi
print(s.count(1))     # 2 — 1-in neçə dəfə olduğu
print(len(s))         # 9 — uzunluq
print(5 in s)         # True — üzvlük yoxlaması
print(min(s))         # 1
print(max(s))         # 9
print(sum(s))         # 36
```

#### Sıralama

```python
s = [3, 1, 4, 1, 5, 9]

s.sort()                    # Yerində sırala (orijinal dəyişir)
s.sort(reverse=True)        # Azalan sıra

yeni = sorted(s)            # Yeni sıralanmış list qaytar (orijinal dəyişmir)
yeni = sorted(s, reverse=True)

# Açar funksiya ilə:
sözlər = ["alma", "kiwi", "armud", "gilas"]
sözlər.sort(key=len)        # Uzunluğa görə sırala
print(sözlər)               # ['kiwi', 'alma', 'armud', 'gilas']
```

#### Digər metodlar

```python
s = [1, 2, 3]
s.reverse()       # Yerində tərsinə çevir → [3, 2, 1]
kopyası = s.copy()          # Səthi kopya

# Birləşdirmə
a = [1, 2]
b = [3, 4]
c = a + b         # [1, 2, 3, 4] — yeni list
a *= 3            # [1, 2, 1, 2, 1, 2]
```

---

### 1.6 Faydalı Əməliyyatlar

```python
# Çevirmə
s = list("Python")       # ['P','y','t','h','o','n']
s = list(range(5))       # [0, 1, 2, 3, 4]

# Zip ilə birlikdə istifadə
adlar = ["Anar", "Leyla"]
yaşlar = [22, 28]
cütlər = list(zip(adlar, yaşlar))
print(cütlər)   # [('Anar', 22), ('Leyla', 28)]
```

---

## 2. Tuple (Dəyişməz Ardıcıllıq)

### 2.1 Tərif

Tuple — **sıralı**, **immutable** (dəyişməz), **dublikat icazə verən** ardıcıllıqdır. List-ə çox bənzəyir, əsas fərq yaradıldıqdan sonra dəyişdirilə **bilməməsidir**.

```python
boş_tuple   = ()
bir_element = (42,)          # ⚠️ Vergül MÜTLƏQDIR — (42) int kimi qiymətlənir!
ədədlər     = (1, 2, 3, 4)
qarışıq     = ("salam", 3.14, True)
mötərizəsiz = 1, 2, 3        # Bu da tuple-dır! (tuple packing)

print(type(()))   # <class 'tuple'>
print(type((42)))   # <class 'int'>   ← Diqqət!
print(type((42,)))  # <class 'tuple'> ← Düzgün
```

---

### 2.2 İndeksləmə (List ilə eynidır)

```python
t = ("alma", "armud", "gilas")

print(t[0])     # "alma"
print(t[-1])    # "gilas"
print(t[1:])    # ("armud", "gilas")
```

---

### 2.3 Immutability (Dəyişməzlik)

```python
t = (1, 2, 3)

t[0] = 99       # TypeError: 'tuple' object does not support item assignment
t.append(4)     # AttributeError: 'tuple' object has no attribute 'append'

# Lakin daxilindəki mutable element dəyişə bilər:
t2 = ([1, 2], [3, 4])
t2[0].append(99)        # Xəta vermır! İçindəki LIST dəyişdirilir
print(t2)               # ([1, 2, 99], [3, 4])
# t2 özü (hansı list-lərə işarə etdiyı) dəyişmir
```

---

### 2.4 Tuple Unpacking

```python
t = ("Əli", 25, "Bakı")
ad, yas, şəhər = t           # Tam unpacking

# Qismən unpacking
birinci, *qalan = (1, 2, 3, 4, 5)
print(birinci)   # 1
print(qalan)     # [2, 3, 4, 5]

*əvvəl, sonuncu = (1, 2, 3, 4, 5)
print(əvvəl)     # [1, 2, 3, 4]
print(sonuncu)   # 5

# Swap (dəyişmə) — klassik Python idiom
a, b = 10, 20
a, b = b, a
print(a, b)   # 20 10
```

---

### 2.5 Mövcud Metodlar

Tuple dəyişməz olduğu üçün **yalnız 2 metodu** var:

```python
t = (1, 2, 3, 2, 1, 2)

print(t.count(2))   # 3 — 2-nin neçə dəfə olduğu
print(t.index(3))   # 2 — 3-ün ilk indeksi
print(len(t))       # 6 — len() built-in funksiya, metod deyil
```

---

### 2.6 Tuple vs List — Nə Zaman Hansını Seç?

| Vəziyyət | Seç |
|---|---|
| Məlumat dəyişməməlidir (koordinatlar, RGB) | `tuple` |
| Funksiyadan çox dəyər qaytarmaq | `tuple` |
| Dictionary açarı lazımdır | `tuple` |
| Sabit konfiqurasiya (DB bağlantı parametrləri) | `tuple` |
| Siyahıya element əlavə/silmə lazımdır | `list` |
| Məlumat dinamik, dəyişkəndir | `list` |

**Performans:** Tuple-lar list-dən daha sürətli və az yaddaş tutur.
```python
import sys
print(sys.getsizeof([1,2,3]))    # 88 bytes
print(sys.getsizeof((1,2,3)))    # 64 bytes
```

---

## 3. Dictionary (Lüğət)

### 3.1 Tərif

Dictionary — **açar-dəyər** (key-value) cütlüklərindən ibarət, **sırasız** (Python 3.7+-da **daxiletmə sırasını qoruyur**), **mutable** məlumat strukturudur. Açarlar **unikal** olmalıdır.

```python
boş        = {}
tələbə     = {"ad": "Aytən", "yas": 22, "bal": 95.5}
qarışıq    = {1: "bir", (2, 3): "tuple açar", "siyahı": [1,2,3]}

print(type({}))   # <class 'dict'>
```

**Açar üçün tələblər:**
- **Immutable** olmalıdır: `str`, `int`, `float`, `tuple`, `bool` ✅
- `list`, `dict`, `set` açar ola **bilməz** ❌

```python
d = {[1,2]: "dəyər"}   # TypeError: unhashable type: 'list'
d = {(1,2): "dəyər"}   # ✅ Tuple açar ola bilər
```

---

### 3.2 Yaratma Üsulları

```python
# Literal sintaksis
d1 = {"ad": "Murad", "yas": 30}

# dict() konstruktoru
d2 = dict(ad="Murad", yas=30)

# Açar-dəyər cütlüklərindən
d3 = dict([("ad", "Murad"), ("yas", 30)])

# fromkeys — eyni dəyərlə açarlar yarat
d4 = dict.fromkeys(["a", "b", "c"], 0)
print(d4)   # {'a': 0, 'b': 0, 'c': 0}
```

---

### 3.3 Elementlərə Müraciət

```python
d = {"ad": "Kamran", "yas": 28, "şəhər": "Bakı"}

# Birbaşa müraciət (mövcud olmayan açar → KeyError)
print(d["ad"])       # "Kamran"
print(d["yoxdur"])   # KeyError!

# .get() — təhlükəsiz müraciət (mövcud olmayan açar → None)
print(d.get("yas"))           # 28
print(d.get("ölkə"))          # None
print(d.get("ölkə", "N/A"))   # "N/A" — default dəyər
```

---

### 3.4 Dəyişdirmə və Əlavə Etmə

```python
d = {"ad": "Leyla"}

d["yas"] = 25           # Yeni açar-dəyər əlavə et
d["ad"] = "Lalə"        # Mövcud dəyəri dəyişdir

# .update() — çoxlu dəyişiklik
d.update({"yas": 26, "şəhər": "Gəncə"})
d.update(aktiv=True)    # Keyword argument ilə
```

---

### 3.5 Silmə

```python
d = {"a": 1, "b": 2, "c": 3, "d": 4}

d.pop("b")            # "b" açarını sil, dəyəri qaytar: 2
d.pop("yox", "N/A")   # Mövcud olmayan açar, KeyError vermır
del d["c"]            # "c" açarını sil (dəyər qaytarmır)
son = d.popitem()     # Son daxil edilmiş açar-dəyəri sil VƏ qaytar (tuple)
d.clear()             # Hamısını sil
```

---

### 3.6 Əsas Metodlar

```python
d = {"ad": "Anar", "yas": 22, "şəhər": "Sumqayıt"}

# Görünüş metodları (view objects — canlı yenilənir)
print(d.keys())    # dict_keys(['ad', 'yas', 'şəhər'])
print(d.values())  # dict_values(['Anar', 22, 'Sumqayıt'])
print(d.items())   # dict_items([('ad','Anar'), ('yas',22), ('şəhər','Sumqayıt')])

# Iterasiya
for açar in d:
    print(açar, d[açar])

for açar, dəyər in d.items():
    print(f"{açar}: {dəyər}")

# Açar yoxlaması
print("ad" in d)       # True
print("Anar" in d)     # False — dəyərlərdə axtarmır, açarlarda axtarır
print("Anar" in d.values())  # True

# Kopya
d2 = d.copy()          # Səthi kopya

# .setdefault() — açar yoxdursa əlavə et, varsa dəyişdirmə
d.setdefault("ölkə", "Azərbaycan")
```

---

### 3.7 Dictionary Birləşdirmə (Python 3.9+)

```python
d1 = {"a": 1, "b": 2}
d2 = {"c": 3, "d": 4}

# Merge
d3 = d1 | d2    # {'a':1, 'b':2, 'c':3, 'd':4}
d1 |= d2        # d1-i d2 ilə yenilə (in-place)
```

---

## 4. Set (Çoxluq)

### 4.1 Tərif

Set — **sırasız** (unordered), **mutable**, **unikal elementlər** toplusudur. Riyaziyyatdakı çoxluq (məcmu) anlayışına uyğundur. Dublikat elementlər saxlanılmır.

```python
boş_set  = set()            # ⚠️ {} boş dict yaradır, boş set DEYIL!
ədədlər  = {1, 2, 3, 4, 5}
mətns    = {"alma", "armud", "gilas"}

# Dublikatlar avtomatik silinir:
s = {1, 2, 2, 3, 3, 3}
print(s)   # {1, 2, 3}

print(type({1, 2}))   # <class 'set'>
print(type({}))       # <class 'dict'>  ← Diqqət!
```

**Set elementləri üçün tələb:** Immutable olmalıdır (list element ola bilməz, tuple ola bilər).

---

### 4.2 Əsas Metodlar

#### Əlavə etmək

```python
s = {1, 2, 3}

s.add(4)            # Bir element əlavə et → {1,2,3,4}
s.add(2)            # Dublikat — dəyişiklik olmur → {1,2,3,4}
s.update([5,6,7])   # Çox element əlavə et → {1,2,3,4,5,6,7}
s.update({8}, [9])  # Çox ardıcıllıq əlavə et
```

#### Silmək

```python
s = {1, 2, 3, 4, 5}

s.remove(3)      # 3-ü sil; mövcud deyilsə → KeyError
s.discard(3)     # 3-ü sil; mövcud deyilsə → Xəta VERMIR ✅
s.pop()          # Təsadüfi bir element sil (set sırasız olduğu üçün)
s.clear()        # Hamısını sil
```

#### Yoxlama

```python
s = {1, 2, 3}

print(3 in s)        # True  — O(1) sürəti (list-dən çox sürətli!)
print(9 not in s)    # True
print(len(s))        # 3
```

---

### 4.3 Çoxluq Əməliyyatları (Set Operations)

Bunlar set-in ən güclü xüsusiyyətləridiır — riyaziyyatdakı çoxluq nəzəriyyəsinə tam uyğundur.

```python
A = {1, 2, 3, 4, 5}
B = {4, 5, 6, 7, 8}
```

#### Birlik (Union) — A ∪ B

Hər iki çoxluqdakı bütün elementlər.

```python
print(A | B)              # {1,2,3,4,5,6,7,8}
print(A.union(B))         # Eynidır
```

#### Kəsişmə (Intersection) — A ∩ B

Hər iki çoxluqda **birlikdə** olan elementlər.

```python
print(A & B)                      # {4, 5}
print(A.intersection(B))          # Eynidır
A.intersection_update(B)          # A-nı yerində dəyişdir
```

#### Fərq (Difference) — A − B

A-da olan, lakin B-də **olmayan** elementlər.

```python
print(A - B)                  # {1, 2, 3}
print(A.difference(B))        # Eynidır
print(B - A)                  # {6, 7, 8}  ← Sıra vacibdir!
```

#### Simmetrik Fərq (Symmetric Difference) — A △ B

Hər iki çoxluqdan **yalnız birində** olan elementlər (kəsişmə xaric).

```python
print(A ^ B)                          # {1, 2, 3, 6, 7, 8}
print(A.symmetric_difference(B))      # Eynidır
```

---

### 4.4 Alt Çoxluq Yoxlamaları

```python
A = {1, 2, 3}
B = {1, 2, 3, 4, 5}

# Alt çoxluq (subset): A-nın hər elementi B-dədir
print(A <= B)             # True
print(A.issubset(B))      # True
print(A < B)              # True — proper subset (A ≠ B)

# Üst çoxluq (superset): B-nin hər elementi A-dadır?
print(B >= A)             # True
print(B.issuperset(A))    # True
print(B > A)              # True — proper superset

# Ayrılıq (disjoint): Heç bir ortaq element yoxdur
C = {10, 11}
print(A.isdisjoint(C))    # True
```

---

### 4.5 `frozenset` — Dəyişməz Set

Tuple-ın list üçün nə olduğu — frozenset-in set üçün odur. Immutable set.

```python
fs = frozenset({1, 2, 3})
fs.add(4)        # AttributeError!

# Dictionary açarı ola bilər:
d = {frozenset({1,2}): "bir-iki"}
```

---

### 4.6 Set-in Praktiki İstifadəsi

```python
# 1. Dublikatları silmək (ən sürətli üsul)
siyahı = [1, 2, 2, 3, 3, 3, 4]
unikal = list(set(siyahı))
print(unikal)   # [1, 2, 3, 4]  ← ⚠️ Sıra dəyişə bilər!

# 2. Üzvlük yoxlaması — Set list-dən qat-qat sürətlidir
böyük_siyahı = list(range(1_000_000))
böyük_set    = set(range(1_000_000))

# list: O(n)  — milyon elementdə axtarır
999999 in böyük_siyahı  # Yavaş

# set: O(1) — hash ilə anında tapır
999999 in böyük_set     # Çox sürətli!

# 3. İki siyahı arasındakı fərqləri tapmaq
köhnə = {"Anar", "Leyla", "Kamran"}
yeni  = {"Leyla", "Kamran", "Zəhra"}

ayrılanlar  = köhnə - yeni       # {"Anar"}
qoşulanlar  = yeni - köhnə       # {"Zəhra"}
qalan       = köhnə & yeni       # {"Leyla", "Kamran"}
```

---

## Dörd Strukturun Ümumi Müqayisəsi

| Xüsusiyyət | `list` | `tuple` | `dict` | `set` |
|---|---|---|---|---|
| Yaratma | `[]` | `()` | `{}` | `set()` |
| Sıralı | ✅ | ✅ | ✅ (3.7+) | ❌ |
| Mutable | ✅ | ❌ | ✅ | ✅ |
| Dublikat | ✅ | ✅ | Açar ❌ | ❌ |
| İndeksləmə | ✅ | ✅ | Açar ilə | ❌ |
| Axtarış sürəti | O(n) | O(n) | O(1) | O(1) |
| Nested ola bilər | ✅ | ✅ | ✅ | ❌ (mutable içərisə) |
| Dict açarı ola bilər | ❌ | ✅ | — | ❌ |

---

## Seçim Qaydası (Decision Guide)

```
Məlumat dəyişməməlidir?
    → Bəli: tuple
    → Xeyr:
        Açar-dəyər cütü lazımdır?
            → Bəli: dict
            → Xeyr:
                Unikal elementlər lazımdır / sürətli axtarış?
                    → Bəli: set
                    → Xeyr: list
```

---

## Xülasə Cədvəli — Metodlar

### List Metodları

| Metod | İşi |
|---|---|
| `append(x)` | Sona bir element əlavə et |
| `insert(i, x)` | i-ci yerə x əlavə et |
| `extend(iterable)` | Bütün elementləri sona əlavə et |
| `remove(x)` | İlk x-i sil (yoxsa KeyError) |
| `pop(i=-1)` | i-ci (default: son) elementi sil və qaytar |
| `clear()` | Hamısını sil |
| `index(x)` | x-in ilk indeksini qaytar |
| `count(x)` | x-in sayını qaytar |
| `sort()` | Yerində sırala |
| `reverse()` | Yerində tərsinə çevir |
| `copy()` | Səthi kopya qaytar |

### Dict Metodları

| Metod | İşi |
|---|---|
| `get(k, default)` | Açarın dəyərini qaytar, yoxsa default |
| `keys()` | Bütün açarları qaytar (view) |
| `values()` | Bütün dəyərləri qaytar (view) |
| `items()` | Açar-dəyər cütlərini qaytar (view) |
| `update(d)` | d-dəki açar-dəyərləri birləşdir |
| `pop(k)` | k açarını sil və dəyərini qaytar |
| `popitem()` | Son cütü sil və qaytar |
| `setdefault(k, v)` | k yoxdursa v dəyəri ilə əlavə et |
| `copy()` | Səthi kopya qaytar |
| `clear()` | Hamısını sil |

### Set Metodları

| Metod / Operator | İşi |
|---|---|
| `add(x)` | x əlavə et |
| `update(iterable)` | Çox element əlavə et |
| `remove(x)` | x-i sil (yoxsa KeyError) |
| `discard(x)` | x-i sil (yoxsa xəta VERMIR) |
| `pop()` | Təsadüfi sil |
| `clear()` | Hamısını sil |
| `A \| B` / `union()` | Birlik |
| `A & B` / `intersection()` | Kəsişmə |
| `A - B` / `difference()` | Fərq |
| `A ^ B` / `symmetric_difference()` | Simmetrik fərq |
| `issubset()` | Alt çoxluqdur? |
| `issuperset()` | Üst çoxluqdur? |
| `isdisjoint()` | Ortaq element yoxdur? |
