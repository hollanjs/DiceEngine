'''
Potential Additional Properties
[ ] `is_all_frozen`: A read-only property returning True if every Die is frozen.
[ ] `min_roll` and `max_roll`: Quickly provide the lowest and highest current rolled values among all dice.

Potential Additional Methods
[ ] `sort_by_roll(descending: bool = False)`: Sorts dice by their rolled value.
[ ] `remove_dice(count: int = 1)`: Removes a specified number of dice from the container, optionally from the end or beginning.
[ ] `split(condition: Callable[[Die], bool]) -> (Dice, Dice)`: Splits the current dice into two new Dice objects based on a condition.

'''


from dataclasses import dataclass, field
from typing import List, Type, Iterator
import copy

from .die import Die


@dataclass
class Dice:
    """
    A container for handling multiple dice of the same type, along with a roll history.

    Attributes:
        die_type (Type[Die]): The class of the die (e.g., SixSidedDie).
        count (int): The number of dice to instantiate.
        dice (List[Die]): The currently active dice.
        roll_history (List[List[Die]]): A history of all past rolls. Each element is
            a snapshot (list) of dice objects from a single roll.
    """
    die_type: Type[Die]
    count: int
    dice: List[Die] = field(init=False)
    roll_history: List[List[Die]] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """
        Initializes the collection of dice using the provided die_type, 
        then records the initial roll state in roll_history.
        """
        self.dice = [self.die_type() for _ in range(self.count)]
        self.roll_history = [copy.deepcopy(self.dice)]

    @classmethod
    def from_dice_list(cls, dice_list: List[Die]) -> "Dice":
        """
        Creates a Dice object from an existing list of dice. Assumes
        all dice in the list have the same type, taking the first
        die's type as the 'die_type'.

        Args:
            dice_list (List[Die]): A pre-constructed list of Die objects.

        Returns:
            Dice: A new Dice container with those dice.
        """
        if not dice_list:
            raise ValueError("Cannot create Dice from an empty list.")
        first_die_type = type(dice_list[0])
        # (Optional) Verify all dice have the same type as the first.
        # If not, raise an error, or handle differently if mixing is allowed.
        dice_instance = cls(die_type=first_die_type, count=0)
        dice_instance.dice = dice_list[:]  # direct copy
        dice_instance.roll_history = [copy.deepcopy(dice_instance.dice)]
        return dice_instance

    def __str__(self) -> str:
        return self.pprint_str(self.current_roll)

    def __len__(self) -> int:
        return len(self.dice)

    def __iter__(self) -> Iterator[Die]:
        return iter(self.dice)

    @property
    def current_roll(self) -> List[Die]:
        return self.roll_history[-1]

    @property
    def previous_roll(self) -> List[Die]:
        if len(self.roll_history) > 1:
            return self.roll_history[-2]
        else:
            raise IndexError(
                "Not enough roll history to obtain a previous roll."
            )

    @property
    def current_total(self) -> int:
        return sum(self.current_roll)

    @property
    def previous_total(self) -> int:
        return sum(self.previous_roll)

    def roll(self) -> List[int]:
        """
        Rolls all dice in this container, then appends the new
        snapshot to roll_history.

        Returns:
            List[int]: A list of new rolled values.
        """
        for die in self.dice:
            die.roll()
        self.roll_history.append(copy.deepcopy(self.dice))
        return self.current_roll

    def add_dice(self, number: int = 1) -> None:
        """
        Dynamically adds a certain number of new dice of the same
        die_type to this Dice object.

        Args:
            number (int): How many dice to add. Default is 1.
        """
        for _ in range(number):
            self.dice.append(self.die_type())
            self.count += 1

    @staticmethod
    def pprint_str(dice: List[Die]) -> str:
        return f"{len(dice)}{dice[0].name}, [{', '.join(str(d.rolled) for d in dice)}]"
