from machine_tests.EbbMachineTestCase import EbbMachineTestCase

class TestAward0(EbbMachineTestCase):
    def test_mode_running_when_selected(self):
        self.start_game()
        self.assertModeNotRunning("award_0")
        # hit targets so this award is selected
        self.select_award_left(3)
        self.advance_time_and_run(1)
        self.assertModeRunning("award_0")
        self.select_award_left(1)
        self.advance_time_and_run(1)
        self.assertModeNotRunning("award_0")
