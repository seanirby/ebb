from mpf.tests.MpfMachineTestCase import MpfMachineTestCase


class EbbMachineTestCase(MpfMachineTestCase):
    def start_game(self):
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
