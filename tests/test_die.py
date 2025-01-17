'''ADDITIONAL TESTS TO CONSIDER

Coverage / Unit Tests
###########################################################
Tests for console_print_face
[ ] Right now, only SixSidedDie implements console_print_face. You might want explicit tests that roll a SixSidedDie for all possible outcomes (1–6) and then confirm that the printed ASCII art is correct for each face.
[ ] You could also test that calling console_print_face on any of the other dice (where it is not implemented) raises the correct NotImplementedError.

Edge Cases for Arithmetic Operators
[ ] Try passing in other non-integer, non-Die objects (e.g., strings, floats, or custom objects) to make sure the ValueError is raised appropriately for +, -, *, /.
[ ] Check that division by a Die with a rolled value of 0 correctly raises ZeroDivisionError.

Testing Invalid or Custom Face Counts
[ ] Although the code uses frozen classes for fixed-face dice, you might consider a scenario where someone tries to instantiate a Die with zero or negative faces. Even if that’s not part of your official API, a thorough test suite would confirm that the class either rejects invalid face counts or fails gracefully.

Testing Equality and Comparisons with Different Dice Classes
[ ] The tests for equality and comparison currently use dice of the same type (SixSidedDie vs. SixSidedDie). You may want to confirm that comparisons between different classes (e.g., FourSidedDie vs. SixSidedDie) either work as expected or raise an error, depending on your intended behavior.

Additional Tests for Randomness / Distribution
[ ] While you wouldn’t unit-test randomness in a strict sense, you could run statistical distribution tests to ensure all faces are showing up in the correct proportions (especially for large sample rolls). This goes beyond simple unit-testing, but can still be included to confirm each face is equally likely.

Freezing / Unfreezing Behavior
[ ] You already have tests that confirm a die doesn’t change value while frozen across many rolls. You might add coverage verifying that if you toggle from frozen to unfrozen, it does indeed allow changes again on subsequent rolls.

String Representation Tests
[ ] You have tests confirming __str__() returns d<face_count>. You could expand that to confirm behavior when certain attributes (like rolled) have changed, though that shouldn’t affect __str__() as currently implemented.

Test Setting rolled Directly
[ ] The current tests use object.__setattr__ to override rolled. You could add coverage explicitly ensuring that rolled cannot be changed normally since it’s a frozen dataclass. This ensures attempts like die.rolled = 3 raise an exception.


Functional Tests
###########################################################
Persistence or Serialization
[ ] If these dice are persisted between sessions (e.g., saving a game state), you could add tests for serializing a die’s state (face count, rolled value, and freeze state) and then deserializing it back. This confirms that the die reconstitutes with the same state.

Batches / Pools of Dice
[ ] Tests that roll a batch of dice simultaneously or in sequence, confirming that sums, differences, or other aggregate operations produce the correct result.

Integration with Other Systems
[ ] In a real RPG or board game setting, you might have a “Roll” function that calls die.roll() multiple times under certain conditions (advantage/disadvantage in some game mechanics). Checking that these external conditions produce expected results for the dice would be a higher-level functional test.

Conditional Rules
[ ] If there are game-specific constraints (like exploding dice in certain RPG systems, or re-roll on 1, etc.), tests could be added to ensure the library can handle or extend those behaviors properly.


Interactive Tests
###########################################################
Console I/O Tests for SixSidedDie.console_print_face
[ ] You might have a simple interactive test confirming that rolling a SixSidedDie and calling console_print_face indeed prints a correct ASCII face. This is more of a manual/integration scenario—some projects automate it by capturing stdout and confirming it matches an expected pattern.

CLI or GUI-Driven Testing
[ ] If dice are used from a CLI or GUI (for example, a small console game), you might set up an integration test that prompts a user to roll a die, freeze it, and then confirm the console messages or displayed output is correct.

User Input Validation
[ ] If your application asks a user which die to roll (d4, d6, etc.) at runtime, you could test that selecting an invalid die type yields a friendly error message.
'''

import unittest
from typing import Type

from src.DiceEngine import (
    FourSidedDie,
    SixSidedDie,
    EightSidedDie,
    TenSidedDie,
    TwelveSidedDie,
    TwentySidedDie,
    OneHundredSidedDie,
    die,
)


