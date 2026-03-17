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
