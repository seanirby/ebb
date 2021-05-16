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
