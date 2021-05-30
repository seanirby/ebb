from machine_tests.EbbMachineTestCase import EbbMachineTestCase

AWARD = "award_4"

class TestAward4(EbbMachineTestCase):
    def test_mode_running_when_selected(self):
        self.start_game()
        self.assertModeNotRunning(AWARD)
        # hit targets so this award is selected
        self.select_award_left(6)
        self.advance_time_and_run(1)
        self.assertModeRunning(AWARD)
        self.select_award_left(1)
        self.assertModeNotRunning(AWARD)

    def test_collected(self):
        self.mock_event("awards_award_collected")
        self.mock_event("spinner_qualified_from_award")
        self.start_game()
        self.select_award_right(1)
        self.advance_time_and_run(1)
        self.assertModeRunning(AWARD)
        self.collect_award()
        self.advance_time_and_run(5)
        self.assertEventCalled("awards_award_collected", 1)
        self.assertEventCalled("spinner_qualified_from_award", 1)
