# Həftə 2 - Gün 3: API-lərlə İşləmək və Web Scraping

`learning/week_2/Week2_Day3_APIs_WebScraping.md`

---

## 1. API-lərlə İşləmək

### 1.1 API Nədir?

**API (Application Programming Interface)** — iki proqram arasında əlaqə qurmaq üçün müəyyən edilmiş qaydalar və protokollar toplusudur. API bir proqramın digər proqramın funksionallığından istifadə etməsinə imkan verir — orijinal kodunu bilmədən.

Gündəlik bir analoji: restoranda siz menyudan seçim edirsiniz (sorğu göndərirsiniz), ofisiant sifarişinizi mətbəxə çatdırır (API), mətbəx yeməyi hazırlayır (server) və ofisiant yeməyi sizə gətirir (cavab). Siz mətbəxin daxili proseslərini bilmirsiniz — yalnız menyunu (API-nin sənədlərini) bilirsiniz.

### 1.2 REST API və HTTP

**REST (Representational State Transfer)** — web API-lərin ən geniş yayılmış arxitektur üslubudur. REST API-lər HTTP protokolu üzərindən işləyir.

**HTTP Metodları:**

| Metod | Təyinat | Analoji | İdempotent? |
|---|---|---|---|
| `GET` | Resurs əldə etmək (oxumaq) | Kitabxanadan kitab almaq | ✅ Bəli |
| `POST` | Yeni resurs yaratmaq | Kitabxanaya yeni kitab əlavə etmək | ❌ Xeyr |
| `PUT` | Resursu tamamilə yeniləmək | Kitabın bütün məlumatlarını dəyişmək | ✅ Bəli |
| `PATCH` | Resursu qismən yeniləmək | Kitabın yalnız adını dəyişmək | ❌ Xeyr |
| `DELETE` | Resursu silmək | Kitabı kitabxanadan silmək | ✅ Bəli |

**HTTP Status Kodları:**

| Kod Aralığı | Kateqoriya | Nümunə |
|---|---|---|
| `2xx` | Uğurlu | `200 OK`, `201 Created`, `204 No Content` |
| `3xx` | Yönləndirmə | `301 Moved Permanently`, `304 Not Modified` |
| `4xx` | Müştəri xətası | `400 Bad Request`, `401 Unauthorized`, `404 Not Found`, `429 Too Many Requests` |
| `5xx` | Server xətası | `500 Internal Server Error`, `503 Service Unavailable` |

### 1.3 `requests` Kitabxanası

`requests` — Python-da HTTP sorğuları göndərmək üçün ən populyar üçüncü tərəf kitabxanasıdır. Standart kitabxanadakı `urllib`-dən qat-qat sadə və istifadəçi dostu interfeys təqdim edir.

```python
import requests

# === GET sorğusu — data almaq ===
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")

# Cavab (Response) obyektinin atributları
print(response.status_code)    # 200 — uğurlu
print(response.ok)             # True (status_code < 400 olduqda)
print(response.headers)        # Cavab başlıqları (dict-ə bənzər)
print(response.text)           # Cavab mətni (string olaraq)
print(response.json())         # JSON cavabı Python dict-ə çevirir

# Status kodunu yoxlamaq
if response.status_code == 200:
    data = response.json()
    print(f"Başlıq: {data['title']}")
elif response.status_code == 404:
    print("Resurs tapılmadı")
else:
    print(f"Xəta: {response.status_code}")

# raise_for_status() — 4xx/5xx status kodlarında exception qaldırır
try:
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    response.raise_for_status()    # Status 200-299 aralığında deyilsə HTTPError qaldırır
    data = response.json()
except requests.exceptions.HTTPError as e:
    print(f"HTTP xətası: {e}")
except requests.exceptions.ConnectionError:
    print("Serverə qoşulmaq mümkün olmadı")
except requests.exceptions.Timeout:
    print("Sorğu vaxt limiti keçdi")
except requests.exceptions.RequestException as e:
    print(f"Ümumi sorğu xətası: {e}")
```

