# Həftə 4 - Gün 2: Qabaqcıl Asinxron Texnikalar

`learning/week_4/Week4_Day2_Advanced_Async.md`

---

## 1. Futures və Coroutines

### 1.1 Future Nədir?

**Future** — hələ tamamlanmamış əməliyyatın **gələcək nəticəsini** təmsil edən obyektdir. "Söz verirəm ki, nəticə olacaq" konseptini ifadə edir. Future yaradıldıqda nəticə hələ yoxdur — əməliyyat tamamlandıqda nəticə Future-ə yazılır.

Python-da iki fərqli Future implementasiyası var:

| Tip | Modul | İstifadə Sahəsi |
|---|---|---|
| `asyncio.Future` | `asyncio` | Asinxron kod (event loop daxilində) |
| `concurrent.futures.Future` | `concurrent.futures` | Thread/process pool-lardan nəticə almaq |

### 1.2 `concurrent.futures` — Birləşdirilmiş İnterfeys

Bu modul threading və multiprocessing üçün **eyni yüksək səviyyəli API** təqdim edir. Yalnız executor sinifini dəyişdirməklə thread-dən process-ə keçid mümkündür.

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import time

def fetch_page(url):
    """Web səhifə yükləmə simulyasiyası (I/O-bound)."""
    print(f"  Yüklənir: {url}")
    time.sleep(1.5)
    return {"url": url, "status": 200, "size": len(url) * 100}

def calculate_checksum(data):
    """Data yoxlama cəmi hesablama (CPU-bound)."""
    total = 0
    for char in data * 10000:
        total += ord(char)
    return total

urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3",
    "https://example.com/page4",
    "https://example.com/page5",
]

# === ThreadPoolExecutor — I/O-bound tapşırıqlar üçün ===
print("Thread Pool ilə:")
start = time.perf_counter()

with ThreadPoolExecutor(max_workers=5) as executor:
    # submit() — hər tapşırığı ayrıca göndərir, Future qaytarır
    futures = {executor.submit(fetch_page, url): url for url in urls}

    # as_completed() — tamamlanan Future-ləri bitdikcə qaytarır (sırasız)
    for future in as_completed(futures):
        url = futures[future]
        try:
            result = future.result()   # Nəticəni almaq
            print(f"  ✅ {url}: {result['size']} bytes")
        except Exception as e:
            print(f"  ❌ {url}: {e}")

print(f"  Vaxt: {time.perf_counter() - start:.1f}s\n")

# === ProcessPoolExecutor — CPU-bound tapşırıqlar üçün ===
if __name__ == "__main__":
    print("Process Pool ilə:")
    data_items = ["alpha", "beta", "gamma", "delta", "epsilon"]
    start = time.perf_counter()

    with ProcessPoolExecutor(max_workers=4) as executor:
        # map() — nəticələr orijinal sıra ilə qaytarılır
        results = list(executor.map(calculate_checksum, data_items))

    for item, checksum in zip(data_items, results):
        print(f"  {item}: checksum = {checksum:,}")
    print(f"  Vaxt: {time.perf_counter() - start:.1f}s")
```

### 1.3 Future Metodları

```python
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import time

def task(name, duration):
    time.sleep(duration)
    if name == "error_task":
        raise ValueError(f"{name} uğursuz oldu!")
    return f"{name}: {duration}s-də tamamlandı"

with ThreadPoolExecutor(max_workers=3) as executor:
    future_a = executor.submit(task, "fast", 1)
    future_b = executor.submit(task, "slow", 4)
    future_c = executor.submit(task, "error_task", 2)

    # Future statusunu yoxlamaq
    print(f"A tamamlandı? {future_a.done()}")      # False (hələ işləyir)
    print(f"A ləğv edilə bilər? {future_a.cancel()}")  # False (artıq başlayıb)

    # result() — nəticəni gözləyir (blocking)
    # timeout parametri ilə vaxt limiti
    try:
        result_a = future_a.result(timeout=5)
        print(f"A nəticəsi: {result_a}")
    except TimeoutError:
        print("A vaxt limiti keçdi")

    # Exception olan Future
    try:
        result_c = future_c.result()
    except ValueError as e:
        print(f"C xətası: {e}")

    # wait() — müəyyən şərtlə gözləmək
    remaining = {future_b}
    done, not_done = wait(remaining, return_when=FIRST_COMPLETED)
    for f in done:
        print(f"Tamamlandı: {f.result()}")
```

### 1.4 Callback — Future Tamamlandıqda Avtomatik Çağırış

```python
from concurrent.futures import ThreadPoolExecutor
import time

def download(url):
    """Yükləmə simulyasiyası."""
    time.sleep(1)
    return {"url": url, "data": f"Content of {url}", "size": len(url) * 50}

