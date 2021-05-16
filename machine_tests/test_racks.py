from machine_tests.EbbMachineTestCase import EbbMachineTestCase

NUM_TARGETS = 7

class TestRacks(EbbMachineTestCase):
    def hit_all_ball_targets(self):
        for i in range(0, NUM_TARGETS):
            self.hit_ball_target(i)

    def test_rack_initial_state(self):
        pass

    def test_rack_collected(self):
        self.mock_event("racks_rack_collected")
        self.start_game()
        self.hit_all_ball_targets()
        self.collect_rack()
        self.assertPlayerVarEqual(1, "racks")
        self.assertEventCalled("racks_rack_collected", 1)