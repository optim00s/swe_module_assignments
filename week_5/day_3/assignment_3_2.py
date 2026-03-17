"""
Assignment 3.2 — Logging Framework Qurulması
Week 5, Day 3
"""

test_scenarios = [
    {"level": "DEBUG", "msg": "Cache hit for key: user_123"},
    {"level": "INFO", "msg": "User login successful", "extra": {"user": "eli", "ip": "192.168.1.10"}},
    {"level": "AUDIT", "msg": "Password changed", "extra": {"user": "leyla"}},
    {"level": "WARNING", "msg": "Rate limit approaching", "extra": {"current": 95, "max": 100}},
    {"level": "ERROR", "msg": "Database connection failed", "extra": {"db": "main", "retry": 3}},
    {"level": "CRITICAL", "msg": "System memory exhausted", "extra": {"usage": "98%"}},
]
