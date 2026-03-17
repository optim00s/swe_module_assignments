"""
Assignment weekly — Weekly Project
Week 3, Day 3
"""

# ===== MƏKANLAR =====
locations_data = {
    "village": {
        "name": "Kölgələr Kəndi",
        "description": "Dağ ətəyində sakit bir kənd. Bazarda tacirlər var, mərkəzdə bulaq axır.",
        "connected": ["forest", "marketplace"],
        "danger_level": 0,
    },
    "marketplace": {
        "name": "Böyük Bazar",
        "description": "Cürbəcür əşyalar satan tacirlər burada toplaşıb.",
        "connected": ["village"],
        "danger_level": 0,
    },
    "forest": {
        "name": "Qaranlıq Meşə",
        "description": "Sıx ağaclar arasında işıq zor keçir. Heyvan səsləri eşidilir.",
        "connected": ["village", "cave", "river"],
        "danger_level": 3,
    },
    "cave": {
        "name": "Əjdaha Mağarası",
        "description": "Qayalıqlar arasında gizlənmiş nəhəng mağara. İçəridən istilik gəlir.",
        "connected": ["forest"],
        "danger_level": 7,
    },
    "river": {
        "name": "Gümüş Çay",
        "description": "Geniş çay sahili. Balıqçılar burada toplaşır.",
        "connected": ["forest", "tower"],
        "danger_level": 2,
    },
    "tower": {
        "name": "Qədim Qüllə",
        "description": "Xarabalığa çevrilmiş qüllə. Ən yuxarıda sirli işıq var.",
        "connected": ["river"],
        "danger_level": 9,
    },
}

# ===== NPC-LƏR =====
npcs_data = {
    "elder": {
        "name": "Ağsaqqal Mirəli",
        "role": "Quest verən",
        "location": "village",
        "personality": "Müdrik, az danışan, sirli. Kəndin tarixini yaxşı bilir. Hər sözün arxasında dərin məna var.",
        "knowledge": "Əjdaha mağarasındakı xəzinə haqqında bilir. Qədim qüllənin sirrini bilir. Kölgələr Kəndinin keçmişi haqqında danışa bilər.",
    },
    "merchant": {
        "name": "Tacir Rüfət",
        "role": "Alver edən",
        "location": "marketplace",
        "personality": "Zarafatcıl, ticarətə həris, amma insaflı. Bəzən maraqlı söhbətlər edir. Əşyalar haqqında detallı məlumat verir.",
        "knowledge": "Bazardakı bütün əşyaların keyfiyyətini bilir. Meşədə nadir bitkilər olduğunu eşidib. Qüllədən gələn işıq haqqında şayiə yayır.",
    },
    "hermit": {
        "name": "Tənha Könül",
        "role": "Müdrik",
        "location": "river",
        "personality": "Sakit, filosofik, təbiətsevər. Metaforlarla danışır. Bəzən cavab əvəzinə sual verir.",
        "knowledge": "Meşədəki heyvanları yaxşı tanıyır. Çayın şəfa verən xüsusiyyətlərini bilir. Qüllədəki işığın qaynağı haqqında fikirlər irəli sürür.",
    },
    "guard": {
        "name": "Keşikçi Anar",
        "role": "Mühafizəçi",
        "location": "forest",
        "personality": "Cəsur, sadiq, az sözlü. Kəndi qorumaq üçün hər şey edər. Döyüş haqqında məsləhət verə bilir.",
        "knowledge": "Meşədəki düşmənlərin yerini bilir. Mağaraya gedən təhlükəsiz yol haqqında məlumatı var. Döyüş taktikalarını öyrədə bilər.",
    },
}

# ===== ƏŞYALAR =====
items_data = {
    "iron_sword": {"name": "Dəmir Qılınc", "type": "weapon", "damage": 15, "price": 120, "durability": 100},
    "steel_shield": {"name": "Polad Qalxan", "type": "armor", "defense": 10, "price": 90, "durability": 80},
    "health_potion": {"name": "Şəfa İksiri", "type": "consumable", "heal": 50, "price": 30, "quantity": 1},
    "mana_potion": {"name": "Mana İksiri", "type": "consumable", "mana_restore": 30, "price": 25, "quantity": 1},
    "fire_scroll": {"name": "Od Tilsimi", "type": "consumable", "damage": 40, "price": 75, "quantity": 1},
    "ancient_map": {"name": "Qədim Xəritə", "type": "quest", "description": "Qüllənin gizli girişini göstərir", "price": 200},
    "dragon_scale": {"name": "Əjdaha Pulcuğu", "type": "material", "description": "Çox nadir, güclü zireh üçün material", "price": 500},
    "crystal_amulet": {"name": "Kristal Talisman", "type": "accessory", "effect": "mana_regen", "bonus": 5, "price": 350},
}

