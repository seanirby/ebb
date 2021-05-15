from machine_tests.EbbMachineTestCase import EbbMachineTestCase
from unittest.mock import MagicMock

DROP_LEFT_DOWN_PLACEHOLDER = "device.drop_targets.left.complete"
DROP_RIGHT_DOWN_PLACEHOLDER = "device.drop_targets.right.complete"
DROP_UPPER_DOWN_PLACEHOLDER = "device.drop_targets.upper.complete"

class TestDrops(EbbMachineTestCase):
    def _init_drops(self):
        self.assertModeRunning("drops")
        self.assertPlaceholderEvaluates(False, DROP_LEFT_DOWN_PLACEHOLDER)
        self.assertPlaceholderEvaluates(True, DROP_RIGHT_DOWN_PLACEHOLDER)
        self.assertPlaceholderEvaluates(False, DROP_UPPER_DOWN_PLACEHOLDER)

    def test_drops_initialization(self):
        self.start_game()
        self._init_drops()

    def test_hook_shot(self):
        self.start_game()
        self._init_drops()
        self.hit_and_release_switch("s_hook")
        self.advance_time_and_run()
        self.assertPlaceholderEvaluates(True, DROP_LEFT_DOWN_PLACEHOLDER)
        self.assertPlaceholderEvaluates(False, DROP_RIGHT_DOWN_PLACEHOLDER)
        self.advance_time_and_run(5)
        self.assertPlaceholderEvaluates(False, DROP_LEFT_DOWN_PLACEHOLDER)
        self.assertPlaceholderEvaluates(True, DROP_RIGHT_DOWN_PLACEHOLDER)
