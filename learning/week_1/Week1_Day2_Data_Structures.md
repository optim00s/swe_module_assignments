# Həftə 1 - Gün 2: Məlumat Strukturları — Lists, Tuples, Dictionaries, Sets

`learning/week_1/Week1_Day2_Data_Structures.md`

---

## 1. Giriş: Niyə Məlumat Strukturları Vacibdir?

Məlumat strukturları (**data structures**) — məlumatların yaddaşda necə təşkil edildiyini, saxlandığını və onlara necə çatıldığını müəyyən edən konseptlərdir. Düzgün məlumat strukturu seçimi proqramın **performansını**, **oxunaqlılığını** və **scalability**-sini birbaşa təsir edir.

Bir analoji: kitabxanada kitabları raflara necə düzdüyünüz kitabların tapılma sürətini müəyyən edir. Eyni şəkildə, proqramda məlumatları necə strukturlaşdırdığınız onlara çatma sürətini müəyyən edir.

Python-un daxili (built-in) məlumat strukturları dörd əsas kateqoriyaya bölünür:

| Struktur | Sıralıdır? (Ordered) | Dəyişəndir? (Mutable) | Dublikat icazə verir? | Sintaksis |
|---|---|---|---|---|
| **List** | ✅ Bəli | ✅ Bəli | ✅ Bəli | `[1, 2, 3]` |
| **Tuple** | ✅ Bəli | ❌ Xeyr | ✅ Bəli | `(1, 2, 3)` |
| **Dictionary** | ✅ Bəli (3.7+) | ✅ Bəli | Key: ❌, Value: ✅ | `{"a": 1}` |
| **Set** | ❌ Xeyr | ✅ Bəli | ❌ Xeyr | `{1, 2, 3}` |

> [!tip] **Best Practice — Big-O ilə Düşünün**
> Hər məlumat strukturunu seçərkən əsas əməliyyatların **zaman mürəkkəbliyini** (time complexity) düşünün. Məsələn, elementə görə axtarış: list-də **O(n)**, set-də **O(1)**, dict-də key ilə **O(1)**. Böyük datasetlərdə bu fərq saniyələrlə milisaniyələr arasındakı fərqi müəyyən edə bilər.

---

## 2. Siyahılar (Lists)

### 2.1 List Nədir?

List — Python-un ən çox istifadə olunan, **sıralı** (ordered), **dəyişən** (mutable) və **heterogen** (fərqli tipli elementlər saxlaya bilən) məlumat strukturudur. Daxili olaraq **dinamik massiv** (dynamic array) kimi implementasiya olunub — bu o deməkdir ki, elementlər yaddaşda ardıcıl (contiguous) saxlanılır və lazım olduqda massiv avtomatik olaraq genişləndirilir.

List-in mutable olması onu tuple-dan əsas fərqləndirən xüsusiyyətdir: yaradıldıqdan sonra elementlər əlavə edilə, silinə və dəyişdirilə bilər.

### 2.2 List Yaratma

```python
# Boş list yaratmanın iki yolu
empty_list_1 = []          # Literal sintaksis — daha sürətli və Pythonic
empty_list_2 = list()      # Constructor — digər iterable-ları list-ə çevirmək üçün daha uyğun

# Elementlərlə list yaratmaq
epochs = [10, 20, 50, 100, 200]              # Homojen list (bütün elementlər int)
mixed = [42, "GPT", 3.14, True, None]        # Heterojen list (fərqli tiplər)
nested = [[1, 2], [3, 4], [5, 6]]            # İç-içə list (2D massiv/matris kimi)

# list() constructor ilə digər iterable-lardan list yaratmaq
from_string = list("Python")          # ['P', 'y', 't', 'h', 'o', 'n']
from_range = list(range(0, 10, 2))    # [0, 2, 4, 6, 8]
from_tuple = list((1, 2, 3))          # [1, 2, 3]
```

### 2.3 İndeksləmə və Dilimlənmə (Indexing & Slicing)

Python-da indekslər **0-dan** başlayır. Mənfi indekslər sondan geriyə sayır.

