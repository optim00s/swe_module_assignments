# Həftə 5 - Gün 1: Kod Keyfiyyəti — Təmiz Kod və Kod Review

`learning/week_5/Week5_Day1_Code_Quality.md`

---

## 1. Təmiz Kod (Clean Code) Prinsipləri

### 1.1 Niyə Kod Keyfiyyəti Vacibdir?

Kod **bir dəfə yazılır**, amma **dəfələrlə oxunur**. Tədqiqatlar göstərir ki, proqramçılar vaxtlarının **~70%-ni** kodu oxumağa, **~30%-ni** isə yazmağa sərf edir. Buna görə kodun oxunaqlılığı onun işləkliyindən sonra ən vacib xüsusiyyətdir.

**Texniki borc (Technical Debt)** — keyfiyyətli kod yazmaq əvəzinə "sürətli həll" seçdikdə yaranan borc. Hər "sonra düzəldərəm" qərarı bu borcu artırır. Vaxt keçdikcə borc böyüyür, yeni xüsusiyyətlər əlavə etmək getdikcə çətinləşir.

### 1.2 Üç Əsas Prinsip: Readability, Maintainability, Simplicity

| Prinsip | Tərif | Praktik Tətbiq |
|---|---|---|
| **Readability** | Kod oxucu üçün aydın olmalıdır | Mənalı adlar, aydın struktur, az sürpriz |
| **Maintainability** | Kodu dəyişdirmək asan olmalıdır | Modular dizayn, az coupling, testlər |
| **Simplicity** | Ən sadə həll ən yaxşısıdır | KISS prinsipi, lazımsız mürəkkəblikdən qaçmaq |

### 1.3 Mənalı Adlandırma (Naming)

Ad seçimi kodun oxunaqlılığına ən böyük təsir edən faktorlardan biridir. Yaxşı ad əlavə şərhə ehtiyac yaratmır — kod özünü izah edir.

```python
# ❌ Pis adlar — oxucu anlamır nə etdiyini
def calc(d, t):
    return d / t

x = calc(150, 3)
lst = [i for i in range(10) if i % 2 == 0]
tmp = {}

# ✅ Yaxşı adlar — məqsəd aydındır
def calculate_average_speed(distance_km, time_hours):
    """Ortalama sürəti hesablayır (km/saat)."""
    return distance_km / time_hours

average_speed = calculate_average_speed(150, 3)
even_numbers = [num for num in range(10) if num % 2 == 0]
student_scores = {}
```

**Adlandırma Qaydaları:**

| Qayda | Pis | Yaxşı |
|---|---|---|
| Niyyəti ifadə edən ad | `d` | `distance_km` |
| Axtarıla bilən ad | `7` (magic number) | `DAYS_IN_WEEK = 7` |
| Qısaltmalardan qaçmaq | `calc_avg_spd` | `calculate_average_speed` |
| Boolean-lar sual formasında | `flag` | `is_valid`, `has_permission` |
| Siniflər isim, funksiyalar feil | `DataProcess` | `DataProcessor` (sinif), `process_data` (funksiya) |
| Sabitlər UPPER_CASE | `max_retry` | `MAX_RETRY_COUNT` |

> [!tip] **Best Practice — Magic Numbers-dan Qaçının**
> Kodda izahsız rəqəmlər ("magic numbers") istifadə etməyin. Hər rəqəmi adlandırılmış sabit (named constant) edin:
> ```python
> # ❌ Bu 0.07 nədir? Vergi? Faiz?
> total = price * 0.07
>
> # ✅ Sabit ilə — mənası aydındır
> TAX_RATE = 0.07
> total = price * TAX_RATE
> ```

### 1.4 Funksiya Dizaynı

#### Tək Məsuliyyət Prinsipi (Single Responsibility)

Hər funksiya **yalnız bir iş** görməlidir. Əgər funksiyanı təsvir edərkən "və" sözü istifadə edirsinizsə, onu bölün.

