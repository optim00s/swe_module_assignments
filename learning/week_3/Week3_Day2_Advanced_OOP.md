# Həftə 3 - Gün 2: Qabaqcıl OOP Konseptləri

`learning/week_3/Week3_Day2_Advanced_OOP.md`

---

## 1. Class Metodlar, Static Metodlar və Properties

### 1.1 Metod Tipləri Müqayisəsi

Python-da sinif daxilində üç fərqli metod tipi var. Hər birinin fərqli məqsədi və istifadə sahəsi var:

| Metod Tipi | Dekorator | Birinci Parametr | Nəyə Müraciət Edə Bilir | İstifadə Halı |
|---|---|---|---|---|
| **Instance Method** | (heç nə) | `self` (obyekt) | Obyektin + sinifin atributları | Obyektə xas əməliyyatlar |
| **Class Method** | `@classmethod` | `cls` (sinif) | Yalnız sinifin atributları | Alternativ konstruktorlar, sinif state |
| **Static Method** | `@staticmethod` | (heç nə) | Heç nəyə (müstəqil) | Sinifə məntiqi olaraq aid yardımçı funksiyalar |

### 1.2 Ətraflı Nümunə

```python
class GuildNavigator:
    """
    Dune — Spacing Guild Naviqatorları.

    Naviqatorlar fəzada təhlükəsiz naviqasiya üçün Spice istifadə edir.
    Bu sinif naviqator idarəetməsini modelləşdirir.
    """

    # Sinif atributları — bütün obyektlər üçün ortaqdır
    guild_name = "Spacing Guild"
    total_navigators = 0
    _max_navigators = 200

    def __init__(self, name, rank, spice_reserve):
        """Instance method — hər obyekt üçün fərdi çağırılır."""
        self.name = name
        self.rank = rank
        self.spice_reserve = spice_reserve
        self._mutations = []
        GuildNavigator.total_navigators += 1

    # === Instance Method ===
    def consume_spice(self, amount):
        """
        Instance method — self (konkret obyekt) ilə işləyir.
        Bu naviqatorun fərdi Spice ehtiyatını dəyişdirir.
        """
        if amount > self.spice_reserve:
            print(f"{self.name}: Kifayət qədər Spice yoxdur!")
            return False
        self.spice_reserve -= amount
        self._mutations.append(f"Spice consumption: {amount}")
        print(f"{self.name} — {amount} Spice istifadə etdi. Qalıq: {self.spice_reserve}")
        return True

    # === Class Method ===
    @classmethod
    def from_string(cls, data_string):
        """
        Class method — alternativ konstruktor (factory method).

        'cls' parametri sinifin özünə istinad edir (GuildNavigator).
        Bu, string-dən obyekt yaratmağa imkan verir.
        """
        # "Ad:Rütbə:SpiceEhtiyatı" formatını parse edirik
        parts = data_string.split(":")
        if len(parts) != 3:
            raise ValueError(f"Yanlış format: '{data_string}'. Gözlənilən: 'Ad:Rütbə:Spice'")
        name, rank, spice = parts
        return cls(name.strip(), rank.strip(), int(spice.strip()))

    @classmethod
    def get_guild_status(cls):
        """Class method — sinif səviyyəsindəki dataya müraciət edir."""
        return (f"{cls.guild_name}: "
                f"{cls.total_navigators}/{cls._max_navigators} naviqator")

    # === Static Method ===
    @staticmethod
    def calculate_spice_for_journey(distance_parsecs, cargo_weight):
        """
        Static method — nə self, nə cls istifadə etmir.

        Bu funksiya sinifə məntiqi olaraq aiddir (naviqasiya hesablaması),
        amma sinifin və ya obyektin heç bir atributuna ehtiyacı yoxdur.
        """
        base_consumption = distance_parsecs * 10
        weight_factor = 1 + (cargo_weight / 1000)
        return round(base_consumption * weight_factor, 2)

    def __repr__(self):
        return f"GuildNavigator(name={self.name!r}, rank={self.rank!r}, spice={self.spice_reserve})"


# === Instance method istifadəsi ===
navigator = GuildNavigator("Edric", "Third Stage", 5000)
navigator.consume_spice(500)

# === Class method istifadəsi ===
# Alternativ konstruktor — string-dən obyekt yaratmaq
nav_from_str = GuildNavigator.from_string("Darius : Second Stage : 8000")
print(nav_from_str)   # GuildNavigator(name='Darius', rank='Second Stage', spice=8000)

# Sinif statusu
print(GuildNavigator.get_guild_status())
# Spacing Guild: 2/200 naviqator

# === Static method istifadəsi ===
spice_needed = GuildNavigator.calculate_spice_for_journey(
    distance_parsecs=150,
    cargo_weight=5000
)
print(f"Lazım olan Spice: {spice_needed}")  # 9000.0
```

