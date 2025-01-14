from parameters import INITIAL_RAW_MATERIAL, RAW_PRICE_MULTIPLIER, RAW_MATERIAL_TAX
# from sympy import harmonic
import math
import time

class RawMaterial:

  def __init__(self):
    """Create a new RawMaterial."""
    self.remaining = INITIAL_RAW_MATERIAL

  def cost(self, k):
    """Calculate the cost of taking raw material"""
    if k <= 0:
      return 0
    if not self.has_raw_material(k + 1):
      return float('inf')
    
    euler_mascheroni = 0.57721566490153286060651209008240243104215933593992
    cost = RAW_PRICE_MULTIPLIER * (math.log(self.remaining) - math.log(self.remaining - k)) + RAW_MATERIAL_TAX * k
    return cost
  
  def has_raw_material(self, k):
    """Check if there is raw material available"""
    return self.remaining > k

  def take_raw_material(self, k):
    """Take raw material"""

    if not self.has_raw_material(k):
      return float('inf')
    
    cost = self.cost(k)
    self.remaining -= k

    return cost

  def get_current_cost(self):
    """Calculate the current cost of raw material at the end of the year"""
    return self.cost(1)