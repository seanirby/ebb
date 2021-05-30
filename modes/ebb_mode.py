import subprocess
from mpf.core.mode import Mode

# TODO: Replace with actual platform check
PLATFORM_IS_WINDOWS = True

class EbbMode(Mode):
    # def __init__(self, *args, **kwargs):
    #     super(EbbMode, self).__init__(*args, **kwargs)

    # def mode_start(self, **kwargs):
    #     super().mode_start(**kwargs)

    # def mode_stop(self, **kwargs):
    #     super().mode_stop(**kwargs)

    def speak(self, message):
        # Create subprocess
        if PLATFORM_IS_WINDOWS:
            subprocess.Popen(["C:\Program Files (x86)\eSpeak\command_line\espeak.exe", "-v", "robot", "-m", "'{}'".format(message)])
        else:
            subprocess.Popen(["espeak", "-v", "robot", "-m", "'{}'".format(message)])

