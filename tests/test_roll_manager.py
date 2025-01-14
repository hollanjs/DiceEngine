import unittest

from src.DiceEngine import (
    RollManager,
    Dice,
    SixSidedDie
)


class TestRollManagerDiceFreezeCapabilities(unittest.TestCase):
    def setUp(self):
        self.dice = Dice(die_type=SixSidedDie, count=3)

    def test_freezing_single_die(self):
        # reset self.dice
        self.setUp()

        # set die ref
        test_die = self.dice.dice[1]
        self.dice.freeze(test_die)
        # self.dice.dice[1].toggle_freeze()
        self.dice.roll()

        self.assertNotEqual(self.dice.dice[0].rolled, 0)
        self.assertEqual(self.dice.dice[1].rolled, 0)
        self.assertNotEqual(self.dice.dice[2].rolled, 0)

    def test_unfreezing_single_die(self):
        # reset self.dice
        self.setUp()

        test_die = self.dice.dice[1]
        self.dice.freeze(test_die)

        # validate is_frozen fsag
        self.dice.roll()
        self.assertNotEqual(self.dice.dice[0].rolled, 0)
        self.assertEqual(self.dice.dice[1].rolled, 0)
        self.assertNotEqual(self.dice.dice[2].rolled, 0)

        # unfreeze and test
        self.dice.unfreeze(test_die)
        self.dice.roll()
        self.assertNotEqual(self.dice.dice[1].rolled, 0)

    def test_freezing_multiple_dice(self):
        # reset self.dice
        self.setUp()

        test_dice = self.dice.dice[0:2]
        self.dice.freeze(test_dice)
        self.dice.roll()

        self.assertEqual(self.dice.dice[0].rolled, 0)
        self.assertEqual(self.dice.dice[1].rolled, 0)
        self.assertNotEqual(self.dice.dice[2].rolled, 0)

    def test_unfreezing_multiple_dice_by_ref(self):
        # reset self.dice
        self.setUp()

        test_dice = self.dice.dice[0:2]
        self.dice.freeze(test_dice)
        self.dice.roll()

        self.assertEqual(self.dice.dice[0].rolled, 0)
        self.assertEqual(self.dice.dice[1].rolled, 0)
        self.assertNotEqual(self.dice.dice[2].rolled, 0)

        self.dice.unfreeze(test_dice)
        self.dice.roll()
        self.assertNotEqual(self.dice.dice[0].rolled, 0)
        self.assertNotEqual(self.dice.dice[1].rolled, 0)

    def test_freezing_all_dice(self):
        # reset self.dice
        self.setUp()

        self.dice.freeze(all_dice=True)
        self.dice.roll()

        self.assertEqual(self.dice.dice[0].rolled, 0)
        self.assertEqual(self.dice.dice[1].rolled, 0)
        self.assertEqual(self.dice.dice[2].rolled, 0)

    def test_unfreezing_all_dice(self):
        # reset self.dice
        self.setUp()

        self.dice.freeze(all_dice=True)
        self.dice.roll()

        self.assertEqual(self.dice.dice[0].rolled, 0)
        self.assertEqual(self.dice.dice[1].rolled, 0)
        self.assertEqual(self.dice.dice[2].rolled, 0)

        self.dice.unfreeze(all_dice=True)
        self.dice.roll()

        self.assertNotEqual(self.dice.dice[0].rolled, 0)
        self.assertNotEqual(self.dice.dice[1].rolled, 0)
        self.assertNotEqual(self.dice.dice[2].rolled, 0)

    def test_freeze_valueerror_with_no_params(self):
        with self.assertRaises(ValueError):
            self.dice.freeze()

    def test_freeze_valueerror_with_dice_object_and_all_dice_set_to_true(self):
        dice_subset = self.dice.dice[0:2]
        with self.assertRaises(ValueError):
            self.dice.freeze(dice_subset, all_dice=True)

    def test_freeze_valueerror_where_dice_object_not_die(self):
        with self.assertRaises(ValueError):
            self.dice.freeze(1)

        with self.assertRaises(ValueError):
            self.dice.freeze("value error")

    def test_freeze_valueerror_where_dice_object_is_empty_list(self):
        with self.assertRaises(ValueError):
            self.dice.freeze([])

    def test_freeze_valueerror_where_dice_list_contains_non_die_object(self):
        dice_subset = self.dice.dice[0:2]
        dice_subset.append("not a die")
        with self.assertRaises(ValueError):
            self.dice.freeze(dice_subset)


if __name__ == '__main__':
    unittest.main()
