# Həftə 3 - Gün 1: Obyektyönümlü Proqramlaşdırmaya Giriş (OOP)

`learning/week_3/Week3_Day1_OOP_Introduction.md`

---

## 1. OOP Nədir?

### 1.1 Konseptual Giriş

**Obyektyönümlü Proqramlaşdırma (Object-Oriented Programming, OOP)** — proqramı **obyektlər** ətrafında strukturlaşdıran proqramlaşdırma paradiqmasıdır. Prosedural proqramlaşdırmada kod funksiyalar və ardıcıl addımlar ətrafında qurulur; OOP-da isə kod **data (atributlar)** və **davranış (metodlar)** birlikdə qruplaşdırılmış obyektlər ətrafında qurulur.

OOP-un dörd əsas prinsipi:

| Prinsip | Tərif | Analoji (Dune kainatından) |
|---|---|---|
| **Encapsulation** | Data və davranışı bir yerdə saxlamaq, daxili detalları gizlətmək | Fremen qəbiləsinin su ehtiyatlarının idarəsi — xaricdəkilər ehtiyatın həcmini bilmir |
| **Inheritance** | Bir sinifin digərindən xüsusiyyətlər miras alması | House Atreides House-dan miras alır — hər Great House-un ümumi xüsusiyyətləri var |
| **Polymorphism** | Eyni interfeysin fərqli davranışlar göstərməsi | `attack()` metodu: Sardaukar əsgəri fərqli, Fremen döyüşçüsü fərqli hücum edir |
| **Abstraction** | Mürəkkəb detalları gizlədib sadə interfeys təqdim etmək | Ornithopter idarəsi — pilot uçuş mexanikasını bilmir, yalnız idarəetmə panelini istifadə edir |

### 1.2 Sinif (Class) və Obyekt (Object) Fərqi

- **Sinif** — obyektlərin yaradılması üçün **şablon** (blueprint)-dur. Hansı atributlar və metodların olacağını müəyyən edir, lakin konkret dəyərlər saxlamır.
- **Obyekt** — sinifin **konkret nümunəsi** (instance)-dir. Şablondakı boşluqlar konkret dəyərlərlə doldurulur.

Analoji: Sinif bir evin plan-çertyojudur — "mətbəx olacaq, 3 otaq olacaq" deyir, amma konkret ev deyil. Obyekt isə həmin plana əsasən tikilmiş **konkret** evdir.

---

## 2. Sinif Təyini və Obyekt Yaratma

### 2.1 Sadə Sinif