> [!tip] **Best Practice — Nə Vaxt Hansı Metod?**
> - `self` lazımdırsa → **Instance method**
> - `cls` lazımdırsa (sinifin özünə müraciət) → **`@classmethod`**
> - Heç birinə ehtiyac yoxdursa, amma sinifə məntiqi olaraq aiddir → **`@staticmethod`**
> - Əgər static method sinifə aid deyilsə → adi modul funksiyası yazın

### 1.3 Properties — Nəzarət Olunan Atributlar

`@property` dekoratoru — atributa **method kimi nəzarət** etməyə, amma **atribut kimi istifadə** etməyə imkan verir. Bu, getter/setter pattern-in Pythonic implementasiyasıdır.

```python
class ShieldGenerator:
    """
    Dune — Holtzman qoruyucu qalxan generatoru.

    Qalxanın gücü 0-100% arasında olmalıdır.
    Birbaşa dəyişdirməyə icazə vermək əvəzinə,
    @property ilə nəzarət edirik.
    """

    def __init__(self, model, max_strength=100):
        self.model = model
        self._max_strength = max_strength
        self._current_strength = max_strength     # Protected atribut
        self._is_active = True

    @property
    def strength(self):
        """
        Getter — qalxanın cari gücünü qaytarır.
        Xaricdən shield.strength kimi oxunur (metod çağırışı deyil!).
        """
        return self._current_strength

    @strength.setter
    def strength(self, value):
        """
        Setter — qalxanın gücünü təyin edir (yoxlama ilə).
        Xaricdən shield.strength = 50 kimi yazılır.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Güc ədəd olmalıdır")
        if value < 0:
            value = 0
        if value > self._max_strength:
            value = self._max_strength
        self._current_strength = value

    @strength.deleter
    def strength(self):
        """Deleter — qalxanı deaktiv edir."""
        print(f"Qalxan {self.model} deaktiv edilir...")
        self._current_strength = 0
        self._is_active = False

    @property
    def is_active(self):
        """Read-only property — yalnız oxuna bilər, dəyişdirilə bilməz."""
        return self._is_active

    @property
    def status_display(self):
        """Hesablanmış (computed) property — hər dəfə dinamik hesablanır."""
        if not self._is_active:
            return f"⭕ {self.model}: DEAKTİV"
        bar_length = self._current_strength // 5
        bar = "█" * bar_length + "░" * (20 - bar_length)
        return f"🛡 {self.model}: [{bar}] {self._current_strength}%"


shield = ShieldGenerator("Holtzman Mark-IV")

# Getter — atribut kimi oxuyuruq (mötərizə yoxdur!)
print(shield.strength)        # 100

# Setter — atribut kimi təyin edirik
shield.strength = 75          # Setter avtomatik yoxlama edir
shield.strength = -10         # 0-a çevrilir (minimum)
shield.strength = 200         # 100-ə çevrilir (maximum)

# Computed property
print(shield.status_display)  # 🛡 Holtzman Mark-IV: [████████████████████] 100%

# Read-only property
# shield.is_active = False    # AttributeError — setter yoxdur

# Deleter
del shield.strength            # Qalxanı deaktiv edir
print(shield.status_display)  # ⭕ Holtzman Mark-IV: DEAKTİV
```

---

## 2. Dekoratorlar ilə Siniflər

### 2.1 `@dataclass` — Boilerplate Azaltma (Python 3.7+)

`@dataclass` dekoratoru `__init__`, `__repr__`, `__eq__` və digər xüsusi metodları **avtomatik yaradır**. Bu, əsasən data saxlamaq üçün istifadə olunan siniflərdə çoxlu təkrar kodu aradan qaldırır.

