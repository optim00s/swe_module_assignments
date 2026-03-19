# Həftə 3 - Gün 3: Paralellik — Threading və Multiprocessing

`learning/week_3/Week3_Day3_Concurrency.md`

---

## 1. Concurrency (Paralellik) Nədir?

### 1.1 Əsas Konseptlər

**Concurrency** — birdən çox tapşırığın **eyni zaman aralığında** idarə edilməsidir. Bu, mütləq eyni anda icra olunma demək deyil — tapşırıqlar növbə ilə, amma **sürətlə keçid edərək** idarə oluna bilər.

**Parallelism** — birdən çox tapşırığın **fiziki olaraq eyni anda** icra edilməsidir. Bunun üçün birdən çox CPU nüvəsi lazımdır.

| Konsept | Tərif | Analoji |
|---|---|---|
| **Concurrency** | Birdən çox tapşırığı idarə etmək | Bir aşpaz iki yeməyi növbə ilə hazırlayır |
| **Parallelism** | Birdən çox tapşırığı eyni anda icra etmək | İki aşpaz hərəsi bir yemək hazırlayır |
| **Thread** | Prosesin daxilində yüngül icra vahidi | Bir mətbəxdəki aşpazlar |
| **Process** | Müstəqil icra vahidi, öz yaddaşı ilə | Ayrı-ayrı mətbəxlər |

### 1.2 Nə Vaxt Hansı Yanaşma?

| Tapşırıq Tipi | Xüsusiyyəti | Həll | Nümunə |
|---|---|---|---|
| **I/O-bound** | Gözləmə çoxdur (disk, şəbəkə) | Threading / Asyncio | Fayl oxuma, API sorğusu |
| **CPU-bound** | Hesablama yoğundur | Multiprocessing | Riyazi hesablamalar, data emalı |

---

## 2. GIL — Global Interpreter Lock

### 2.1 GIL Nədir?

**GIL (Global Interpreter Lock)** — CPython interpretatorundakı mexanizmdir ki, **eyni anda yalnız bir thread-in** Python bytecode-u icra etməsinə icazə verir. Bu, CPython-un yaddaş idarəetməsini (reference counting) thread-safe etmək üçün lazımdır.

**GIL-in Nəticələri:**

| Tapşırıq Tipi | GIL-in Təsiri | Nəticə |
|---|---|---|
| **I/O-bound** | GIL I/O gözləyərkən buraxılır | Threading **effektivdir** |
| **CPU-bound** | GIL thread-lər arasında paylaşılır | Threading **effektiv deyil** — multiprocessing lazımdır |

```
CPU-bound tapşırıq + Threading:
Thread 1: ████░░░░████░░░░████   (GIL var → gözləyir)
Thread 2: ░░░░████░░░░████░░░░   (GIL var → gözləyir)
Nəticə: Tək thread-dən YAVAŞ ola bilər (context switching overhead)

I/O-bound tapşırıq + Threading:
Thread 1: ██░░░░░░██░░░░░░██     (I/O gözləyir → GIL buraxılır)
Thread 2: ░░██░░░░░░██░░░░░░██   (GIL boş → işləyir)
Nəticə: Threading EFFEKTIV — gözləmə zamanı digər iş görülür
```

---

## 3. Threading Modulu

### 3.1 Thread Yaratmaq