### 1.4 Query Parametrləri və Headers

```python
import requests

# === Query parametrləri — URL-in ?key=value hissəsi ===
params = {
    "userId": 1,             # Müəyyən istifadəçinin postları
    "_limit": 5,             # Maksimum 5 nəticə
    "_sort": "title",        # Başlığa görə sırala
}
response = requests.get(
    "https://jsonplaceholder.typicode.com/posts",
    params=params    # URL: .../posts?userId=1&_limit=5&_sort=title
)
posts = response.json()

# === Headers — Sorğu başlıqları ===
headers = {
    "Accept": "application/json",          # JSON formatında cavab istəyirik
    "User-Agent": "MyApp/1.0",            # Tətbiqin identifikasiyası
    "Authorization": "Bearer TOKEN_HERE",  # Autentifikasiya tokeni
}
response = requests.get(
    "https://api.example.com/data",
    headers=headers
)

# === Timeout — Sorğu vaxt limiti ===
try:
    response = requests.get(
        "https://api.example.com/slow-endpoint",
        timeout=5     # Maksimum 5 saniyə gözlə (connect + read)
    )
except requests.exceptions.Timeout:
    print("Sorğu 5 saniyə ərzində cavab almadı")
```

> [!tip] **Best Practice — Həmişə Timeout Təyin Edin**
> `requests.get()` çağırışında timeout verilməzsə, proqram **sonsuza qədər** cavab gözləyə bilər. Production kodda həmişə `timeout` parametri göstərin. Tuple olaraq da verilə bilər: `timeout=(3, 10)` — 3 saniyə qoşulma, 10 saniyə oxuma limiti.

### 1.5 POST, PUT, DELETE Sorğuları

```python
import requests

# === POST — Yeni resurs yaratmaq ===
new_post = {
    "title": "Python Öyrənmə Günlüyü",
    "body": "Bu gün API-lərlə işləməyi öyrəndim.",
    "userId": 1,
}

response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json=new_post    # Python dict-i avtomatik JSON-a çevirir
)
print(response.status_code)   # 201 — yaradıldı
print(response.json())        # Server tərəfindən qaytarılan data (id daxil)

# === PUT — Resursu tamamilə yeniləmək ===
updated_post = {
    "id": 1,
    "title": "Yenilənmiş Başlıq",
    "body": "Yenilənmiş məzmun",
    "userId": 1,
}
response = requests.put(
    "https://jsonplaceholder.typicode.com/posts/1",
    json=updated_post
)

# === PATCH — Resursu qismən yeniləmək ===
partial_update = {"title": "Yalnız Başlıq Dəyişdi"}
response = requests.patch(
    "https://jsonplaceholder.typicode.com/posts/1",
    json=partial_update
)

# === DELETE — Resursu silmək ===
response = requests.delete("https://jsonplaceholder.typicode.com/posts/1")
print(response.status_code)   # 200 — uğurla silindi
```

### 1.6 Session — Çoxlu Sorğuları Optimallaşdırmaq

```python
import requests

# Session — HTTP bağlantısını təkrar istifadə edir (connection pooling)
# Hər sorğu üçün yeni bağlantı açmaq əvəzinə, eyni bağlantını istifadə edir
session = requests.Session()

# Session-a ortaq headers və auth təyin etmək
session.headers.update({
    "Accept": "application/json",
    "User-Agent": "StudentApp/2.0",
})

# Artıq hər sorğuda headers təkrar yazmağa ehtiyac yoxdur
response_1 = session.get("https://jsonplaceholder.typicode.com/posts/1")
response_2 = session.get("https://jsonplaceholder.typicode.com/posts/2")
response_3 = session.get("https://jsonplaceholder.typicode.com/users/1")

# Session-u bağlamaq (context manager ilə)
with requests.Session() as s:
    s.headers.update({"Authorization": "Bearer my_token"})
    data = s.get("https://api.example.com/data").json()
```