```python
from dataclasses import dataclass, field

# Adi sinif — çox boilerplate
class PlanetManual:
    def __init__(self, name, diameter, population, moons):
        self.name = name
        self.diameter = diameter
        self.population = population
        self.moons = moons

    def __repr__(self):
        return (f"Planet(name={self.name!r}, diameter={self.diameter}, "
                f"population={self.population}, moons={self.moons})")

    def __eq__(self, other):
        if not isinstance(other, PlanetManual):
            return NotImplemented
        return (self.name == other.name and self.diameter == other.diameter
                and self.population == other.population and self.moons == other.moons)


# @dataclass ilə — eyni funksionallıq, çox az kod
@dataclass
class Planet:
    """Dataclass — __init__, __repr__, __eq__ avtomatik yaradılır."""
    name: str
    diameter: int
    population: int
    moons: int = 0                                    # Default dəyər
    resources: list = field(default_factory=list)      # Mutable default üçün field()

arrakis = Planet("Arrakis", 12_104, 10_000_000, 2)
caladan = Planet("Caladan", 13_200, 50_000_000, 1, ["su", "balıq"])

print(arrakis)
# Planet(name='Arrakis', diameter=12104, population=10000000, moons=2, resources=[])

print(arrakis == Planet("Arrakis", 12_104, 10_000_000, 2))  # True — __eq__ avtomatik


# Frozen dataclass — immutable (dəyişilməz)
@dataclass(frozen=True)
class Coordinates:
    """Dəyişilməz koordinatlar — yaradıldıqdan sonra dəyişdirilə bilməz."""
    latitude: float
    longitude: float

point = Coordinates(41.0082, 28.9784)
# point.latitude = 0  # FrozenInstanceError!
```

> [!tip] **Best Practice — `@dataclass` vs `NamedTuple` vs Adi Sinif**
> - **`@dataclass`**: Mutable data konteyneri, default dəyərlər, metodlar əlavə etmək lazımdırsa
> - **`NamedTuple`**: Immutable, çox yüngül, sadə data qrupu
> - **Adi sinif**: Mürəkkəb davranış məntiqi, custom `__init__`, xüsusi meta-proqramlaşdırma lazımdırsa

---

## 3. Miras Alma vs Kompozisiya

### 3.1 "Is-a" vs "Has-a"

Bu, OOP dizaynında ən vacib qərarlardan biridir:
- **Miras alma (Inheritance)** → **"Is-a"** əlaqəsi — "X bir növ Y-dir"
- **Kompozisiya (Composition)** → **"Has-a"** əlaqəsi — "X-in Y-si var"

| Xüsusiyyət | Inheritance | Composition |
|---|---|---|
| **Əlaqə** | "Is-a" (bir növüdür) | "Has-a" (sahib olduğu) |
| **Coupling** | Sıx bağlılıq (tight coupling) | Zəif bağlılıq (loose coupling) |
| **Elastiklik** | Statik — compile-time | Dinamik — runtime-da dəyişdirilə bilər |
| **Kod təkrarı** | Az (miras alınır) | Bir qədər çox (delegation lazımdır) |
| **Mürəkkəblik** | Dərin iyerarxiyalar çətindir | Daha sadə, düz struktur |

### 3.2 Kompozisiya Nümunəsi

