# Həftə 5 - Gün 3: Debugging Texnikaları və Alətləri

`learning/week_5/Week5_Day3_Debugging.md`

---

## 1. Debugging Nədir?

### 1.1 Giriş

**Debugging** — proqramdakı xətaların (bug) mənbəyini tapmaq və aradan qaldırmaq prosesidir. "Bug" termini 1947-ci ildə Harvard kompüterində tapılan **həqiqi böcəkdən** (güvə) qaynaqlanır.

Debugging sadəcə "xətanı düzəltmək" deyil — bu, **sistemli düşüncə** tələb edən prosesdir. Effektiv debugging proqramçının ən vacib bacarıqlarından biridir.

### 1.2 Bug Tipləri

| Tip | Tərif | Nümunə | Aşkarlama Çətinliyi |
|---|---|---|---|
| **Syntax Error** | Dil qaydalarının pozulması | `)` unudulub, `:` çatmır | Asan — Python dərhal bildirir |
| **Runtime Error** | İcra zamanı yaranan xəta | `ZeroDivisionError`, `KeyError` | Orta — xəta mesajı var |
| **Logic Error** | Kod işləyir, amma nəticə səhvdir | Yanlış hesablama, səhv şərt | Çətin — xəta mesajı yoxdur |
| **Heisenbug** | Debug edərkən yox olan bug | Race condition, timing issues | Çox çətin |

---

## 2. Debugging Strategiyaları

### 2.1 Sistemli Bug Axtarma Prosesi

```
1. REPRODUCE — Bug-ı təkrarla
   "Hansı addımlarla bu xəta baş verir?"

2. ISOLATE — Problemi təcrid et
   "Kodun hansı hissəsi xətalıdır?"

3. IDENTIFY — Səbəbi müəyyən et
   "Niyə belə davranır?"

4. FIX — Düzəlt
   "Ən minimal, təhlükəsiz düzəliş nədir?"

5. VERIFY — Yoxla
   "Düzəliş işləyir? Yeni bug yaratmadı?"

6. PREVENT — Gələcəkdə qarşısını al
   "Bu bug üçün test yazım."
```

### 2.2 Rubber Duck Debugging

Bu texnika absurd görünsə də, çox effektivdir: problemi **başqa birinə** (və ya rezin ördəyə) sözlə izah edərkən beyin problemi fərqli perspektivdən görür və tez-tez həlli tapır.

```
1. Rezin ördəyi masanıza qoyun (və ya təsəvvür edin)
2. Ördəyə kodu sətir-sətir izah edin
3. "Bu sətir X edir, çünki Y lazımdır..."
4. Çox vaxt izah edərkən "Bir saniyə... burada problem var!" deyirsiniz
```

### 2.3 Binary Search Debugging

Böyük kod bazasında bug-ı tapmaq üçün **ikili axtarış** strategiyası:

```python
def find_bug_in_pipeline(data):
    """
    Uzun pipeline-da bug-ı tapmaq üçün aralıq nəticələri yoxlayırıq.
    """
    step_1 = read_data(data)
    print(f"DEBUG step_1: {step_1[:3]}...")      # Aralıq nəticəni yoxla

    step_2 = clean_data(step_1)
    print(f"DEBUG step_2: {step_2[:3]}...")      # Burada düzgündür?

    step_3 = transform_data(step_2)
    print(f"DEBUG step_3: {step_3[:3]}...")      # Burada problem başlayır?

    step_4 = aggregate_data(step_3)              # Bug burada olmalıdır
    print(f"DEBUG step_4: {step_4}")

    return step_4
```

---

## 3. `print()` Debugging

Ən sadə debugging üsulu — strateji nöqtələrə `print()` əlavə etmək. Sadə bug-lar üçün effektivdir, amma böyük layihələrdə idarəolunmaz olur.

```python
def calculate_discount(price, customer_type, quantity):
    """Endirimi hesablayır — debugging ilə."""
    print(f"DEBUG: price={price}, type={customer_type}, qty={quantity}")

    if customer_type == "premium":
        base_discount = 0.15
    elif customer_type == "regular":
        base_discount = 0.05
    else:
        base_discount = 0

    print(f"DEBUG: base_discount={base_discount}")

    # Toplu alış bonusu
    if quantity >= 100:
        bulk_bonus = 0.10
    elif quantity >= 50:
        bulk_bonus = 0.05
    else:
        bulk_bonus = 0

    print(f"DEBUG: bulk_bonus={bulk_bonus}")

    total_discount = base_discount + bulk_bonus
    final_price = price * quantity * (1 - total_discount)

    print(f"DEBUG: total_discount={total_discount}, final={final_price}")
    return final_price
```

