from machine_tests.EbbMachineTestCase import EbbMachineTestCase

class TestEarth(EbbMachineTestCase):
    def test_earth_running_on_game_start(self):
        self.start_game()
        self.assertModeRunning("earth")

    def test_earth_disabled_after_rack_collect(self):
        self.mock_event("saucer_collect_rack_show_start")
        self.mock_event("sh_racks_qualify_collect_hit")
        self.mock_event("sh_racks_collect_hit")

        self.start_game()

        self.collect_earth_rack()
        self.assertEventCalled("sh_racks_qualify_collect_hit")
        self.assertEventCalled("sh_racks_collect_hit")
        self.assertEventCalled("saucer_collect_rack_show_start")
        self.assertModeNotRunning("earth")

    def test_hitting_ball_posts_announce_event(self):
        self.mock_event("announce_ball_collected")
        self.start_game()
        self.hit_ball_targets(1)
        self.assertEventCalled("announce_ball_collected")