def on_download_complete(future):
    """Future tamamlandıqda avtomatik çağırılan callback."""
    try:
        result = future.result()
        print(f"  ✅ Yükləndi: {result['url']} ({result['size']} bytes)")
    except Exception as e:
        print(f"  ❌ Xəta: {e}")

with ThreadPoolExecutor(max_workers=3) as executor:
    urls = ["page1.html", "page2.html", "page3.html"]
    for url in urls:
        future = executor.submit(download, url)
        # add_done_callback() — Future bitdikdə çağırılacaq funksiya
        future.add_done_callback(on_download_complete)

    # Callback-lər avtomatik çağırılır — gözləməyə ehtiyac yoxdur
```

---

## 2. Asyncio-da Xəta İdarəetmə

### 2.1 Exception Handling Async Kodda

```python
import asyncio

async def risky_operation(name, should_fail=False):
    """Xəta ola biləcək asinxron əməliyyat."""
    await asyncio.sleep(1)
    if should_fail:
        raise ConnectionError(f"{name}: Bağlantı uğursuz oldu!")
    return f"{name}: uğurlu"


async def safe_gather():
    """
    asyncio.gather() ilə xəta idarəetmə.

    return_exceptions=True olduqda, xətalar Exception obyekti olaraq
    nəticə siyahısına daxil edilir (raise olunmur).
    """
    results = await asyncio.gather(
        risky_operation("Task-1"),
        risky_operation("Task-2", should_fail=True),
        risky_operation("Task-3"),
        return_exceptions=True     # Xətaları nəticə kimi qaytarır
    )

    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"  Task-{i+1}: ❌ Xəta — {result}")
        else:
            print(f"  Task-{i+1}: ✅ {result}")

# asyncio.run(safe_gather())
# Task-1: ✅ Task-1: uğurlu
# Task-2: ❌ Xəta — Task-2: Bağlantı uğursuz oldu!
# Task-3: ✅ Task-3: uğurlu
```

### 2.2 Task Ləğvetmə (Cancellation)

```python
import asyncio

async def long_running_task():
    """Uzun müddətli tapşırıq — ləğv edilə bilər."""
    try:
        print("Tapşırıq başladı...")
        for i in range(10):
            print(f"  Addım {i+1}/10")
            await asyncio.sleep(1)   # Hər addımda ləğv yoxlanılır
        return "Tamamlandı"
    except asyncio.CancelledError:
        # Task ləğv edildikdə bu exception qaldırılır
        print("  Tapşırıq ləğv edildi! Təmizlik işləri aparılır...")
        # Burada resurs təmizləmə işləri aparıla bilər
        raise    # CancelledError-u yenidən qaldırın (best practice)

async def main():
    task = asyncio.create_task(long_running_task())

    # 3 saniyə sonra task-ı ləğv et
    await asyncio.sleep(3)
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print("Main: Task uğurla ləğv edildi.")

# asyncio.run(main())
```

---

## 3. Semaphore — Eynivaxtlılığı Məhdudlaşdırmaq

**Semaphore** — eyni vaxtda icra olunan əməliyyatların sayını məhdudlaşdıran mexanizmdir. Bu, serveri çoxlu sorğularla yükləməmək üçün vacibdir (rate limiting).

```python
import asyncio

async def fetch_with_limit(semaphore, url, session_id):
    """Semaphore ilə məhdudlaşdırılmış asinxron sorğu."""
    async with semaphore:
        # Semaphore daxilindəki kod — eyni vaxtda max N əməliyyat
        print(f"  [{session_id}] Başladı: {url}")
        await asyncio.sleep(2)    # Sorğu simulyasiyası
        print(f"  [{session_id}] Bitdi: {url}")
        return f"Result from {url}"

async def main():
    # Eyni vaxtda maksimum 3 sorğu icazə verilir
    semaphore = asyncio.Semaphore(3)

    urls = [f"https://api.example.com/data/{i}" for i in range(10)]

    tasks = [
        fetch_with_limit(semaphore, url, i)
        for i, url in enumerate(urls)
    ]

    results = await asyncio.gather(*tasks)
    print(f"\n{len(results)} sorğu tamamlandı.")

# asyncio.run(main())
# Nəticə: 10 sorğu 3-3-3-1 qruplarla icra olunur
# Cəmi vaxt: ~8s (3 qrup × 2s + 1 qrup × 2s) əvəzinə 20s (ardıcıl)
```

---

## 4. Asinxron İteratorlar və Generatorlar

### 4.1 `async for` ilə Asinxron İterasiya

```python
import asyncio

