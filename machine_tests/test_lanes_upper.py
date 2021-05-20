from machine_tests.EbbMachineTestCase import EbbMachineTestCase

LANE_LEFT_PLACEHOLDER = "device.shots.sh_lanes_upper_left.state_name"
LANE_CENTER_PLACEHOLDER = "device.shots.sh_lanes_upper_center.state_name"
LANE_RIGHT_PLACEHOLDER = "device.shots.sh_lanes_upper_right.state_name"

PLACEHOLDERS = [
    LANE_LEFT_PLACEHOLDER,
    LANE_CENTER_PLACEHOLDER,
    LANE_RIGHT_PLACEHOLDER
]

LANE_STATES = [
    "unlit",
    "lit"
]

class TestLanesUpper(EbbMachineTestCase):
    def assert_lanes(self, state):
        for i, placeholder in enumerate(PLACEHOLDERS):
            self.assertPlaceholderEvaluates(LANE_STATES[state[i]], placeholder)

    def test_upper_lanes_unlit_on_game_start(self):
        self.start_game()
        self.assertModeRunning("lanes_upper")
        self.assert_lanes([0, 0, 0])

    def test_lane_is_lit_when_collected(self):
        self.start_game()

        self.hit_and_release_switch_and_run('s_upper_lane_left')
        self.assert_lanes([1, 0, 0])
        self.hit_and_release_switch_and_run('s_upper_lane_left')
        self.assert_lanes([1, 0, 0])

        self.hit_and_release_switch_and_run('s_upper_lane_center')
        self.assert_lanes([1, 1, 0])
        self.hit_and_release_switch_and_run('s_upper_lane_center')
        self.assert_lanes([1, 1, 0])

        # TODO: need to verify a little show is played when all complete
        # self.hit_and_release_switch_and_run('s_upper_lane_right')
        # self.assert_lanes([1, 1, 1])
        # self.hit_and_release_switch_and_run('s_upper_lane_right')
        # self.assert_lanes([1, 1, 1])


    def test_lanes_should_rotate_left_when_flipper_is_pressed(self):
        self.start_game()

        self.hit_and_release_switch_and_run('s_upper_lane_left')
        self.assert_lanes([1, 0, 0])

        self.flip_left()
        # wraps to right side
        self.assert_lanes([0, 0, 1])

        # back to original position
        self.flip_left(2)
        self.assert_lanes([1, 0, 0])


    def test_lanes_should_rotate_right_when_flipper_is_pressed(self):
        self.start_game()

        self.hit_and_release_switch_and_run('s_upper_lane_right')
        self.assert_lanes([0, 0, 1])

        self.flip_right()
        # wraps to right side
        self.assert_lanes([1, 0, 0])

        # back to original position
        self.flip_right(2)
        self.assert_lanes([0, 0, 1])

    def test_bonus_x_is_incremented_when_all_lanes_collected(self):
        self.mock_event("increment_bonus_x")
        self.start_game()
        self.hit_and_release_switch_and_run("s_upper_lane_left")
        self.hit_and_release_switch_and_run("s_upper_lane_center")
        self.hit_and_release_switch_and_run("s_upper_lane_right")
        self.assertEventCalled("increment_bonus_x", 1)

    def test_lanes_are_unlit_when_all_lanes_collected(self):
        self.start_game()
        self.hit_and_release_switch_and_run("s_upper_lane_left")
        self.hit_and_release_switch_and_run("s_upper_lane_center")
        self.hit_and_release_switch_and_run("s_upper_lane_right")
        # TODO: also assert that some success show ran
        self.advance_time_and_run(1)
        self.assert_lanes([0, 0, 0])