```python
layers = ["Input", "Conv2D", "BatchNorm", "ReLU", "Dense", "Softmax"]
#           0        1          2          3        4        5       (müsbət)
#          -6       -5         -4         -3       -2       -1       (mənfi)

# Tək element əldə etmək (indexing)
print(layers[0])       # "Input" — birinci element
print(layers[-1])      # "Softmax" — sonuncu element
print(layers[3])       # "ReLU" — indeks 3-dəki element

# Dilimləmə (slicing) — [start:stop:step]
# start daxildir, stop daxil deyil
print(layers[1:4])     # ['Conv2D', 'BatchNorm', 'ReLU'] — indeks 1, 2, 3
print(layers[:3])      # ['Input', 'Conv2D', 'BatchNorm'] — əvvəldən 3-ə qədər
print(layers[3:])      # ['ReLU', 'Dense', 'Softmax'] — 3-dən sona qədər
print(layers[::2])     # ['Input', 'BatchNorm', 'Dense'] — hər ikinci element
print(layers[::-1])    # ['Softmax', 'Dense', 'ReLU', 'BatchNorm', 'Conv2D', 'Input'] — tərsinə

# Slicing ilə dəyişiklik etmək (list mutable olduğu üçün)
layers[1:3] = ["Conv1D", "LayerNorm"]  # İndeks 1 və 2-ni əvəz edir
print(layers)  # ['Input', 'Conv1D', 'LayerNorm', 'ReLU', 'Dense', 'Softmax']
```

### 2.4 List Metodları

List-in dəyişdirilməsini (mutation) və sorğulanmasını təmin edən əsas metodlar:

#### Elementlər Əlavə Etmə

```python
# Başlanğıc list
pipeline = ["data_collection"]

# append() — Sona tək element əlavə edir. O(1) amortized.
pipeline.append("preprocessing")
print(pipeline)  # ['data_collection', 'preprocessing']

# insert(index, element) — Müəyyən indeksə element yerləşdirir. O(n).
# Sonrakı bütün elementlər bir mövqe sağa sürüşdürülür.
pipeline.insert(1, "data_validation")
print(pipeline)  # ['data_collection', 'data_validation', 'preprocessing']

# extend() — Başqa iterable-ın elementlərini sona əlavə edir. O(k), k = əlavə olunan say.
pipeline.extend(["training", "evaluation", "deployment"])
print(pipeline)
# ['data_collection', 'data_validation', 'preprocessing', 'training', 'evaluation', 'deployment']

# '+' operatoru — İki list-i birləşdirərək yeni list yaradır. O(n+m).
# Orijinal list-lər dəyişmir.
extra_steps = pipeline + ["monitoring"]
print(extra_steps)  # [..., 'deployment', 'monitoring']
print(pipeline)     # Orijinal dəyişməyib
```

> [!tip] **Best Practice — `append()` vs `+` vs `extend()`**
> - Tək element əlavə etmək üçün: `append()` — O(1)
> - Çoxlu element əlavə etmək üçün: `extend()` — O(k)
> - `+` operatoru hər dəfə **yeni list yaradır** — loop içində `list = list + [item]` istifadə etmək O(n²) mürəkkəbliyə gətirib çıxarır. Bunun əvəzinə `append()` istifadə edin.

#### Elementlərin Silinməsi

```python
frameworks = ["TensorFlow", "PyTorch", "Keras", "JAX", "Keras", "Caffe"]

# remove(value) — Verilmiş dəyərin İLK rast gəlinən nüsxəsini silir. O(n).
# Element tapılmazsa ValueError verir.
frameworks.remove("Keras")
print(frameworks)  # ['TensorFlow', 'PyTorch', 'JAX', 'Keras', 'Caffe'] — ilk "Keras" silindi

# pop(index) — Verilmiş indeksdəki elementi silir və QAYTARIR. Default: sonuncu element.
# pop() (indeks olmadan) — O(1), pop(i) — O(n)
last = frameworks.pop()       # "Caffe" — sonuncu elementi silir və qaytarır
second = frameworks.pop(1)    # "PyTorch" — indeks 1-dəki elementi silir
print(last, second)           # Caffe PyTorch
print(frameworks)             # ['TensorFlow', 'JAX', 'Keras']

# del ifadəsi — İndeks və ya dilim ilə silir. Dəyər qaytarmır.
del frameworks[0]             # İndeks 0-dakı elementi silir
print(frameworks)             # ['JAX', 'Keras']

# clear() — Bütün elementləri silir, boş list qalır. O(n).
frameworks.clear()
print(frameworks)             # []
```

#### Sıralama və Axtarış

