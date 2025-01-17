'''
Potential Additional Properties
[ ] `history_limit`: Limits the size of roll history if that feature exists, discarding oldest entries when exceeding the limit.
[ ] `user_metadata`: A dictionary or similar container for storing user-specific data, like who is rolling the dice.

Potential Additional Methods
[ ] `roll_specific(dice_indexes: List[int])`: Rolls only a subset of the dice in the managed container.
[ ] `apply_modifier(modifier_fn: Callable[[Dice], None])`: Allows external logic to modify dice or totals (e.g., special RPG rules).
[ ] `undo_last_roll()`: Reverts the Dice object to its previous roll state if needed for an “undo” feature.

'''

from typing import Union, List


from .die import Die
from .dice import Dice


class RollManager:
    """
    Manages dice-rolling logic by holding a single `Dice` object internally.
    Provides convenience methods for rolling with advantage, disadvantage,
    or regular rolls.

    Example usage:
        single_Die = SixSidedDie()
        multiple_dice_list = [SixSidedDie() for _ in range(4)]
        dice_container = Dice(Die_type=SixSidedDie, count=4)

        # All can be passed to RollManager:
        RollManager(single_Die).roll()
        RollManager(multiple_dice_list).roll_with_advantage()
        RollManager(dice_container).roll_with_disadvantage()
    """

    def __init__(self, dice_input: Union[Die, List[Die], Dice]) -> None:
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
            # Single Die -> build a Dice container with count=0,
            # then add the single Die as a list.
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
        Performs a roll with advantage by adding one extra Die, rolling all dice,
        then removing the lowest roll, and returning the total of the remaining dice.

        Returns:
            int: The total after rolling with advantage.
        """
        print(f"Rolling with advantage. Adding an extra {
              self._dice.Die_type.__name__}.")
        self._dice.add_dice(number=1)
        self._dice.roll()
        self._dice.remove_lowest_roll()
        total = self._dice.current_total
        print(f"Advantage roll total: {total}")
        return total

    def roll_with_disadvantage(self) -> int:
        """
        Performs a roll with disadvantage by adding one extra Die, rolling all dice,
        then removing the highest roll, and returning the total of the remaining dice.

        Returns:
            int: The total after rolling with disadvantage.
        """
        print(f"Rolling with disadvantage. Adding an extra {
              self._dice.Die_type.__name__}.")
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
              self._dice.Die_type.__name__} Die/dice to RollManager.")

    def remove_lowest_roll(self) -> None:
        """
        Removes the Die with the lowest rolled value from the Dice object.
        This only affects the dice pool for subsequent rolls.
        """
        self._dice.remove_lowest_roll()

    def remove_highest_roll(self) -> None:
        """
        Removes the Die with the highest rolled value from the Dice object.
        This only affects the dice pool for subsequent rolls.
        """
        self._dice.remove_highest_roll()

    def __validate_method_params_freeze_unfreeze(self, dice: Die | List[Die] | None, all_dice: bool) -> None:
        if not dice and not all_dice:
            raise ValueError(
                'No input provided - expected input for dice parameter or all_dice=True')

        if dice is not None and all_dice:
            raise ValueError(
                'You cannot input a value for the dice parameter and set all_dice=True')

        if isinstance(dice, Die):
            return

        if isinstance(dice, list) and all(isinstance(d, Die) for d in dice):
            return

        if not dice and all_dice:
            return

        non_die_values = [d for d in (dice if isinstance(dice, list) else [
                                      dice]) if not isinstance(d, Die)]
        if non_die_values:
            raise ValueError(
                'One or more values passed in for dice '
                'is not a subclass of Die or a list of objects that are subclasses of type Die: '
                f'{", ".join(map(str, non_die_values))}'
            )

    def freeze(self, dice: Die | List[Die] | None = None, all_dice: bool = False) -> None:
        self.__validate_method_params_freeze_unfreeze(
            dice=dice, all_dice=all_dice)
        if isinstance(dice, Die):
            dice.is_frozen or dice.toggle_freeze()
        elif isinstance(dice, List) and all([isinstance(_, Die) for _ in dice]):
            for die in dice:
                self.freeze(die)
        elif all_dice:
            self.freeze(self.dice)

    def unfreeze(self, dice: Die | List[Die] | None = None, all_dice: bool = False) -> None:
        self.__validate_method_params_freeze_unfreeze(
            dice=dice, all_dice=all_dice)
        if isinstance(dice, Die):
            dice.is_frozen and dice.toggle_freeze()
        elif isinstance(dice, List) and all([isinstance(_, Die) for _ in dice]):
            for die in dice:
                self.unfreeze(die)
        elif all_dice:
            self.unfreeze(self.dice)
