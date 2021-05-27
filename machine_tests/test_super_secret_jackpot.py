from machine_tests.EbbMachineTestCase import EbbMachineTestCase

class TestJackpot(EbbMachineTestCase):
    def test_jackpot_is_disabled_outside_multiball(self):
        self.start_game()
        self.assertModeNotRunning("jackpot")

    def test_jackpot_is_enabled_during_multiball(self):
        self.start_game()
        self.start_mball()
        self.assertModeRunning('mball')
        self.assertModeRunning('jackpot')

    def test_jackpot_disabled_after_multiball(self):
        self.start_game()
        self.start_mball()
        self.assertModeRunning('mball')
        self.assertModeRunning('jackpot')
        self.advance_time_and_run(100)
        self.drain_balls(0, 1)
        self.advance_time_and_run(5)
        self.assertModeNotRunning('jackpot')

    # TODO: this test probably unnecessary
    def test_jackpot_disabled_when_ball_ends(self):
        self.start_game()
        self.start_mball()
        self.assertModeRunning('mball')
        self.assertModeRunning('jackpot')
        self.advance_time_and_run(100)
        self.drain_balls(0, 1)
        self.drain_balls(0, 1)
        self.advance_time_and_run(5)
        self.assertModeNotRunning('jackpot')

    # TODO: implement drop target assertions once I've figured out why they aren't working in tests
    def test_drop_lights_when_hook_shot_hit(self):
        self.start_game()
        self.start_mball()
        # self.assertPlaceholderEvaluates(True, "device.drop_targets.right.complete")
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_qualify.enabled")
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_collect.enabled")

        self.hit_and_release_switch_and_run('s_hook', .1)
        # self.assertPlaceholderEvaluates(False, "device.drop_targets.right.complete")
        self.assertPlaceholderEvaluates('flash', "device.shots.sh_jackpot_qualify.state_name")
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_collect.enabled")

    def test_jackpot_collect_lights_when_right_drop_hit(self):
        self.start_game()
        self.start_mball()
        # self.assertPlaceholderEvaluates(True, "device.drop_targets.right.complete")
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_qualify.enabled")
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_collect.enabled")

        self.hit_and_release_switch_and_run('s_hook', .1)
        # self.assertPlaceholderEvaluates(False, "device.drop_targets.right.complete")
        self.assertPlaceholderEvaluates('flash', "device.shots.sh_jackpot_qualify.state_name")
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_collect.enabled")

        self.hit_switch_and_run('s_drop_right', .1)
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_qualify.enabled")
        self.assertPlaceholderEvaluates('flash', "device.shots.sh_jackpot_collect.state_name")

    def test_jackpot_lights_disabled_if_collected(self):
        self.start_game()
        self.start_mball()
        # self.assertPlaceholderEvaluates(True, "device.drop_targets.right.complete")
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_qualify.enabled")
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_collect.enabled")

        self.hit_and_release_switch_and_run('s_hook', .1)
        # self.assertPlaceholderEvaluates(False, "device.drop_targets.right.complete")
        self.assertPlaceholderEvaluates('flash', "device.shots.sh_jackpot_qualify.state_name")
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_collect.enabled")

        self.hit_switch_and_run('s_drop_right', .1)
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_qualify.enabled")
        self.assertPlaceholderEvaluates('flash', "device.shots.sh_jackpot_collect.state_name")

        # TODO: Update timing to be more responsive because ~1.5 seconds is too long
        self.hit_switch_and_run('s_saucer', 1.5)
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_qualify.enabled")
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_collect.enabled")

    def test_jackpot_lights_disabled_if_uncollected(self):
        self.start_game()
        self.start_mball()
        # self.assertPlaceholderEvaluates(True, "device.drop_targets.right.complete")
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_qualify.enabled")
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_collect.enabled")

        self.hit_and_release_switch_and_run('s_hook', .1)
        # self.assertPlaceholderEvaluates(False, "device.drop_targets.right.complete")
        self.assertPlaceholderEvaluates('flash', "device.shots.sh_jackpot_qualify.state_name")
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_collect.enabled")

        self.hit_switch_and_run('s_drop_right', .1)
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_qualify.enabled")
        self.assertPlaceholderEvaluates('flash', "device.shots.sh_jackpot_collect.state_name")

        # TODO: Update timing to be more responsive because ~1.5 seconds is too long
        self.advance_time_and_run(10)
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_qualify.enabled")
        self.assertPlaceholderEvaluates(False, "device.shots.sh_jackpot_collect.enabled")