```python
scores = [88, 72, 95, 61, 83, 95, 77]

# sort() — List-i yerində (in-place) sıralayır. Timsort alqoritmi: O(n log n).
# Yeni list yaratmır, orijinalı dəyişdirir.
scores.sort()
print(scores)  # [61, 72, 77, 83, 88, 95, 95] — artan sıra (default)

scores.sort(reverse=True)
print(scores)  # [95, 95, 88, 83, 77, 72, 61] — azalan sıra

# sorted() — Yeni sıralanmış list qaytarır, orijinalı dəyişdirmir.
original = [3, 1, 4, 1, 5, 9]
sorted_copy = sorted(original)
print(original)     # [3, 1, 4, 1, 5, 9] — dəyişməyib
print(sorted_copy)  # [1, 1, 3, 4, 5, 9]

# key parametri ilə xüsusi sıralama meyarı
models = [
    {"name": "ModelA", "accuracy": 0.92},
    {"name": "ModelB", "accuracy": 0.87},
    {"name": "ModelC", "accuracy": 0.95},
]
models.sort(key=lambda m: m["accuracy"], reverse=True)
# accuracy-yə görə azalan sıra ilə sıralanır

# index(value) — Elementin ilk rast gəlindiyi indeksi qaytarır. O(n).
nums = [10, 20, 30, 20, 40]
print(nums.index(20))       # 1 — ilk 20-nin indeksi
# nums.index(99)            # ValueError — element tapılmadıqda

# count(value) — Elementin neçə dəfə rast gəldiyini sayır. O(n).
print(nums.count(20))       # 2

# 'in' operatoru — Elementin mövcudluğunu yoxlayır. O(n).
print(30 in nums)           # True
print(99 in nums)           # False
```

### 2.5 Shallow Copy vs Deep Copy

Bu, Python-da ən çox qarışdırılan və bug-a səbəb olan konseptlərdən biridir. Fərqi bilmək **kritikdir**.

**Shallow copy** — yeni list yaradır, lakin daxili obyektlərə köhnə list ilə **eyni istinadları** (references) saxlayır. Yəni, əgər daxili element mutable-dırsa (məsələn, list içindəki list), hər iki kopya **eyni daxili obyektə** işarə edir.

**Deep copy** — yeni list yaradır və daxili bütün obyektlərin də **müstəqil kopyalarını** yaradır. Heç bir istinad paylaşılmır.

```python
import copy

# Orijinal: iç-içə list (nested list)
original = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# === Shallow Copy ===
# Üst səviyyə elementlər kopyalanır, amma daxili list-lər EYNI obyektə istinad edir
shallow = original.copy()          # Alternativlər: list(original), original[:]
shallow[0][0] = 999                # Daxili list-i dəyişdirmək...
print(original[0][0])              # 999! — Orijinal DA dəyişdi, çünki eyni obyektə istinad edirlər

# === Deep Copy ===
original = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  # Orijinalı bərpa edirik
deep = copy.deepcopy(original)     # Hər şeyin tam müstəqil kopyası
deep[0][0] = 999                   # Daxili list-i dəyişdirmək...
print(original[0][0])              # 1 — Orijinal dəyişMƏDİ, çünki müstəqil kopyalardır
```

### Shallow Copy vs Deep Copy Müqayisə Cədvəli

| Xüsusiyyət | Shallow Copy | Deep Copy |
|---|---|---|
| **Üst səviyyə** | Yeni obyekt yaradır | Yeni obyekt yaradır |
| **Daxili obyektlər** | Orijinalla eyni istinadı paylaşır | Tam müstəqil kopyalar yaradır |
| **Performans** | Sürətli — O(n) | Yavaş — O(n·m), n = elementlər, m = dərinlik |
| **Yaddaş** | Az yaddaş istifadə edir | Daha çox yaddaş istifadə edir |
| **İstifadə halı** | Flat (tək səviyyəli) list-lər | İç-içə (nested) strukturlar |
| **Yaratma** | `.copy()`, `list()`, `[:]` | `copy.deepcopy()` |

> [!tip] **Best Practice — Nə Vaxt Deep Copy Lazımdır?**
> Əgər list-inizdə yalnız immutable elementlər varsa (int, str, tuple, float), shallow copy kifayətdir — immutable elementlər onsuz da dəyişdirilə bilməz. Deep copy yalnız **mutable daxili obyektlər** (list, dict, set) olduqda lazımdır. ML-də, məsələn, model hiperparametrlərinin dict-inin kopyalanması zamanı deep copy lazım ola bilər.

---

## 3. Dəyişməz Ardıcıllıqlar (Tuples)

### 3.1 Tuple Nədir?

Tuple — **sıralı** (ordered) və **dəyişilməz** (immutable) məlumat strukturudur. Yaradıldıqdan sonra elementlər əlavə edilə, silinə və ya dəyişdirilə bilməz. Bu dəyişilməzlik tuple-ı list-dən fərqləndirən əsas xüsusiyyətdir.

Tuple-ın immutable olmasının praktik faydaları:
1. **Hashable-dır** — dictionary key-i və ya set elementi ola bilər (list isə bilməz)
2. **Thread-safe-dir** — paralel proqramlaşdırmada sinxronizasiya lazım deyil
3. **Daha az yaddaş** istifadə edir — list-dən bir qədər daha optimallaşdırılmışdır
4. **Semantik məna** — "bu məlumat dəyişməməlidir" niyyətini kodda aydın ifadə edir

### 3.2 Tuple Yaratma

