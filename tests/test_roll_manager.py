'''ADDITIONAL TESTING TO CONSIDER

Coverage / Unit Tests
###########################################
RollManager Initialization
[ ] Test passing a single Die, confirming it becomes a Dice container internally.
[ ] Test passing a list of Dice to confirm correct internal representation.
[ ] Test passing an empty list to confirm ValueError is raised.
[ ] Test passing an invalid type to confirm TypeError is raised.

Rolling Logic
[ ] Test `roll_with_advantage` ensuring the extra die is added, lowest roll is removed, and total is correct.
[ ] Test `roll_with_disadvantage` ensuring the extra die is added, highest roll is removed, and total is correct.
[ ] Test repeated calls to advantage or disadvantage in succession.

Freeze / Unfreeze Method Validation
[ ] Confirm that freezing/unfreezing dice works when done via `RollManager` rather than directly on `Dice`.
[ ] Check that invalid calls (e.g., both `dice` parameter and `all_dice=True`) raise the correct error.

Remove Lowest / Highest Roll
[ ] Ensure these methods behave correctly when the dice pool has only 1 die.
[ ] Confirm removing the same roll multiple times raises an error or behaves correctly if the die no longer exists.

Functional Tests
###########################################
Integration of RollManager with Dice
[ ] Test scenario with multiple consecutive advantage/disadvantage rolls and confirm correct totals in each state.
[ ] Verify that a user can add dice, roll, freeze, unfreeze, remove highest roll, then roll again without errors.

Bulk Rolling
[ ] Roll hundreds of times to confirm distribution is sensible (especially with advantage and disadvantage).
[ ] Check performance when a large number of dice are managed (e.g., 50+ dice).

Edge Cases in Real Gameplay
[ ] Remove dice, then add new dice, freeze some of them, roll with advantage, and confirm final total is as expected.
[ ] Confirm roll history (if integrated) remains consistent after multiple remove/add/freeze/unfreeze cycles.

Interactive Tests
###########################################
Console Interaction
[ ] Simulate a CLI flow where a user chooses between normal roll, advantage, or disadvantage, confirms correct output each time.
[ ] User attempts freeze/unfreeze commands on specific dice or all dice, checks the resulting roll outputs in a live session.

Live Removal / Addition
[ ] A user removes the lowest roll die after a normal roll, re-rolls, then checks if the total changes accordingly.
[ ] A user adds multiple dice, then tries rolling with disadvantage to confirm the new dice are included in the final total.

User Feedback / Error Handling
[ ] Supply invalid options (e.g., trying to remove dice from an empty pool or freezing an invalid reference) to confirm proper error messages.
[ ] Provide boundary inputs like removing the only die in the pool and confirm subsequent rolls behave as expected.


############################################

Potential Tests for Additional Properties
[ ] `history_limit`:
    - Set a `history_limit` and roll multiple times, confirming that once the limit is reached, older entries are removed.
    - Test edge case when `history_limit` is 0 or very small.
[ ] `user_metadata`:
    - Assign user-specific data (e.g., player name) to `user_metadata` and confirm it’s retained.
    - Update or remove metadata, verifying changes persist as expected.

Potential Tests for Additional Methods
[ ] `roll_specific(dice_indexes: List[int])`:
    - Ensure only the specified dice are rolled, while others retain their prior `rolled` values.
    - Test invalid indexes to confirm appropriate handling or errors.
[ ] `apply_modifier(modifier_fn: Callable[[Dice], None])`:
    - Provide a function that modifies dice (e.g., sets all rolls above 5 to 5). Confirm changes occur as intended.
    - Test an empty or no-op modifier to confirm no changes occur.
[ ] `undo_last_roll()`:
    - Roll normally, then call `undo_last_roll()`. Confirm the dice revert to their previous rolled values.
    - Test repeated undo calls and confirm the correct historical state is restored each time.
'''


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