### 1.7 Praktik Nümunə: Hava Məlumatı Əldə Etmə

```python
import requests
import json
from pathlib import Path

def fetch_weather(city, api_key):
    """
    Verilmiş şəhər üçün hava məlumatını əldə edir.

    Args:
        city: Şəhər adı
        api_key: OpenWeatherMap API açarı

    Returns:
        dict: Hava məlumatı və ya None (xəta baş verdikdə)
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",       # Celsius
        "lang": "az",            # Azərbaycan dili
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print(f"Şəhər tapılmadı: {city}")
        elif response.status_code == 401:
            print("Etibarsız API açarı")
        else:
            print(f"HTTP xətası: {e}")
    except requests.exceptions.ConnectionError:
        print("İnternet bağlantısı yoxdur")
    except requests.exceptions.Timeout:
        print("Sorğu vaxt limiti keçdi")

    return None


def save_weather_report(data, filepath):
    """Hava məlumatını JSON faylda saxlayır."""
    if data is None:
        return

    report = {
        "city": data.get("name", "Naməlum"),
        "temperature": data.get("main", {}).get("temp"),
        "feels_like": data.get("main", {}).get("feels_like"),
        "humidity": data.get("main", {}).get("humidity"),
        "description": data.get("weather", [{}])[0].get("description", ""),
        "wind_speed": data.get("wind", {}).get("speed"),
    }

    Path(filepath).write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"Hesabat saxlanıldı: {filepath}")
```

---

## 2. Web Scraping

### 2.1 Web Scraping Nədir?

**Web scraping** — veb səhifələrdən strukturlaşdırılmış data çıxarma prosesidir. API mövcud olmadıqda və ya API-nin təqdim etdiyi data kifayət etmədikdə istifadə olunur.

Proses sadə şəkildə belədir:
1. HTTP sorğusu ilə səhifənin HTML kodunu almaq
2. HTML-i parse etmək (strukturlaşdırılmış ağac formasına çevirmək)
3. Lazımi məlumatları çıxarmaq (extract)
4. Məlumatları saxlamaq (fayla, verilənlər bazasına)

### 2.2 Etik və Hüquqi Qaydalar

> [!warning] **Vacib — Web Scraping Etikası**
> Web scraping güclü alətdir, lakin etik və hüquqi qaydaları bilmək lazımdır:
> 1. **`robots.txt` faylını yoxlayın** — Sayt hansı hissələrin scrape edilə biləcəyini bu faylda göstərir
> 2. **Rate limiting tətbiq edin** — Sorğular arasında gecikmə qoyun, serveri yükləməyin
> 3. **İstifadə şərtlərini oxuyun** — Bəzi saytlar scraping-i qadağan edir
> 4. **Şəxsi məlumatları toplamayın** — GDPR və digər qanunlara riayət edin
> 5. **API mövcuddursa, API istifadə edin** — Scraping son vasitə olmalıdır

### 2.3 `BeautifulSoup` ilə HTML Parsing

**BeautifulSoup** — HTML/XML sənədlərini parse etmək üçün ən populyar Python kitabxanasıdır. O, HTML-i ağac strukturuna (DOM — Document Object Model) çevirir və elementlərə müxtəlif üsullarla müraciət etməyə imkan verir.