class DieTypeAndPropertyTestCases(unittest.TestCase):
    @staticmethod
    def TestDieProperties(test: unittest.TestCase, die: die, die_type: Type, num_faces: int) -> None:
        valid_rolls = list(range(1, (num_faces+1)))

        test.assertIsInstance(die, die_type)

        test.assertEqual(die.rolled, 0)
        test.assertEqual(die.face_count, num_faces)
        test.assertEqual(die.name, f'd{num_faces}')
        test.assertEqual(die.__str__(), f'd{num_faces}')

        # test rolled property updates when rolled
        roll_result = die.roll()
        test.assertIsInstance(roll_result, int)
        test.assertIsNot(roll_result, 0)
        test.assertIn(die.rolled, valid_rolls, f"{
                      die.name} rolled outside of valid range")

        # test 1K roll iterations
        for i in range(1000):
            die.roll()
            test.assertIn(die.rolled, valid_rolls, f"{
                          die.name} rolled outside of valid range")

    def test_four_sided_die_properties(self):
        """Test all properties of 4 sided dice (d4)"""
        test_die = FourSidedDie()
        DieTypeAndPropertyTestCases.TestDieProperties(test=self,
                                                      die=test_die,
                                                      die_type=type(test_die),
                                                      num_faces=4)

    def test_six_sided_die_properties(self):
        """Test all properties of 6 sided dice (d6)"""
        test_die = SixSidedDie()
        DieTypeAndPropertyTestCases.TestDieProperties(test=self,
                                                      die=test_die,
                                                      die_type=type(test_die),
                                                      num_faces=6)

    def test_eight_sided_die_properties(self):
        """Test all properties of 8 sided dice (d8)"""
        test_die = EightSidedDie()
        DieTypeAndPropertyTestCases.TestDieProperties(test=self,
                                                      die=test_die,
                                                      die_type=type(test_die),
                                                      num_faces=8)

    def test_ten_sided_die_properties(self):
        """Test all properties of 10 sided dice (d10)"""
        test_die = TenSidedDie()
        DieTypeAndPropertyTestCases.TestDieProperties(test=self,
                                                      die=test_die,
                                                      die_type=type(test_die),
                                                      num_faces=10)

    def test_twelve_sided_die_properties(self):
        """Test all properties of 12 sided dice (d12)"""
        test_die = TwelveSidedDie()
        DieTypeAndPropertyTestCases.TestDieProperties(test=self,
                                                      die=test_die,
                                                      die_type=type(test_die),
                                                      num_faces=12)

    def test_twenty_sided_die_properties(self):
        """Test all properties of 20 sided dice (d20)"""
        test_die = TwentySidedDie()
        DieTypeAndPropertyTestCases.TestDieProperties(test=self,
                                                      die=test_die,
                                                      die_type=type(test_die),
                                                      num_faces=20)

    def test_onehundred_sided_die_properties(self):
        """Test all properties of 100 sided dice (d100)"""
        test_die = OneHundredSidedDie()
        DieTypeAndPropertyTestCases.TestDieProperties(test=self,
                                                      die=test_die,
                                                      die_type=type(test_die),
                                                      num_faces=100)


