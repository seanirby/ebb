from mpf.tests.MpfMachineTestCase import MpfMachineTestCase


class TestMultiball(MpfMachineTestCase):
    def test_start_game(self):
        # self.hit_switch_and_run("s_trough_0", .1)
        # self.hit_switch_and_run("s_trough_1", .1)
        self.advance_time_and_run(10)
        self.assertNumBallsKnown(2)
        self.assertFalse(self.machine.game)

        self.hit_and_release_switch("s_start")
        self.advance_time_and_run(10)
        self.assertTrue(self.machine.game)
        self.hit_and_release_switch("s_orbit")
        self.assertEqual(1, self.machine.playfield.available_balls)
        self.assertPlaceholderEvaluates(True, "device.diverters.div_drop_upper.active")


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
        self.test_start_game()
        self.assert_mball_qualifying()

    def hit_upper_drop(self):
        self.hit_and_release_switch("s_drop_upper")
        self.advance_time_and_run(5)

    def test_mball_qualifying_to_lock(self):
        self.test_start_game()
        self.assert_mball_qualifying()
        # start of game, two already qualified by default
        self.assertPlaceholderEvaluates("two_qualified", "device.shots.sh_qualify_lock.state_name")
        # hitting upper drop makes lock qualified
        self.hit_upper_drop()
        self.assertPlaceholderEvaluates("lock_qualified", "device.shots.sh_qualify_lock.state_name")

    def test_mball_qualifying_with_drain(self):
        self.test_start_game()
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
        self.test_start_game()
        self.assert_mball_qualifying()
        self.hit_upper_drop()
        self.assertPlaceholderEvaluates("lock_qualified", "device.shots.sh_qualify_lock.state_name")
        self.advance_time_and_run(40)

        self.hit_switch_and_run("s_trough_0", 10)

        self.assertPlayerVarEqual(2, "ball")
        self.assertPlaceholderEvaluates("lock_qualified", "device.shots.sh_qualify_lock.state_name")

    def test_mball(self):
        self.test_start_game()
        self.assert_mball_qualifying()
        self.assertPlaceholderEvaluates(True, "device.diverters.div_drop_upper.active")

        self.hit_upper_drop()

        # self.assertPlaceholderEvaluates(False, "device.diverters.div_drop_upper.enabled")
        self.assert_mball_qualifying()
        self.assertPlaceholderEvaluates("lock_qualified", "device.shots.sh_qualify_lock.state_name")
        self.assertPlaceholderEvaluates(False, "device.diverters.div_drop_upper.active")

        # hit scoop
        self.hit_switch_and_run("s_scoop", 5)
        self.assert_mball_locked()
        self.assertPlaceholderEvaluates(True, "device.diverters.div_drop_upper.active")
        self.assertPlaceholderEvaluates(1, "device.multiball_locks.scoop.locked_balls")
        self.hit_upper_drop()
        self.assert_mball_running()

        self.advance_time_and_run(50)
        self.hit_switch_and_run("s_trough_0", 10)
        self.assert_mball_qualifying()
        self.assertPlaceholderEvaluates("one_qualified", "device.shots.sh_qualify_lock.state_name")
