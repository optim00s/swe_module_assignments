"""
Assignment 3.2 — Funksiya Decorator Dəsti (Decorator Toolkit)
Week 1, Day 3
"""

@timer
@call_counter
@cache_result
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def process_data(data):
    """Datanı emal edib nəticə qaytarır — bilərəkdən yavaş işləyir."""
    import time
    time.sleep(0.5)
    return [x ** 2 for x in data if x % 2 == 0]