```python
class GreatHouse:
    """
    Dune kainatındakı Böyük Evləri (Great Houses) təmsil edən sinif.

    Hər bir GreatHouse obyekti bir aristokrat ailəni təmsil edir —
    adı, planeti, hərbi gücü və xəzinəsi ilə.
    """

    def __init__(self, name, planet, military_strength, treasury):
        """
        Sinifin konstruktoru — hər yeni obyekt yaradıldıqda avtomatik çağırılır.

        __init__ — "initialize" (başlatmaq) deməkdir. Bu metod obyektin
        başlanğıc vəziyyətini (initial state) təyin edir.

        Args:
            name: Evin adı (məs. "Atreides")
            planet: Nəzarət etdiyi planet (məs. "Caladan")
            military_strength: Hərbi güc (əsgər sayı)
            treasury: Xəzinə (Solari valyutası ilə)
        """
        # 'self' — yaradılan konkret obyektə istinad edir
        # self olmadan atributlar obyektə bağlanmaz, lokal dəyişən olar
        self.name = name
        self.planet = planet
        self.military_strength = military_strength
        self.treasury = treasury
        self.allies = []           # Başlanğıcda müttəfiq yoxdur
        self.is_active = True      # Ev aktivdir

    def recruit_soldiers(self, count):
        """Əsgər toplamaq — xəzinədən xərc çıxarır."""
        cost_per_soldier = 100     # Hər əsgər 100 Solari
        total_cost = count * cost_per_soldier

        if total_cost > self.treasury:
            affordable = self.treasury // cost_per_soldier
            print(f"{self.name}: Xəzinə kifayət etmir. "
                  f"Yalnız {affordable} əsgər toplana bilər.")
            return

        self.military_strength += count
        self.treasury -= total_cost
        print(f"{self.name}: {count} yeni əsgər toplandı. "
              f"Cəmi güc: {self.military_strength}")

    def form_alliance(self, other_house):
        """Başqa bir Ev ilə ittifaq qurmaq."""
        if other_house.name in self.allies:
            print(f"{self.name} artıq {other_house.name} ilə müttəfiqdir.")
            return

        self.allies.append(other_house.name)
        other_house.allies.append(self.name)
        print(f"İttifaq quruldu: {self.name} ↔ {other_house.name}")

    def get_status(self):
        """Evin cari vəziyyətini qaytarır."""
        return (
            f"House {self.name}\n"
            f"  Planet: {self.planet}\n"
            f"  Hərbi güc: {self.military_strength:,} əsgər\n"
            f"  Xəzinə: {self.treasury:,} Solari\n"
            f"  Müttəfiqlər: {', '.join(self.allies) if self.allies else 'Yoxdur'}\n"
            f"  Status: {'Aktiv' if self.is_active else 'Deaktiv'}"
        )


# === Obyekt yaratmaq (Instantiation) ===
atreides = GreatHouse("Atreides", "Caladan", 5000, 1_000_000)
harkonnen = GreatHouse("Harkonnen", "Giedi Prime", 12000, 3_000_000)
fremen = GreatHouse("Fremen", "Arrakis", 8000, 200_000)

# === Metodları çağırmaq ===
atreides.recruit_soldiers(2000)
# Atreides: 2000 yeni əsgər toplandı. Cəmi güc: 7000

atreides.form_alliance(fremen)
# İttifaq quruldu: Atreides ↔ Fremen

# === Atributlara müraciət ===
print(atreides.name)                  # "Atreides"
print(atreides.military_strength)     # 7000
print(atreides.allies)                # ['Fremen']

# === Status hesabatı ===
print(atreides.get_status())
```

### 2.2 `self` Nədir?

`self` — sinif metodlarının **birinci parametri**dir və Python tərəfindən **avtomatik ötürülür**. O, həmin metodu çağıran **konkret obyektə** istinad edir.

```python
class SpiceHarvester:
    def __init__(self, harvester_id, capacity):
        # self.harvester_id — BU KONKRETobiçektin atributu olur
        self.harvester_id = harvester_id
        self.capacity = capacity
        self.collected = 0

    def harvest(self, amount):
        # 'self' burada hansı harvester-in harvest etdiyini müəyyən edir
        if self.collected + amount > self.capacity:
            amount = self.capacity - self.collected
        self.collected += amount
        return amount

# İki fərqli obyekt — hər birinin öz 'self'-i var
harvester_1 = SpiceHarvester("H-001", 500)
harvester_2 = SpiceHarvester("H-002", 300)

harvester_1.harvest(200)  # self = harvester_1 — yalnız H-001-in collected-i dəyişir
harvester_2.harvest(100)  # self = harvester_2 — yalnız H-002-nin collected-i dəyişir

print(harvester_1.collected)  # 200
print(harvester_2.collected)  # 100
# Hər biri müstəqildir!
```

### 2.3 `__str__` və `__repr__` — Obyektin String Təmsili