# ===== DÜŞMƏNLƏR =====
enemies_data = {
    "wolf": {"name": "Vəhşi Canavar", "hp": 40, "damage": 8, "defense": 3, "xp": 20, "loot": ["health_potion"]},
    "bandit": {"name": "Yol Kəsən", "hp": 60, "damage": 12, "defense": 5, "xp": 35, "loot": ["health_potion", "iron_sword"]},
    "spider": {"name": "Nəhəng Hörümçək", "hp": 50, "damage": 15, "defense": 2, "xp": 30, "loot": ["mana_potion"]},
    "golem": {"name": "Daş Qolem", "hp": 120, "damage": 20, "defense": 15, "xp": 80, "loot": ["steel_shield", "crystal_amulet"]},
    "dragon": {"name": "Kölgə Əjdahası", "hp": 300, "damage": 35, "defense": 20, "xp": 500, "loot": ["dragon_scale", "fire_scroll", "ancient_map"]},
}

# ===== QUESTLƏR =====
quests_data = [
    {
        "id": "Q-001", "title": "Meşənin Təhlükəsi",
        "giver": "elder", "description": "Meşədən 3 canavar öldür və kəndə qayıt.",
        "objectives": [{"type": "kill", "target": "wolf", "count": 3}],
        "reward": {"xp": 100, "gold": 150, "items": ["health_potion"]},
        "prerequisite": None
    },
    {
        "id": "Q-002", "title": "Tacirin Sifarişi",
        "giver": "merchant", "description": "Meşədən nadir bitki tap və Tacir Rüfətə gətir.",
        "objectives": [{"type": "collect", "target": "rare_herb", "count": 5}],
        "reward": {"xp": 80, "gold": 200, "items": ["mana_potion"]},
        "prerequisite": None
    },
    {
        "id": "Q-003", "title": "Mağara Sirri",
        "giver": "elder", "description": "Mağaraya gir, Daş Qolemi məğlub et, qədim artefaktı tap.",
        "objectives": [{"type": "kill", "target": "golem", "count": 1}, {"type": "collect", "target": "ancient_artifact", "count": 1}],
        "reward": {"xp": 250, "gold": 400, "items": ["crystal_amulet"]},
        "prerequisite": "Q-001"
    },
    {
        "id": "Q-004", "title": "Kölgə Əjdahası",
        "giver": "hermit", "description": "Qüllənin zirvəsinə qalx və Kölgə Əjdahasını məğlub et.",
        "objectives": [{"type": "kill", "target": "dragon", "count": 1}],
        "reward": {"xp": 1000, "gold": 2000, "items": ["dragon_scale"]},
        "prerequisite": "Q-003"
    },
]

class NPCBrain:
    def __init__(self, api_key, model="google/gemma-3-4b-it:free"):
        self.api_key = api_key
        self.conversation_history = []

    def generate_response(self, npc_data, player_message, game_context):
        system_prompt = f"""Sən "{npc_data['name']}" adlı NPC-sən.
        Rolun: {npc_data['role']}
        Şəxsiyyətin: {npc_data['personality']}
        Bildiyin məlumatlar: {npc_data['knowledge']}
        
        Oyunçunun hazırkı vəziyyəti:
        - Səviyyə: {game_context['level']}, HP: {game_context['hp']}/{game_context['max_hp']}
        - Məkan: {game_context['location']}
        - Aktiv questlər: {game_context['active_quests']}
        
        QAYDALAR:
        - Həmişə öz rolunda qal, xarakterindən çıxma
        - Qısa və oyun dünyasına uyğun cavab ver (2-4 cümlə)
        - Lazım gəldikdə quest və ya ipucu ver
        - Azərbaycan dilində cavab ver"""
        # API call...
