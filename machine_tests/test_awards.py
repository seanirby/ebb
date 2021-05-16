from machine_tests.EbbMachineTestCase import EbbMachineTestCase

AWARD_SELECTED = "award_selected"

class TestAwards(EbbMachineTestCase):
    def test_conditions_on_ball_start(self):
        self.start_game()
        self.assertModeRunning('awards')
        self.assertPlayerVarEqual(3, AWARD_SELECTED)

    # TODO: Fix ordering of awards, should be 0 indexed from left to right
    def test_selecting_awards(self):
        self.start_game()
        self.select_award_left(1)
        self.assertPlayerVarEqual(2, AWARD_SELECTED)
        self.select_award_right(1)
        self.assertPlayerVarEqual(3, AWARD_SELECTED)
        # selection wraps
        self.select_award_left(4)
        self.assertPlayerVarEqual(6, AWARD_SELECTED)
        self.select_award_right(1)
        self.assertPlayerVarEqual(0, AWARD_SELECTED)

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


    def test_collecting_awards(self):
        self.start_game()
        self.assertPlayerVarEqual(0, "award_3_collected")
        self.collect_award()
        self.advance_time_and_run(5)
        self.assertPlayerVarEqual(1, "award_3_collected")
