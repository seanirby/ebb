from machine_tests.EbbMachineTestCase import EbbMachineTestCase

class TestJackpot(EbbMachineTestCase):
    def test_jackpot_is_disabled_outside_multiball(self):
        self.start_game()
        self.assertModeNotRunning("jackpot")

    def test_jackpot_is_enabled_during_multiball(self):
        self.start_game()
        self.start_mball()
        self.assertModeRunning("jackpot")

    def test_jackpot_disabled_after_multiball(self):
        self.start_game()
        self.start_mball()
        self.advance_time_and_run(100)
        self.drain_balls(1, 1)
        self.assertModeNotRunning("jackpot")

    def test_right_drop_lights_when_hook_shot_hit(self):
        self.start_game()
        self.start_mball()
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_qualify.enabled")
        self.hit_and_release_switch_and_run("s_hook", .1)
        self.assertPlaceholderEvaluates(True, "device.shots.sh_jackpot_qualify.enabled")


    def test_jackpot_collect_lights_when_right_drop_hit(self):
        self.start_game()
        self.start_mball()
        self.hit_and_release_switch_and_run("s_hook", .1)
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_collect.enabled")
        self.hit_switch_and_run("s_drop_right", .1)
        self.assertPlaceholderEvaluates(True, "device.shots.sh_jackpot_collect.enabled")

    def test_jackpot_lights_disabled_if_collected(self):
        self.start_game()
        self.start_mball()
        self.hit_and_release_switch_and_run("s_hook", .1)
        self.hit_switch_and_run("s_drop_right", .1)
        self.hit_switch_and_run("s_saucer", 1.5)
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_qualify.enabled")
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_collect.enabled")

    def test_jackpot_lights_disabled_if_uncollected(self):
        self.start_game()
        self.start_mball()
        self.hit_and_release_switch_and_run("s_hook", .1)
        self.hit_switch_and_run("s_drop_right", .1)
        self.advance_time_and_run(10)
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_qualify.enabled")
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_collect.enabled")

    def test_jackpot_collect_increases_score(self):
        pass
