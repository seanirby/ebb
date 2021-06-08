from machine_tests.EbbMachineTestCase import EbbMachineTestCase, MAX_BALLS

LEFT_OUTLANE_ENABLED_PLACEHOLDER = "device.shots.sh_scratch_guards_left.enabled"
RIGHT_OUTLANE_ENABLED_PLACEHOLDER = "device.shots.sh_scratch_guards_right.enabled"
LEFT_SAVE_ENABLED_PLACEHOLDER = "device.ball_saves.scratch_guards_left.enabled"
RIGHT_SAVE_ENABLED_PLACEHOLDER = "device.ball_saves.scratch_guards_right.enabled"

class TestScratchGuards(EbbMachineTestCase):
    def enable_scratch_guard(self):
        # Scratch Guard is selected at game start
        # self.select_award_left(1)
        self.collect_award()

    def test_lights_outlanes_when_enabled(self):
        self.start_game()
        self.assertModeRunning("scratch_guards")
        self.assertPlaceholderEvaluates(False, LEFT_OUTLANE_ENABLED_PLACEHOLDER)
        self.assertPlaceholderEvaluates(False, RIGHT_OUTLANE_ENABLED_PLACEHOLDER)
        self.assertPlaceholderEvaluates(False, LEFT_SAVE_ENABLED_PLACEHOLDER)
        self.assertPlaceholderEvaluates(False, RIGHT_SAVE_ENABLED_PLACEHOLDER)
        self.enable_scratch_guard()
        self.assertPlaceholderEvaluates(True, LEFT_OUTLANE_ENABLED_PLACEHOLDER)
        self.assertPlaceholderEvaluates(True, RIGHT_OUTLANE_ENABLED_PLACEHOLDER)
        # The save isn't active until you actually roll over the outlane
        self.assertPlaceholderEvaluates(False, LEFT_SAVE_ENABLED_PLACEHOLDER)
        self.assertPlaceholderEvaluates(False, RIGHT_SAVE_ENABLED_PLACEHOLDER)

    def test_ball_saves_left(self):
        self.start_game()
        self.enable_scratch_guard()
        self.advance_time_and_run(10)
        self.hit_and_release_switch("s_outlane_left")
        self.advance_time_and_run(.1)
        self.assertPlaceholderEvaluates(False, LEFT_SAVE_ENABLED_PLACEHOLDER)
        self.assertSwitchState("s_trough_1", True)
        self.assertSwitchState("s_trough_0", False)
        # drain ball
        self.drain_balls()
        self.activate_playfield()
        # still on ball 1
        self.assertPlayerVarEqual(1, "ball")
        self.assertBallsOnPlayfield(1)
        self.assertEqual(MAX_BALLS-1, self.machine.ball_devices["bd_trough"].available_balls)
        self.assertPlaceholderEvaluates(False, LEFT_SAVE_ENABLED_PLACEHOLDER)

    def test_ball_saves_right(self):
        self.start_game()
        self.enable_scratch_guard()
        self.advance_time_and_run(10)
        self.hit_and_release_switch("s_outlane_left")
        self.advance_time_and_run(.1)
        self.assertSwitchState("s_trough_1", True)
        self.assertSwitchState("s_trough_0", False)
        # drain ball
        self.drain_balls()
        self.activate_playfield()
        # still on ball 1
        self.assertPlayerVarEqual(1, "ball")
        self.assertBallsOnPlayfield(1)
        self.assertEqual(MAX_BALLS-1, self.machine.ball_devices["bd_trough"].available_balls)
        self.assertPlaceholderEvaluates(False, RIGHT_SAVE_ENABLED_PLACEHOLDER)

    def test_disabled_when_both_saves_used(self):
        self.start_game()
        self.enable_scratch_guard()

        # use left save
        self.advance_time_and_run(10)
        self.hit_and_release_switch("s_outlane_left")
        self.advance_time_and_run(.1)
        self.assertPlaceholderEvaluates(False, LEFT_OUTLANE_ENABLED_PLACEHOLDER)
        self.assertSwitchState("s_trough_1", True)
        self.assertSwitchState("s_trough_0", False)
        # drain ball
        self.drain_balls()
        self.activate_playfield()
        # still on ball 1
        self.assertPlayerVarEqual(1, "ball")
        self.assertBallsOnPlayfield(1)
        self.assertEqual(MAX_BALLS-1, self.machine.ball_devices["bd_trough"].available_balls)
        self.assertPlaceholderEvaluates(False, LEFT_SAVE_ENABLED_PLACEHOLDER)

        # use right save
        self.hit_and_release_switch("s_outlane_right")
        self.advance_time_and_run(.1)
        self.assertSwitchState("s_trough_1", True)
        self.assertSwitchState("s_trough_0", False)
        # drain ball
        self.drain_balls()
        self.activate_playfield()
        # still on ball 1
        self.assertPlayerVarEqual(1, "ball")
        self.assertBallsOnPlayfield(1)
        self.assertEqual(MAX_BALLS-1, self.machine.ball_devices["bd_trough"].available_balls)
        self.assertPlaceholderEvaluates(False, RIGHT_SAVE_ENABLED_PLACEHOLDER)
        self.assertModeNotRunning("scratch_guards")

    def test_maintains_state_across_balls(self):
        self.start_game()
        self.enable_scratch_guard()
        self.advance_time_and_run(10)
        self.hit_and_release_switch("s_outlane_left")
        self.advance_time_and_run(.1)
        self.assertPlaceholderEvaluates(False, LEFT_OUTLANE_ENABLED_PLACEHOLDER)
        self.assertSwitchState("s_trough_1", True)
        self.assertSwitchState("s_trough_0", False)
        # drain ball
        self.drain_balls()
        self.activate_playfield()
        # still on ball 1
        self.assertPlayerVarEqual(1, "ball")
        self.assertBallsOnPlayfield(1)
        self.assertEqual(MAX_BALLS-1, self.machine.ball_devices["bd_trough"].available_balls)
        self.assertPlaceholderEvaluates(False, LEFT_SAVE_ENABLED_PLACEHOLDER)

        self.drain_balls()
        self.activate_playfield()
        self.assertPlayerVarEqual(2, "ball")
        self.assertModeRunning("scratch_guards")
        self.assertPlaceholderEvaluates(True, RIGHT_OUTLANE_ENABLED_PLACEHOLDER)