```python
# Tuple yaratmanın müxtəlif yolları
empty_tuple = ()                           # Boş tuple
single_element = (42,)                     # Tək elementli tuple — vergül VACİBDİR
without_parens = 42,                       # Mötərizəsiz də tuple yaradılır (tuple packing)
coordinates = (41.0082, 28.9784)           # İstanbul koordinatları
mixed = ("Transformer", 2017, ["attention", "feedforward"])  # Fərqli tiplər

# tuple() constructor
from_list = tuple([1, 2, 3])              # List-dən tuple: (1, 2, 3)
from_string = tuple("AI")                 # String-dən tuple: ('A', 'I')
from_range = tuple(range(5))              # Range-dən tuple: (0, 1, 2, 3, 4)

# DİQQƏT: Tək elementli tuple-da vergül unudulsa, tuple deyil, sadəcə dəyər olur
not_a_tuple = (42)    # Bu int-dir, tuple deyil!
is_a_tuple = (42,)    # Bu tuple-dır
print(type(not_a_tuple))  # <class 'int'>
print(type(is_a_tuple))   # <class 'tuple'>
```

### 3.3 Tuple Əməliyyatları

```python
# İndeksləmə və slicing — list ilə eyni qaydada
model_info = ("GPT-4", "OpenAI", 2023, 1.76e12)
print(model_info[0])      # "GPT-4"
print(model_info[-1])     # 1760000000000.0
print(model_info[1:3])    # ("OpenAI", 2023) — slice nəticəsi də tuple-dır

# Tuple metodları (cəmi 2 metod var — immutable olduğu üçün)
numbers = (3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5)
print(numbers.count(5))   # 3 — 5 rəqəmi 3 dəfə var
print(numbers.index(9))   # 5 — 9 rəqəminin ilk indeksi

# Tuple birləşdirmə — yeni tuple yaradır, orijinallar dəyişmir
part1 = (1, 2, 3)
part2 = (4, 5, 6)
combined = part1 + part2   # (1, 2, 3, 4, 5, 6) — yeni obyekt
repeated = part1 * 3       # (1, 2, 3, 1, 2, 3, 1, 2, 3)

# Tuple dəyişdirilə bilməz — cəhd etdikdə TypeError
# model_info[0] = "GPT-5"  # TypeError: 'tuple' object does not support item assignment
```

### 3.4 Tuple Unpacking (Açma)

Tuple unpacking — tuple-ın elementlərini ayrı-ayrı dəyişənlərə təyin etmək prosesidir. Bu, Python-un ən güclü və gözəl xüsusiyyətlərindən biridir.

```python
# Sadə unpacking
model_name, company, year = ("BERT", "Google", 2018)
print(model_name)   # "BERT"
print(year)         # 2018

# Dəyişən dəyərlərini swap etmək — temp dəyişəninə ehtiyac yoxdur
a, b = 10, 20
a, b = b, a          # Python bunu tuple unpacking ilə edir: (b, a) = (20, 10)
print(a, b)          # 20 10

# * (star) ilə qalan elementləri toplamaq
first, *middle, last = (1, 2, 3, 4, 5)
print(first)    # 1
print(middle)   # [2, 3, 4] — list olaraq toplanır
print(last)     # 5

# Funksiyadan çoxlu dəyər qaytarmaq (əslində tuple qaytarılır)
def evaluate_model(predictions, labels):
    correct = sum(p == l for p, l in zip(predictions, labels))
    total = len(predictions)
    accuracy = correct / total
    error_rate = 1 - accuracy
    return accuracy, error_rate   # Tuple olaraq qaytarır: (accuracy, error_rate)

acc, err = evaluate_model([1, 0, 1, 1], [1, 1, 1, 1])
print(f"Accuracy: {acc:.2%}, Error: {err:.2%}")  # Accuracy: 75.00%, Error: 25.00%

# İstifadə olunmayan dəyərləri '_' ilə keçmək
_, _, year = ("BERT", "Google", 2018)
print(year)  # 2018 — yalnız year lazımdır, qalanları nəzərə almırıq
```

### 3.5 Named Tuples

`collections.namedtuple` — tuple-ın oxunaqlı versiyasıdır. Elementlərə indeks əvəzinə **ad ilə** müraciət etmək imkanı verir, eyni zamanda tuple-ın bütün üstünlüklərini (immutability, hashability, memory efficiency) saxlayır.

