"""
Assignment 3.2 — Real-time Məlumat Toplayıcısı
Week 3, Day 3
"""

sources_config = [
    {"id": "stock", "name": "Birja Qiymətləri", "interval": 0.5, "data_gen": lambda: {"symbol": random.choice(["AAPL","GOOGL","MSFT"]), "price": round(random.uniform(100,500),2)}},
    {"id": "weather", "name": "Hava Məlumatı", "interval": 2.0, "data_gen": lambda: {"city": random.choice(["Bakı","Gəncə"]), "temp": round(random.uniform(5,35),1)}},
    {"id": "traffic", "name": "Trafik Sensorları", "interval": 1.0, "data_gen": lambda: {"road": random.choice(["M1","M2","M3"]), "vehicles": random.randint(10,200)}},
    {"id": "social", "name": "Sosial Media", "interval": 0.3, "data_gen": lambda: {"platform": random.choice(["Twitter","Reddit"]), "mentions": random.randint(0,500)}},
]