```python
class Weapon:
    """Silah komponenti — müstəqil sinif."""

    def __init__(self, name, damage, weapon_type):
        self.name = name
        self.damage = damage
        self.weapon_type = weapon_type

    def strike(self):
        print(f"{self.name} ilə hücum! Zərər: {self.damage}")
        return self.damage

    def __repr__(self):
        return f"Weapon({self.name!r}, damage={self.damage})"


class Armor:
    """Zireh komponenti — müstəqil sinif."""

    def __init__(self, name, defense, weight):
        self.name = name
        self.defense = defense
        self.weight = weight

    def absorb_damage(self, incoming):
        absorbed = min(incoming, self.defense)
        actual = incoming - absorbed
        print(f"{self.name} zirehı {absorbed} zərər uddu. Keçən: {actual}")
        return actual

    def __repr__(self):
        return f"Armor({self.name!r}, defense={self.defense})"


class DuneCharacter:
    """
    Dune personajı — Composition ilə qurulub.

    Personaj "bir növ silah" DEYİL (inheritance yanlış olardı).
    Personajın silahı və zirehı VAR (composition düzgündür).
    """

    def __init__(self, name, health):
        self.name = name
        self.health = health
        self.weapon = None       # Has-a: Silahı ola da bilər, olmaya da
        self.armor = None        # Has-a: Zirehı ola da bilər, olmaya da

    def equip_weapon(self, weapon):
        """Silah təchiz etmək — runtime-da dəyişdirilə bilər."""
        self.weapon = weapon
        print(f"{self.name} — {weapon.name} silahını götürdü.")

    def equip_armor(self, armor):
        """Zireh geyinmək."""
        self.armor = armor
        print(f"{self.name} — {armor.name} zirehini geyindi.")

    def attack(self, target):
        """Hücum — silah varsa istifadə edir, yoxdursa əl ilə."""
        if self.weapon:
            damage = self.weapon.strike()
        else:
            damage = 5
            print(f"{self.name} yumruqla hücum etdi! Zərər: {damage}")

        target.receive_damage(damage)

    def receive_damage(self, amount):
        """Zərər almaq — zireh varsa zərəri azaldır."""
        if self.armor:
            amount = self.armor.absorb_damage(amount)
        self.health -= amount
        print(f"{self.name} — {amount} zərər aldı. Sağlamlıq: {self.health}")


# Komponentlər yaratmaq
crysknife = Weapon("Crysknife", 45, "melee")
lasgun = Weapon("Lasgun", 80, "ranged")
stilsuit_armor = Armor("Stilsuit Armor", 20, 5)
sardaukar_plate = Armor("Sardaukar Plate", 40, 15)

# Personajlar yaratmaq
paul = DuneCharacter("Paul Atreides", 120)
feyd = DuneCharacter("Feyd-Rautha", 130)

# Runtime-da silah/zireh dəyişdirmək (Composition-un elastikliyi)
paul.equip_weapon(crysknife)       # Əvvəlcə crysknife
paul.equip_armor(stilsuit_armor)

feyd.equip_weapon(lasgun)
feyd.equip_armor(sardaukar_plate)

# Döyüş
paul.attack(feyd)
feyd.attack(paul)

# Paul silah dəyişdirir — runtime-da mümkündür!
paul.equip_weapon(lasgun)          # İndi lasgun ilə
paul.attack(feyd)
```

> [!tip] **Best Practice — "Favour Composition over Inheritance"**
> Bu, OOP dizaynının ən vacib prinsiplərindən biridir. Inheritance yalnız həqiqətən "is-a" əlaqəsi olduqda istifadə edin. Əgər şübhəniz varsa — composition seçin. Dərin inheritance iyerarxiyaları (3+ səviyyə) demək olar ki, həmişə pis dizayn əlamətidir. Composition daha elastik, test edilməsi asan və refactor edilməsi rahat kod yaradır.

---

## 4. Abstrakt Siniflər (Abstract Base Classes)

### 4.1 Abstrakt Sinif Nədir?

**Abstrakt sinif** — birbaşa obyekt yaradıla bilməyən, yalnız **interfeys** (şablon) təmin edən sinifdir. Alt siniflər **məcburi olaraq** müəyyən metodları implementasiya etməlidir. Bu, polimorfizmin formal təminatıdır.

```python
from abc import ABC, abstractmethod

class Transport(ABC):
    """
    Abstrakt sinif — bütün nəqliyyat vasitələrinin interfeysi.

    Bu sinifdən birbaşa obyekt yaratmaq mümkün DEYİL.
    Alt siniflər move() və fuel_cost() metodlarını
    MÜTLƏQimplementasiya etməlidir.
    """

    def __init__(self, name, speed):
        self.name = name
        self.speed = speed

    @abstractmethod
    def move(self, destination):
        """Alt sinif bu metodu MÜTLƏQ implementasiya etməlidir."""
        pass

    @abstractmethod
    def fuel_cost(self, distance):
        """Yanacaq xərcini hesablayır — alt sinif implementasiya etməlidir."""
        pass

    # Konkret (non-abstract) metod — alt siniflər miras alır
    def get_info(self):
        """Bu metod artıq implementasiya olunub — override etmək məcburi deyil."""
        return f"{self.name} — Sürət: {self.speed} km/s"


class Frigate(Transport):
    """Fəza freqatı — Transport interfeyisini implementasiya edir."""

    def __init__(self, name, speed, crew_size):
        super().__init__(name, speed)
        self.crew_size = crew_size

    def move(self, destination):
        print(f"Freqat {self.name} — {destination}-ə fəzadan hərəkət edir.")

    def fuel_cost(self, distance):
        return distance * 0.5 * self.crew_size


class Sandcrawler(Transport):
    """Qum tankı — Arrakis-in səthində hərəkət edir."""

    def __init__(self, name, speed, cargo_capacity):
        super().__init__(name, speed)
        self.cargo_capacity = cargo_capacity

    def move(self, destination):
        print(f"Sandcrawler {self.name} — {destination}-ə qum üzərində hərəkət edir.")

    def fuel_cost(self, distance):
        return distance * 2.0 + self.cargo_capacity * 0.1


# Transport() yaratmaq mümkün deyil — abstrakt sinifdir
# transport = Transport("Test", 100)  # TypeError: Can't instantiate abstract class

# Alt siniflər yaradıla bilər
frigate = Frigate("Heighliner", 9999, 200)
crawler = Sandcrawler("Crawler-7", 30, 500)

# Polimorfik istifadə
vehicles = [frigate, crawler]
for v in vehicles:
    v.move("Arrakeen")
    cost = v.fuel_cost(100)
    print(f"  Yanacaq xərci: {cost}")
```