```python
class Planet:
    """Dune kainatındakı planetləri təmsil edir."""

    def __init__(self, name, climate, population, primary_resource):
        self.name = name
        self.climate = climate
        self.population = population
        self.primary_resource = primary_resource

    def __str__(self):
        """
        İnsan üçün oxunaqlı string təmsili.
        print() və str() çağırıldıqda istifadə olunur.
        """
        return (f"Planet {self.name} — {self.climate} iqlim, "
                f"əhali: {self.population:,}, resurs: {self.primary_resource}")

    def __repr__(self):
        """
        Developer üçün texniki string təmsili.
        Obyekti təkrar yaratmağa imkan verməlidir (ideal halda).
        REPL-də və debug zamanı göstərilir.
        """
        return (f"Planet(name={self.name!r}, climate={self.climate!r}, "
                f"population={self.population}, "
                f"primary_resource={self.primary_resource!r})")


arrakis = Planet("Arrakis", "Səhra", 10_000_000, "Spice Melange")
caladan = Planet("Caladan", "Okean", 50_000_000, "Balıq")

print(arrakis)       # print() → __str__ çağırılır
# Planet Arrakis — Səhra iqlim, əhali: 10,000,000, resurs: Spice Melange

print(repr(arrakis)) # repr() → __repr__ çağırılır
# Planet(name='Arrakis', climate='Səhra', population=10000000, primary_resource='Spice Melange')

# List içində olduqda __repr__ istifadə olunur
planets = [arrakis, caladan]
print(planets)
# [Planet(name='Arrakis', ...), Planet(name='Caladan', ...)]
```

> [!tip] **Best Practice — `__repr__` Həmişə Təyin Edin**
> Hər sinifə **ən azı** `__repr__` metodu əlavə edin. Bu, debugging zamanı obyektin vəziyyətini görmək üçün əvəzolunmazdır. Əgər `__str__` təyin edilməyibsə, Python `__repr__`-i istifadə edir. `__repr__` idealda `eval(repr(obj)) == obj` olmalıdır — yəni string-dən obyekti bərpa etmək mümkün olmalıdır.

---

## 3. Miras Alma (Inheritance)

### 3.1 Miras Alma Nədir?

**Miras alma** — bir sinifin (child/subclass) başqa bir sinifin (parent/superclass) atribut və metodlarını **miras alması** mexanizmidir. Bu, kodun təkrar yazılmasının qarşısını alır (**DRY prinsipi**) və siniflər arasında **"is-a"** (bir növüdür) əlaqəsi yaradır.

Dune kainatı kontekstində: Sardaukar əsgəri **bir növ** əsgərdir. Fremen döyüşçüsü **bir növ** əsgərdir. Hər ikisi əsgərdir, amma fərqli xüsusiyyətləri var.

### 3.2 Sadə Miras Alma