class AsyncPaginator:
    """
    Asinxron paginator — API səhifələrini ardıcıl yükləyir.

    __aiter__ və __anext__ metodları async for dəstəyi verir.
    """

    def __init__(self, base_url, total_pages):
        self.base_url = base_url
        self.total_pages = total_pages
        self.current_page = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.current_page >= self.total_pages:
            raise StopAsyncIteration    # Asinxron iterasiyanı dayandırır

        self.current_page += 1
        # Səhifə yükləmə simulyasiyası
        await asyncio.sleep(0.5)
        return {
            "page": self.current_page,
            "url": f"{self.base_url}?page={self.current_page}",
            "items": [f"item_{self.current_page}_{i}" for i in range(5)],
        }


async def main():
    paginator = AsyncPaginator("https://api.example.com/items", total_pages=4)

    all_items = []
    async for page_data in paginator:
        print(f"Səhifə {page_data['page']} yükləndi: {len(page_data['items'])} element")
        all_items.extend(page_data['items'])

    print(f"Cəmi: {len(all_items)} element toplandı")

# asyncio.run(main())
```

### 4.2 Async Generator Funksiyası

```python
import asyncio

async def event_stream(source, count):
    """
    Asinxron generator — hadisə axını simulyasiyası.
    'async def' + 'yield' = asinxron generator.
    """
    for i in range(count):
        await asyncio.sleep(0.3)     # Hadisəni gözləmək
        event = {
            "source": source,
            "event_id": i,
            "data": f"Event data #{i} from {source}",
        }
        yield event    # Hadisəni qaytarır

async def merge_streams():
    """İki event stream-i birləşdirir."""
    # Asinxron generatorlar async for ilə istifadə olunur
    async for event in event_stream("sensor_a", 3):
        print(f"  Received: {event['source']} — #{event['event_id']}")

    async for event in event_stream("sensor_b", 2):
        print(f"  Received: {event['source']} — #{event['event_id']}")

# asyncio.run(merge_streams())
```

---

## 5. Sinxron Kodu Async Kodda İstifadə Etmək

### 5.1 `run_in_executor()` — Sinxron Bloklaşdırıcı Kodu Async Etmək

Bəzən sinxron kitabxanalardan (requests, sqlite3 və s.) istifadə etmək lazım gəlir. Bu kitabxanalar async deyil — birbaşa çağırsaq event loop bloklayar. `run_in_executor()` onları ayrı thread-də icra edir.

```python
import asyncio
import time

def sync_heavy_io(filepath):
    """Sinxron I/O əməliyyatı — async DEYİL."""
    time.sleep(2)    # Disk I/O simulyasiyası
    return f"Data from {filepath}"

def sync_cpu_work(n):
    """Sinxron CPU hesablaması — async DEYİL."""
    total = sum(i * i for i in range(n))
    return total

async def main():
    loop = asyncio.get_event_loop()

    # Sinxron I/O funksiyasını thread pool-da icra etmək
    # None = default ThreadPoolExecutor
    result_io = await loop.run_in_executor(
        None,                          # None = default thread pool
        sync_heavy_io, "data.csv"      # Funksiya və arqumentlər
    )
    print(f"I/O nəticəsi: {result_io}")

    # Birdən çox sinxron tapşırığı paralel icra etmək
    tasks = [
        loop.run_in_executor(None, sync_heavy_io, f"file_{i}.csv")
        for i in range(5)
    ]
    results = await asyncio.gather(*tasks)
    print(f"Bütün fayllar: {results}")

# asyncio.run(main())
```

> [!tip] **Best Practice — Async Ekosistemini Üstün Tutun**
> Mümkün olduqda sinxron kitabxanaların async alternativlərini istifadə edin:
> - `requests` → **`aiohttp`** və ya **`httpx`** (async HTTP client)
> - `sqlite3` → **`aiosqlite`**
> - `open()` (fayl) → **`aiofiles`**
>
> `run_in_executor()` son çarə olmalıdır — async kitabxana mövcud deyilsə.

---

## 6. Gün 2 — Xülasə

| Mövzu | Əsas Nöqtə |
|---|---|
| **Future** | Hələ tamamlanmamış əməliyyatın gələcək nəticəsi |
| **`concurrent.futures`** | ThreadPool / ProcessPool üçün birləşdirilmiş API |
| **Exception handling** | `return_exceptions=True`, `CancelledError` |
| **Semaphore** | Eynivaxtlılığı məhdudlaşdırmaq (rate limiting) |
| **Async iterator** | `__aiter__` / `__anext__`, `async for` |
| **Async generator** | `async def` + `yield` |
| **`run_in_executor()`** | Sinxron kodu async-də istifadə etmək |

---

> [!note] **Növbəti Gün**
> **Gün 3**-də Python tətbiqlərinin verilənlər bazası ilə inteqrasiyası, paketləmə və Docker ilə konteynerləşdirilməsini öyrənəcəyik.
