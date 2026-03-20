# Həftə 4 - Gün 1: Asinxron Proqramlaşdırmaya Giriş

`learning/week_4/Week4_Day1_Async_Introduction.md`

---

## 1. Asinxron Proqramlaşdırma Nədir?

### 1.1 Sinxron vs Asinxron

**Sinxron (synchronous)** icrada hər əməliyyat növbəti əməliyyat başlamazdan əvvəl tamamlanmalıdır. Əgər bir əməliyyat gözləmə tələb edirsə (disk, şəbəkə), bütün proqram həmin gözləmə bitənə qədər dayanır.

**Asinxron (asynchronous)** icrada isə gözləmə tələb edən əməliyyat başladıqda proqram dayanmır — gözləmə davam edərkən başqa işlər görülür. Gözləmə bitdikdə əvvəlki əməliyyata qayıdılır.

```
Sinxron (ardıcıl):
Tapşırıq A: ████████░░░░░░░░░████    (░ = gözləmə, █ = iş)
Tapşırıq B:                      ████████░░░░████
Tapşırıq C:                                      ████░░████
Cəmi vaxt: ═══════════════════════════════════════════════

Asinxron (kooperativ):
Tapşırıq A: ████████                ████
Tapşırıq B:         ████████            ████
Tapşırıq C:                 ████            ████
Gözləmə:            ░░░░░░░░░░░░░░░░░░░░░░░
Cəmi vaxt: ══════════════════════════════
```

| Yanaşma | Mexanizm | Uyğun Tapşırıq | GIL Problemi |
|---|---|---|---|
| **Sinxron** | Ardıcıl icra | Sadə, xətti axın | — |
| **Threading** | OS thread-ləri, paralel | I/O-bound | GIL maneə olur (CPU üçün) |
| **Multiprocessing** | Ayrı proseslər | CPU-bound | GIL yoxdur |
| **Asyncio** | Tək thread, kooperativ | I/O-bound (çoxlu gözləmə) | GIL problem deyil |

### 1.2 Threading vs Asyncio

Hər ikisi I/O-bound tapşırıqlar üçün uyğundur, amma fərqli mexanizmlərlə:

| Xüsusiyyət | Threading | Asyncio |
|---|---|---|
| **Keçid mexanizmi** | OS qərar verir (preemptive) | Proqramçı qərar verir (cooperative) |
| **Thread sayı** | OS limiti var (~yüzlərlə) | Minlərlə coroutine mümkün |
| **Race condition** | Var — Lock lazımdır | Yoxdur — tək thread |
| **Yaddaş** | Hər thread üçün stack (~8 MB) | Hər coroutine üçün ~1 KB |
| **Debugging** | Çətin (non-deterministic) | Asan (deterministic) |
| **Öyrənmə əyrisi** | Aşağı | Orta-yüksək |

> [!tip] **Best Practice — Nə Vaxt Asyncio?**
> Asyncio bu hallarda threading-dən üstündür:
> - **Çoxlu eyni vaxtlı I/O əməliyyatı** — yüzlərlə/minlərlə API sorğusu, WebSocket bağlantısı
> - **Race condition riski** — tək thread olduğu üçün paylaşılan dataya eyni anda müraciət yoxdur
> - **Yüksək sayda bağlantı** — web server-lər, chat tətbiqləri
>
> Threading isə bu hallarda daha uyğundur:
> - Mövcud sinxron kitabxanalarla inteqrasiya
> - Sadə paralel tapşırıqlar (3-5 thread)

---

## 2. `asyncio` Modulu

### 2.1 Əsas Konseptlər

`asyncio` — Python-un standart kitabxanasında olan asinxron I/O framework-üdür. Üç əsas komponenti var:

- **Event Loop** — bütün asinxron tapşırıqları idarə edən mərkəzi mexanizm
- **Coroutine** — `async def` ilə təyin olunan, dayandırıla bilən funksiya
- **Task** — event loop-da idarə olunan coroutine sarğısı

### 2.2 `async` və `await` Açar Sözləri

`async def` — funksiyanı **coroutine** olaraq təyin edir. Adi funksiyalardan fərqli olaraq, coroutine çağırıldıqda dərhal icra olunmur — əvvəlcə coroutine obyekti yaradılır, sonra `await` və ya event loop vasitəsilə icra edilir.

`await` — asinxron əməliyyatın nəticəsini gözləyir. `await` nöqtəsində coroutine **dayandırılır** və event loop başqa coroutine-ləri icra edə bilər. Əməliyyat tamamlandıqda coroutine davam edir.

