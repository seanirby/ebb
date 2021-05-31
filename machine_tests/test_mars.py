from machine_tests.EbbMachineTestCase import EbbMachineTestCase, NUM_TARGETS, MAX_PROGRESS

class TestMars(EbbMachineTestCase):
    def activate_mars_multicue(self):
        self.hit_and_release_switch_and_run("s_standup_upper", .1)

    def assert_earth_rack_column(self, column, **kwargs):
        state = kwargs.get("state")
        enabled = kwargs.get("enabled")

        if enabled == None:
            should_assert_enabled = False
        else:
            should_assert_enabled = True

        if state == None:
            should_assert_state = False
        else:
            should_assert_state = True

        for i in range(NUM_TARGETS):
            if should_assert_enabled:
                self.assertPlaceholderEvaluates(enabled, "device.shots.sh_mars_earth_l_{}_{}.enabled".format(i, column))

            if should_assert_state:
                self.assertPlaceholderEvaluates(state, "device.shots.sh_mars_earth_l_{}_{}.state_name".format(i, column))
                

    # def test_mars_not_running_on_game_start(self):
    #     self.start_game()
    #     self.assertModeNotRunning("mars")

    # def test_mars_enabled_after_one_rack_collect(self):
    #     self.start_game()
    #     self.collect_earth_rack()
    #     self.assertModeRunning("mars")

    # def test_mars_disables_regular_multicue(self):
    #     self.start_game()
    #     self.assertPlaceholderEvaluates(True, "device.shots.sh_multicue.enabled")
    #     self.assertPlaceholderEvaluates(False, "device.shots.sh_mars_multicue.enabled")
    #     self.collect_earth_rack()
    #     self.assertPlaceholderEvaluates(False, "device.shots.sh_multicue.enabled")
    #     self.assertPlaceholderEvaluates(True, "device.shots.sh_mars_multicue.enabled")
    #     self.assertPlaceholderEvaluates("flash", "device.shots.sh_mars_multicue.state_name")

    # def test_three_ball_is_flashing(self):
    #     self.start_game()
    #     self.collect_earth_rack()
    #     self.assertPlaceholderEvaluates("flash_one", "device.shots.sh_mars_hurry_up.state_name")

    # def test_hitting_three_ball_four_times_finishes_hurry_up(self):
    #     self.start_game()
    #     self.collect_earth_rack()
    #     self.assertPlaceholderEvaluates(False, "device.timers.mars_hurry_up.running")
    #     self.assertPlaceholderEvaluates("flash_one", "device.shots.sh_mars_hurry_up.state_name")

    #     self.hit_ball_target(2)
    #     self.assertPlaceholderEvaluates("flash_two", "device.shots.sh_mars_hurry_up.state_name")
    #     self.assertPlaceholderEvaluates(True, "device.timers.mars_hurry_up.running")

    #     self.hit_ball_target(2)
    #     self.assertPlaceholderEvaluates("flash_three", "device.shots.sh_mars_hurry_up.state_name")
    #     self.assertPlaceholderEvaluates(True, "device.timers.mars_hurry_up.running")

    #     self.hit_ball_target(2)
    #     self.assertPlaceholderEvaluates("flash_four", "device.shots.sh_mars_hurry_up.state_name")
    #     self.assertPlaceholderEvaluates(True, "device.timers.mars_hurry_up.running")

    #     self.assertPlaceholderEvaluates(False, "device.shots.sh_racks_qualify_collect.enabled")
    #     self.hit_ball_target(2)
    #     # TODO: Play a show that fills in grid with red lights, how do we assert this?
    #     self.assertPlaceholderEvaluates(True, "device.shots.sh_racks_qualify_collect.enabled")
    #     self.assertPlaceholderEvaluates(False, "device.timers.mars_hurry_up.running")

    # def test_hurry_up_shot_disabled_on_timeout(self):
    #     self.start_game()
    #     self.collect_earth_rack()
    #     self.assertPlaceholderEvaluates(False, "device.timers.mars_hurry_up.running")
    #     self.assertPlaceholderEvaluates("flash_one", "device.shots.sh_mars_hurry_up.state_name")

    #     self.hit_ball_target(2)
    #     self.assertPlaceholderEvaluates("flash_two", "device.shots.sh_mars_hurry_up.state_name")
    #     self.assertPlaceholderEvaluates(True, "device.timers.mars_hurry_up.running")
    #     self.advance_time_and_run(30)
    #     self.assertPlaceholderEvaluates(False, "device.timers.mars_hurry_up.running")
    #     self.assertPlaceholderEvaluates(False, "device.shots.sh_mars_hurry_up.enabled")


    # def test_multicue_restarts_hurry_up(self):
    #     self.start_game()
    #     self.collect_earth_rack()
    #     self.assertPlaceholderEvaluates(False, "device.timers.mars_hurry_up.running")
    #     self.assertPlaceholderEvaluates("flash_one", "device.shots.sh_mars_hurry_up.state_name")

    #     self.hit_ball_target(2)
    #     self.assertPlaceholderEvaluates("flash_two", "device.shots.sh_mars_hurry_up.state_name")
    #     self.assertPlaceholderEvaluates(True, "device.timers.mars_hurry_up.running")
    #     self.advance_time_and_run(30)
    #     self.assertPlaceholderEvaluates(False, "device.timers.mars_hurry_up.running")
    #     self.assertPlaceholderEvaluates(False, "device.shots.sh_mars_hurry_up.enabled")

    #     self.activate_mars_multicue()
    #     self.assertPlaceholderEvaluates(True, "device.timers.mars_hurry_up.running")
    #     self.assertPlaceholderEvaluates(True, "device.shots.sh_mars_hurry_up.enabled")
    #     self.assertPlaceholderEvaluates("flash_two", "device.shots.sh_mars_hurry_up.state_name")
        
    # def test_earth_timeout_collect_rack(self):
    #     self.mock_event("mars_enable_earth_rules")

    #     self.start_game()
    #     self.collect_earth_rack()
    #     self.assertPlaceholderEvaluates(False, "device.timers.mars_hurry_up.running")
    #     self.assertPlaceholderEvaluates("flash_one", "device.shots.sh_mars_hurry_up.state_name")

    #     self.hit_ball_target(2)
    #     self.advance_time_and_run(30)
    #     self.assertPlaceholderEvaluates(False, "device.shots.sh_mars_hurry_up.enabled")
    #     self.assertPlaceholderEvaluates(False, "device.shots.sh_racks_qualify_collect.enabled")
    #     self.assertEventCalled("mars_enable_earth_rules")
    #     self.assert_earth_rack_column(0, state="flash", enabled=True)

    #     self.hit_ball_targets()
    #     self.assert_earth_rack_column(0, state="on", enabled=True)
    #     self.assertPlaceholderEvaluates(True, "device.shots.sh_racks_qualify_collect.enabled")

    # def test_earth_timeout_multicue_restarts_hurry_up(self):
    #     self.mock_event("mars_disable_earth_rules")

    #     self.start_game()
    #     self.collect_earth_rack()

    #     self.hit_ball_target(2)
    #     self.assert_earth_rack_column(0, enabled=False)

    #     # wait for timer to expire
    #     self.advance_time_and_run(30)
    #     self.assert_earth_rack_column(0, state="flash", enabled=True)
    #     self.assertPlaceholderEvaluates(True, "device.shots.sh_mars_multicue.enabled")
    #     self.assertPlaceholderEvaluates(False, "device.timers.mars_hurry_up.running")

    #     # hit mars multicue
    #     self.assertEventNotCalled("mars_disable_earth_rules")
    #     self.activate_mars_multicue()
    #     self.assertEventCalled("mars_disable_earth_rules")
    #     self.assert_earth_rack_column(0, enabled=False)
    #     self.assertPlaceholderEvaluates(True, "device.timers.mars_hurry_up.running")
        
    #     # timeout takes you back to earth
    #     self.advance_time_and_run(30)
    #     self.assert_earth_rack_column(0, enabled=True)

    # def test_qualifying_earth_rack_only_applies_in_earth_rules(self):
    #     self.start_game()
    #     self.collect_earth_rack()

    #     self.hit_ball_target(2)
    #     self.assert_earth_rack_column(0, enabled=False)

    #     # wait for timer to expire
    #     self.advance_time_and_run(30)
    #     self.hit_ball_targets()
    #     self.assertPlaceholderEvaluates(True, "device.shots.sh_racks_qualify_collect.enabled")

    #     # hit mars multicue
    #     self.activate_mars_multicue()
        
    #     # timeout takes you back to earth
    #     self.assertPlaceholderEvaluates(False, "device.shots.sh_racks_qualify_collect.enabled")

    def test_mars_before_hurry_up_has_multicue_disabled(self):
        self.start_game()

        # self.collect_earth_rack()
        self.assertPlaceholderEvaluates(False, "device.shots.sh_multicue.enabled")
        self.assertPlaceholderEvaluates(False, "device.shots.sh_mars_multicue.enabled")
        self.hit_and_release_switch_and_run("s_standup_upper", .1)
        self.assertPlaceholderEvaluates(False, "device.shots.sh_multicue.enabled")
        self.assertPlaceholderEvaluates(False, "device.shots.sh_mars_multicue.enabled")




