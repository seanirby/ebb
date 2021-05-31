from machine_tests.EbbMachineTestCase import EbbMachineTestCase

class TestRacks(EbbMachineTestCase):
  def test_racks_running_on_game_start(self):
    self.start_game()
    self.assertModeRunning("racks")

  def test_racks_qualify_collect_unlit_on_game_start(self):
    self.start_game()
    self.assertPlaceholderEvaluates(False,"device.shots.sh_racks_qualify_collect.enabled")
    self.assertPlaceholderEvaluates(False,"device.shots.sh_racks_collect.enabled")

  def test_racks_qualify_collect_lit_after_collecting_7_balls_on_earth(self):
    self.start_game()
    self.hit_ball_targets()
    self.assertPlaceholderEvaluates(True,"device.shots.sh_racks_qualify_collect.enabled")
    self.assertPlaceholderEvaluates(False,"device.shots.sh_racks_collect.enabled")

  def test_racks_collect_lit_after_hitting_qualify_collect(self):
    self.start_game()
    self.hit_ball_targets()
    self.hit_and_release_switch_and_run("s_hook", .1)
    self.assertPlaceholderEvaluates(False,"device.shots.sh_racks_qualify_collect.enabled")
    self.assertPlaceholderEvaluates(True,"device.shots.sh_racks_collect.enabled")

  def test_racks_collect_lit_after_hitting_qualify_collect(self):
    self.start_game()
    self.hit_ball_targets()
    self.hit_and_release_switch_and_run("s_hook", .1)
    self.hit_switch_and_run("s_saucer", 1.5)
    self.assertPlaceholderEvaluates(False,"device.shots.sh_racks_qualify_collect.enabled")
    self.assertPlaceholderEvaluates(False,"device.shots.sh_racks_collect.enabled")

  def test_racks_collect_unlit_after_timeout(self):
    self.start_game()
    self.hit_ball_targets()
    self.hit_and_release_switch_and_run("s_hook", .1)
    self.advance_time_and_run(10)
    self.assertPlaceholderEvaluates(True, "device.shots.sh_racks_qualify_collect.enabled")
    self.assertPlaceholderEvaluates(False,"device.shots.sh_racks_collect.enabled")
