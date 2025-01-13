import unittest

from src.DiceEngine import (
    Dice, 
    Die, 
    SixSidedDie,
)


class DiceInitTests(unittest.TestCase):
    def setUp(self):
        self.dice = Dice(die_type=SixSidedDie, count=3)

    def test_dice_init(self):
        self.assertIsInstance(self.dice, Dice)

    def test_dice_initial_state(self):
        self.assertIsInstance(self.dice.dice[0], SixSidedDie)
        self.assertIsInstance(self.dice.dice[1], SixSidedDie)
        self.assertIsInstance(self.dice.dice[2], SixSidedDie)
        self.assertEqual(self.dice.dice[0].rolled, 0)
        self.assertEqual(self.dice.dice[1].rolled, 0)
        self.assertEqual(self.dice.dice[2].rolled, 0)


class DicePropertyTests(unittest.TestCase):
    def setUp(self):
        self.dice = Dice(die_type=SixSidedDie, count=3)

    def test_getting_len_of_dice(self):
        self.assertEqual(len(self.dice), 3)

    def test_dice_count(self):
        self.assertEqual(len(self.dice.dice), 3)
        with self.assertRaises(IndexError):
            self.dice.dice[3]

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


class DicePrintTests(unittest.TestCase):
    def setUp(self):
        self.dice = Dice(die_type=SixSidedDie, count=3)

    def test_dice_print(self):
        self.assertEqual(self.dice.__str__(), "3d6, [0, 0, 0]")

    def test_dice_print_after_roll(self):
        # set dice roll state of current_roll manually for assertion
        object.__setattr__(self.dice.roll_history[0][0], "rolled", 4)
        object.__setattr__(self.dice.roll_history[0][1], "rolled", 2)
        object.__setattr__(self.dice.roll_history[0][2], "rolled", 5)
        self.assertEqual(self.dice.__str__(), "3d6, [4, 2, 5]")


class DiceRollingTests(unittest.TestCase):
    def setUp(self):
        self.dice = Dice(die_type=SixSidedDie, count=3)

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

class DiceListTests(unittest.TestCase):
    def setUp(self):
        self.dice = Dice(die_type=SixSidedDie, count=3)

    @unittest.skip
    def test_get_die_index_from_ref(self):
        # reset self.dice
        self.setUp()

        #set specific die index state
        object.__setattr__(self.dice.dice[1], "rolled", 3)
        self.assertEqual([_.rolled for _ in self.dice], [0,3,0])

        #test getting index from ref
        test_die = self.dice.dice[1]
        self.assertEqual(self.dice.get_index(test_die), 1)

    @unittest.skip
    def test_get_multiple_dice_indexes_from_ref(self):
        # reset self.dice
        self.setUp()

        #set specific die index state
        object.__setattr__(self.dice.dice[1], "rolled", 3)
        self.assertEqual([_.rolled for _ in self.dice], [0,3,0])

        #test getting index from ref
        test_dice = [die for die in self.dice if die.rolled == 0]
        self.assertEqual(self.dice.get_index(test_dice), [0,2])

    @unittest.skip
    def test_get_die_ref_by_value(self):
        # reset self.dice
        self.setUp()

        #set specific die index state
        object.__setattr__(self.dice.dice[1], "rolled", 3)
        self.assertEqual([_.rolled for _ in self.dice], [0,3,0])

        #test getting all dice with value 0
        cached_die_1 = self.dice.dice[0]
        cached_die_2 = self.dice.dice[2]
        found_dice = self.dice.get_dice_with_value(0)
        self.assertEqual(len(found_dice), 2)
        self.assertIs(found_dice[0], cached_die_1)
        self.assertIs(found_dice[1], cached_die_2)

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
    
    @unittest.skip
    def test_removing_die_from_dice_by_index(self):
        # reset self.dice
        self.setUp()
        self.dice.add_dice(2) #5 total dice
        self.assertEqual(self.dice.count, 5)
        #force dice state to all 1's
        for die in self.dice:
            object.__setattr__(die, "rolled", 1)
        # set 4th index specifically to 3
        object.__setattr__(self.dice.dice[3], "rolled", 3)
        #ensure state
        self.assertEqual([_.rolled for _ in self.dice], [1,1,1,3,1])

        #test removal
        self.dice.remove_die(3)
        self.assertEqual(self.dice.count, 4)
        self.assertEqual([_.rolled for _ in self.dice], [1,1,1,1])

    @unittest.skip
    def test_removing_die_from_dice_by_ref(self):
        # reset self.dice
        self.setUp()
        self.dice.add_dice(2) #5 total dice
        self.assertEqual(self.dice.count, 5)
        #force dice state to all 1's
        for die in self.dice:
            object.__setattr__(die, "rolled", 1)
        # set 4th index specifically to 3
        object.__setattr__(self.dice.dice[3], "rolled", 3)
        #ensure state
        self.assertEqual([_.rolled for _ in self.dice], [1,1,1,3,1])

        #test removal
        test_die = self.dice.dice[3]
        self.dice.remove_die(test_die)
        self.assertEqual(self.dice.count, 4)
        self.assertEqual([_.rolled for _ in self.dice], [1,1,1,1])
        
    @unittest.skip
    def test_removing_multiple_dice_from_dice_by_indexes(self):
        raise NotImplementedError()
    
    @unittest.skip
    def test_removing_multiple_dice_from_dice_by_ref(self):
        raise NotImplementedError()


class DiceFreezeTests(unittest.TestCase):
    def setUp(self):
        self.dice = Dice(die_type=SixSidedDie, count=3)

    def test_freezing_single_die(self):
        # reset self.dice
        self.setUp()

        #set die ref
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

        #validate is_frozen fsag
        self.dice.roll()
        self.assertNotEqual(self.dice.dice[0].rolled, 0)
        self.assertEqual(self.dice.dice[1].rolled, 0)
        self.assertNotEqual(self.dice.dice[2].rolled, 0)

        #unfreeze and test
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
            
    
    
class DiceGroupValueTests(unittest.TestCase):
    def setUp(self):
        self.dice = Dice(die_type=SixSidedDie, count=9)

    @unittest.skip
    def test_get_count_of_specific_roll_value(self):
        raise NotImplementedError()
    
    @unittest.skip
    def test_get_array_of_roll_value_counts(self):
        raise NotImplementedError()



if __name__ == '__main__':
    unittest.main()
