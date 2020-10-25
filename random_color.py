import random as rd

def rand_color():
    """
    Generate random HTML color code for visualising each routes in the map

    """
    # There are 16,777,216 different HTML colors, so in python (0 to 16,777,215)
    num = rd.randint(0, 16777215)
    # Transform integer to hex number 
    hex_num = hex(num)
    # Delete '0x' infront of the hexcode (0x is always in first two)
    hex_num = hex_num[2:]
    # The color code starts with '#' 
    hex_num = '#'+ hex_num

    return hex_num

# hexdd = rand_color()
# print(hexdd)
# hexde = rand_color()
# print(hexde)
# hexdf = rand_color()
# print(hexdf)