```python
import asyncio
import time

# === Adi (sinxron) funksiya ===
def sync_fetch(url, delay):
    """Sinxron — gözləmə zamanı bütün proqram dayanır."""
    print(f"  [SYNC] Başladı: {url}")
    time.sleep(delay)              # Bloklaşdırıcı gözləmə
    print(f"  [SYNC] Bitdi: {url}")
    return f"Data from {url}"


# === Asinxron (coroutine) funksiya ===
async def async_fetch(url, delay):
    """
    Asinxron — gözləmə zamanı başqa coroutine-lər işləyə bilər.

    'async def' bu funksiyanı coroutine edir.
    'await' gözləmə nöqtəsini müəyyən edir — burada
    event loop başqa tapşırıqlara keçə bilər.
    """
    print(f"  [ASYNC] Başladı: {url}")
    await asyncio.sleep(delay)     # Non-blocking gözləmə
    print(f"  [ASYNC] Bitdi: {url}")
    return f"Data from {url}"


# === Sinxron icra ===
def run_sync():
    start = time.perf_counter()
    sync_fetch("site-a.com", 2)
    sync_fetch("site-b.com", 3)
    sync_fetch("site-c.com", 1)
    elapsed = time.perf_counter() - start
    print(f"  Sinxron cəmi: {elapsed:.1f}s\n")   # ~6.0s


# === Asinxron icra ===
async def run_async():
    start = time.perf_counter()

    # asyncio.gather() — birdən çox coroutine-i eyni vaxtda başladır
    results = await asyncio.gather(
        async_fetch("site-a.com", 2),
        async_fetch("site-b.com", 3),
        async_fetch("site-c.com", 1),
    )

    elapsed = time.perf_counter() - start
    print(f"  Asinxron cəmi: {elapsed:.1f}s")     # ~3.0s (ən uzun tapşırığın vaxtı)
    print(f"  Nəticələr: {results}")


# İcra
run_sync()                     # Sinxron
asyncio.run(run_async())       # Asinxron — event loop yaradır və çalışdırır
```

### 2.3 Event Loop — İş Prinsipi

Event loop asinxron proqramlaşdırmanın **ürəyidir**. O, bütün coroutine-ləri, callback-ləri və I/O əməliyyatlarını idarə edir.

```
Event Loop iş axını:
┌──────────────────────────────────┐
│          EVENT LOOP              │
│                                  │
│  1. Hazır tapşırıq var?          │
│     → Bəli: İcra et             │
│     → Xeyr: Gözlə              │
│                                  │
│  2. Tapşırıq 'await' etdi?       │
│     → Bəli: Dayandır, növbətiyə │
│     → Xeyr: Davam et            │
│                                  │
│  3. I/O tamamlandı?              │
│     → Bəli: Coroutine-i oyat    │
│     → Xeyr: Digər tapşırıqlara  │
│                                  │
│  4. Bütün tapşırıqlar bitdi?     │
│     → Bəli: Loop-u dayandır     │
│     → Xeyr: 1-ə qayıt          │
└──────────────────────────────────┘
```

```python
import asyncio

async def boil_water():
    """Su qaynatmaq — uzun I/O əməliyyatı."""
    print("Su ocağa qoyuldu...")
    await asyncio.sleep(5)         # 5 saniyə gözləmə — bu vaxt başqa iş görülə bilər
    print("Su qaynadi!")
    return "Qaynar su"

async def chop_vegetables():
    """Tərəvəzləri doğramaq — qısa iş."""
    print("Tərəvəzlər doğranır...")
    await asyncio.sleep(2)
    print("Tərəvəzlər hazırdır!")
    return "Doğranmış tərəvəzlər"

async def prepare_spices():
    """Ədviyyatlar hazırlamaq — çox qısa iş."""
    print("Ədviyyatlar hazırlanır...")
    await asyncio.sleep(1)
    print("Ədviyyatlar hazırdır!")
    return "Ədviyyatlar"

async def cook_meal():
    """
    Yemək hazırlamaq — bütün addımları eyni vaxtda başladır.
    Su qaynayarkən tərəvəzlər doğranır, ədviyyatlar hazırlanır.
    """
    print("=== Yemək hazırlanması başladı ===\n")

    # Bütün tapşırıqları eyni vaxtda başlat
    water, veggies, spices = await asyncio.gather(
        boil_water(),
        chop_vegetables(),
        prepare_spices(),
    )

    print(f"\nBütün inqrediyentlər hazırdır:")
    print(f"  - {water}")
    print(f"  - {veggies}")
    print(f"  - {spices}")
    print("Yemək bişirilir... Nuş olsun!")

# asyncio.run(cook_meal())
# Cəmi ~5 saniyə (ardıcıl olsaydı 8 saniyə olardı)
```

