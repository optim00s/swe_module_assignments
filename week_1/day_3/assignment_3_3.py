"""
Assignment 3.3 — Data Pipeline (Comprehension + Generator ilə)
Week 1, Day 3
"""

orders = [
    {"id": "ORD-1001", "customer": "Əli", "items": [("Laptop", 2500, 1), ("Siçan", 35, 2)], "city": "Bakı", "status": "delivered", "date": "2026-03-01"},
    {"id": "ORD-1002", "customer": "Leyla", "items": [("Telefon", 1800, 1), ("Qabıq", 25, 1)], "city": "Gəncə", "status": "delivered", "date": "2026-03-02"},
    {"id": "ORD-1003", "customer": "Tural", "items": [("Qulaqlıq", 120, 3), ("Kabel", 10, 5)], "city": "Bakı", "status": "cancelled", "date": "2026-03-02"},
    {"id": "ORD-1004", "customer": "Nigar", "items": [("Monitor", 800, 2), ("Klaviatura", 90, 1)], "city": "Sumqayıt", "status": "delivered", "date": "2026-03-03"},
    {"id": "ORD-1005", "customer": "Rəşad", "items": [("Printer", 450, 1), ("Kağız", 15, 10)], "city": "Bakı", "status": "shipped", "date": "2026-03-03"},
    {"id": "ORD-1006", "customer": "Səbinə", "items": [("Tablet", 650, 1), ("Stylus", 40, 1)], "city": "Lənkəran", "status": "delivered", "date": "2026-03-04"},
    {"id": "ORD-1007", "customer": "Orxan", "items": [("SSD", 95, 2), ("RAM", 70, 4)], "city": "Bakı", "status": "delivered", "date": "2026-03-05"},
    {"id": "ORD-1008", "customer": "Günel", "items": [("Webcam", 75, 1), ("Mikrofon", 110, 1)], "city": "Gəncə", "status": "returned", "date": "2026-03-05"},
    {"id": "ORD-1009", "customer": "Kamran", "items": [("GPU", 1200, 1), ("PSU", 180, 1)], "city": "Bakı", "status": "delivered", "date": "2026-03-06"},
    {"id": "ORD-1010", "customer": "Fidan", "items": [("Router", 85, 1), ("Ethernet Kabel", 8, 3)], "city": "Şəki", "status": "shipped", "date": "2026-03-07"},
    {"id": "ORD-1011", "customer": "Əli", "items": [("USB Hub", 52, 2), ("Adapter", 18, 3)], "city": "Bakı", "status": "delivered", "date": "2026-03-07"},
    {"id": "ORD-1012", "customer": "Leyla", "items": [("Smart Saat", 320, 1)], "city": "Gəncə", "status": "delivered", "date": "2026-03-08"},
]
