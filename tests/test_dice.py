import unittest

from src.Dice import Dice
from src.Die import Die, SixSidedDie


class DiceTests(unittest.TestCase):
    def setUp(self):
        self.dice = Dice(die_type=SixSidedDie, count=3)

    def test_dice_init(self):
        self.assertIsInstance(self.dice, Dice)

    def test_getting_len_of_dice(self):
        self.assertEqual(len(self.dice), 3)

    def test_dice_print(self):
        self.assertEqual(self.dice.__str__(), "3d6, [0, 0, 0]")

    def test_dice_print_after_roll(self):
        # set dice roll state of current_roll manually for assertion
        object.__setattr__(self.dice.roll_history[0][0], "rolled", 4)
        object.__setattr__(self.dice.roll_history[0][1], "rolled", 2)
        object.__setattr__(self.dice.roll_history[0][2], "rolled", 5)
        self.assertEqual(self.dice.__str__(), "3d6, [4, 2, 5]")

    def test_dice_count(self):
        self.assertEqual(len(self.dice.dice), 3)
        with self.assertRaises(IndexError):
            self.dice.dice[3]

    def test_dice_initial_state(self):
        self.assertIsInstance(self.dice.dice[0], SixSidedDie)
        self.assertIsInstance(self.dice.dice[1], SixSidedDie)
        self.assertIsInstance(self.dice.dice[2], SixSidedDie)
        self.assertEqual(self.dice.dice[0].rolled, 0)
        self.assertEqual(self.dice.dice[1].rolled, 0)
        self.assertEqual(self.dice.dice[2].rolled, 0)

    def test_rolling_dice(self):
        rolled = self.dice.roll()

        # validate roll return
        self.assertEqual(len(rolled), 3)
        self.assertIsInstance(rolled[0], Die)
        self.assertIsInstance(rolled[1], Die)
        self.assertIsInstance(rolled[2], Die)
        self.assertGreater(rolled[0].rolled, 0)
        self.assertGreater(rolled[1].rolled, 0)
        self.assertGreater(rolled[2].rolled, 0)

        # validate dice update within dice object
        self.assertGreater(self.dice.dice[0].rolled, 0)
        self.assertGreater(self.dice.dice[1].rolled, 0)
        self.assertGreater(self.dice.dice[2].rolled, 0)

    def test_rolling_updates_history(self):
        # reset self.dice
        self.setUp()
        start_len = 1

        self.assertEqual([d.rolled for d in self.dice.current_roll], [0, 0, 0])
        self.assertEqual(len(self.dice.roll_history), start_len)
        self.assertEqual(self.dice.current_roll, self.dice.dice)
        with self.assertRaises(IndexError):
            self.dice.previous_roll

        start_len += 1
        self.dice.roll()
        self.assertEqual(len(self.dice.roll_history), start_len)
        self.assertNotEqual(
            [d.rolled for d in self.dice.current_roll], [0, 0, 0])
        self.assertEqual(
            [d.rolled for d in self.dice.previous_roll], [0, 0, 0])
        self.assertIsNotNone(self.dice.previous_roll)
        self.assertNotEqual(self.dice.current_roll, self.dice.previous_roll)
        self.assertEqual(self.dice.current_roll, self.dice.dice)

        # do it a couple more times to validate roll history updates
        for i in range(5):
            start_len += 1
            self.dice.roll()
            self.assertEqual(len(self.dice.roll_history), start_len)
            self.assertNotEqual(
                [d.rolled for d in self.dice.current_roll], [0, 0, 0])
            self.assertNotEqual(
                [d.rolled for d in self.dice.previous_roll], [0, 0, 0])
            self.assertEqual(self.dice.current_roll, self.dice.dice)

    def test_returning_totals(self):
        # reset self.dice
        self.setUp()

        self.assertEqual(len(self.dice.roll_history), 1)
        self.assertEqual(self.dice.current_total, 0)
        with self.assertRaises(IndexError):
            self.dice.previous_total

        self.dice.roll()
        self.assertEqual(len(self.dice.roll_history), 2)
        self.assertNotEqual(self.dice.current_total, 0)
        self.assertIsNotNone(self.dice.previous_total)
        self.assertEqual(self.dice.previous_total, 0)

        self.dice.roll()
        self.assertEqual(len(self.dice.roll_history), 3)
        self.assertNotEqual(self.dice.current_total, 0)
        self.assertNotEqual(self.dice.previous_total, 0)

    def test_freezing_single_die(self):
        # reset self.dice
        self.setUp()

        self.dice.freeze_die(1)
        # self.dice.dice[1].toggle_freeze()
        self.dice.roll()

        self.assertNotEqual(self.dice.dice[0].rolled, 0)
        self.assertEqual(self.dice.dice[1].rolled, 0)
        self.assertNotEqual(self.dice.dice[2].rolled, 0)
    
    def test_unfreezing_single_die(self):
        # reset self.dice
        self.setUp()

        self.dice.freeze_die(1)
        # self.dice.dice[1].toggle_freeze()

        #validate is_frozen fsag
        self.dice.roll()
        self.assertNotEqual(self.dice.dice[0].rolled, 0)
        self.assertEqual(self.dice.dice[1].rolled, 0)
        self.assertNotEqual(self.dice.dice[2].rolled, 0)

        #unfreeze and test
        self.dice.unfreeze_die(1)
        # self.dice.dice[1].toggle_freeze()
        self.dice.roll()
        self.assertNotEqual(self.dice.dice[1].rolled, 0)
    
    def test_freezing_multiple_dice(self):
        # reset self.dice
        self.setUp()

        self.dice.freeze_dice([0,1])
        # self.dice.dice[0].toggle_freeze()
        # self.dice.dice[1].toggle_freeze()
        self.dice.roll()

        self.assertEqual(self.dice.dice[0].rolled, 0)
        self.assertEqual(self.dice.dice[1].rolled, 0)
        self.assertNotEqual(self.dice.dice[2].rolled, 0)

    def test_unfreezing_multiple_dice(self):
        # reset self.dice
        self.setUp()

        self.dice.freeze_dice([0,1])
        self.dice.roll()

        self.assertEqual(self.dice.dice[0].rolled, 0)
        self.assertEqual(self.dice.dice[1].rolled, 0)
        self.assertNotEqual(self.dice.dice[2].rolled, 0)

        self.dice.unfreeze_dice([0,1])
        self.dice.roll()
        self.assertNotEqual(self.dice.dice[0].rolled, 0)
        self.assertNotEqual(self.dice.dice[1].rolled, 0)

    def test_freezing_all_dice(self):
        # reset self.dice
        self.setUp()

        self.dice.freeze_all_dice()
        self.dice.roll()

        self.assertEqual(self.dice.dice[0].rolled, 0)
        self.assertEqual(self.dice.dice[1].rolled, 0)
        self.assertEqual(self.dice.dice[2].rolled, 0)

    def test_unfreezing_all_dice(self):
        # reset self.dice
        self.setUp()

        self.dice.freeze_all_dice()
        self.dice.roll()

        self.assertEqual(self.dice.dice[0].rolled, 0)
        self.assertEqual(self.dice.dice[1].rolled, 0)
        self.assertEqual(self.dice.dice[2].rolled, 0)

        self.dice.unfreeze_all_dice()
        self.dice.roll()

        self.assertNotEqual(self.dice.dice[0].rolled, 0)
        self.assertNotEqual(self.dice.dice[1].rolled, 0)
        self.assertNotEqual(self.dice.dice[2].rolled, 0)
    
    def test_adding_single_die_to_dice(self):
        # reset self.dice
        self.setUp()

        #setup dice and verify test default
        self.dice.roll()
        self.assertEqual(len(self.dice.current_roll), 3)
        self.assertEqual(len(self.dice.previous_roll), 3)
        with self.assertRaises(IndexError):
            self.dice.dice[3]

        # check adding unrolled die
        self.dice.add_dice()
        self.assertIsNotNone(self.dice.dice[3])
        self.assertEqual(self.dice.count, 4)
        self.assertEqual(self.dice.dice[3].rolled, 0)

        # check history update of new die on rolls
        self.dice.roll()
        self.assertNotEqual(self.dice.dice[3].rolled, 0)
        self.assertEqual(len(self.dice.current_roll), 4)
        self.assertEqual(len(self.dice.previous_roll), 3)
        self.dice.roll()
        self.assertEqual(len(self.dice.current_roll), 4)
        self.assertEqual(len(self.dice.previous_roll), 4)
    
    def test_adding_multiple_die_to_dice(self):
        # reset self.dice
        self.setUp()

        #setup dice and verify test default
        self.dice.roll()
        self.assertEqual(len(self.dice.current_roll), 3)
        self.assertEqual(len(self.dice.previous_roll), 3)
        with self.assertRaises(IndexError):
            self.dice.dice[3]

        # check adding multiple unrolled die
        self.dice.add_dice(4) #bring dice total to 7
        self.assertIsNotNone(self.dice.dice[6])
        self.assertEqual(self.dice.count, 7)
        # check all new dice are unrolled
        self.assertTrue(all([x.rolled == 0 for x in self.dice.dice[3:]]))

        # check history update of new die on rolls
        self.dice.roll()
        # check all new dice are no longer 0 after roll
        self.assertTrue(all([x.rolled != 0 for x in self.dice.dice[3:]]))
        self.assertEqual(len(self.dice.current_roll), 7)
        self.assertEqual(len(self.dice.previous_roll), 3)
        self.dice.roll()
        self.assertEqual(len(self.dice.current_roll), 7)
        self.assertEqual(len(self.dice.previous_roll), 7)
    
    def test_removing_die_from_dice_by_index(self):
        # reset self.dice
        self.setUp()
        self.dice.add_dice(2) #5 total dice
        #force dice state
        for ind, die in enumerate(self.dice):
            object.__setattr__(self.dice.roll_history[0][0], "rolled", 4)
        
        
    
    @unittest.skip
    def test_removing_multiple_dice_from_dice_by_indexes(self):
        raise NotImplementedError()

    @unittest.skip
    def test_get_count_of_specific_roll_value(self):
        raise NotImplementedError()
    
    @unittest.skip
    def test_get_array_of_roll_value_counts(self):
        raise NotImplementedError()



if __name__ == '__main__':
    unittest.main()
