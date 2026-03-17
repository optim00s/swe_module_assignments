"""
Assignment 3.3 — Debug Detective: Performans Analizi
Week 5, Day 3
"""

import time, random

def slow_search(data, target):
    """Siyahıda axtarış — çox yavaş"""
    for i in range(len(data)):
        for j in range(len(data)):  # BUG: niyə iç-içə loop?
            if data[i] == target:
                return i
    return -1

def slow_remove_duplicates(data):
    """Təkrarları silir — O(n³)"""
    result = []
    for item in data:
        is_dup = False
        for existing in result:
            if item == existing:
                is_dup = True
                break
        if not is_dup:
            result.append(item)
    return result

def slow_sort(data):
    """Bubble sort — O(n²) hətta sıralanmış data üçün"""
    arr = data.copy()
    for i in range(len(arr)):
        for j in range(len(arr) - 1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def slow_aggregate(records):
    """Qruplaşdırma — hər dəfə siyahıdan axtarır"""
    groups = {}
    for record in records:
        key = record["category"]
        if key not in groups:
            groups[key] = {"items": [], "total": 0, "count": 0}
        groups[key]["items"].append(record)
        groups[key]["count"] += 1
        groups[key]["total"] += record["value"]
        # Hər dəfə ən böyüyü tapır — əvəzinə sorted saxlamaq olar
        groups[key]["max"] = max(r["value"] for r in groups[key]["items"])
        groups[key]["min"] = min(r["value"] for r in groups[key]["items"])
    return groups

def slow_string_builder(words):
    """String birləşdirmə — O(n²) yaddaş"""
    result = ""
    for word in words:
        result = result + word + " "  # hər dəfə yeni string yaranır
        result = result.strip()
        result = result + " "
    return result.strip()

# Test data
data = [random.randint(1, 10000) for _ in range(5000)]
records = [{"id": i, "category": random.choice(["A","B","C","D","E"]), "value": random.uniform(10,1000)} for i in range(10000)]
words = [f"word_{i}" for i in range(5000)]
