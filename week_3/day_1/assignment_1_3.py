"""
Assignment 1.3 — Bank Hesab Sistemi
Week 3, Day 1
"""

customers_data = [
    {"id": "C-001", "name": "Əli Həsənov", "accounts": [
        {"number": "AZ01-0001", "type": "checking", "balance": 5200.00, "currency": "AZN"},
        {"number": "AZ01-0002", "type": "savings", "balance": 15000.00, "currency": "AZN", "interest_rate": 0.08}
    ]},
    {"id": "C-002", "name": "Leyla Məmmədova", "accounts": [
        {"number": "AZ01-0003", "type": "checking", "balance": 3800.00, "currency": "AZN"},
        {"number": "AZ01-0004", "type": "deposit", "balance": 10000.00, "currency": "USD", "interest_rate": 0.05, "term_months": 12, "start_date": "2026-01-15"}
    ]},
    {"id": "C-003", "name": "Tural Əliyev", "accounts": [
        {"number": "AZ01-0005", "type": "savings", "balance": 800.00, "currency": "AZN", "interest_rate": 0.06}
    ]},
]