---

## 5. Dunder (Magic) Metodlar

### 5.1 Nədir?

**Dunder metodlar** (double underscore — `__metod__`) — Python-un xüsusi metodlarıdır. Onlar operatorların, daxili funksiyaların və protokolların davranışını təyin edir.

```python
class SpiceReserve:
    """
    Spice ehtiyatı — arifmetik operatorlarla işləyə bilən sinif.

    Dunder metodlar vasitəsilə +, -, >, <, len() və s.
    operatorları təyin edirik.
    """

    def __init__(self, amount, purity=0.95):
        self.amount = amount
        self.purity = purity

    # === Arifmetik operatorlar ===
    def __add__(self, other):
        """self + other → Yeni SpiceReserve qaytarır."""
        if isinstance(other, SpiceReserve):
            new_amount = self.amount + other.amount
            # Ortalama saflıq
            avg_purity = (self.purity * self.amount + other.purity * other.amount) / new_amount
            return SpiceReserve(new_amount, round(avg_purity, 4))
        if isinstance(other, (int, float)):
            return SpiceReserve(self.amount + other, self.purity)
        return NotImplemented

    def __sub__(self, other):
        """self - other"""
        if isinstance(other, (int, float)):
            return SpiceReserve(max(0, self.amount - other), self.purity)
        return NotImplemented

    # === Müqayisə operatorları ===
    def __eq__(self, other):
        """self == other"""
        if isinstance(other, SpiceReserve):
            return self.amount == other.amount
        return NotImplemented

    def __lt__(self, other):
        """self < other"""
        if isinstance(other, SpiceReserve):
            return self.amount < other.amount
        return NotImplemented

    def __le__(self, other):
        """self <= other"""
        if isinstance(other, SpiceReserve):
            return self.amount <= other.amount
        return NotImplemented

    # === Daxili funksiyalar ===
    def __len__(self):
        """len(self) — ehtiyatın miqdarını qaytarır."""
        return int(self.amount)

    def __bool__(self):
        """bool(self) — ehtiyat varsa True."""
        return self.amount > 0

    def __repr__(self):
        return f"SpiceReserve(amount={self.amount}, purity={self.purity})"

    # === Kontekst meneceri protokolu ===
    def __enter__(self):
        """with bloku başladıqda."""
        print(f"Spice anbarı açıldı: {self.amount} vahid")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """with bloku bitdikdə (hətta xəta olsa belə)."""
        print(f"Spice anbarı bağlandı. Qalıq: {self.amount}")
        return False


# === İstifadə ===
reserve_a = SpiceReserve(5000, 0.98)
reserve_b = SpiceReserve(3000, 0.92)

# + operatoru → __add__
combined = reserve_a + reserve_b
print(combined)           # SpiceReserve(amount=8000, purity=0.9575)

# Müqayisə
print(reserve_a > reserve_b)   # True
print(reserve_a == SpiceReserve(5000))  # True

# len() və bool()
print(len(reserve_a))     # 5000
print(bool(reserve_a))    # True
print(bool(SpiceReserve(0)))  # False

# Context manager
with SpiceReserve(1000) as vault:
    print(f"İstifadə edilir: {vault.amount}")
# Spice anbarı açıldı: 1000 vahid
# İstifadə edilir: 1000
# Spice anbarı bağlandı. Qalıq: 1000
```