```python
from collections import namedtuple

# Named tuple təyini — ModelConfig adlı yeni tip yaradır
ModelConfig = namedtuple("ModelConfig", ["name", "params", "layers", "accuracy"])

# Obyekt yaratmaq
gpt4 = ModelConfig(
    name="GPT-4",
    params=1.76e12,
    layers=120,
    accuracy=0.945
)

# Elementlərə ad ilə müraciət — indeks əvəzinə
print(gpt4.name)       # "GPT-4" — çox daha oxunaqlı
print(gpt4.accuracy)   # 0.945
print(gpt4[0])         # "GPT-4" — indeks ilə müraciət hələ də işləyir

# Named tuple immutable-dır
# gpt4.accuracy = 0.96  # AttributeError

# _replace() — dəyişikliklə yeni tuple yaradır (orijinal dəyişmir)
gpt4_updated = gpt4._replace(accuracy=0.96)
print(gpt4_updated)    # ModelConfig(name='GPT-4', params=1760000000000.0, layers=120, accuracy=0.96)
```

> [!tip] **Best Practice — Named Tuple vs Dataclass**
> Python 3.7+ ilə gələn `@dataclass` dekoratoru named tuple-a güclü alternativdir. Əsas fərq: dataclass-lar default olaraq **mutable**-dır (lakin `frozen=True` ilə immutable edilə bilər) və daha çox funksionallıq təklif edir (default dəyərlər, metodlar, `__post_init__`). Sadə, dəyişməz data konteynerləri üçün named tuple; daha mürəkkəb data modelləri üçün dataclass istifadə edin.

---

## 4. Lüğətlər (Dictionaries)

### 4.1 Dictionary Nədir?

Dictionary (dict) — **açar-dəyər** (key-value) cütlərindən ibarət, **sıralı** (Python 3.7+-da daxiletmə sırasını qoruyur), **dəyişən** (mutable) məlumat strukturudur. Daxili olaraq **hash table** kimi implementasiya olunub — bu, key ilə axtarışın **orta O(1)** mürəkkəbliklə baş verməsini təmin edir.

Dictionary-nin key-ləri **hashable** olmalıdır — bu o deməkdir ki, key kimi yalnız immutable tiplər (str, int, float, tuple) istifadə edilə bilər. List, dict, set kimi mutable tiplər key ola bilməz, çünki onların hash dəyəri dəyişə bilər.

### 4.2 Dictionary Yaratma

```python
# Literal sintaksis — ən çox istifadə olunan yol
model_registry = {
    "gpt-4": {"provider": "OpenAI", "params": "1.76T", "type": "LLM"},
    "claude-3": {"provider": "Anthropic", "params": "Unknown", "type": "LLM"},
    "gemini": {"provider": "Google", "params": "Unknown", "type": "Multimodal"},
}

# dict() constructor
config = dict(learning_rate=0.001, epochs=100, batch_size=32)
# {'learning_rate': 0.001, 'epochs': 100, 'batch_size': 32}

# Cütlər siyahısından dict yaratmaq
pairs = [("name", "ResNet"), ("layers", 50), ("accuracy", 0.93)]
model = dict(pairs)
# {'name': 'ResNet', 'layers': 50, 'accuracy': 0.93}

# dict.fromkeys() — eyni default dəyərlə birdən çox key yaratmaq
metrics = dict.fromkeys(["precision", "recall", "f1_score"], 0.0)
# {'precision': 0.0, 'recall': 0.0, 'f1_score': 0.0}

# zip() ilə iki list-dən dict yaratmaq
keys = ["name", "version", "framework"]
values = ["BERT", "base", "PyTorch"]
model_info = dict(zip(keys, values))
# {'name': 'BERT', 'version': 'base', 'framework': 'PyTorch'}
```

### 4.3 Elementlərə Müraciət

```python
config = {
    "model": "Transformer",
    "layers": 12,
    "hidden_size": 768,
    "attention_heads": 12,
}

# Birbaşa indeksləmə — key mövcud deyilsə KeyError verir
print(config["model"])     # "Transformer"
# print(config["missing"])  # KeyError: 'missing'

# get() metodu — key mövcud deyilsə default dəyər qaytarır (KeyError vermir)
print(config.get("model"))           # "Transformer"
print(config.get("dropout", 0.1))    # 0.1 — key yoxdur, default qaytarılır
print(config.get("missing"))         # None — default verilməyibsə None qaytarılır
```

> [!tip] **Best Practice — `[]` vs `get()`**
> - Key-in **mütləq olmalı** olduğu hallarda `[]` istifadə edin — KeyError xətası bug-u erkən aşkar etməyə kömək edir (fail fast prinsipi).
> - Key-in **ola da, olmaya da biləcəyi** hallarda `get()` istifadə edin — xüsusilə konfiqurasiya oxuyarkən, API cavablarını emal edərkən.
> - `get()` istifadəsi `if key in dict` yoxlamasından daha Pythonic və effektivdir.

### 4.4 Dictionary Metodları

```python
# Yeni key-value əlavə etmək / mövcud olanı yeniləmək
config = {"model": "BERT", "layers": 12}

config["dropout"] = 0.1                 # Yeni key əlavə edir
config["layers"] = 24                   # Mövcud key-in dəyərini yeniləyir
print(config)  # {'model': 'BERT', 'layers': 24, 'dropout': 0.1}

# update() — Başqa dict-dən toplu yeniləmə
config.update({"optimizer": "AdamW", "layers": 36})
print(config)  # {'model': 'BERT', 'layers': 36, 'dropout': 0.1, 'optimizer': 'AdamW'}

# | operatoru ilə merge (Python 3.9+)
defaults = {"lr": 0.001, "epochs": 100}
overrides = {"epochs": 50, "batch_size": 32}
final = defaults | overrides    # overrides üstünlük qazanır
# {'lr': 0.001, 'epochs': 50, 'batch_size': 32}

# setdefault() — Key varsa dəyərini qaytarır, yoxdursa əlavə edib qaytarır
config.setdefault("scheduler", "cosine")   # "scheduler" yoxdur, əlavə edir
config.setdefault("model", "GPT")          # "model" artıq var, dəyişdirmir
print(config["scheduler"])  # "cosine"
print(config["model"])      # "BERT" — dəyişmədi

# Silmə əməliyyatları
removed_value = config.pop("dropout")       # Key-i silir və dəyərini qaytarır
print(removed_value)                        # 0.1
safe_remove = config.pop("missing", None)   # Key yoxdursa default qaytarır
last_item = config.popitem()                # Sonuncu key-value cütünü silir (LIFO)

del config["optimizer"]                     # del ilə silmə — dəyər qaytarmır
```

### 4.5 Dictionary Üzərində İterasiya

```python
hyperparams = {
    "learning_rate": 0.001,
    "batch_size": 32,
    "epochs": 100,
    "dropout": 0.3,
}

# Yalnız key-lər üzərində (default davranış)
for key in hyperparams:
    print(key)
# learning_rate, batch_size, epochs, dropout

# Yalnız dəyərlər üzərində
for value in hyperparams.values():
    print(value)
# 0.001, 32, 100, 0.3

# Key-value cütləri üzərində (ən çox istifadə olunan)
for key, value in hyperparams.items():
    print(f"{key}: {value}")

# Dict comprehension ilə dəyərləri transformasiya etmək
# Bütün string dəyərləri böyük hərfə çevirmək
metadata = {"name": "bert", "version": "large", "task": "classification"}
upper_metadata = {k: v.upper() for k, v in metadata.items()}
# {'name': 'BERT', 'version': 'LARGE', 'task': 'CLASSIFICATION'}
```

### 4.6 defaultdict və Counter

`collections` modulundakı xüsusi dict tipləri çox faydalıdır:

```python
from collections import defaultdict, Counter

# defaultdict — mövcud olmayan key-ə müraciət edildikdə avtomatik default dəyər yaradır
# KeyError əvəzinə default factory function çağırılır

# Sözləri kateqoriyalara görə qruplaşdırmaq
word_categories = defaultdict(list)   # Default dəyər: boş list []
words = [("noun", "model"), ("verb", "train"), ("noun", "data"), ("verb", "predict")]

for category, word in words:
    # Key yoxdursa avtomatik boş list yaradılır, sonra append edilir
    word_categories[category].append(word)

print(dict(word_categories))
# {'noun': ['model', 'data'], 'verb': ['train', 'predict']}

# Sayğac olaraq defaultdict
char_count = defaultdict(int)   # Default dəyər: 0
for char in "transformer":
    char_count[char] += 1       # Mövcud deyilsə 0-dan başlayır

print(dict(char_count))
# {'t': 1, 'r': 3, 'a': 1, 'n': 1, 's': 1, 'f': 1, 'o': 1, 'e': 1}

# Counter — elementləri sayma üçün xüsusi dict
predictions = ["positive", "negative", "positive", "neutral", "positive", "negative"]
count = Counter(predictions)
print(count)                        # Counter({'positive': 3, 'negative': 2, 'neutral': 1})
print(count.most_common(2))         # [('positive', 3), ('negative', 2)] — ən çox rast gələn 2
```

---

## 5. Çoxluqlar (Sets)

### 5.1 Set Nədir?

Set — **sırasız** (unordered), **dəyişən** (mutable) və **yalnız unikal elementlər** saxlayan məlumat strukturudur. Daxili olaraq hash table kimi implementasiya olunub — bu, üzvlük yoxlaması (`in` operatoru) və əlavə/silmə əməliyyatlarının **orta O(1)** mürəkkəbliklə baş verməsini təmin edir.

Set-in elementləri **hashable** olmalıdır — yəni yalnız immutable tiplər (int, str, float, tuple) ola bilər. List, dict, digər set kimi mutable tiplər set elementi ola bilməz.

### 5.2 Set Yaratma

