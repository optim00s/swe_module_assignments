"""
Assignment weekly — Weekly Project
Week 5, Day 3
"""

# sample_bad_code.py — bilərəkdən pis kod
def f(x,y,z):
 if x>0:
  if y>0:
   if z>0:
    return x+y+z
   else:
    return x+y
  else:
   return x
 else:
  return 0

class c:
 def __init__(s,a,b):
  s.a=a;s.b=b
 def m(s):
  import math
  return math.sqrt(s.a**2+s.b**2)

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