> [!warning] **Diqqət — `print()` Debugging-in Problemləri**
> 1. **Production-a getmə riski** — print ifadələrini silməyi unutmaq
> 2. **Performans** — çoxlu print I/O-nu yavaşladır
> 3. **İdarəolunmazlıq** — çox print olduqda output oxunmaz olur
> 4. **Yetersizlik** — mürəkkəb obyektləri, stack trace-i göstərmir
>
> Bunun əvəzinə **logging modulu** və ya **debugger** istifadə edin.

---

## 4. `pdb` — Python Debugger

### 4.1 pdb Nədir?

`pdb` — Python-un daxili, interaktiv debugging alətidir. Kodu **addım-addım** icra etməyə, dəyişənləri **yoxlamağa** və **breakpoint** (dayandırma nöqtəsi) qoymağa imkan verir.

### 4.2 Breakpoint Qoymaq

```python
def process_orders(orders):
    """Sifarişləri emal edir — debugging üçün breakpoint var."""
    results = []

    for order in orders:
        # Python 3.7+ — daxili breakpoint() funksiyası
        # İcra burada dayanacaq və interaktiv debug rejimi açılacaq
        breakpoint()

        subtotal = order["price"] * order["quantity"]
        tax = subtotal * 0.18
        total = subtotal + tax
        results.append({
            "id": order["id"],
            "total": round(total, 2)
        })

    return results

# Test datası
orders = [
    {"id": 1, "price": 25.00, "quantity": 3},
    {"id": 2, "price": 50.00, "quantity": 1},
    {"id": 3, "price": 10.00, "quantity": 10},
]

# Bu çağırılanda pdb rejimi açılır
# process_orders(orders)
```

### 4.3 pdb Əmrləri

| Əmr | Qısa | Nə Edir |
|---|---|---|
| `help` | `h` | Kömək göstərir |
| `next` | `n` | Növbəti sətirə keç (funksiyaya girmədən) |
| `step` | `s` | Növbəti sətirə keç (funksiyaya gir) |
| `continue` | `c` | Növbəti breakpoint-ə qədər davam et |
| `print(expr)` | `p expr` | İfadəni qiymətləndir və göstər |
| `pp expr` | | Pretty-print (gözəl format) |
| `list` | `l` | Cari kod konteksini göstər |
| `longlist` | `ll` | Bütün funksiyanı göstər |
| `where` | `w` | Stack trace — harada olduğunuzu göstərir |
| `up` | `u` | Stack-da yuxarı keç |
| `down` | `d` | Stack-da aşağı keç |
| `break N` | `b N` | N-ci sətirə breakpoint qoy |
| `clear N` | `cl N` | N nömrəli breakpoint-i sil |
| `return` | `r` | Funksiyanın sonuna qədər davam et |
| `quit` | `q` | Debugger-dən çıx |

### 4.4 Praktik Debug Sessiyası

```python
def find_outliers(data, threshold=2.0):
    """
    Standart kənarlaşmaya görə outlier-ları tapır.
    Bug: nəticə düzgün deyil — debugging lazımdır.
    """
    n = len(data)
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    std_dev = variance ** 0.5

    outliers = []
    for value in data:
        z_score = (value - mean) / std_dev
        if abs(z_score) > threshold:
            outliers.append(value)

    return outliers

# Debugging sessiyası:
# 1. breakpoint() əlavə edin
# 2. python script.py icra edin
# 3. pdb> promptunda:
#    p mean        → ortalamanı yoxlayın
#    p std_dev     → standart kənarlaşmanı yoxlayın
#    n             → növbəti sətirə keçin
#    p z_score     → hər elementin z-score-unu yoxlayın
#    c             → davam edin
```

> [!tip] **Best Practice — Debugger İstifadə Qaydaları**
> 1. `breakpoint()` istifadə edin (`import pdb; pdb.set_trace()` əvəzinə) — Python 3.7+
> 2. **PYTHONBREAKPOINT=0** mühit dəyişəni ilə bütün breakpoint-ləri söndürün (production)
> 3. IDE debugger-i (VS Code, PyCharm) daha rahatdır — vizual breakpoint, dəyişən paneli
> 4. Breakpoint-ləri commit etməyin — `.pre-commit` hook ilə yoxlayın

---

## 5. IDE Debugger (VS Code / Cursor)

### 5.1 VS Code Debugger Xüsusiyyətləri

