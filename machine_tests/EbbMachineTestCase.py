from mpf.tests.MpfMachineTestCase import MpfMachineTestCase


class EbbMachineTestCase(MpfMachineTestCase):
    def select_award_left(self, times):
        # TODO: whats the correct syntax for a for loop where you dont use the index
        for i in range(0, times):
            self.hit_and_release_switch("s_thin_standup_left")
            self.advance_time_and_run(.1)

    def select_award_right(self, times):
        # TODO: whats the correct syntax for a for loop where you dont use the index
        for i in range(0, times):
            self.hit_and_release_switch("s_thin_standup_right")
            self.advance_time_and_run(.1)

    # TODO: Need to update MPF Smart virtual platform so drop reset/knockdown events fire coils
    def start_game(self):
        self.hit_switch_and_run("s_trough_0", 0)
        self.hit_switch_and_run("s_trough_1", 1)
        self.advance_time_and_run(10)
        self.assertFalse(self.machine.game)
        self.assertEqual(2, self.machine.ball_devices["bd_trough"].available_balls)
        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(10)
        self.assertTrue(self.machine.game)
        self.hit_switch_and_run("s_orbit", .1)
        self.release_switch_and_run("s_orbit", .1)

        self.advance_time_and_run(100)

        self.assertBallsOnPlayfield(1)
        self.assertNumBallsKnown(2)
        self.assertEqual("idle", self.machine.ball_devices["bd_trough"].state)
        self.assertEqual("idle", self.machine.ball_devices["bd_plunger"].state)
        self.assertEqual(1, self.machine.ball_devices["bd_trough"].available_balls)
        self.assertEqual(1, self.machine.playfield.available_balls)

    def hit_ball_target(self, target_number):
        self.assertTrue(target_number in range(0, 7))
        self.hit_and_release_switch("s_standup_left_{}".format(target_number))

    def collect_award(self):
        # TODO: check drop target state, create diverters for my left/right single drop targets
        self.assertPlaceholderEvaluates("flash", "device.shots.sh_awards_qualify_collect.state_name")
        self.assertPlaceholderEvaluates(False, "device.shots.sh_awards_collect.enabled")
        self.hit_switch_and_run('s_hook', .5)
        self.release_switch_and_run('s_hook', .5)
        # self.machine.events.post('s_hook_active')
        self.assertPlaceholderEvaluates(False, "device.shots.sh_awards_qualify_collect.enabled")
        self.assertPlaceholderEvaluates("flash", "device.shots.sh_awards_collect.state_name")
        # self.assertPlaceholderEvaluates(True, "device.diverters.div_drop_right.active")
        # self.assertPlaceholderEvaluates(False, "device.diverters.div_drop_left.active")
        self.machine.events.post("sh_saucer_debounced_hit")
        # self.assertPlaceholderEvaluates(False, "device.diverters.div_drop_right.active")
        # self.assertPlaceholderEvaluates(True, "device.diverters.div_drop_left.active")
        self.advance_time_and_run(1)