### 2.4 Task Yaratmaq — `asyncio.create_task()`

`asyncio.gather()` bir qrup coroutine-i birlikdə icra edir. `asyncio.create_task()` isə coroutine-i **dərhal** background-da işə salmağa imkan verir — nəticəni sonra almaq olar.

```python
import asyncio

async def long_operation(name, seconds):
    """Uzun müddətli əməliyyat simulyasiyası."""
    print(f"[{name}] Başladı...")
    await asyncio.sleep(seconds)
    print(f"[{name}] Bitdi! ({seconds}s)")
    return f"{name}: tamamlandı"

async def main():
    # create_task() — coroutine-i dərhal background-da başladır
    task_a = asyncio.create_task(long_operation("A", 3))
    task_b = asyncio.create_task(long_operation("B", 2))
    task_c = asyncio.create_task(long_operation("C", 4))

    # Task-lar artıq işləyir! Biz burada başqa iş görə bilərik
    print("Task-lar işə salındı, digər iş görülür...")
    await asyncio.sleep(1)
    print("1 saniyə keçdi, task-lar hələ işləyir...")

    # Nəticələri gözləyirik
    result_a = await task_a    # A bitənə qədər gözlə
    result_b = await task_b    # B artıq bitmiş ola bilər
    result_c = await task_c    # C bitənə qədər gözlə

    print(f"\nNəticələr: {result_a}, {result_b}, {result_c}")

    # Task-ın statusunu yoxlamaq
    print(f"task_a bitdi? {task_a.done()}")      # True
    print(f"task_a ləğv edildi? {task_a.cancelled()}")  # False

# asyncio.run(main())
```

### 2.5 Timeout — Vaxt Limiti

```python
import asyncio

async def slow_operation():
    """Çox uzun süren əməliyyat."""
    await asyncio.sleep(10)
    return "Nəticə"

async def with_timeout():
    """Əməliyyata vaxt limiti qoymaq."""
    try:
        # asyncio.wait_for() — verilmiş vaxtda tamamlanmazsa TimeoutError
        result = await asyncio.wait_for(slow_operation(), timeout=3.0)
        print(f"Nəticə: {result}")
    except asyncio.TimeoutError:
        print("Əməliyyat 3 saniyə ərzində tamamlanmadı — ləğv edildi!")

    # Python 3.11+ — asyncio.timeout() kontekst meneceri
    # async with asyncio.timeout(3.0):
    #     result = await slow_operation()

# asyncio.run(with_timeout())
```

### 2.6 `asyncio.gather()` vs `asyncio.create_task()` vs `asyncio.wait()`

| Funksiya | Nə Edir | Nə Vaxt İstifadə |
|---|---|---|
| `gather(*coros)` | Hamısını eyni vaxtda icra edir, nəticələri list olaraq qaytarır | Bütün nəticələr lazımdır |
| `create_task(coro)` | Coroutine-i dərhal background-da başladır | Task-ı sonra gözləmək lazımdır |
| `wait(tasks)` | Müxtəlif tamamlanma strategiyaları (FIRST_COMPLETED və s.) | İlk bitəni tutmaq lazımdır |

```python
import asyncio

async def fetch(name, delay):
    await asyncio.sleep(delay)
    return f"{name} tamamlandı"

async def demo_wait():
    """asyncio.wait() — ilk tamamlananı tutmaq."""
    tasks = {
        asyncio.create_task(fetch("Sürətli", 1)),
        asyncio.create_task(fetch("Orta", 3)),
        asyncio.create_task(fetch("Yavaş", 5)),
    }

    # FIRST_COMPLETED — ilk bitən task hazır olduqda qayıdır
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    for task in done:
        print(f"Bitdi: {task.result()}")
    print(f"Hələ davam edir: {len(pending)} task")

    # Qalan task-ları da gözləyirik
    done2, _ = await asyncio.wait(pending)
    for task in done2:
        print(f"Bitdi: {task.result()}")

# asyncio.run(demo_wait())
```

---

