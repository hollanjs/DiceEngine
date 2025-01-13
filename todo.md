[ ] add the following to a roll_manager class

```Python
'''
ripped from the dice class - update but maintain logic(?)
'''
def remove_lowest_roll(self) -> None:
    """
    Removes the die with the lowest `rolled` value from the
    current set of dice. Raises ValueError if no dice remain.
    """
    if not self.dice:
        raise ValueError("No dice to remove.")
    lowest_die = min(self.dice, key=lambda d: d.rolled)
    self.dice.remove(lowest_die)
    self.count -= 1

def remove_highest_roll(self) -> None:
    """
    Removes the die with the highest `rolled` value from the
    current set of dice. Raises ValueError if no dice remain.
    """
    if not self.dice:
        raise ValueError("No dice to remove.")
    highest_die = max(self.dice, key=lambda d: d.rolled)
    self.dice.remove(highest_die)
    self.count -= 1
```

<hr/>

[ ] move the following to a print utility class

    [ ] even better, create a render chain-of-command up from die to dice to maybe something more abstract so you can inject a renderer that will render the dice the way you need to

        [ ] create abstract render class to enforce render classes required

```Python
"""
ripped from dice class
"""
@staticmethod
def pprint_dice(dice: List[Die]) -> None:
    print(Dice.pprint_str(dice))

def pprint_roll_history(self) -> None:
    for roll in self.roll_history:
        self.pprint_dice(roll)
```