```python
# ❌ Bir funksiya çox şey edir
def process_student_data(filepath):
    # Faylı oxuyur VƏ datanı parse edir VƏ hesablayır VƏ fayla yazır
    with open(filepath) as f:
        lines = f.readlines()
    students = []
    for line in lines:
        parts = line.strip().split(",")
        name = parts[0]
        scores = [float(s) for s in parts[1:]]
        avg = sum(scores) / len(scores)
        grade = "A" if avg >= 90 else "B" if avg >= 80 else "C" if avg >= 70 else "F"
        students.append({"name": name, "avg": avg, "grade": grade})
    with open("report.txt", "w") as f:
        for s in students:
            f.write(f"{s['name']}: {s['grade']}\n")
    return students

# ✅ Hər funksiya tək bir iş görür
def read_student_lines(filepath):
    """Fayldan tələbə sətrlərini oxuyur."""
    with open(filepath, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def parse_student(line):
    """Tək sətri tələbə dict-inə çevirir."""
    parts = line.split(",")
    name = parts[0].strip()
    scores = [float(s) for s in parts[1:]]
    return {"name": name, "scores": scores}

def calculate_grade(average):
    """Ortalama bala görə qiymət təyin edir."""
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    return "F"

def write_report(students, filepath):
    """Tələbə hesabatını fayla yazır."""
    with open(filepath, "w", encoding="utf-8") as f:
        for student in students:
            f.write(f"{student['name']}: {student['grade']}\n")
```

#### Funksiya Ölçüsü və Parametr Sayı

```python
# ❌ Çox parametr — funksiya çox şey bilməli olur
def create_report(title, data, format_type, include_header, include_footer,
                  page_size, font_name, font_size, color_scheme,
                  output_path, compress, encrypt):
    pass

# ✅ Parametrləri qruplaşdırmaq — dataclass və ya dict istifadə edin
from dataclasses import dataclass

@dataclass
class ReportConfig:
    format_type: str = "pdf"
    include_header: bool = True
    include_footer: bool = True
    page_size: str = "A4"
    font_name: str = "Arial"
    font_size: int = 12
    color_scheme: str = "default"

def create_report(title, data, config, output_path):
    """Parametr sayı azaldı — 4 əvəzinə 12."""
    pass
```

> [!tip] **Best Practice — Funksiya Qaydaları**
> 1. **Tək məsuliyyət** — bir funksiya bir iş
> 2. **Kiçik ölçü** — ideal: 20 sətirdən az, maksimum: 50 sətir
> 3. **Az parametr** — ideal: 0-2, maksimum: 4-5 (çoxdursa, qruplaşdırın)
> 4. **Abstraction səviyyəsi** — funksiya daxilindəki bütün əməliyyatlar eyni səviyyədə olmalıdır
> 5. **Side effects-dən qaçın** — funksiya ya dəyər qaytarmalı, ya da state dəyişməli; ikisini birlikdə etməməli

### 1.5 DRY, KISS, YAGNI

| Prinsip | Tam Ad | Məna |
|---|---|---|
| **DRY** | Don't Repeat Yourself | Eyni kodu iki yerdə yazmayın |
| **KISS** | Keep It Simple, Stupid | Ən sadə həlli seçin |
| **YAGNI** | You Aren't Gonna Need It | Lazım olmayan xüsusiyyəti əlavə etməyin |

```python
# ❌ DRY pozulub — eyni məntiq təkrarlanır
def get_active_students(students):
    result = []
    for s in students:
        if s["is_active"] and s["score"] >= 50:
            result.append(s)
    return result

def get_active_teachers(teachers):
    result = []
    for t in teachers:
        if t["is_active"] and t["experience"] >= 2:
            result.append(t)
    return result

# ✅ DRY — ümumi filtr funksiyası
def filter_by(items, predicate):
    """İstənilən siyahını verilmiş şərtə görə filtrləyir."""
    return [item for item in items if predicate(item)]

active_students = filter_by(
    students, lambda s: s["is_active"] and s["score"] >= 50
)
active_teachers = filter_by(
    teachers, lambda t: t["is_active"] and t["experience"] >= 2
)
```

### 1.6 SOLID Prinsipləri