```python
import threading
import time

def download_file(filename, size_mb):
    """Fayl yükləmə simulyasiyası (I/O-bound tapşırıq)."""
    print(f"[{threading.current_thread().name}] "
          f"'{filename}' yüklənir ({size_mb} MB)...")
    time.sleep(size_mb / 10)   # Hər 10 MB üçün 1 saniyə gözləmə
    print(f"[{threading.current_thread().name}] "
          f"'{filename}' yükləndi!")
    return filename


# === Ardıcıl icra (threading olmadan) ===
start = time.perf_counter()
download_file("data_1.csv", 30)
download_file("data_2.csv", 20)
download_file("data_3.csv", 40)
sequential_time = time.perf_counter() - start
print(f"Ardıcıl: {sequential_time:.1f} saniyə\n")   # ~9.0 saniyə


# === Threading ilə paralel icra ===
start = time.perf_counter()

# Thread obyektləri yaratmaq
thread_1 = threading.Thread(
    target=download_file,          # İcra ediləcək funksiya
    args=("data_1.csv", 30),       # Funksiyanın arqumentləri
    name="Downloader-1"            # Thread-in adı (opsional, debug üçün)
)
thread_2 = threading.Thread(
    target=download_file,
    args=("data_2.csv", 20),
    name="Downloader-2"
)
thread_3 = threading.Thread(
    target=download_file,
    args=("data_3.csv", 40),
    name="Downloader-3"
)

# Thread-ləri başlatmaq
thread_1.start()
thread_2.start()
thread_3.start()

# Bütün thread-lərin bitməsini gözləmək
thread_1.join()     # Main thread burada dayanır, thread_1 bitənə qədər
thread_2.join()
thread_3.join()

threaded_time = time.perf_counter() - start
print(f"Threading: {threaded_time:.1f} saniyə")   # ~4.0 saniyə (ən uzun tapşırığın vaxtı)
print(f"Sürət artımı: {sequential_time/threaded_time:.1f}x")
```

### 3.2 Thread Pool — `concurrent.futures`

`ThreadPoolExecutor` — thread-ləri əl ilə yaratmaq/idarə etmək əvəzinə, **thread pool** (thread hovuzu) təqdim edir. Bu, threading-in ən tövsiyə olunan yüksək səviyyəli interfeysidir.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def process_file(filepath):
    """Fayl emalı simulyasiyası."""
    print(f"  İşlənir: {filepath}")
    time.sleep(1)   # I/O simulyasiyası
    line_count = len(filepath) * 100     # Sadə hesablama
    return {"file": filepath, "lines": line_count}

files = [
    "report_jan.csv", "report_feb.csv", "report_mar.csv",
    "report_apr.csv", "report_may.csv", "report_jun.csv",
]

# === ThreadPoolExecutor ilə ===
start = time.perf_counter()
results = []

with ThreadPoolExecutor(max_workers=3) as executor:
    # submit() — hər tapşırığı ayrıca göndərir, Future qaytarır
    future_to_file = {
        executor.submit(process_file, f): f
        for f in files
    }

    # as_completed() — tamamlanan tapşırıqları bitdikcə qaytarır
    for future in as_completed(future_to_file):
        filepath = future_to_file[future]
        try:
            result = future.result()    # Nəticəni almaq (xəta varsa re-raise edir)
            results.append(result)
        except Exception as e:
            print(f"Xəta ({filepath}): {e}")

elapsed = time.perf_counter() - start
print(f"\n{len(results)} fayl {elapsed:.1f} saniyədə emal edildi.")

# === map() — daha sadə interfeys (sıra qorunur) ===
with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(process_file, files))
```

### 3.3 Thread Safety — Paylaşılan Data Problemi

Birdən çox thread eyni data üzərində işlədikdə **race condition** yarana bilər — nəticə thread-lərin icra sırasından asılı olur və gözlənilməz olur.

```python
import threading

# === PROBLEM — Race Condition ===
class UnsafeCounter:
    """Thread-safe OLMAYAN sayğac — race condition var."""
    def __init__(self):
        self.count = 0

    def increment(self):
        # Bu əməliyyat atomik DEYİL — bir neçə addımdan ibarətdir:
        # 1. self.count dəyərini oxu
        # 2. 1 əlavə et
        # 3. Nəticəni self.count-a yaz
        # Thread-lər arasında keçid bu addımlar arasında baş verə bilər!
        current = self.count
        current += 1
        self.count = current


# === HƏLL — Lock istifadə etmək ===
class SafeCounter:
    """Thread-safe sayğac — Lock ilə qorunur."""
    def __init__(self):
        self.count = 0
        self._lock = threading.Lock()   # Kilidləmə mexanizmi

    def increment(self):
        with self._lock:
            # Lock aldıqda yalnız BU thread bu kodu icra edə bilər
            # Digər thread-lər gözləyir (blocked)
            current = self.count
            current += 1
            self.count = current