| Xüsusiyyət | Təsvir |
|---|---|
| **Breakpoint** | Sətir nömrəsinin soluna klik — qırmızı nöqtə |
| **Conditional Breakpoint** | Yalnız şərt doğru olduqda dayandırır |
| **Watch** | Dəyişənlərin dəyərini real vaxtda izləmək |
| **Call Stack** | Funksiyanın haradan çağırıldığını görmək |
| **Variables Panel** | Bütün lokal/qlobal dəyişənləri görmək |
| **Step Over (F10)** | Növbəti sətir (funksiyaya girmədən) |
| **Step Into (F11)** | Funksiyaya daxil olmaq |
| **Step Out (Shift+F11)** | Funksiyadan çıxmaq |
| **Continue (F5)** | Növbəti breakpoint-ə qədər davam etmək |

### 5.2 `launch.json` Konfiqurasiyası

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true
        },
        {
            "name": "Python: Pytest",
            "type": "debugpy",
            "request": "launch",
            "module": "pytest",
            "args": ["-v", "--tb=short"],
            "console": "integratedTerminal"
        }
    ]
}
```

---

## 6. Logging Modulu

### 6.1 Niyə Logging?

`logging` modulu `print()`-in peşəkar alternatividir. O, mesajları **səviyyəsinə** görə süzür, **faylda** saxlayır, **formatlaşdırır** və **production-da** söndürülmədən saxlanıla bilir.

### 6.2 Log Səviyyələri

| Səviyyə | Ədədi | İstifadə |
|---|---|---|
| `DEBUG` | 10 | Ətraflı texniki məlumat — yalnız development |
| `INFO` | 20 | Ümumi əməliyyat məlumatları |
| `WARNING` | 30 | Potensial problem — amma hələ işləyir |
| `ERROR` | 40 | Xəta baş verdi — əməliyyat uğursuz |
| `CRITICAL` | 50 | Ciddi xəta — sistem işləyə bilmir |

### 6.3 Əsas İstifadə

```python
import logging

# Logger yaratmaq — modulun adı ilə
logger = logging.getLogger(__name__)

# Konfiqurasiya — fayla və konsola yazmaq
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(name)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),     # Fayla yaz
        logging.StreamHandler(),                               # Konsola yaz
    ]
)

def process_student_record(record):
    """Tələbə qeydini emal edir — logging ilə."""
    logger.debug(f"Qeyd emal edilir: {record}")

    if not record.get("name"):
        logger.warning(f"Adsız qeyd tapıldı: {record}")
        return None

    try:
        score = float(record["score"])
        logger.info(f"Tələbə emal edildi: {record['name']} — {score}")
    except (ValueError, KeyError) as e:
        logger.error(f"Qeyd emalında xəta: {record} — {e}")
        return None
    except Exception as e:
        logger.critical(f"Gözlənilməz xəta: {e}", exc_info=True)
        raise

    return {"name": record["name"], "score": score}

# İstifadə
process_student_record({"name": "Əli", "score": "85"})
# 2026-03-19 14:30:45 | __main__ | DEBUG    | Qeyd emal edilir: {'name': 'Əli', 'score': '85'}
# 2026-03-19 14:30:45 | __main__ | INFO     | Tələbə emal edildi: Əli — 85.0

process_student_record({"name": "", "score": "90"})
# 2026-03-19 14:30:45 | __main__ | WARNING  | Adsız qeyd tapıldı: {'name': '', 'score': '90'}
```

### 6.4 Peşəkar Logging Konfiqurasiyası

```python
import logging
import logging.handlers
from pathlib import Path

def setup_logging(log_dir="logs", level=logging.INFO):
    """
    Peşəkar logging konfiqurasiyası.

    - Konsola — rəngli, qısa format
    - Fayla — ətraflı format, rotasiya ilə
    """
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Konsol handler — yalnız INFO və yuxarı
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_format = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S"
    )
    console_handler.setFormatter(console_format)

    # Fayl handler — rotasiya ilə (5MB-dan böyük olduqda yeni fayl)
    file_handler = logging.handlers.RotatingFileHandler(
        log_path / "app.log",
        maxBytes=5 * 1024 * 1024,     # 5 MB
        backupCount=5,                 # Maksimum 5 köhnə fayl saxlanılır
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        "%(asctime)s | %(name)-20s | %(levelname)-8s | "
        "%(filename)s:%(lineno)d | %(message)s"
    )
    file_handler.setFormatter(file_format)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    return root_logger

