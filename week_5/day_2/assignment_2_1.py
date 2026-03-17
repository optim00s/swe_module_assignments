# calculator.py
from datetime import datetime, timedelta
from typing import Union

class Calculator:
    def __init__(self):
        self.history: list[dict] = []
        self.memory: float = 0.0
    
    def add(self, a: float, b: float) -> float:
        result = a + b
        self._record("add", a, b, result)
        return result
    
    def subtract(self, a: float, b: float) -> float:
        result = a - b
        self._record("subtract", a, b, result)
        return result
    
    def multiply(self, a: float, b: float) -> float:
        result = a * b
        self._record("multiply", a, b, result)
        return result
    
    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("Sıfıra bölmək olmaz")
        result = a / b
        self._record("divide", a, b, result)
        return result
    
    def power(self, base: float, exp: float) -> float:
        if base == 0 and exp < 0:
            raise ValueError("Sıfırın mənfi qüvvəti mövcud deyil")
        result = base ** exp
        self._record("power", base, exp, result)
        return result
    
    def percentage(self, value: float, percent: float) -> float:
        result = value * percent / 100
        self._record("percentage", value, percent, result)
        return result
    
    def chain(self, initial: float, *operations: tuple) -> float:
        result = initial
        for op, value in operations:
            method = getattr(self, op, None)
            if method is None:
                raise AttributeError(f"Naməlum əməliyyat: {op}")
            result = method(result, value)
        return result
    
    def store_memory(self, value: float) -> None:
        self.memory = value
    
    def recall_memory(self) -> float:
        return self.memory
    
    def clear_history(self) -> None:
        self.history.clear()
    
    def get_history(self, last_n: int = None) -> list[dict]:
        if last_n:
            return self.history[-last_n:]
        return self.history.copy()
    
    def _record(self, op: str, a: float, b: float, result: float) -> None:
        self.history.append({
            "operation": op, "operand_a": a, "operand_b": b,
            "result": result, "timestamp": datetime.now().isoformat()
        })


class StatisticsCalculator:
    @staticmethod
    def mean(data: list[float]) -> float:
        if not data:
            raise ValueError("Boş siyahı üçün orta hesablana bilməz")
        return sum(data) / len(data)
    
    @staticmethod
    def median(data: list[float]) -> float:
        if not data:
            raise ValueError("Boş siyahı")
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n % 2 == 0:
            return (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
        return sorted_data[n//2]
    
    @staticmethod
    def mode(data: list[float]) -> list[float]:
        if not data:
            raise ValueError("Boş siyahı")
        from collections import Counter
        counts = Counter(data)
        max_count = max(counts.values())
        return sorted([val for val, count in counts.items() if count == max_count])
    
    @staticmethod
    def std_dev(data: list[float]) -> float:
        if len(data) < 2:
            raise ValueError("Minimum 2 element lazımdır")
        mean = sum(data) / len(data)
        variance = sum((x - mean) ** 2 for x in data) / (len(data) - 1)
        return variance ** 0.5
    
    @staticmethod
    def percentile(data: list[float], p: float) -> float:
        if not 0 <= p <= 100:
            raise ValueError("Percentile 0-100 arasında olmalıdır")
        sorted_data = sorted(data)
        index = (p / 100) * (len(sorted_data) - 1)
        lower = int(index)
        upper = lower + 1
        if upper >= len(sorted_data):
            return sorted_data[-1]
        weight = index - lower
        return sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight
