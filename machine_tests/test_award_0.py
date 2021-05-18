from machine_tests.EbbMachineTestCase import EbbMachineTestCase

AWARD = "award_0"

class TestAward0(EbbMachineTestCase):
    def test_mode_running_when_selected(self):
        self.start_game()
        self.assertModeNotRunning(AWARD)
        # hit targets so this award is selected
        self.select_award_left(3)
        self.advance_time_and_run(1)
        self.assertModeRunning(AWARD)
        self.select_award_left(1)
        self.assertModeNotRunning(AWARD)

    def test_collected(self):
        self.start_game()