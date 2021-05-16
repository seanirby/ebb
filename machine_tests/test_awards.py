from machine_tests.EbbMachineTestCase import EbbMachineTestCase

AWARD_SELECTED = "award_selected"

class TestAwards(EbbMachineTestCase):
    def test_conditions_on_ball_start(self):
        self.start_game()
        self.assertModeRunning('awards')
        self.assertPlayerVarEqual(3, AWARD_SELECTED)

    # TODO: Fix ordering of awards, should be 0 indexed from left to right
    def test_selecting_awards(self):
        self.start_game()
        self.select_award_left(1)
        self.assertPlayerVarEqual(2, AWARD_SELECTED)
        self.select_award_right(1)
        self.assertPlayerVarEqual(3, AWARD_SELECTED)
        # selection wraps
        self.select_award_left(4)
        self.assertPlayerVarEqual(6, AWARD_SELECTED)
        self.select_award_right(1)
        self.assertPlayerVarEqual(0, AWARD_SELECTED)

    def test_collecting_awards(self):
        self.start_game()
        self.assertPlayerVarEqual(0, "award_3_collected")
        self.collect_award()
        self.advance_time_and_run(5)
        self.assertPlayerVarEqual(1, "award_3_collected")

    def test_collecting_award_1_last(self):
        self.start_game()
        self.select_award_left(1)
        # award 2
        self.collect_award()
        self.advance_time_and_run(5)
        self.assertPlayerVarEqual(1, "award_2_collected")
        # award 3
        self.collect_award()
        self.advance_time_and_run(5)
        self.assertPlayerVarEqual(1, "award_3_collected")
        # award 4
        self.collect_award()
        self.advance_time_and_run(5)
        self.assertPlayerVarEqual(1, "award_4_collected")
        # award 5
        self.collect_award()
        self.advance_time_and_run(5)
        self.assertPlayerVarEqual(1, "award_5_collected")
        # award 6
        self.collect_award()
        self.advance_time_and_run(5)
        self.assertPlayerVarEqual(1, "award_6_collected")
        # award 0
        self.collect_award()
        self.advance_time_and_run(5)
        self.assertPlayerVarEqual(1, "award_0_collected")
        # award 1
        self.collect_award()
        self.advance_time_and_run(5)
        # award sets incremented and awards reset
        self.assertPlayerVarEqual(1, "award_sets")
        for i in range(0, 6):
            self.assertPlayerVarEqual(0, "award_{}_collected".format(i))
