from dataclasses import dataclass, field
from typing import List, Type
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

    def __iter__(self):
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
            
    def __validate_method_params_freeze_unfreeze(dice: Die | List[Die] | None, all_dice: bool) -> None:
        if dice is None and all_dice is False:
            raise ValueError('No input provided - expected input for dice parameter or all_dice=True')
        if dice is not None and all_dice is True:
            raise ValueError('You cannot input a value for the dice parameter and set all_dice=True')

        if isinstance(dice, Die):
            return
        elif isinstance(dice, list) and all(isinstance(d, Die) for d in dice):
            return
        else:
            non_die_values = [d for d in (dice if isinstance(dice, list) else [dice]) if not isinstance(d, Die)]
            raise ValueError(
                'One or more values passed in for dice '
                'is not a subclass of Die or a list of objects that are subclasses of type Die: '
                f'{", ".join(map(str, non_die_values))}'
            )

    def freeze(self, dice: Die | List[Die] | None = None, all_dice: bool = False) -> None:
        self.__validate_method_params_freeze_unfreeze(dice, all_dice)
        if isinstance(dice, Die):
            pass
        elif isinstance(dice, List) and all([isinstance(_, Die) for _ in dice]):
            pass

    def unfreeze(dice: Die | List[Die] | None = None, all_dice: bool = False) -> None:
        self.__validate_method_params_freeze_unfreeze(dice, all_dice)
        if isinstance(dice, Die):
            pass
        elif isinstance(dice, List) and all([isinstance(_, Die) for _ in dice]):
            pass