**SOLID** — obyektyönümlü dizaynın beş əsas prinsipini təmsil edən akronimdir. Bu prinsiplər kodu **daha elastik**, **daha test edilə bilən** və **daha asan genişləndirilə bilən** edir. Robert C. Martin ("Uncle Bob") tərəfindən populyarlaşdırılıb.

| Hərf | Prinsip | Qısa Tərif |
|---|---|---|
| **S** | Single Responsibility | Sinifin yalnız bir dəyişmə səbəbi olmalıdır |
| **O** | Open/Closed | Genişləndirməyə açıq, dəyişikliyə qapalı |
| **L** | Liskov Substitution | Alt sinif ata sinifin yerinə istifadə oluna bilməlidir |
| **I** | Interface Segregation | Böyük interfeyslər kiçik, xüsusi interfeyslərə bölünməlidir |
| **D** | Dependency Inversion | Yüksək səviyyəli modullar aşağı səviyyəli modullara asılı olmamalıdır |

#### S — Single Responsibility Principle (Tək Məsuliyyət)

**Bir sinifin dəyişmək üçün yalnız bir səbəbi olmalıdır.** Əgər sinif birdən çox məsuliyyət daşıyırsa, bir sahədəki dəyişiklik digər sahəni sındıra bilər.

```python
# ❌ SRP pozulub — bu sinif HƏM data idarəetməsini, HƏM formatlaşdırmanı,
# HƏM də fayla yazmağı edir. Üç fərqli dəyişmə səbəbi var.
class SpiceReport:
    def __init__(self):
        self.records = []

    def add_record(self, region, amount):
        self.records.append({"region": region, "amount": amount})

    def calculate_total(self):
        return sum(r["amount"] for r in self.records)

    def format_as_text(self):
        lines = [f"{r['region']}: {r['amount']} ton" for r in self.records]
        lines.append(f"Cəmi: {self.calculate_total()} ton")
        return "\n".join(lines)

    def save_to_file(self, filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.format_as_text())


# ✅ SRP — hər sinif tək bir məsuliyyət daşıyır
class SpiceInventory:
    """Yalnız Spice ehtiyatlarının data idarəetməsi."""

    def __init__(self):
        self.records = []

    def add_record(self, region, amount):
        self.records.append({"region": region, "amount": amount})

    def calculate_total(self):
        return sum(r["amount"] for r in self.records)

    def get_records(self):
        return list(self.records)


class SpiceReportFormatter:
    """Yalnız formatlaşdırma — data haradan gəlir bilmir."""

    def format_as_text(self, records, total):
        lines = [f"{r['region']}: {r['amount']} ton" for r in records]
        lines.append(f"Cəmi: {total} ton")
        return "\n".join(lines)

    def format_as_csv(self, records, total):
        lines = ["region,amount"]
        lines.extend(f"{r['region']},{r['amount']}" for r in records)
        lines.append(f"TOTAL,{total}")
        return "\n".join(lines)


class FileWriter:
    """Yalnız fayla yazmaq — nəyin yazıldığını bilmir."""

    def write(self, filepath, content):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)


# İstifadə — hər sinif öz işini görür
inventory = SpiceInventory()
inventory.add_record("Arrakeen", 5000)
inventory.add_record("Sietch Tabr", 3200)

formatter = SpiceReportFormatter()
text = formatter.format_as_text(inventory.get_records(), inventory.calculate_total())

writer = FileWriter()
writer.write("spice_report.txt", text)
```

#### O — Open/Closed Principle (Açıq/Qapalı)

**Sinif genişləndirməyə açıq, dəyişikliyə qapalı olmalıdır.** Yeni funksionallıq əlavə etmək üçün mövcud kodu dəyişdirmək lazım olmamalıdır — əvəzinə yeni kod yazmaq kifayət etməlidir.