```python
# Literal sintaksis
unique_frameworks = {"TensorFlow", "PyTorch", "JAX", "TensorFlow"}
print(unique_frameworks)   # {'TensorFlow', 'PyTorch', 'JAX'} — dublikat avtomatik silinir

# DIQQƏT: Boş set yaratmaq üçün {} istifadə etmək olmaz — bu boş dict yaradır!
empty_dict = {}            # Bu DICT-dir, set deyil!
empty_set = set()          # Boş set yaratmanın düzgün yolu

# set() constructor — istənilən iterable-dan dublikatları silir
numbers = set([1, 2, 2, 3, 3, 3, 4])   # {1, 2, 3, 4}
chars = set("mississippi")              # {'m', 'i', 's', 'p'} — unikal simvollar
```

### 5.3 Set Əməliyyatları

```python
# Element əlavə etmə və silmə
skills = {"python", "sql", "git"}

skills.add("docker")           # Tək element əlavə edir. O(1).
skills.add("python")           # Artıq var — heç bir effekt yoxdur
print(skills)                  # {'python', 'sql', 'git', 'docker'}

skills.update(["kubernetes", "linux"])  # Birdən çox element əlavə edir
print(skills)                  # {'python', 'sql', 'git', 'docker', 'kubernetes', 'linux'}

skills.remove("sql")           # Elementi silir. Element yoxdursa KeyError verir.
skills.discard("java")         # Elementi silir. Element yoxdursa XƏTASİZ keçir.
popped = skills.pop()          # Təsadüfi bir elementi silir və qaytarır
```

### 5.4 Set Cəbri Əməliyyatları (Set Algebra)

Set-in ən güclü tərəfi riyazi çoxluq əməliyyatlarıdır. Bu əməliyyatlar data müqayisəsi, filtrasiya və analiz üçün son dərəcə faydalıdır.

```python
# İki ML mühəndisinin bacarıq dəstləri
engineer_a = {"python", "pytorch", "docker", "sql", "kubernetes"}
engineer_b = {"python", "tensorflow", "aws", "sql", "spark"}

# BİRLƏŞMƏ (Union) — Hər iki set-dəki bütün unikal elementlər
all_skills = engineer_a | engineer_b    # və ya: engineer_a.union(engineer_b)
print(all_skills)
# {'python', 'pytorch', 'docker', 'sql', 'kubernetes', 'tensorflow', 'aws', 'spark'}

# KƏSİŞMƏ (Intersection) — Hər iki set-də ortaq olan elementlər
common_skills = engineer_a & engineer_b   # və ya: engineer_a.intersection(engineer_b)
print(common_skills)
# {'python', 'sql'}

# FƏRQ (Difference) — A-da olub B-də olmayan elementlər
only_a = engineer_a - engineer_b          # və ya: engineer_a.difference(engineer_b)
print(only_a)
# {'pytorch', 'docker', 'kubernetes'}

only_b = engineer_b - engineer_a
print(only_b)
# {'tensorflow', 'aws', 'spark'}

# SİMMETRİK FƏRQ (Symmetric Difference) — Yalnız birində olan elementlər (ortaq olmayanlar)
unique_to_each = engineer_a ^ engineer_b  # və ya: engineer_a.symmetric_difference(engineer_b)
print(unique_to_each)
# {'pytorch', 'docker', 'kubernetes', 'tensorflow', 'aws', 'spark'}
```

```python
# Set müqayisə əməliyyatları
required_skills = {"python", "sql"}
candidate_skills = {"python", "sql", "docker", "pytorch"}

# Alt çoxluq (Subset) yoxlaması — "required bütünlüklə candidate-in içindədir?"
print(required_skills <= candidate_skills)    # True — issubset()
print(required_skills < candidate_skills)     # True — strict subset (tam eyni deyil)

# Üst çoxluq (Superset) yoxlaması
print(candidate_skills >= required_skills)    # True — issuperset()

# Kəsişməsiz (Disjoint) yoxlaması — "heç bir ortaq element yoxdur?"
set_a = {1, 2, 3}
set_b = {4, 5, 6}
print(set_a.isdisjoint(set_b))               # True — ortaq element yoxdur
```

### 5.5 Frozenset — Dəyişilməz Set

`frozenset` — set-in immutable versiyasıdır. Dict key-i və ya başqa set-in elementi ola bilər.

```python
# Frozenset yaratmaq
immutable_set = frozenset([1, 2, 3, 4])
# immutable_set.add(5)  # AttributeError — dəyişdirilə bilməz

# Dict key-i kimi istifadə — adi set bunu edə bilməz
permissions = {
    frozenset({"read", "write"}): "Editor",
    frozenset({"read"}): "Viewer",
    frozenset({"read", "write", "admin"}): "Admin",
}

user_perms = frozenset({"read", "write"})
print(permissions[user_perms])  # "Editor"
```

