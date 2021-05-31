from machine_tests.EbbMachineTestCase import EbbMachineTestCase

class TestPlanets(EbbMachineTestCase):
  def test_starts_first_planet_on_ball_start(self):
    self.start_game()
    self.assertModeRunning("planets")
    self.assertModeRunning("earth")
    self.assertPlaceholderEvaluates("current", "device.shots.sh_planets_status_0.state_name")

  def test_advances_to_second_planet_after_eight_ball_collected(self):
    self.mock_event("planets_mars_start")
    self.start_game()
    self.assertPlaceholderEvaluates("unlit", "device.shots.sh_planets_status_1.state_name")
    self.collect_earth_rack()
    self.assertPlaceholderEvaluates("completed", "device.shots.sh_planets_status_0.state_name")
    self.assertEventCalled("planets_mars_start")
    self.assertModeRunning("mars")
    self.assertPlaceholderEvaluates("current", "device.shots.sh_planets_status_1.state_name")