```python
class Warrior:
    """
    Əsas döyüşçü sinifi — bütün döyüşçü tiplərinin ata sinifi.
    Bütün döyüşçülərin ümumi xüsusiyyətlərini təyin edir.
    """

    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.is_alive = True

    def attack(self, target):
        """Hədəfə hücum edir — zərər verir."""
        if not self.is_alive:
            print(f"{self.name} döyüşə qabil deyil.")
            return 0

        damage = self.attack_power
        target.health -= damage
        if target.health <= 0:
            target.health = 0
            target.is_alive = False
        print(f"{self.name} → {target.name}-ə {damage} zərər verdi. "
              f"({target.name} sağlamlıq: {target.health})")
        return damage

    def heal(self, amount):
        """Sağlamlığı bərpa edir."""
        if not self.is_alive:
            print(f"{self.name} artıq bərpa oluna bilməz.")
            return
        self.health += amount
        print(f"{self.name} {amount} sağlamlıq bərpa etdi. "
              f"Cari: {self.health}")

    def __str__(self):
        status = "Sağ" if self.is_alive else "Həlak"
        return f"{self.name} [HP: {self.health}, ATK: {self.attack_power}, {status}]"


class Sardaukar(Warrior):
    """
    İmperator Sardaukar əsgəri — Warrior sinifindən miras alır.

    Sardaukar-lar güclü silahlanmaya sahibdir, amma uyğunlaşma
    qabiliyyəti aşağıdır.
    """

    def __init__(self, name, health, attack_power, armor_rating):
        # super() — ata sinifin __init__ metodunu çağırır
        # Bu, ata sinifin atributlarını təyin etməmizə imkan verir
        super().__init__(name, health, attack_power)
        self.armor_rating = armor_rating   # Yeni atribut — yalnız Sardaukar-a xas

    def attack(self, target):
        """Override — Sardaukar-ın xüsusi hücum üsulu."""
        if not self.is_alive:
            print(f"{self.name} döyüşə qabil deyil.")
            return 0

        # Sardaukar ağır silahla hücum edir — bonus zərər
        damage = self.attack_power + self.armor_rating // 2
        target.health -= damage
        if target.health <= 0:
            target.health = 0
            target.is_alive = False
        print(f"⚔ Sardaukar {self.name} → {target.name}-ə {damage} ağır zərər verdi!")
        return damage


class Fremen(Warrior):
    """
    Fremen döyüşçüsü — Warrior sinifindən miras alır.

    Fremen-lər crysknife ustasıdır və səhrada görünməz hərəkət edə bilir.
    """

    def __init__(self, name, health, attack_power, stealth_level):
        super().__init__(name, health, attack_power)
        self.stealth_level = stealth_level    # 0-100 arası gizlilik
        self.has_crysknife = True

    def attack(self, target):
        """Override — Fremen-in gizli hücum üsulu."""
        if not self.is_alive:
            print(f"{self.name} döyüşə qabil deyil.")
            return 0

        # Gizlilik bonusu — yüksək stealth daha çox zərər deməkdir
        stealth_bonus = self.stealth_level // 10
        damage = self.attack_power + stealth_bonus
        target.health -= damage
        if target.health <= 0:
            target.health = 0
            target.is_alive = False
        print(f"🗡 Fremen {self.name} gizli hücum etdi → {target.name}-ə {damage} zərər!")
        return damage

    def sandwalk(self):
        """Qum üzərində ritmik yürüyüş — qurd cəlb etmir."""
        print(f"{self.name} rhythmic sandwalk ilə hərəkət edir — "
              f"sandworm-lar cəlb olunmur.")


# === Obyektlər yaratmaq ===
guard = Sardaukar("Kapitan Zheng", health=150, attack_power=40, armor_rating=30)
stilgar = Fremen("Stilgar", health=120, attack_power=35, stealth_level=85)

# === Hər biri öz attack() metodunu istifadə edir (Polymorphism) ===
guard.attack(stilgar)    # ⚔ Sardaukar hücumu
stilgar.attack(guard)    # 🗡 Fremen gizli hücumu

# === Miras alınmış metod (heal) ata sinifindəndir ===
stilgar.heal(20)         # Warrior.heal() — dəyişdirilməyib

# === isinstance() — Obyektin tipini yoxlamaq ===
print(isinstance(stilgar, Fremen))    # True — stilgar Fremen-dir
print(isinstance(stilgar, Warrior))   # True — Fremen Warrior-DAN miras alır
print(isinstance(guard, Fremen))      # False — Sardaukar Fremen deyil
```

### 3.3 `super()` Funksiyası

`super()` — ata sinifə müraciət etmək üçün istifadə olunur. Xüsusilə `__init__` metodunda ata sinifin konstruktorunu çağırmaq üçün lazımdır.

```python
class ImperialSoldier(Sardaukar):
    """
    İmperator Şəxsi Mühafizəçisi — Sardaukar-dan miras alır.
    Üç pilləli iyerarxiya: Warrior → Sardaukar → ImperialSoldier
    """

    def __init__(self, name, health, attack_power, armor_rating, loyalty_level):
        # super() burada Sardaukar.__init__-i çağırır
        # Sardaukar.__init__ isə Warrior.__init__-i çağırır
        # Beləliklə bütün zəncir işləyir
        super().__init__(name, health, attack_power, armor_rating)
        self.loyalty_level = loyalty_level

    def __str__(self):
        base = super().__str__()    # Ata sinifin __str__-ini çağırır
        return f"{base} | Sədaqət: {self.loyalty_level}%"
```

---

## 4. Polimorfizm (Polymorphism)

### 4.1 Polimorfizm Nədir?