```python
from bs4 import BeautifulSoup

# Nümunə HTML (real səhifə əvəzinə test üçün)
html_content = """
<html>
<head><title>Kitab Mağazası</title></head>
<body>
    <h1 class="title">Ən Çox Satılanlar</h1>
    <div class="book-list">
        <div class="book" id="book-1">
            <h2 class="book-title">Python Proqramlaşdırma</h2>
            <span class="author">Əli Həsənov</span>
            <span class="price">25.99 AZN</span>
            <p class="description">Python dilinin əsaslarından...</p>
        </div>
        <div class="book" id="book-2">
            <h2 class="book-title">Alqoritmlər</h2>
            <span class="author">Vəli Məmmədov</span>
            <span class="price">32.50 AZN</span>
            <p class="description">Əsas alqoritmlər və data...</p>
        </div>
        <div class="book" id="book-3">
            <h2 class="book-title">Verilənlər Bazası</h2>
            <span class="author">Leyla Əliyeva</span>
            <span class="price">28.00 AZN</span>
            <p class="description">SQL və NoSQL verilənlər...</p>
        </div>
    </div>
    <a href="https://example.com/page2">Növbəti Səhifə</a>
</body>
</html>
"""

# BeautifulSoup obyekti yaratmaq
soup = BeautifulSoup(html_content, "html.parser")

# === Element tapmaq ===
# find() — İLK uyğun elementi tapır
title = soup.find("h1")
print(title.text)                       # "Ən Çox Satılanlar"

# find() — atributlara görə axtarış
first_book_title = soup.find("h2", class_="book-title")
print(first_book_title.text)            # "Python Proqramlaşdırma"

# find() — id ilə axtarış
book_2 = soup.find("div", id="book-2")
print(book_2.find("span", class_="author").text)  # "Vəli Məmmədov"

# === Birdən çox element tapmaq ===
# find_all() — BÜTÜN uyğun elementləri list olaraq qaytarır
all_titles = soup.find_all("h2", class_="book-title")
for t in all_titles:
    print(t.text)
# Python Proqramlaşdırma
# Alqoritmlər
# Verilənlər Bazası

# === Linklər (a tag-ları) ===
links = soup.find_all("a")
for link in links:
    href = link.get("href")              # Atribut dəyərini almaq
    text = link.text
    print(f"Mətn: {text}, URL: {href}")

# === CSS Selektorları ilə axtarış ===
# select() — CSS selektoru ilə birdən çox element
prices = soup.select(".book .price")     # .book sinifinin içindəki .price
for price in prices:
    print(price.text)

# select_one() — CSS selektoru ilə ilk element
first_desc = soup.select_one("#book-1 .description")
print(first_desc.text)
```

### 2.4 Strukturlaşdırılmış Data Çıxarma

```python
from bs4 import BeautifulSoup
import csv
import json

def extract_books(html):
    """HTML-dən kitab məlumatlarını strukturlaşdırılmış formada çıxarır."""
    soup = BeautifulSoup(html, "html.parser")
    books = []

    # Hər bir kitab div-ini tapırıq
    for book_div in soup.find_all("div", class_="book"):
        book = {
            "id": book_div.get("id", ""),
            "title": book_div.find("h2", class_="book-title").text.strip(),
            "author": book_div.find("span", class_="author").text.strip(),
            "price": book_div.find("span", class_="price").text.strip(),
            "description": book_div.find("p", class_="description").text.strip(),
        }

        # Qiyməti ədədə çevirmək
        price_text = book["price"].replace("AZN", "").strip()
        try:
            book["price_numeric"] = float(price_text)
        except ValueError:
            book["price_numeric"] = 0.0

        books.append(book)

    return books


def save_books_to_csv(books, filepath):
    """Kitab siyahısını CSV faylda saxlayır."""
    if not books:
        print("Saxlamaq üçün data yoxdur.")
        return

    headers = books[0].keys()
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(books)
    print(f"{len(books)} kitab '{filepath}' faylına saxlanıldı.")


def save_books_to_json(books, filepath):
    """Kitab siyahısını JSON faylda saxlayır."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=2, ensure_ascii=False)
    print(f"{len(books)} kitab '{filepath}' faylına saxlanıldı.")
```

### 2.5 Real Veb Səhifəni Scrape Etmək