# Layihənin giriş nöqtəsində çağırın
# setup_logging(level=logging.DEBUG)  # Development
# setup_logging(level=logging.INFO)   # Production
```

> [!tip] **Best Practice — Logging Qaydaları**
> 1. **Modul başına logger** — `logger = logging.getLogger(__name__)` hər modula ayrı logger verir
> 2. **Düzgün səviyyə** — `DEBUG` development üçün, `INFO` production üçün
> 3. **Structured logging** — JSON formatında log (ELK stack ilə inteqrasiya üçün)
> 4. **Heç vaxt geniş except istifadə etməyin** — `except Exception as e: logger.error(e)` ən azı
> 5. **`exc_info=True`** — xəta log-larında stack trace daxil edin
> 6. **Sensitive datanı log etməyin** — parol, API key, şəxsi məlumatlar

---

## 7. Ümumi Debugging Texnikaları Müqayisəsi

| Texnika | Sürət | Güc | Nə Vaxt İstifadə |
|---|---|---|---|
| **`print()`** | Çox sürətli | Aşağı | Sadə, müvəqqəti debug |
| **`breakpoint()`/pdb** | Orta | Yüksək | İnteraktiv araşdırma |
| **IDE Debugger** | Orta | Çox yüksək | Vizual, mürəkkəb debug |
| **Logging** | Sürətli | Orta-yüksək | Production monitoring |
| **Testlər** | Yavaş (yazma) | Çox yüksək | Bug-ın təkrarlanması, reqression |
| **Rubber Duck** | Sürətli | Orta | Məntiq xətaları |
| **Git bisect** | Orta | Yüksək | "Bu bug nə vaxt yaranıb?" |

---

## 8. `traceback` Oxumaq

Python xəta mesajlarını (traceback) düzgün oxumaq debugging-in əsasıdır.

```python
# Nümunə traceback:
#
# Traceback (most recent call last):           ← Ən son çağırış ən altdadır
#   File "main.py", line 25, in <module>       ← Giriş nöqtəsi
#     result = process_data(raw_data)
#   File "main.py", line 18, in process_data   ← Orta çağırış
#     cleaned = clean_record(record)
#   File "utils.py", line 7, in clean_record   ← Bug BURADADIR (ən alt)
#     score = int(record["score"])
# ValueError: invalid literal for int() with base 10: 'N/A'
#
# OXUMA QAYDALARI:
# 1. Ən ALTDAN oxuyun — xətanın baş verdiyi yer
# 2. Exception tipi və mesajı: ValueError — "N/A" int-ə çevrilə bilməz
# 3. Fayl və sətir nömrəsi: utils.py, sətir 7
# 4. Çağırış zənciri: main → process_data → clean_record
```

---

## 9. Gün 3 — Xülasə

| Mövzu | Əsas Nöqtə |
|---|---|
| **Debugging prosesi** | Reproduce → Isolate → Identify → Fix → Verify → Prevent |
| **print() debug** | Sadə, sürətli, amma production-a uyğun deyil |
| **pdb / breakpoint()** | İnteraktiv debug; `n`, `s`, `c`, `p` əmrləri |
| **IDE Debugger** | Vizual breakpoint, watch, call stack |
| **Logging** | Production-ready; səviyyəli, faylda saxlanılan |
| **Traceback oxuma** | Altdan yuxarıya oxuyun; exception tipi + mesaj + sətir |

---

## 10. Proqram Tamamlanması — Ümumi Xülasə

Bu 5 həftəlik proqramda Python-un əsaslarından başlayaraq peşəkar proqram təminatı mühəndisliyi prinsiplərinə qədər geniş bir yol keçdiniz:

| Həftə | Mövzu | Əsas Bacarıqlar |
|---|---|---|
| **Həftə 1** | Python əsasları | Dəyişənlər, kontrol strukturları, funksiyalar, data strukturları, comprehensions, generators, decorators |
| **Həftə 2** | Qabaqcıl xüsusiyyətlər | File I/O, exceptions, modullar/paketlər, API/web scraping |
| **Həftə 3** | OOP | Siniflər, miras alma, polimorfizm, composition, abstraction, concurrency |
| **Həftə 4** | Async & Deployment | asyncio, async/await, futures, database, Docker |
| **Həftə 5** | Keyfiyyət | Clean code, testing (pytest/TDD), debugging, logging |

> [!tip] **Növbəti Addım**
> Bu əsaslar üzərində qurmağa davam edin:
> - **Layihə qurun** — öyrəndiklərinizi real layihədə tətbiq edin
> - **Open source** — başqalarının kodunu oxuyun, töhfə verin
> - **Hər gün kod yazın** — ardıcıllıq hər şeydən vacibdir
