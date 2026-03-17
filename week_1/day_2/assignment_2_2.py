"""
Assignment 2.2 — İnventar İdarəetmə Sistemi
Week 1, Day 2
"""

inventory = {
    "SKU001": {"name": "Mexanik Klaviatura", "price": 89.99, "qty": 45, "category": "Elektronika", "supplier": "TechCo"},
    "SKU002": {"name": "Simsiz Siçan", "price": 34.50, "qty": 120, "category": "Elektronika", "supplier": "TechCo"},
    "SKU003": {"name": "USB-C Hub", "price": 52.00, "qty": 0, "category": "Aksessuar", "supplier": "GadgetPro"},
    "SKU004": {"name": "Monitor Standı", "price": 45.00, "qty": 18, "category": "Aksessuar", "supplier": "OfficePlus"},
    "SKU005": {"name": "Noutbuk Çantası", "price": 29.99, "qty": 200, "category": "Aksessuar", "supplier": "BagWorld"},
    "SKU006": {"name": "Webcam HD", "price": 75.00, "qty": 8, "category": "Elektronika", "supplier": "GadgetPro"},
    "SKU007": {"name": "Qulaqlıq", "price": 120.00, "qty": 32, "category": "Elektronika", "supplier": "AudioMax"},
    "SKU008": {"name": "Elektrik Ştekeri", "price": 12.50, "qty": 500, "category": "Aksessuar", "supplier": "OfficePlus"},
    "SKU009": {"name": "SSD 1TB", "price": 95.00, "qty": 15, "category": "Elektronika", "supplier": "TechCo"},
    "SKU010": {"name": "Ergonomik Kreslo", "price": 350.00, "qty": 5, "category": "Mebel", "supplier": "OfficePlus"}
}

transactions = [
    ("SKU001", "sell", 5),
    ("SKU002", "sell", 30),
    ("SKU003", "restock", 50),
    ("SKU006", "sell", 8),
    ("SKU005", "sell", 15),
    ("SKU009", "restock", 25),
    ("SKU007", "sell", 10),
    ("SKU004", "sell", 3),
    ("SKU001", "restock", 20),
    ("SKU010", "sell", 2),
    ("SKU008", "sell", 100),
    ("SKU003", "sell", 25),
    ("SKU006", "restock", 30),
    ("SKU002", "sell", 50),
]
