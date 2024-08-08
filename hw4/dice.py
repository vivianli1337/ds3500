"""
File: dice.py
Description: Demo of DRV by throwing multiple n-sided dice
"""

from drv import DRV


def D(n):
    """ Creates a DRV representing an n-sided die """
    return DRV({x:1/n for x in range(1, n+1)})


def main():
    total = 3 * D(6) + D(4) - D(6) ** D(3)
    print(total)
    total.plot()


if __name__ == '__main__':
    main()

