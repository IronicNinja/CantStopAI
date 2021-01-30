
a = 2
b = 6
c = 7

def not_x(x):
    return pow(1-((6-abs(7-x))/36), 6)

get_one = 1-(not_x(a)*not_x(b)*not_x(c))
print(get_one)