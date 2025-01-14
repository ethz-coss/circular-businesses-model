import math 
import numpy as np

def quadratic_solver(a, b, c): 

    dis = b * b - 4 * a * c 
    sqrt_val = math.sqrt(abs(dis)) 
    
    # checking condition for discriminant
    if dis >= 0: 
        return (-b + sqrt_val)/(2 * a), (-b - sqrt_val)/(2 * a)
    
    # when discriminant is less than 0
    else:
        return None, None
    
def compare_solutions(sol1, sol2):
    """
    Calculate percent differences between two solutions.
    """
    sol1 = np.array(sol1)
    sol2 = np.array(sol2)
    percent_differences = abs(sol1 - sol2) / abs(sol1) * 100
    differences = sol1 - sol2
    return percent_differences