from parser import Parser

"""
INPUT:
    F          -> facilities qty
    C          -> clients qty
    P          -> qty of facilities to open
    capacity[f]
    fixed_cost[f]
    demand[c]
    dist[c][f]
"""


def main():
    print(Parser.parse_instance("input/input.txt"))


main()