**Polimorfizm** — "çox formallıq" deməkdir. Bu, **eyni interfeysin** (metod adı) **fərqli siniflərdə fərqli davranış** göstərməsidir. Bu sayədə, fərqli tipli obyektlərlə **eyni şəkildə** işləyə bilərik — hər bir obyekt öz tipinə uyğun davranır.

```python
# Polimorfizm nümunəsi — fərqli döyüşçülər eyni interfeys
def battle_round(attacker, defender):
    """
    Bir döyüş raundunu icra edir.

    Bu funksiya attacker və defender-in hansı sinifə aid olduğunu BİLMİR.
    Yalnız onların attack() metodu olduğunu bilir.
    Bu, polimorfizmdir.
    """
    print(f"\n--- {attacker.name} vs {defender.name} ---")
    attacker.attack(defender)
    if defender.is_alive:
        defender.attack(attacker)

# Fərqli tipli döyüşçülər
guard = Sardaukar("Sardaukar Alpha", 150, 40, 30)
fighter = Fremen("Chani", 120, 35, 90)
basic = Warrior("Muad", 100, 25)

# Eyni funksiya — fərqli davranışlar
battle_round(guard, fighter)   # Sardaukar.attack() + Fremen.attack()
battle_round(fighter, basic)   # Fremen.attack() + Warrior.attack()

# Siyahıdakı fərqli tipli obyektlər üzərində iterasiya
warriors = [guard, fighter, basic]
target = Warrior("Test Dummy", 500, 0)
for warrior in warriors:
    warrior.attack(target)    # Hər biri öz attack() metodunu çağırır
```

### 4.2 Duck Typing

Python **duck typing** prinsipini izləyir: "Əgər ördək kimi gəzirsə və ördək kimi quğuldayırsa, deməli ördəkdir." Python-da obyektin sinifi deyil, **hansı metodlara sahib olduğu** vacibdir.

```python
class Ornithopter:
    """Dune kainatındakı uçan nəqliyyat vasitəsi."""

    def __init__(self, model, capacity):
        self.model = model
        self.capacity = capacity

    def move(self, destination):
        print(f"Ornithopter {self.model} — {destination}-ə uçur.")

class Sandworm:
    """Arrakis-in nəhəng qum qurdları."""

    def __init__(self, length_meters):
        self.length_meters = length_meters

    def move(self, destination):
        print(f"{self.length_meters}m uzunluğunda Sandworm — "
              f"{destination}-ə qumun altından hərəkət edir.")

class Carryall:
    """Ağır yük daşıyan hava gəmisi."""

    def __init__(self, cargo_tons):
        self.cargo_tons = cargo_tons

    def move(self, destination):
        print(f"Carryall ({self.cargo_tons}t yük) — "
              f"{destination}-ə yükü daşıyır.")


def travel_to(vehicle, destination):
    """
    İstənilən nəqliyyat vasitəsi ilə səyahət.

    Bu funksiya vehicle-in sinifini yoxlamır — yalnız
    move() metodunun olmasını tələb edir (duck typing).
    """
    vehicle.move(destination)


# Fərqli tiplər, eyni interfeys
thopter = Ornithopter("Mark-VII", 6)
worm = Sandworm(400)
carryall = Carryall(50)

travel_to(thopter, "Arrakeen")   # Ornithopter uçur
travel_to(worm, "Sietch Tabr")   # Sandworm qumda hərəkət edir
travel_to(carryall, "Spice field") # Carryall yük daşıyır
```

---

## 5. Encapsulation (Kapsullaşdırma)

### 5.1 Giriş Nəzarəti (Access Control)

Python-da C++ və ya Java-dakı kimi sərt `private`, `protected` açar sözləri yoxdur. Əvəzinə **ad konvensiyaları** istifadə olunur:

| Konvensiya | Format | Məna | Python-un Davranışı |
|---|---|---|---|
| Public | `self.name` | Hər kəs üçün açıqdır | Normal müraciət |
| Protected | `self._name` | "İstifadə etmə" xəbərdarlığı | Normal müraciət (konvensiya) |
| Private | `self.__name` | Sinif daxili istifadə | Name mangling tətbiq olunur |

