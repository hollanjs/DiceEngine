"""
This module defines classes for dice-based rolling mechanics, including a base Die class
and its specific subclasses (e.g., FourSidedDie, SixSidedDie, etc.), as well as a Dice
container class that manages multiple dice and maintains their roll history.

TODO:
[ ] add method to alter roll history by index
[ ] update rollmanager to use dice alter history by index to replace roll histories
    with extra dice (roll with advantage/disadvantage) to reflect roll after
    the extra dice are removed
[ ] add rollmanager method to roll multiple dice objects and return roll totals
    use case: DnD where you need to roll  a weapon with a modifier, ex
        3d6, 2d8
[ ] add functionality for roll manager to work with dice roll history
[ ] read through and update ai generated docstrings where necessary
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Self, List, Type, Union, override
import random
import copy


@dataclass(order=True, frozen=True)
class Die(ABC):
    """
    Represents a generic die, enforcing a minimum interface for dice logic.

    Attributes:
        face_count (int): The number of faces on the die (e.g., 6 for a six-sided die).
        name (str): A computed name, set automatically to 'd<face_count>'.
        rolled (int): The most recent roll result.
    """
    face_count: int = field(compare=False)
    name: str = field(compare=False, init=False)
    rolled: int = field(default=0, compare=True)
    is_frozen: bool = field(default=False, init=False, compare=False)

    @abstractmethod
    def console_print_face(self):
        pass

    def toggle_freeze(self):
        object.__setattr__(self, "is_frozen", not self.is_frozen)

    def __post_init__(self):
        """
        Automatically sets the `name` attribute based on the `face_count`.
        For instance, a die with 6 faces will have `name = 'd6'`.
        """
        object.__setattr__(self, "name", f'd{self.face_count}')

    def __str__(self):
        """
        Returns the name of the die (e.g., 'd6') as a string representation.
        """
        return self.name

    def __add__(self, other) -> int:
        """
        Adds this die's rolled value to another die's rolled value or an integer.

        If other is 0, returns this die's rolled value.
        If other is also a Die, returns sum of rolled values.
        If other is int, returns sum of this die's rolled value and the integer.
        Raises ValueError if `other` is none of the above.
        """
        if other == 0:
            return self.rolled
        elif isinstance(other, self.__class__):
            return self.rolled + other.rolled
        elif isinstance(other, int):
            return self.rolled + other
        else:
            raise ValueError(
                f"unsupported (+) types: '{type(self)}' and '{type(other)}'")

    def __radd__(self, other) -> int:
        """
        Called when using reversed operands with the + operator (e.g., 5 + die).
        Delegates to the regular __add__ method.
        """
        return self.__add__(other)

    def __sub__(self, other) -> int:
        """
        Subtracts another die's rolled value or an integer from this die's rolled value.

        If other is 0, returns this die's rolled value.
        If other is also a Die, returns difference of rolled values.
        If other is int, returns the difference of this die's rolled value and the integer.
        Raises ValueError if `other` is none of the above.
        """
        if other == 0:
            return self.rolled
        elif isinstance(other, self.__class__):
            return self.rolled - other.rolled
        elif isinstance(other, int):
            return self.rolled - other
        else:
            raise ValueError(
                f"unsupported (-) types: '{type(self)}' and '{type(other)}'")

    def __rsub__(self, other) -> int:
        """
        Handles subtraction when the die is on the right side of the - operator (e.g., 5 - die).
        Delegates to the logic in __sub__, but swaps operands appropriately.
        """
        if (other == 0):
            return self.rolled
        elif isinstance(other, self.__class__):
            return other.rolled - self.rolled
        elif isinstance(other, int):
            return other - self.rolled
        else:
            raise ValueError(
                f"unsupported (-) types: '{type(self)}' and '{type(other)}'")

    def __mul__(self, other) -> int:
        """
        Multiplies this die's rolled value with another die's rolled value or an integer.

        Returns 0 if other is 0.
        Returns product of rolled values if other is a Die.
        Returns product of die's rolled value with an integer if other is int.
        Raises ValueError if `other` is none of the above.
        """
        if other == 0:
            return 0
        elif isinstance(other, self.__class__):
            return self.rolled * other.rolled
        elif isinstance(other, int):
            return self.rolled * other
        else:
            raise ValueError(
                f"unsupported (*) types: '{type(self)}' and '{type(other)}'")

    def __rmul__(self, other) -> int:
        """
        Called when using reversed operands with the * operator (e.g., 5 * die).
        Delegates to the regular __mul__ method.
        """
        return self.__mul__(other)

    def __truediv__(self, other) -> int:
        """
        Divides this die's rolled value by another die's rolled value or an integer.

        Uses floor division by default. Raises ZeroDivisionError if dividing by zero.
        Raises ValueError if `other` is neither a Die nor an int.
        """
        if other == 0:
            raise ZeroDivisionError(f"{self.rolled} cannot divided by 0")
        elif isinstance(other, self.__class__):
            return self.rolled // other.rolled
        elif isinstance(other, int):
            return self.rolled // other
        else:
            raise ValueError(
                f"unsupported (/) types: '{type(self)}' and '{type(other)}'")

    def __rtruediv__(self, other) -> int:
        """
        Handles division when the die is on the right side of the / operator (e.g., 5 / die).

        Uses floor division by default. Raises ZeroDivisionError if dividing by zero.
        Raises ValueError if `other` is neither a Die nor an int.
        """
        if self.rolled == 0:
            raise ZeroDivisionError("Cannot divided by 0")
        elif isinstance(other, self.__class__):
            return other.rolled // self.rolled
        elif isinstance(other, int):
            return other // self.rolled
        else:
            raise ValueError(
                f"unsupported (/) types: '{type(self)}' and '{type(other)}'")

    def roll(self) -> int:
        """
        Rolls the die to obtain a random integer between 1 and `face_count`,
        and updates the `rolled` attribute with that value.

        Returns:
            int: The result of the roll.
        """
        if(not self.is_frozen):
            object.__setattr__(self, "rolled", random.randint(1, self.face_count))
        return self.rolled


@dataclass(order=True, frozen=True)
class FourSidedDie(Die):
    """
    A four-sided die with face_count set to 4 by default.
    """
    face_count: int = 4

    @override
    def console_print_face(self):
        raise NotImplementedError(f'{self.__class__.__name__} does not implement this method')


@dataclass(order=True, frozen=True)
class SixSidedDie(Die):
    """
    A six-sided die with face_count set to 6 by default.
    """
    face_count: int = 6

    face_art_arr = [
        [[" ", " ", " "],
         [" ", " ", " "],
         [" ", " ", " "]],

        [[" ", " ", " "],
         [" ", "o", " "],
         [" ", " ", " "]], 

        [["o", " ", " "],
         [" ", " ", " "],
         [" ", " ", "o"]], 

        [["o", " ", " "],
         [" ", "o", " "],
         [" ", " ", "o"]], 

        [["o", " ", "o"],
         [" ", " ", " "],
         ["o", " ", "o"]], 

        [["o", " ", "o"],
         [" ", "o", " "],
         ["o", " ", "o"]], 

        [["o", " ", "o"],
         ["o", " ", "o"],
         ["o", " ", "o"]]
    ]

    @override
    def console_print_face(self):
        face_art = self.face_art_arr[self.rolled]
        print(f" {"---".join(["-" for _ in face_art])} ")
        for row in face_art:
            print(f'| {"  ".join(row)} |')
        print(f" {"---".join(["-" for _ in face_art])} ")


@dataclass(order=True, frozen=True)
class EightSidedDie(Die):
    """
    An eight-sided die with face_count set to 8 by default.
    """
    face_count: int = 8

    @override
    def console_print_face(self):
        raise NotImplementedError(f'{self.__class__.__name__} does not implement this method')


@dataclass(order=True, frozen=True)
class TenSidedDie(Die):
    """
    A ten-sided die with face_count set to 10 by default.
    """
    face_count: int = 10

    @override
    def console_print_face(self):
        raise NotImplementedError(f'{self.__class__.__name__} does not implement this method')


@dataclass(order=True, frozen=True)
class TwelveSidedDie(Die):
    """
    A twelve-sided die with face_count set to 12 by default.
    """
    face_count: int = 12

    @override
    def console_print_face(self):
        raise NotImplementedError(f'{self.__class__.__name__} does not implement this method')


@dataclass(order=True, frozen=True)
class TwentySidedDie(Die):
    """
    A twenty-sided die with face_count set to 20 by default.
    """
    face_count: int = 20

    @override
    def console_print_face(self):
        raise NotImplementedError(f'{self.__class__.__name__} does not implement this method')


@dataclass(order=True, frozen=True)
class OneHundredSidedDie(Die):
    """
    A one-hundred-sided die with face_count set to 100 by default.
    """
    face_count: int = 100

    @override
    def console_print_face(self):
        raise NotImplementedError(f'{self.__class__.__name__} does not implement this method')


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
    die_type: Type["Die"]
    count: int
    dice: List["Die"] = field(init=False)
    roll_history: List[List["Die"]] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """
        Initializes the collection of dice using the provided die_type, 
        then records the initial roll state in roll_history.
        """
        self.dice = [self.die_type() for _ in range(self.count)]
        self.roll_history = [copy.deepcopy(self.dice)]

    @classmethod
    def from_dice_list(cls, dice_list: List["Die"]) -> "Dice":
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
    def current_roll(self) -> List["Die"]:
        return self.roll_history[-1]

    @property
    def previous_roll(self) -> List["Die"]:
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

    def remove_lowest_roll(self) -> None:
        """
        Removes the die with the lowest `rolled` value from the
        current set of dice. Raises ValueError if no dice remain.
        """
        if not self.dice:
            raise ValueError("No dice to remove.")
        lowest_die = min(self.dice, key=lambda d: d.rolled)
        self.dice.remove(lowest_die)

    def remove_highest_roll(self) -> None:
        """
        Removes the die with the highest `rolled` value from the
        current set of dice. Raises ValueError if no dice remain.
        """
        if not self.dice:
            raise ValueError("No dice to remove.")
        highest_die = max(self.dice, key=lambda d: d.rolled)
        self.dice.remove(highest_die)

    @staticmethod
    def pprint_str(dice: List["Die"]) -> str:
        return f"{len(dice)}{dice[0].name}, [{', '.join(str(d.rolled) for d in dice)}]"

    @staticmethod
    def pprint_dice(dice: List["Die"]) -> None:
        print(Dice.pprint_str(dice))

    def pprint_roll_history(self) -> None:
        for roll in self.roll_history:
            self.pprint_dice(roll)


class RollManager:
    """
    Manages dice-rolling logic by holding a single `Dice` object internally.
    Provides convenience methods for rolling with advantage, disadvantage,
    or regular rolls.

    Example usage:
        single_die = SixSidedDie()
        multiple_dice_list = [SixSidedDie() for _ in range(4)]
        dice_container = Dice(die_type=SixSidedDie, count=4)

        # All can be passed to RollManager:
        RollManager(single_die).roll()
        RollManager(multiple_dice_list).roll_with_advantage()
        RollManager(dice_container).roll_with_disadvantage()
    """

    def __init__(self, dice_input: Union["Die", List["Die"], Dice]) -> None:
        """
        Constructs a RollManager that always manages a single Dice object
        internally, regardless of the initial input type.

        Args:
            dice_input (Die | List[Die] | Dice): Input can be a single Die,
                a list of Die objects, or an existing Dice object.

        Raises:
            ValueError: If an empty list is provided or the argument is invalid.
        """
        if isinstance(dice_input, Die):
            # Single die -> build a Dice container with count=0,
            # then add the single die as a list.
            self._dice = Dice.from_dice_list([dice_input])
        elif isinstance(dice_input, list):
            if not dice_input:
                raise ValueError(
                    "Cannot create RollManager from an empty list of dice.")
            self._dice = Dice.from_dice_list(dice_input)
        elif isinstance(dice_input, Dice):
            self._dice = dice_input
        else:
            raise TypeError(
                "dice_input must be a Die, list of Die, or Dice instance.")

    def roll(self) -> int:
        """
        Performs a normal roll of all dice in the `Dice` object and returns
        the total of their rolled values.

        Returns:
            int: The total of the rolled values.
        """
        self._dice.roll()
        total = self._dice.current_total
        print(f"Regular roll total: {total}")
        return total

    def roll_with_advantage(self) -> int:
        """
        Performs a roll with advantage by adding one extra die, rolling all dice,
        then removing the lowest roll, and returning the total of the remaining dice.

        Returns:
            int: The total after rolling with advantage.
        """
        print(f"Rolling with advantage. Adding an extra {
              self._dice.die_type.__name__}.")
        self._dice.add_dice(number=1)
        self._dice.roll()
        self._dice.remove_lowest_roll()
        total = self._dice.current_total
        print(f"Advantage roll total: {total}")
        return total

    def roll_with_disadvantage(self) -> int:
        """
        Performs a roll with disadvantage by adding one extra die, rolling all dice,
        then removing the highest roll, and returning the total of the remaining dice.

        Returns:
            int: The total after rolling with disadvantage.
        """
        print(f"Rolling with disadvantage. Adding an extra {
              self._dice.die_type.__name__}.")
        self._dice.add_dice(number=1)
        self._dice.roll()
        self._dice.remove_highest_roll()
        total = self._dice.current_total
        print(f"Disadvantage roll total: {total}")
        return total

    def get_roll_total(self) -> int:
        """
        Returns the sum of the currently rolled dice values.

        Returns:
            int: The total of dice in `_dice.current_roll`.
        """
        return self._dice.current_total

    def add_dice(self, number: int = 1) -> None:
        """
        Dynamically adds additional dice to the current Dice object without rolling them.

        Args:
            number (int): How many dice to add. Default is 1.
        """
        self._dice.add_dice(number=number)
        print(f"Added {number} {
              self._dice.die_type.__name__} die/dice to RollManager.")

    def remove_lowest_roll(self) -> None:
        """
        Removes the die with the lowest rolled value from the Dice object.
        This only affects the dice pool for subsequent rolls.
        """
        self._dice.remove_lowest_roll()

    def remove_highest_roll(self) -> None:
        """
        Removes the die with the highest rolled value from the Dice object.
        This only affects the dice pool for subsequent rolls.
        """
        self._dice.remove_highest_roll()