def stress_test(counter, iterations=100000):
    """Sayğacı çoxlu thread ilə test edir."""
    def worker():
        for _ in range(iterations):
            counter.increment()

    threads = [threading.Thread(target=worker) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    expected = iterations * 5
    print(f"  Gözlənilən: {expected:,}")
    print(f"  Faktiki:    {counter.count:,}")
    print(f"  Düzgün?     {'✅' if counter.count == expected else '❌'}")


print("Unsafe counter (race condition):")
stress_test(UnsafeCounter())
# Gözlənilən: 500,000 | Faktiki: 487,234 (və ya fərqli ədəd) ❌

print("\nSafe counter (with Lock):")
stress_test(SafeCounter())
# Gözlənilən: 500,000 | Faktiki: 500,000 ✅
```

> [!tip] **Best Practice — Thread Safety**
> 1. **Paylaşılan dəyişənləri minimuma endirin** — thread-lər arası paylaşılan state ən az olmalıdır
> 2. **Lock istifadə edin** — `threading.Lock()` və ya `threading.RLock()` (reentrant lock)
> 3. **`with lock:` sintaksisi** istifadə edin — lock-un mütləq release olunmasını təmin edir
> 4. **Thread-safe data strukturları** istifadə edin — `queue.Queue` kimi
> 5. **Deadlock-dan qaçının** — iki thread bir-birinin lock-unu gözlədiyi vəziyyət

---

## 4. Multiprocessing Modulu

### 4.1 Niyə Multiprocessing?

Threading **I/O-bound** tapşırıqlar üçün effektivdir, amma **CPU-bound** tapşırıqlar üçün GIL maneəsi var. Multiprocessing **ayrı-ayrı proseslər** yaradır — hər prosesin öz Python interpretatoru və GIL-i var. Bu, çoxnüvəli CPU-ların tam potensialından istifadə etməyə imkan verir.

| Xüsusiyyət | Threading | Multiprocessing |
|---|---|---|
| **GIL təsiri** | ✅ GIL tətbiq olunur | ❌ GIL yoxdur (hər prosesin öz GIL-i) |
| **Yaddaş** | Paylaşılan (shared memory) | Ayrı (isolated memory) |
| **Yaratma xərci** | Yüngül (kilobytes) | Ağır (megabytes — yeni proses) |
| **Kommunikasiya** | Asan (ortaq dəyişənlər) | Çətin (pickle/unpickle lazım) |
| **Uyğun tapşırıq** | I/O-bound | CPU-bound |
| **Xəta təcridliyi** | Bir thread crash edərsə, proses ölür | Bir proses crash edərsə, digəri davam edir |

### 4.2 Multiprocessing ilə CPU-bound Tapşırıq

```python
import multiprocessing
import time

def calculate_sum_of_squares(start, end):
    """
    Verilmiş aralıqdakı ədədlərin kvadratlar cəmini hesablayır.
    Bu, CPU-intensive tapşırıqdır.
    """
    total = sum(i * i for i in range(start, end))
    return total


# === Ardıcıl icra ===
def sequential_calculation():
    start_time = time.perf_counter()
    total = calculate_sum_of_squares(0, 50_000_000)
    elapsed = time.perf_counter() - start_time
    print(f"Ardıcıl: {elapsed:.2f}s, Nəticə: {total}")
    return elapsed


# === Multiprocessing ilə paralel icra ===
def parallel_calculation():
    start_time = time.perf_counter()

    # İşi 4 hissəyə bölürük
    ranges = [
        (0, 12_500_000),
        (12_500_000, 25_000_000),
        (25_000_000, 37_500_000),
        (37_500_000, 50_000_000),
    ]

    with multiprocessing.Pool(processes=4) as pool:
        # starmap() — hər tuple-ı funksiyaya argument olaraq ötürür
        results = pool.starmap(calculate_sum_of_squares, ranges)

    total = sum(results)
    elapsed = time.perf_counter() - start_time
    print(f"Paralel:  {elapsed:.2f}s, Nəticə: {total}")
    return elapsed


if __name__ == "__main__":
    seq_time = sequential_calculation()
    par_time = parallel_calculation()
    print(f"Sürət artımı: {seq_time/par_time:.1f}x")
```

### 4.3 ProcessPoolExecutor

`concurrent.futures.ProcessPoolExecutor` — multiprocessing-in yüksək səviyyəli interfeysidir. `ThreadPoolExecutor` ilə **eyni API**-yə malikdir — yalnız backend fərqlidir.

```python
from concurrent.futures import ProcessPoolExecutor
import time

def heavy_computation(n):
    """CPU-intensive hesablama."""
    total = 0
    for i in range(n):
        total += i ** 2 - i + 1
    return total

if __name__ == "__main__":
    numbers = [5_000_000, 8_000_000, 3_000_000, 7_000_000, 6_000_000]

    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(heavy_computation, numbers))
    elapsed = time.perf_counter() - start

    for n, r in zip(numbers, results):
        print(f"  n={n:>10,}: result={r:>20,}")
    print(f"\nCəmi vaxt: {elapsed:.2f}s")
