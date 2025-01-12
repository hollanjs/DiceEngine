#!/usr/bin/env python3

from DiceEngine import Dice, SixSidedDie

'''
DICE BATTLE
    Players take turns rolling 5d6
    Player with the highest total wins
'''

if __name__ == "__main__":
    Player1 = Dice(SixSidedDie, 5)
    Player2 = Dice(SixSidedDie, 5)

    while (choice := input("Battle? [yes/no, default=yes]: ") or "yes") != "no":
        Player1.roll()
        Player2.roll()
        if Player1.current_total > Player2.current_total:
            print(f"Player 1 wins with a total of {Player1.current_total} ({Player1.__str__()})")
            print(f"Player 2 loses with a total of {Player2.current_total} ({Player2.__str__()})")
        elif Player1.current_total == Player2.current_total:
            print(f"Player 1 ties with Player 2 with a total of {Player1.current_total} ({Player1.__str__()})")
            print(f"Player 2 ties with Player 1 with a total of {Player2.current_total} ({Player2.__str__()})")
        else:
            print(f"Player 2 wins with a total of {Player2.current_total} ({Player2.__str__()})")
            print(f"Player 1 loses with a total of {Player1.current_total} ({Player1.__str__()})")
