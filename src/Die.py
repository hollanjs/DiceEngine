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
from typing import override
import random


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