```

> [!warning] **Diqqət — `if __name__ == "__main__":`**
> Windows-da multiprocessing istifadə edərkən `if __name__ == "__main__":` **mütləqdir**. Windows-da yeni proses yaratmaq üçün modul yenidən import edilir — bu qoruyucu olmadan sonsuz proses yaranması baş verə bilər.

---

## 5. Thread-safe Kommunikasiya — `queue.Queue`

```python
import threading
import queue
import time

def producer(q, items):
    """Məhsul istehsalçısı — növbəyə elementlər əlavə edir."""
    for item in items:
        time.sleep(0.5)    # İstehsal simulyasiyası
        q.put(item)
        print(f"  [Producer] Əlavə edildi: {item} (Növbədə: {q.qsize()})")
    q.put(None)            # Siqnal: "daha element yoxdur"

def consumer(q, results):
    """İstehlakçı — növbədən elementlər alır və emal edir."""
    while True:
        item = q.get()     # Element gələnə qədər gözləyir (blocking)
        if item is None:
            break
        processed = item.upper()
        results.append(processed)
        print(f"  [Consumer] Emal edildi: {item} → {processed}")
        q.task_done()      # Tapşırığın tamamlandığını bildirir


task_queue = queue.Queue(maxsize=5)   # Maksimum 5 element saxlaya bilər
results = []

items = ["alpha", "beta", "gamma", "delta", "epsilon"]

prod = threading.Thread(target=producer, args=(task_queue, items))
cons = threading.Thread(target=consumer, args=(task_queue, results))

prod.start()
cons.start()
prod.join()
cons.join()

print(f"\nNəticələr: {results}")
```

---

## 6. Gün 3 — Xülasə

| Mövzu | Əsas Nöqtə |
|---|---|
| **Concurrency vs Parallelism** | Concurrency = idarəetmə, Parallelism = eyni anda icra |
| **GIL** | CPython-da yalnız 1 thread Python kodu icra edə bilər |
| **Threading** | I/O-bound tapşırıqlar üçün; GIL I/O zamanı buraxılır |
| **Lock** | Paylaşılan datanı race condition-dan qoruyur |
| **Multiprocessing** | CPU-bound tapşırıqlar üçün; ayrı proseslər, ayrı GIL |
| **`concurrent.futures`** | ThreadPoolExecutor / ProcessPoolExecutor — yüksək səviyyəli API |
| **Queue** | Thread-safe kommunikasiya — producer/consumer pattern |

---

> [!note] **Növbəti Həftə**
> **Həftə 4, Gün 1**-də Python-un asinxron proqramlaşdırma mexanizmlərini — `asyncio`, `async/await` öyrənəcəyik.