```python
class SpiceVault:
    """
    Spice saxlama anbarı — encapsulation nümunəsi.

    Anbarın daxili ehtiyatlarına birbaşa müraciət etmək əvəzinə,
    yalnız təyin edilmiş metodlar vasitəsilə idarə olunur.
    """

    def __init__(self, owner, initial_amount):
        self.owner = owner                  # Public — hər kəs görə bilər
        self._location = "Sietch Tabr"     # Protected — daxili istifadə üçün nəzərdə tutulub
        self.__reserve = initial_amount     # Private — xaricdən birbaşa müraciət olunmamalıdır

    def deposit(self, amount):
        """Ehtiyata Spice əlavə etmək — yoxlama ilə."""
        if amount <= 0:
            raise ValueError("Miqdar müsbət olmalıdır")
        self.__reserve += amount
        print(f"{amount} Spice əlavə edildi. Cəmi: {self.__reserve}")

    def withdraw(self, amount):
        """Ehtiyatdan Spice çıxarmaq — yoxlama ilə."""
        if amount <= 0:
            raise ValueError("Miqdar müsbət olmalıdır")
        if amount > self.__reserve:
            raise ValueError(
                f"Kifayət qədər Spice yoxdur. "
                f"İstənilən: {amount}, Mövcud: {self.__reserve}"
            )
        self.__reserve -= amount
        print(f"{amount} Spice çıxarıldı. Qalıq: {self.__reserve}")
        return amount

    def get_balance(self):
        """Ehtiyatın cari miqdarını qaytarır (read-only giriş)."""
        return self.__reserve


vault = SpiceVault("Fremen Council", 10000)

# Public atribut — normal müraciət
print(vault.owner)                   # "Fremen Council"

# Protected atribut — işləyir, amma konvensiyaya görə xaricdən istifadə olunmamalıdır
print(vault._location)               # "Sietch Tabr" (xəbərdarlıq!)

# Private atribut — name mangling: __reserve → _SpiceVault__reserve olur
# print(vault.__reserve)             # AttributeError!
print(vault._SpiceVault__reserve)    # 10000 — texniki olaraq mümkündür, amma etməyin

# Düzgün yol — metodlar vasitəsilə müraciət
vault.deposit(5000)
vault.withdraw(3000)
print(vault.get_balance())           # 12000
```

> [!tip] **Best Practice — Python-da Encapsulation Fəlsəfəsi**
> Python "We are all consenting adults here" (Hamımız yetkin insanlarıq) fəlsəfəsini izləyir. Sərt giriş nəzarəti əvəzinə **konvensiyalara** güvənilir. `_` prefiksi "daxili istifadə üçündür" mesajı verir — bu kifayət etməlidir. `__` prefiksi yalnız ad çakışmalarının qarşısını almaq üçün lazım olduqda istifadə edilməlidir, "gizlətmə" üçün deyil.

---

## 6. Gün 1 — Xülasə

| Mövzu | Əsas Nöqtə |
|---|---|
| **OOP** | Data + davranış = obyekt; 4 prinsip: encapsulation, inheritance, polymorphism, abstraction |
| **Sinif / Obyekt** | Sinif = şablon, Obyekt = sinifin konkret nümunəsi |
| **`__init__`** | Konstruktor — obyektin başlanğıc vəziyyətini təyin edir |
| **`self`** | Cari obyektə istinad; atributları və metodları bağlayır |
| **`__str__`/`__repr__`** | String təmsili — insan üçün / developer üçün |
| **Inheritance** | Alt sinif ata sinifin xüsusiyyətlərini miras alır; `super()` ilə müraciət |
| **Polymorphism** | Eyni interfeys, fərqli davranış; duck typing |
| **Encapsulation** | `_protected`, `__private` konvensiyaları; name mangling |

---

> [!note] **Növbəti Gün**
> **Gün 2**-də OOP-un qabaqcıl konseptlərini öyrənəcəyik — class metodlar, static metodlar, properties, abstract siniflər və composition vs inheritance.