```python
from abc import ABC, abstractmethod

# ❌ OCP pozulub — yeni endirim tipi əlavə etmək üçün mövcud kodu dəyişmək lazımdır
def calculate_discount_bad(price, customer_type):
    if customer_type == "regular":
        return price * 0.05
    elif customer_type == "premium":
        return price * 0.15
    elif customer_type == "vip":
        return price * 0.25
    # Yeni tip əlavə etmək üçün bu funksiyanı DƏYİŞMƏK lazımdır


# ✅ OCP — yeni endirim tipi əlavə etmək üçün yeni sinif yaratmaq kifayətdir
class DiscountStrategy(ABC):
    """Endirim strategiyasının abstrakt interfeysi."""

    @abstractmethod
    def calculate(self, price):
        pass

class RegularDiscount(DiscountStrategy):
    def calculate(self, price):
        return price * 0.05

class PremiumDiscount(DiscountStrategy):
    def calculate(self, price):
        return price * 0.15

class VIPDiscount(DiscountStrategy):
    def calculate(self, price):
        return price * 0.25

class FremenAllyDiscount(DiscountStrategy):
    """Yeni endirim tipi — heç bir mövcud kodu DƏYİŞMƏDƏN əlavə edildi."""
    def calculate(self, price):
        return price * 0.30


class OrderProcessor:
    """Sifariş emalı — endirim strategiyasını parametr olaraq alır."""

    def process(self, price, discount_strategy):
        discount = discount_strategy.calculate(price)
        final_price = price - discount
        return round(final_price, 2)

# İstifadə
processor = OrderProcessor()
print(processor.process(1000, RegularDiscount()))       # 950.0
print(processor.process(1000, FremenAllyDiscount()))     # 700.0
```

#### L — Liskov Substitution Principle (Liskov Əvəzetmə)

**Alt sinif ata sinifin yerinə istifadə olunduqda proqramın düzgün davranışı pozulmamalıdır.** Yəni, ata sinifi gözləyən hər hansı funksiya alt sinifi qəbul etdikdə də düzgün işləməlidir.

```python
# ❌ LSP pozulub
class Vehicle:
    def __init__(self, fuel_capacity):
        self.fuel_capacity = fuel_capacity
        self.fuel_level = 0

    def refuel(self, amount):
        if amount < 0:
            raise ValueError("Mənfi miqdar ola bilməz")
        self.fuel_level = min(self.fuel_level + amount, self.fuel_capacity)

    def get_range_km(self):
        return self.fuel_level * 10    # Hər litr üçün 10 km


class Bicycle(Vehicle):
    """Velosiped Vehicle-dən miras alır — amma yanacaq məntiqi yoxdur!"""

    def refuel(self, amount):
        # Velosipedin yanacağı yoxdur — ata sinifin davranışı pozulur
        raise NotImplementedError("Velosipedə yanacaq doldurulmur!")

    def get_range_km(self):
        return 50    # Sabit məsafə


def plan_journey(vehicle, distance_km):
    """Bu funksiya HƏR Vehicle üçün işləməlidir."""
    needed_fuel = distance_km / 10
    vehicle.refuel(needed_fuel)          # Bicycle burada XƏTA verəcək!
    return vehicle.get_range_km() >= distance_km


# ✅ LSP — düzgün iyerarxiya
class Transport(ABC):
    """Bütün nəqliyyat vasitələrinin ortaq interfeysi."""

    @abstractmethod
    def get_range_km(self):
        pass

    @abstractmethod
    def prepare_for_journey(self, distance_km):
        """Səyahətə hazırlıq — hər transport öz yolu ilə."""
        pass


class FueledVehicle(Transport):
    """Yanacaqla işləyən nəqliyyat."""

    def __init__(self, fuel_capacity, km_per_liter):
        self.fuel_capacity = fuel_capacity
        self.fuel_level = 0
        self.km_per_liter = km_per_liter

    def refuel(self, amount):
        self.fuel_level = min(self.fuel_level + amount, self.fuel_capacity)

    def get_range_km(self):
        return self.fuel_level * self.km_per_liter

    def prepare_for_journey(self, distance_km):
        needed = distance_km / self.km_per_liter
        self.refuel(needed)


class HumanPowered(Transport):
    """İnsan gücü ilə işləyən nəqliyyat."""

    def __init__(self, max_range_km):
        self.max_range_km = max_range_km

    def get_range_km(self):
        return self.max_range_km

    def prepare_for_journey(self, distance_km):
        if distance_km > self.max_range_km:
            raise ValueError(f"Bu vasitə ilə {distance_km} km mümkün deyil")


# İndi hər ikisi eyni interfeyslə düzgün işləyir
def can_make_journey(transport, distance_km):
    """HƏR Transport alt sinifi üçün düzgün işləyir — LSP qorunur."""
    try:
        transport.prepare_for_journey(distance_km)
        return transport.get_range_km() >= distance_km
    except ValueError:
        return False
```

