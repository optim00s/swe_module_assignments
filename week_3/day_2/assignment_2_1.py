"""
Assignment 2.1 — Plugin Sistemi
Week 3, Day 2
"""

pipeline_config = {
    "plugins": [
        {"name": "TextTransform", "version": "1.0", "enabled": True, "priority": 1, "settings": {"operation": "uppercase"}},
        {"name": "Validation", "version": "1.2", "enabled": True, "priority": 2, "settings": {"rules": ["not_empty", "max_length:100"]}},
        {"name": "Math", "version": "2.0", "enabled": False, "priority": 3, "settings": {"precision": 4}},
    ],
    "pipeline_order": ["Validation", "TextTransform"]
}

test_data = [
    {"text": "Hello World", "numbers": [1, 2, 3, 4, 5], "email": "test@example.com"},
    {"text": "", "numbers": [], "email": "invalid-email"},
    {"text": "Python OOP", "numbers": [10, 20, 30], "email": "user@academy.az"},
]
