from machine_tests.EbbMachineTestCase import EbbMachineTestCase

NUM_TARGETS = 7
INITIAL_POSITION = 3
SIZE = 1
MOVE_LEFT_SWITCH = "s_flipper_left"
MOVE_RIGHT_SWITCH = "s_flipper_right"
MULTICUE_SHOT_STATE_PLACEHOLDER = "device.shots.sh_multicue.state_name"

class TestMulticue(EbbMachineTestCase):
    def activate_multicue(self):
        self.assertModeRunning('multicue')
        self.assertPlaceholderEvaluates("flash", MULTICUE_SHOT_STATE_PLACEHOLDER)
        self.hit_switch_and_run("s_standup_upper", 1)
        self.assertPlaceholderEvaluates("off", MULTICUE_SHOT_STATE_PLACEHOLDER)

    def assert_multicue_shots(self, active_shot_indices):
        for i in range(0, NUM_TARGETS):
            shot = "sh_multicue_{}".format(i)
            placeholder = "device.shots." + shot + ".state_name"
            if i in active_shot_indices:
                self.assertPlaceholderEvaluates("lit", placeholder)
            else:
                self.assertPlaceholderEvaluates("unlit", placeholder)

    def move_left(self):
        self.hit_and_release_switch(MOVE_LEFT_SWITCH)
        self.advance_time_and_run(1)

    def move_right(self):
        self.hit_and_release_switch(MOVE_RIGHT_SWITCH)
        self.advance_time_and_run(1)

    def test_multicue(self):
        self.start_game()
        self.activate_multicue()

        # some shots are available for multicue when it's activated, others unlit
        self.assert_multicue_shots([2, 3, 4])

    def test_moving_multicue(self):
        self.start_game()
        self.activate_multicue()

        # can move down 1 position with left flipper
        self.move_left()
        self.assertPlayerVarEqual(2, "multicue_position")
        self.assert_multicue_shots([1, 2, 3])
        # can move up 1 position with right flipper
        self.move_right()
        self.assert_multicue_shots([2, 3, 4])
        self.assertPlayerVarEqual(3, "multicue_position")

        # shots 'wrap' around to the other side at the bottom
        self.move_left()
        self.move_left()
        self.move_left()
        self.assertPlayerVarEqual(0, "multicue_position")
        self.assert_multicue_shots([0, 1, 6])

        # and wrap at top
        self.move_right()
        self.move_right()
        self.move_right()
        self.move_right()
        self.move_right()
        self.move_right()
        self.assertPlayerVarEqual(6, "multicue_position")
        self.assert_multicue_shots([0, 5, 6])

    def assert_progress(self, progress):
        self.assertEqual(7, len(progress))
        for i, p in enumerate(progress):
            self.assertPlayerVarEqual(p, "tl_{}_progress".format(i))

    def test_hitting_multicue(self):
        self.start_game()
        self.activate_multicue()

        # TODO: verify shots too
        self.assert_progress([0, 0, 0, 0, 0, 0, 0])
        self.hit_ball_target(3)
        self.assert_progress([0, 0, 1, 1, 1, 0, 0])


    def test_hitting_multicue_offcenter_left(self):
        self.start_game()
        self.activate_multicue()

        self.assert_progress([0, 0, 0, 0, 0, 0, 0])
        self.hit_ball_target(2)
        self.assert_progress([0, 0, 1, 1, 1, 0, 0])

    def test_hitting_multicue_offcenter_left(self):
        self.start_game()
        self.activate_multicue()

        self.assert_progress([0, 0, 0, 0, 0, 0, 0])
        self.hit_ball_target(4)
        self.assert_progress([0, 0, 1, 1, 1, 0, 0])
