import math

def prob_on_next(x):
    """
    probability that some number will be rolled on the next move
    """
    return 1-pow(1-((6-abs(7-x))/36), 6)

def prob_repeat(x):
    """
    probability one of the pair of die are the same
    """
    return 1-pow(1-(pow((6-abs(7-x))/36, 2)), 3)

"""
There's a difference between probability you are expected to continue and expect value of next move
Next move is calculated by x/36, since the extra probability is canceled out by the possibility of moving 2 forwards
"""

num_arr = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
steps_arr = [3, 5, 7, 9, 11, 13, 11, 9, 7, 5, 3]
prob_to_end = {}

for i in range(len(num_arr)):
    num = num_arr[i]
    tmp_arr = [0 for i in range(steps_arr[i]+1)]
    tmp_arr[0] = 1
    tmp_arr[1] = prob_on_next(num)

    # RECURSION
    for i in range(2, steps_arr[i]+1):
        prob = prob_on_next(num)
        repeat = prob_repeat(num)
        tmp_arr[i] = repeat*tmp_arr[i-2] + (prob-repeat)*tmp_arr[i-1]

    prob_to_end[num] = tmp_arr[::-1]

#print(prob_to_end)
rounded_dict = {k: [round(x, 2) for x in v] for k, v in prob_to_end.items()}
print(rounded_dict)

chips_list = []
my_chips = [0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0]
their_chips = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def prob_algo(mc, tc, num):
    # mc = my chips, tc = their chips
    prob_arr = prob_to_end[num]
    return prob_arr[mc]/(prob_arr[mc]+prob_arr[tc])*prob_on_next(num)

def comparison(x1, x2, my_chips=my_chips, their_chips=their_chips):
    if x1 == x2:
        if my_chips[x1-2] + 2 >= steps_arr[x1-2]:
            return 2
        else:
            return prob_algo(my_chips[x1-2]+2, their_chips[x1-2], x1)*2
    else:
        if my_chips[x1-2] + 1 >= steps_arr[x1-2] and my_chips[x2-2] + 1 >= steps_arr[x2-2]:
            return 2
        elif my_chips[x1-2] + 1 >= steps_arr[x1-2]:
            return 1+prob_algo(my_chips[x2-2]+1, their_chips[x2-2], x2)
        elif my_chips[x2-2] + 1 >= steps_arr[x2-2]:
            return 1+prob_algo(my_chips[x1-2]+1, their_chips[x1-2], x1)
        else:
            return prob_algo(my_chips[x1-2]+1, their_chips[x1-2], x1) + prob_algo(my_chips[x2-2]+1, their_chips[x2-2], x2)

while True:
    a1, a2 = [int(x) for x in input("Top Dice: ").split()]
    b1, b2 = [int(x) for x in input("Middle Dice: ").split()]
    c1, c2 = [int(x) for x in input("Last Dice: ").split()]
    
    prob_list = [comparison(a1, a2), comparison(b1, b2), comparison(c1, c2)]
    print(prob_list)
    break