## 3. Asinxron Generatorlar və Kontekst Menecerləri

### 3.1 Async Generator

```python
import asyncio

async def countdown(name, start):
    """
    Asinxron generator — async for ilə istifadə olunur.
    Hər dəyər arasında asinxron gözləmə olur.
    """
    for i in range(start, 0, -1):
        await asyncio.sleep(0.5)     # Hər element arasında gözləmə
        yield f"[{name}] {i}"       # Dəyəri qaytarır və dayandırılır

async def main():
    # async for — asinxron generator üzərində iterasiya
    async for value in countdown("Raket", 5):
        print(value)

# asyncio.run(main())
```

### 3.2 Async Context Manager

```python
import asyncio

class AsyncFileProcessor:
    """
    Asinxron kontekst meneceri — 'async with' ilə istifadə olunur.
    __aenter__ və __aexit__ metodları lazımdır.
    """

    def __init__(self, name):
        self.name = name
        self.connection = None

    async def __aenter__(self):
        """async with blokunun başlanğıcında çağırılır."""
        print(f"Bağlantı açılır: {self.name}...")
        await asyncio.sleep(0.5)    # Bağlantı açma simulyasiyası
        self.connection = f"Connection<{self.name}>"
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """async with bloku bitdikdə çağırılır."""
        print(f"Bağlantı bağlanır: {self.name}...")
        await asyncio.sleep(0.2)    # Bağlantı bağlama simulyasiyası
        self.connection = None
        return False

    async def process(self, data):
        """Data emal etmək."""
        print(f"[{self.name}] Emal edilir: {data}")
        await asyncio.sleep(0.3)
        return f"Processed: {data}"

async def main():
    async with AsyncFileProcessor("DB-1") as processor:
        result = await processor.process("Tələbə məlumatları")
        print(f"Nəticə: {result}")
    # Burada bağlantı avtomatik bağlanıb

# asyncio.run(main())
```

---

## 4. Vacib Qaydalar və Tələlər

### 4.1 Async Kodda Sinxron Blocking Çağırmayın

```python
import asyncio
import time

# ❌ SƏHV — sinxron sleep bütün event loop-u bloklayır
async def bad_example():
    time.sleep(5)              # BÜTÜNcoroutine-lər 5 saniyə dayanır!
    return "Bu çox pisdir"

# ✅ DÜZGÜN — asinxron sleep yalnız bu coroutine-i dayandırır
async def good_example():
    await asyncio.sleep(5)     # Yalnız bu coroutine dayandırılır, digərləri işləyir
    return "Bu düzgündür"

# Sinxron kitabxananı async kodda istifadə etmək lazımdırsa:
async def run_sync_in_async():
    loop = asyncio.get_event_loop()
    # run_in_executor() — sinxron kodu ayrı thread-də icra edir
    result = await loop.run_in_executor(None, time.sleep, 2)
    return result
```

### 4.2 Ümumi Xətalar

| Xəta | Problem | Həll |
|---|---|---|
| `await` olmadan coroutine çağırmaq | Coroutine icra olunmur | `await coro()` yazın |
| Sinxron `time.sleep()` | Event loop bloklanan | `await asyncio.sleep()` istifadə edin |
| Async funksiyada sinxron I/O | Event loop bloklanan | `run_in_executor()` istifadə edin |
| `asyncio.run()` iç-içə çağırmaq | RuntimeError | Yalnız bir dəfə, ən yuxarıda çağırın |

---

## 5. Gün 1 — Xülasə

| Mövzu | Əsas Nöqtə |
|---|---|
| **Asinxron proqramlaşdırma** | Gözləmə zamanı başqa iş görmək — tək thread, kooperativ |
| **Event Loop** | Bütün async tapşırıqları idarə edən mərkəzi mexanizm |
| **`async def`** | Funksiyanı coroutine edir |
| **`await`** | Coroutine-i dayandırıb event loop-a nəzarəti verir |
| **`asyncio.gather()`** | Birdən çox coroutine-i eyni vaxtda icra edir |
| **`asyncio.create_task()`** | Coroutine-i background-da başladır |
| **Async generator** | `async for` ilə iterasiya; `yield` + `await` |
| **Async context manager** | `async with`; `__aenter__` / `__aexit__` |

---

> [!note] **Növbəti Gün**
> **Gün 2**-də qabaqcıl asinxron texnikaları — futures, semaphore, exception handling və `concurrent.futures` ilə parallelism öyrənəcəyik.