### 5.6 Set Əməliyyatları Müqayisə Cədvəli

| Əməliyyat | Operator | Metod | Nəticə |
|---|---|---|---|
| Birləşmə | `a \| b` | `a.union(b)` | Hər iki set-dəki bütün elementlər |
| Kəsişmə | `a & b` | `a.intersection(b)` | Ortaq elementlər |
| Fərq | `a - b` | `a.difference(b)` | A-da olub B-də olmayanlar |
| Simmetrik fərq | `a ^ b` | `a.symmetric_difference(b)` | Yalnız birində olanlar |
| Alt çoxluq | `a <= b` | `a.issubset(b)` | A, B-nin alt çoxluğudur? |
| Üst çoxluq | `a >= b` | `a.issuperset(b)` | A, B-nin üst çoxluğudur? |

---

## 6. Əsas Data Strukturlarının Müqayisəsi

### 6.1 List vs Tuple

| Xüsusiyyət | List | Tuple |
|---|---|---|
| **Sintaksis** | `[1, 2, 3]` | `(1, 2, 3)` |
| **Mutable?** | ✅ Bəli | ❌ Xeyr |
| **Hashable?** | ❌ Xeyr | ✅ Bəli (elementlər hashable olduqda) |
| **Dict key ola bilər?** | ❌ Xeyr | ✅ Bəli |
| **Performans** | Bir qədər yavaş | Bir qədər sürətli (immutability optimallaşdırması) |
| **Yaddaş** | Daha çox (dynamic resize üçün əlavə yer) | Daha az |
| **Metodlar** | 11+ metod | 2 metod (count, index) |
| **İstifadə halı** | Dinamik kolleksiyalar, elementlər dəyişə bilər | Sabit data: koordinatlar, RGB, qaytarma dəyərləri |
| **Semantik məna** | "Eyni tipdə şeylərin dəyişkən siyahısı" | "Fərqli tiplərdə sabit data qrupu" |

### 6.2 List vs Set

| Xüsusiyyət | List | Set |
|---|---|---|
| **Sıralıdır?** | ✅ Bəli | ❌ Xeyr |
| **Dublikat?** | ✅ İcazə verir | ❌ Yalnız unikal |
| **İndekslə müraciət** | ✅ `list[0]` | ❌ Mümkün deyil |
| **`in` axtarış sürəti** | O(n) — yavaş | O(1) — çox sürətli |
| **Element tipi** | İstənilən | Yalnız hashable |
| **İstifadə halı** | Sıralı data, dublikat lazımdır | Unikal data, sürətli axtarış |

### 6.3 Dictionary vs List of Tuples

| Xüsusiyyət | Dictionary | List of Tuples |
|---|---|---|
| **Key ilə axtarış** | O(1) | O(n) |
| **Sıralıdır?** | ✅ (3.7+) | ✅ |
| **Dublikat key?** | ❌ Son dəyər qalır | ✅ İcazə verir |
| **Yaddaş** | Daha çox (hash table overhead) | Daha az |
| **İstifadə halı** | Key-value mapping, sürətli axtarış | Sıralı cütlər, dublikat key lazımdır |

### 6.4 Əməliyyatların Zaman Mürəkkəbliyi (Time Complexity)

| Əməliyyat | List | Tuple | Dict | Set |
|---|---|---|---|---|
| **İndekslə müraciət** | O(1) | O(1) | — | — |
| **Key ilə axtarış** | — | — | O(1) avg | — |
| **`in` (üzvlük yoxlama)** | O(n) | O(n) | O(1) avg | O(1) avg |
| **Sona əlavə** | O(1) amort. | — | O(1) avg | O(1) avg |
| **Əvvələ əlavə** | O(n) | — | — | — |
| **Silmə (dəyərə görə)** | O(n) | — | O(1) avg | O(1) avg |
| **Sıralama** | O(n log n) | — | — | — |

---

## 7. Gün 2 — Xülasə

| Mövzu | Əsas Nöqtə |
|---|---|
| **List** | Sıralı, mutable, dynamic array; ən universal data struktur |
| **Tuple** | Sıralı, immutable; sabit data üçün, dict key ola bilər |
| **Dictionary** | Key-value cütləri, hash table, O(1) axtarış |
| **Set** | Unikal elementlər, hash table, çoxluq əməliyyatları |
| **Shallow vs Deep Copy** | Nested mutable obyektlər olduqda deep copy lazımdır |
| **Big-O** | Data strukturu seçimi performansa birbaşa təsir edir |

---

> [!note] **Növbəti Gün**
> **Gün 3**-də Python-un güclü funksional alətlərini — List Comprehensions, Generators və Decorators öyrənəcəyik. Bu alətlər kodun qısalığını, oxunaqlılığını və yaddaş effektivliyini artırır.
