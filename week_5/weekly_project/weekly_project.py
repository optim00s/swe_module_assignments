# sample_good_code.py — yaxşı yazılmış kod
"""İki nöqtə arasında məsafə hesablayan modul."""
import math
from dataclasses import dataclass

@dataclass
class Point:
    """İki ölçülü koordinat nöqtəsi."""
    x: float
    y: float
    
    def distance_to(self, other: 'Point') -> float:
        """Bu nöqtədən digər nöqtəyə olan məsafəni hesablayır."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