### 5.2 Ən Vacib Dunder Metodlar

| Dunder Metod | Operator/Funksiya | Nümunə |
|---|---|---|
| `__init__` | Konstruktor | `obj = MyClass()` |
| `__str__` | `str()`, `print()` | `print(obj)` |
| `__repr__` | `repr()`, REPL | `repr(obj)` |
| `__len__` | `len()` | `len(obj)` |
| `__bool__` | `bool()`, `if obj:` | `if obj:` |
| `__eq__` | `==` | `a == b` |
| `__lt__` / `__gt__` | `<` / `>` | `a < b` |
| `__add__` / `__sub__` | `+` / `-` | `a + b` |
| `__mul__` | `*` | `a * 3` |
| `__contains__` | `in` | `x in obj` |
| `__getitem__` | `[]` indexing | `obj[0]` |
| `__iter__` / `__next__` | `for x in obj:` | İterasiya |
| `__enter__` / `__exit__` | `with obj:` | Kontekst meneceri |
| `__call__` | `obj()` çağırışı | Obyekti funksiya kimi çağırmaq |
| `__hash__` | `hash()` | Dict key, set element |

---

## 6. Multiple Inheritance (Çoxlu Miras Alma)

Python çoxlu miras almağı dəstəkləyir — bir sinif birdən çox ata sinifin xüsusiyyətlərini miras ala bilər. Lakin bu, **MRO (Method Resolution Order)** və **Diamond Problem** kimi mürəkkəbliklər yaradır.

```python
class HasShield:
    """Mixin — qoruyucu qalxan funksionallığı əlavə edir."""
    def __init__(self, *args, shield_strength=50, **kwargs):
        super().__init__(*args, **kwargs)
        self.shield_strength = shield_strength

    def activate_shield(self):
        print(f"Qalxan aktivləşdirildi! Güc: {self.shield_strength}%")

class HasWeapon:
    """Mixin — silah funksionallığı əlavə edir."""
    def __init__(self, *args, weapon_name="Lasgun", **kwargs):
        super().__init__(*args, **kwargs)
        self.weapon_name = weapon_name

    def fire_weapon(self):
        print(f"{self.weapon_name} atəş açdı!")

class BaseUnit:
    """Əsas hərbi vahid."""
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def __str__(self):
        return f"{self.name} [HP: {self.health}]"

class EliteSoldier(HasShield, HasWeapon, BaseUnit):
    """
    Elit əsgər — üç sinifdən miras alır.
    MRO: EliteSoldier → HasShield → HasWeapon → BaseUnit → object
    """
    def __init__(self, name, health, **kwargs):
        super().__init__(name=name, health=health, **kwargs)


soldier = EliteSoldier("Commander", 200, shield_strength=80, weapon_name="Crysknife")
soldier.activate_shield()   # HasShield-dən
soldier.fire_weapon()       # HasWeapon-dan
print(soldier)              # BaseUnit.__str__-dən

# MRO-nu görmək
print(EliteSoldier.__mro__)
```

> [!warning] **Diqqət — Multiple Inheritance Ehtiyatla**
> Çoxlu miras alma güclü, amma təhlükəli alətdir. **Mixin** pattern-i (kiçik, fokuslanmış əlavə siniflər) istifadə edin. Dərin və geniş inheritance ağaclarından qaçının. Çoxlu inheritance əvəzinə **composition** düşünün.

---

## 7. Gün 2 — Xülasə

| Mövzu | Əsas Nöqtə |
|---|---|
| **Instance/Class/Static** | self (obyekt), cls (sinif), heç biri (müstəqil) |
| **@property** | Atribut kimi istifadə, metod kimi nəzarət; getter/setter/deleter |
| **@dataclass** | Boilerplate azaltma; __init__, __repr__, __eq__ avtomatik |
| **Composition** | "Has-a" əlaqəsi; inheritance-dən üstün tutulmalıdır |
| **Abstract Classes** | İnterfeys təminatı; alt siniflər məcburi implementasiya edir |
| **Dunder Metodlar** | Operatorlar və daxili funksiyaları customizasiya etmək |
| **Multiple Inheritance** | MRO, mixin pattern; ehtiyatla istifadə edin |

---

> [!note] **Növbəti Gün**
> **Gün 3**-də Python-da paralellik (concurrency) əsaslarını — threading və multiprocessing modullarını öyrənəcəyik.
