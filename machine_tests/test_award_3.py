from machine_tests.EbbMachineTestCase import EbbMachineTestCase

AWARD = "award_3"

class TestAward3(EbbMachineTestCase):
    def test_mode_running_when_selected(self):
        self.start_game()
        # This is mode selected on game startup
        self.assertModeRunning(AWARD)
        self.select_award_left(1)
        self.assertModeNotRunning(AWARD)

    def test_collected(self):
        self.start_game()