#### I — Interface Segregation Principle (İnterfeys Ayrılması)

**Müştəri istifadə etmədiyi metodlara asılı olmamalıdır.** Bir böyük, "hər şeyi edən" interfeys əvəzinə, bir neçə kiçik, fokuslanmış interfeys yaradın.

```python
from abc import ABC, abstractmethod

# ❌ ISP pozulub — bir nəhəng interfeys hər şeyi tələb edir
class GuildWorker(ABC):
    @abstractmethod
    def navigate(self): pass

    @abstractmethod
    def fight(self): pass

    @abstractmethod
    def trade(self): pass

    @abstractmethod
    def heal(self): pass

# Navigator yalnız navigate() istifadə edir, amma fight(), trade(), heal()
# metodlarını da implementasiya etməyə MƏCBURDUR — mənasız!


# ✅ ISP — kiçik, fokuslanmış interfeyslər
class Navigable(ABC):
    @abstractmethod
    def navigate(self, destination): pass

class Combatant(ABC):
    @abstractmethod
    def fight(self, target): pass

class Trader(ABC):
    @abstractmethod
    def trade(self, goods, partner): pass

class Healer(ABC):
    @abstractmethod
    def heal(self, patient): pass


class GuildNavigator(Navigable):
    """Navigator yalnız Navigable interfeysinə uyğundur — əlavə yük yoxdur."""
    def navigate(self, destination):
        print(f"Fəzada {destination}-ə naviqasiya edilir...")

class FremenWarrior(Navigable, Combatant):
    """Fremen həm naviqasiya, həm döyüşə qabildir — yalnız lazımi interfeysləri alır."""
    def navigate(self, destination):
        print(f"Səhrada {destination}-ə doğru irəliləyir...")

    def fight(self, target):
        print(f"Crysknife ilə {target}-a hücum!")

class SukDoctor(Healer):
    """Suk həkimi yalnız müalicə edir."""
    def heal(self, patient):
        print(f"{patient} müalicə olunur...")


def send_to_battle(combatant: Combatant):
    """Yalnız döyüşə qabil olanları qəbul edir — Navigator buraya düşməz."""
    combatant.fight("düşmən")
```

#### D — Dependency Inversion Principle (Asılılıq İnversiyası)

**Yüksək səviyyəli modullar aşağı səviyyəli modullara birbaşa asılı olmamalıdır. Hər ikisi abstraksiyalara asılı olmalıdır.** Bu, komponentlər arasındakı bağlılığı (coupling) azaldır və test etməni asanlaşdırır.

```python
from abc import ABC, abstractmethod

# ❌ DIP pozulub — OrderService birbaşa konkret sinifə asılıdır
class MySQLDatabase:
    def save(self, data):
        print(f"MySQL-ə saxlanıldı: {data}")

class OrderServiceBad:
    def __init__(self):
        # Birbaşa konkret sinifə asılılıq — MySQL-i dəyişmək mümkün deyil
        self.db = MySQLDatabase()

    def place_order(self, order):
        self.db.save(order)


# ✅ DIP — abstraksiyaya asılılıq
class DataStore(ABC):
    """Abstraksiya — data saxlama interfeysi."""

    @abstractmethod
    def save(self, data):
        pass

    @abstractmethod
    def find_by_id(self, record_id):
        pass


class SQLiteStore(DataStore):
    """Konkret implementasiya — SQLite."""

    def __init__(self, db_path):
        self.db_path = db_path

    def save(self, data):
        print(f"SQLite-ə saxlanıldı ({self.db_path}): {data}")
        return True

    def find_by_id(self, record_id):
        print(f"SQLite-dən axtarılır: {record_id}")
        return {"id": record_id}


class InMemoryStore(DataStore):
    """Test üçün yaddaş əsaslı saxlama — fayl/DB lazım deyil."""

    def __init__(self):
        self.data = {}
        self._next_id = 1

    def save(self, data):
        self.data[self._next_id] = data
        self._next_id += 1
        return True

    def find_by_id(self, record_id):
        return self.data.get(record_id)


class OrderService:
    """
    Yüksək səviyyəli modul — DataStore abstraksiyasına asılıdır.
    Hansı DB istifadə olunduğunu BİLMİR və bilməməlidir.
    """

    def __init__(self, store: DataStore):
        # Asılılıq xaricdən ötürülür (Dependency Injection)
        self.store = store

    def place_order(self, customer, items):
        order = {"customer": customer, "items": items, "status": "new"}
        self.store.save(order)
        return order


# Production-da SQLite istifadə olunur
service = OrderService(SQLiteStore("orders.db"))
service.place_order("House Atreides", ["spice", "water"])

# Testdə InMemoryStore istifadə olunur — DB lazım deyil!
test_service = OrderService(InMemoryStore())
test_service.place_order("Test Customer", ["item_1"])
```

