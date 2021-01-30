import math

def prob_on_next(x):
    """
    probability that some number will be rolled on the next move
    """
    return 1-pow(1-((6-abs(7-x))/36), 6)

a1, a2, a3 = [int(x) for x in input("Chips: ").split()]

num = 1-(1-prob_on_next(a1))*(1-prob_on_next(a2))*(1-prob_on_next(a3))
print(f"Expected 50% chance: {math.floor(math.log(0.5)/math.log(num))}")