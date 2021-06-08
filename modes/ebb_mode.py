import subprocess
from mpf.core.mode import Mode

PLANETS = [
    "earth",
    "mars",
    "jupiter",
    "saturn",
    "neptune",
    "uranus",
    "pluto",
    "beyond"
]

NUM_PLANETS = len(PLANETS)
NUM_TARGETS = 7
MAX_PROGRESS = 4
MULTICUE_SIZE = 1
# TODO: Replace with actual platform check
PLATFORM_IS_WINDOWS = False

class EbbMode(Mode):
    # def __init__(self, *args, **kwargs):
    #     super(EbbMode, self).__init__(*args, **kwargs)

    # def mode_start(self, **kwargs):
        # super().mode_start(**kwargs)
        # self.machine._ebb_running_from_test = True


    # def mode_stop(self, **kwargs):
    #     super().mode_stop(**kwargs)

    def is_running_from_test(self):
        return hasattr(self.machine, "_ebb_running_from_test") and self.machine._ebb_running_from_test

    def speak(self, message):
        # turn off speaking during tests
        if self.is_running_from_test():
            return 

        # Create subprocess
        if PLATFORM_IS_WINDOWS:
            subprocess.Popen(["C:\Program Files (x86)\eSpeak\command_line\espeak.exe", "-a", "200", "-v", "robot", "-m", "'{}'".format(message)])
        else:
            subprocess.Popen(["espeak", "-v", "robot", "-m", "'{}'".format(message)])