```python
import requests
from bs4 import BeautifulSoup
import time

def scrape_with_retry(url, max_retries=3, delay=2):
    """
    Veb səhifəni scrape edir — uğursuz olduqda təkrar cəhd edir.

    Args:
        url: Scrape ediləcək URL
        max_retries: Maksimum cəhd sayı
        delay: Cəhdlər arası gecikmə (saniyə)

    Returns:
        BeautifulSoup obyekti və ya None
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            print(f"Cəhd {attempt}/{max_retries} uğursuz: {e}")
            if attempt < max_retries:
                print(f"{delay} saniyə gözlənilir...")
                time.sleep(delay)
                delay *= 2    # Exponential backoff — hər dəfə gözləmə ikiqat artır

    print("Bütün cəhdlər uğursuz oldu.")
    return None


def scrape_multiple_pages(base_url, page_count, delay_between=1.0):
    """
    Bir neçə səhifəni ardıcıl scrape edir.

    Args:
        base_url: Əsas URL (səhifə nömrəsi üçün {} placeholder)
        page_count: Scrape ediləcək səhifə sayı
        delay_between: Sorğular arası gecikmə (saniyə)

    Returns:
        Bütün səhifələrdən toplanan data-nın siyahısı
    """
    all_data = []
    for page in range(1, page_count + 1):
        url = base_url.format(page)
        print(f"Səhifə {page}/{page_count} scrape edilir: {url}")

        soup = scrape_with_retry(url)
        if soup is None:
            print(f"Səhifə {page} atlayıldı.")
            continue

        # Burada səhifəyə xas parsing kodu olacaq
        # items = soup.find_all("div", class_="item")
        # for item in items:
        #     all_data.append(extract_item(item))

        # Serveri yükləməmək üçün gecikmə
        if page < page_count:
            time.sleep(delay_between)

    print(f"Cəmi {len(all_data)} element toplandı.")
    return all_data
```

> [!tip] **Best Practice — Scraping Performansı**
> 1. **`time.sleep()` istifadə edin** — Hər sorğu arasında ən azı 1-2 saniyə gözləyin
> 2. **Session istifadə edin** — Eyni sayta çoxlu sorğu göndərirsinizsə `requests.Session()` bağlantını təkrar istifadə edir
> 3. **Nəticələri cache-ləyin** — Eyni səhifəni təkrar yükləmək əvəzinə yerli faylda saxlayın
> 4. **robots.txt yoxlayın** — `urllib.robotparser` modulu bunu avtomatik yoxlaya bilər

### 2.6 `requests` vs `BeautifulSoup` — Rollarının Fərqi

| Alət | Rol | Nə Edir | Nə Etmir |
|---|---|---|---|
| **`requests`** | HTTP müştəri | Sorğu göndərir, cavab alır | HTML parse etmir |
| **`BeautifulSoup`** | HTML parser | HTML-i parse edir, element tapır | HTTP sorğusu göndərmir |

Bu iki alət birlikdə işləyir: `requests` veb səhifənin HTML kodunu alır, `BeautifulSoup` isə həmin HTML-i parse edərək lazımi məlumatları çıxarır.

---

## 3. Gün 3 — Xülasə

| Mövzu | Əsas Nöqtə |
|---|---|
| **API** | Proqramlar arası interfeys; REST API HTTP üzərindən işləyir |
| **HTTP Metodları** | GET (oxumaq), POST (yaratmaq), PUT/PATCH (yeniləmək), DELETE (silmək) |
| **`requests`** | HTTP sorğuları göndərmək; `.json()`, `.status_code`, `.raise_for_status()` |
| **Session** | Çoxlu sorğuları optimallaşdırmaq, ortaq headers/auth |
| **Web Scraping** | Veb səhifələrdən data çıxarma; etik qaydalara riayət |
| **BeautifulSoup** | HTML parsing; `find()`, `find_all()`, `select()` |

---

> [!note] **Növbəti Həftə**
> **Həftə 3, Gün 1**-də Python-un Obyektyönümlü Proqramlaşdırma (OOP) əsaslarını öyrənəcəyik — siniflər, obyektlər, miras alma və polimorfizm.