> [!tip] **Best Practice — SOLID Nə Vaxt Tətbiq Etməli?**
> SOLID prinsipləri **hər yerdə** fanatik şəkildə tətbiq edilməməlidir. Kiçik, sadə skriptlər üçün SOLID artıq mürəkkəblik yarada bilər. Bu prinsiplər əsasən bunlar üçün vacibdir:
> - Uzun müddət davam edəcək layihələr
> - Komanda ilə işlənən layihələr
> - Tez-tez dəyişən tələblər olan sistemlər
> - Test edilməli olan kod
>
> **Qızıl qayda**: Əgər kodu dəyişdirmək və ya test etmək çətinləşirsə — SOLID prinsiplərinə müraciət edin.

---

## 2. Linting və Formatlaşdırma Alətləri

### 2.1 Linter Nədir?

**Linter** — kodu icra etmədən statik analiz edərək potensial xətaları, stil pozuntularını və pis praktikaları aşkar edən alətdir. Kod yazdıqca real vaxtda xəbərdarlıqlar verir.

### 2.2 Əsas Python Alətləri

| Alət | Kateqoriya | Nə Edir |
|---|---|---|
| **Ruff** | Linter + Formatter | Çox sürətli linter və formatter (Rust-da yazılıb) |
| **Flake8** | Linter | PEP 8 yoxlaması, məntiqi xətalar |
| **Pylint** | Linter | Ən hərtərəfli linter, code smells |
| **mypy** | Type checker | Type hint-ləri statik yoxlayır |
| **Black** | Formatter | Kodu avtomatik formatlaşdırır |
| **isort** | Import sorter | Import-ları avtomatik sıralayır |

```bash
# Ruff — müasir, sürətli, hamı-bir-yerdə alət
pip install ruff

# Linting (xətaları tapmaq)
ruff check .
ruff check --fix .          # Avtomatik düzəltmə

# Formatting (kodu formatlaşdırmaq)
ruff format .

# mypy — tip yoxlaması
pip install mypy
mypy src/ --strict          # Sərt rejim
```

### 2.3 Konfiqurasiya — `pyproject.toml`

```toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "N",    # pep8-naming
    "UP",   # pyupgrade
    "B",    # flake8-bugbear
    "SIM",  # flake8-simplify
]

[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

> [!tip] **Best Practice — CI/CD-yə Linter Əlavə Edin**
> Linting-i yalnız lokal istifadə etməyin — CI/CD pipeline-ına əlavə edin ki, linting keçməyən kod merge olunmasın. Bu, bütün komanda üzvlərini eyni standarta riayət etməyə məcbur edir. Ruff + mypy kombinasiyası müasir Python layihələri üçün optimal seçimdir.

---

## 3. Kod Review (Kod Nəzərdən Keçirmə)

### 3.1 Kod Review Nədir?

**Kod review** — yazılmış kodun başqa bir developer tərəfindən nəzərdən keçirilməsi prosesidir. Bu, bug-ların aşkar edilməsi, bilik paylaşılması və kod keyfiyyətinin təmin edilməsi üçün ən effektiv üsullardan biridir.

### 3.2 Nə Yoxlamaq Lazımdır?

| Kateqoriya | Yoxlanacaq Suallar |
|---|---|
| **Düzgünlük** | Kod düzgün işləyir? Edge case-lər nəzərə alınıb? |
| **Dizayn** | Düzgün abstraksiya? Single Responsibility? |
| **Oxunaqlılıq** | Ad seçimi aydındır? Mürəkkəb hissələr şərhlənib? |
| **Sadəlik** | Daha sadə həll varmı? Lazımsız mürəkkəblik var? |
| **Testlər** | Testlər yazılıb? Edge case-lər test edilib? |
| **Performans** | Açıq performans problemi var? (vaxtından əvvəl optimallaşdırmayın!) |
| **Təhlükəsizlik** | SQL injection? Hardcoded sirlər? Input validation? |

### 3.3 Yaxşı Review Verməyin Qaydaları

```markdown
# ❌ Pis review
"Bu kod pisdir, yenidən yaz."
"Niyə belə etdin?"

# ✅ Yaxşı review
"Bu funksiya 50 sətirdən çoxdur — `parse_header()` və `validate_body()`
kimi kiçik funksiyalara bölməyi təklif edirəm. Bu, test yazmağı da
asanlaşdıracaq."

"Burada `dict.get()` əvəzinə `dict[]` istifadə olunub — əgər key
mövcud deyilsə KeyError verəcək. Bu nəzərdə tutulubdur, yoxsa
`get()` ilə default dəyər qaytarmaq daha təhlükəsiz olardı?"
```

**Review qaydaları:**
1. **Koda hücum edin, şəxsə deyil** — "Sən səhv etdin" əvəzinə "Bu hissə daha yaxşı ola bilər"
2. **Konstruktiv olun** — problem göstərəndə həll də təklif edin
3. **Prioritetləşdirin** — hər şeyi eyni anda dəyişdirməyi tələb etməyin
4. **Yaxşı kodu da qeyd edin** — yalnız mənfi deyil, müsbət feedback də verin
5. **Avtomatlaşdırın** — formatter və linter-in edə biləcəyini review-da yazmayın

### 3.4 Self-Review Checklist

Kod review-a göndərməzdən əvvəl özünüzü yoxlayın:

```markdown
- [ ] Kod kompile olunur / icra olunur (xəta yoxdur)
- [ ] Bütün testlər keçir
- [ ] Linter xəbərdarlıqları həll edilib
- [ ] Yeni funksiyalara type hints əlavə edilib
- [ ] Mürəkkəb məntiq şərhlərlə izah edilib
- [ ] Magic number yoxdur (sabitlər adlandırılıb)
- [ ] Edge case-lər (boş input, None, mənfi ədədlər) nəzərə alınıb
- [ ] Hardcoded dəyərlər (URL, parol, açar) konfiqurasiyaya çıxarılıb
- [ ] `print()` debugging izləri silinib
- [ ] Commit mesajı aydın və təsviredicidir
```

---

## 4. Gün 1 — Xülasə

| Mövzu | Əsas Nöqtə |
|---|---|
| **Təmiz kod** | Oxunaqlılıq, qoruma asanlığı, sadəlik |
| **Adlandırma** | Niyyəti ifadə edən, axtarıla bilən, mənalı adlar |
| **Funksiya dizaynı** | Tək məsuliyyət, kiçik ölçü, az parametr |
| **DRY/KISS/YAGNI** | Təkrar etmə, sadə saxla, lazımsız əlavə etmə |
| **SOLID** | SRP, OCP, LSP, ISP, DIP — elastik, genişləndirilə bilən OOP dizaynı |
| **Linting** | Ruff, mypy — avtomatik keyfiyyət yoxlaması |
| **Kod review** | Konstruktiv, koda yönəlik, həll təklif edən |

---

> [!note] **Növbəti Gün**
> **Gün 2**-də unit testing əsaslarını — `unittest`, `pytest` framework-lərini və Test-Driven Development (TDD) metodologiyasını öyrənəcəyik.
