from machine_tests.EbbMachineTestCase import EbbMachineTestCase

DROP_UPPER_DOWN_PLACEHOLDER = "device.drop_targets.upper.complete"

class TestMultiball(EbbMachineTestCase):
    def assert_mball_qualifying(self):
        self.assertModeRunning("mball_qualifying")
        self.assertModeNotRunning("mball_startup")
        self.assertModeNotRunning("mball_locked")
        self.assertModeNotRunning("mball")

    def assert_mball_running(self):
        self.assertModeNotRunning("mball_qualifying")
        self.assertModeNotRunning("mball_locked")
        self.assertModeRunning("mball")

    def assert_mball_locked(self):
        self.assertModeNotRunning("mball_qualifying")
        self.assertModeRunning("mball_locked")
        self.assertModeNotRunning("mball")

    def test_mball_qualifying(self):
        self.start_game()
        self.assert_mball_qualifying()

    def hit_upper_drop(self):
        self.assertModeRunning("orbit_left")
        self.assertPlaceholderEvaluates(False, DROP_UPPER_DOWN_PLACEHOLDER)
        self.hit_and_release_switch("s_spinner")
        self.advance_time_and_run(.1)
        self.hit_and_release_switch("s_drop_upper")
        self.advance_time_and_run(1)

    def hit_scoop(self):
        self.assertModeRunning("orbit_left")
        self.assertPlaceholderEvaluates(True, DROP_UPPER_DOWN_PLACEHOLDER)
        self.post_event("s_spinner_active")
        self.hit_switch_and_run("s_scoop", 4)
        self.advance_time_and_run()

    def test_mball_qualifying_to_lock(self):
        self.start_game()
        self.assert_mball_qualifying()
        # start of game, two already qualified by default
        self.assertPlaceholderEvaluates("two_qualified", "device.shots.sh_qualify_lock.state_name")
        # hitting upper drop makes lock qualified
        self.hit_upper_drop()
        self.assertPlaceholderEvaluates("lock_qualified", "device.shots.sh_qualify_lock.state_name")
        self.assertPlaceholderEvaluates(True, DROP_UPPER_DOWN_PLACEHOLDER)

    def test_mball_qualifying_with_drain(self):
        self.start_game()
        self.assert_mball_qualifying()
        # start of game, two already qualified by default
        self.assertPlaceholderEvaluates("two_qualified", "device.shots.sh_qualify_lock.state_name")
        # make sure ball save is over
        self.advance_time_and_run(40)
        self.hit_switch_and_run("s_trough_0", 10)
        # make sure drain happened
        self.assertPlayerVarEqual(2, "ball")
        self.assertPlaceholderEvaluates("two_qualified", "device.shots.sh_qualify_lock.state_name")

    def test_mball_qualifying_to_locked_with_drain(self):
        self.start_game()
        self.assert_mball_qualifying()
        self.hit_upper_drop()
        self.assertPlaceholderEvaluates("lock_qualified", "device.shots.sh_qualify_lock.state_name")
        self.advance_time_and_run(40)

        self.hit_switch_and_run("s_trough_0", 10)

        self.assertPlayerVarEqual(2, "ball")
        self.assertPlaceholderEvaluates("lock_qualified", "device.shots.sh_qualify_lock.state_name")

    def test_mball(self):
        self.mock_event("sh_orbit_left_drop_hit")
        self.mock_event("sh_orbit_left_scoop_hit")
        self.start_game()
        self.assert_mball_qualifying()
        self.assertPlaceholderEvaluates(False, DROP_UPPER_DOWN_PLACEHOLDER)

        self.assertEventCalled("sh_orbit_left_drop_hit", 0)
        self.hit_upper_drop()
        self.assertEventCalled("sh_orbit_left_drop_hit", 1)

        self.assert_mball_qualifying()
        self.assertPlaceholderEvaluates("lock_qualified", "device.shots.sh_qualify_lock.state_name")
        self.assertPlaceholderEvaluates(True, DROP_UPPER_DOWN_PLACEHOLDER)

        # hit scoop
        self.assertEventCalled("sh_orbit_left_scoop_hit", 0)
        self.hit_scoop()
        self.assertEventCalled("sh_orbit_left_scoop_hit", 1)
        self.assert_mball_locked()
        self.assertPlaceholderEvaluates(False, DROP_UPPER_DOWN_PLACEHOLDER)
        self.assertPlaceholderEvaluates(1, "device.multiball_locks.scoop.locked_balls")

        self.hit_and_release_switch("s_spinner")
        self.advance_time_and_run(.1)
        self.hit_and_release_switch("s_drop_upper")
        self.advance_time_and_run()
        self.assertEventCalled("sh_orbit_left_drop_hit", 2)
        self.assertPlaceholderEvaluates(True, DROP_UPPER_DOWN_PLACEHOLDER)
        self.advance_time_and_run(2)
        self.assertPlaceholderEvaluates(True, DROP_UPPER_DOWN_PLACEHOLDER)

        self.advance_time_and_run(50)
        self.hit_switch_and_run("s_trough_0", 10)
        self.assert_mball_qualifying()
        self.assertPlaceholderEvaluates("one_qualified", "device.shots.sh_qualify_lock.state_name")