class DieMethodTestCases(unittest.TestCase):
    def setUp(self):
        self.four_sided_a = FourSidedDie()
        self.four_sided_b = FourSidedDie()
        self.four_sided_c = FourSidedDie()

        self.twenty_sided_a = TwentySidedDie()
        self.twenty_sided_b = TwentySidedDie()

    # ##########################################################################
    # DIE LOGIC

    def test_comparing_dice(self):
        die1 = SixSidedDie()
        object.__setattr__(die1, "rolled", 2)
        die2 = SixSidedDie()
        object.__setattr__(die2, "rolled", 4)
        die3 = SixSidedDie()
        object.__setattr__(die3, "rolled", 4)

        self.assertEqual(die2, die3)
        self.assertNotEqual(die1, die2)
        self.assertGreater(die2, die1)
        self.assertGreaterEqual(die2, die1)
        self.assertGreaterEqual(die3, die2)
        self.assertLess(die1, die2)
        self.assertLessEqual(die3, die2)
        self.assertLessEqual(die1, die2)
        self.assertNotEqual(die1, die2)

    # ##########################################################################
    # SUMMING DIE

    def test_adding_die_rolls_together_from_same_dietype(self):
        """test adding same type dice objects returns total of both dice's rolls"""
        object.__setattr__(self.four_sided_a, "rolled", 4)
        object.__setattr__(self.four_sided_b, "rolled", 3)
        self.assertEqual(self.four_sided_a + self.four_sided_b, 7)

    def test_adding_die_and_int(self):
        """test adding dice object with a whole number returns the dice's roll plus the number"""
        object.__setattr__(self.four_sided_a, "rolled", 4)
        self.assertEqual(self.four_sided_a + 5, 9)

    def test_adding_int_and_die(self):
        """test adding a whole number with a die returns the sum of the number and dice's roll"""
        object.__setattr__(self.four_sided_a, "rolled", 4)
        self.assertEqual(5 + self.four_sided_a, 9)

    def test_summing_array_of_dice(self):
        """test ability to use sum() on an array of dice to get the roll total of all dice in array"""
        object.__setattr__(self.four_sided_a, "rolled", 4)
        object.__setattr__(self.four_sided_b, "rolled", 3)
        object.__setattr__(self.four_sided_c, "rolled", 2)
        dice_arr = [self.four_sided_a, self.four_sided_b, self.four_sided_c]
        self.assertEqual(sum(dice_arr), 9)

    def test_summing_array_of_dice_and_ints(self):
        object.__setattr__(self.four_sided_a, "rolled", 4)
        object.__setattr__(self.four_sided_b, "rolled", 3)
        object.__setattr__(self.four_sided_c, "rolled", 2)
        # [die, int, die, int, die]
        dice_arr = [self.four_sided_a, 5,
                    self.four_sided_b, 2, self.four_sided_c]
        self.assertEqual(sum(dice_arr), 16)

    # ##########################################################################
    # SUBTRACTING DIE

    def test_subtracting_die_rolls_from_same_dietype(self):
        """test subtracting same type dice objects returns difference of both dice's rolls"""
        object.__setattr__(self.four_sided_a, "rolled", 4)
        object.__setattr__(self.four_sided_b, "rolled", 1)
        self.assertEqual(self.four_sided_a - self.four_sided_b, 3)

    def test_subtracting_die_and_int(self):
        """test subtracting dice object with a whole number returns the dice's roll minus the number"""
        object.__setattr__(self.four_sided_a, "rolled", 4)
        self.assertEqual(self.four_sided_a - 2, 2)

    def test_subtracting_int_and_die(self):
        """test subtracting int with a die returns the number minus the dice's roll"""
        object.__setattr__(self.four_sided_a, "rolled", 3)
        self.assertEqual(4 - self.four_sided_a, 1)

    # ##########################################################################
    # MULTIPLYING DIE

    def test_multiplying_die_rolls_from_same_dietype(self):
        """test multiplying same type dice objects returns the product of both dice's rolls"""
        object.__setattr__(self.four_sided_a, "rolled", 3)
        object.__setattr__(self.four_sided_b, "rolled", 2)
        self.assertEqual(self.four_sided_a * self.four_sided_b, 6)

    def test_multiplying_die_and_int(self):
        """test multiplying dice object with a whole number returns the dice's roll times the number"""
        object.__setattr__(self.four_sided_a, "rolled", 3)
        self.assertEqual(self.four_sided_a * 4, 12)

    def test_multiplying_int_and_die(self):
        """test multiplying int with dice object returns the product of the int and the dice's roll"""
        object.__setattr__(self.four_sided_a, "rolled", 2)
        self.assertEqual(4 * self.four_sided_a, 8)

    # ##########################################################################
    # DIVIDING DIE
    #   default is floor divide (we need whole numbers)

    def test_dividing_die_rolls_from_same_dietype(self):
        """test dividing same type dice objects returns the division of dice's rolls"""
        object.__setattr__(self.twenty_sided_a, "rolled", 12)
        object.__setattr__(self.twenty_sided_b, "rolled", 4)
        self.assertEqual(self.twenty_sided_a / self.twenty_sided_b, 3)

        object.__setattr__(self.twenty_sided_a, "rolled", 17)
        object.__setattr__(self.twenty_sided_b, "rolled", 4)
        self.assertEqual(self.twenty_sided_a / self.twenty_sided_b, 4)

    def test_dividing_die_and_int(self):
        """test dividing dice object with a whole number returns the dice's roll divided by the number"""
        object.__setattr__(self.twenty_sided_a, "rolled", 15)
        self.assertEqual(self.twenty_sided_a / 2, 7)

    def test_dividing_int_and_die(self):
        """test dividing int with dice object returns the result of int divided by dice's roll"""
        object.__setattr__(self.twenty_sided_a, "rolled", 5)
        self.assertEqual(19 / self.twenty_sided_a, 3)

    @unittest.skip("no known need to implement ceiling logic yet...")
    def test_setting_ceiling_divide(self):
        raise NotImplementedError(
            "Create tests for test_setting_ceiling_divide")

    def test_freezing_roll(self):
        self.assertFalse(self.twenty_sided_a.is_frozen)
        self.twenty_sided_a.toggle_freeze()
        self.assertTrue(self.twenty_sided_a.is_frozen)
        self.twenty_sided_a.toggle_freeze()
        self.assertFalse(self.twenty_sided_a.is_frozen)

    def test_frozen_roll(self):
        # hard to test other than rolling many times and ensuring no change
        # chance of no change over 1,000,000 rolls is very slim... but still possible...

        # force object state
        object.__setattr__(self.twenty_sided_a, "rolled", 9)
        object.__setattr__(self.twenty_sided_a, "is_frozen", True)

        # run tests
        for _ in range(1_000_000):
            self.twenty_sided_a.roll()
            self.assertEqual(self.twenty_sided_a.rolled, 9)

    def test_unfrozen_roll(self):
        # much easier to test change
        # chance of change over 1,000 rolls is very likely

        # force object state
        object.__setattr__(self.twenty_sided_a, "rolled", 9)
        object.__setattr__(self.twenty_sided_a, "is_frozen", False)

        # ensure a roll other than 9 occured in 1,000 rolls
        self.assertTrue(
            any(filter(lambda x: x != 9, [self.twenty_sided_a.roll() for _ in range(1000)])))


if __name__ == '__main__':
    unittest.main()
