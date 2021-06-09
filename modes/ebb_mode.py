import subprocess
import platform
import asyncio
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
PLATFORM_IS_LINUX = platform.system() == 'Linux'

class EbbMode(Mode):
    # def __init__(self, *args, **kwargs):
    #     super(EbbMode, self).__init__(*args, **kwargs)
    #     self.speech_stack = []

    def mode_start(self, **kwargs):
        super().mode_start(**kwargs)
        self.speech_stack = []

    # def mode_stop(self, **kwargs):
    #     super().mode_stop(**kwargs)

    async def speak_async(self):
        command = self.speech_stack[0]["command"]
        print('stirby creating shell {}'.format(command))

        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        self.speech_stack[0]["process"] = proc

        stdout, stderr = await proc.communicate()
        
        if stdout:
            print(f'[stdout]\n{stdout.decode()} stirby')
        if stderr:
            print(f'[stderr]\n{stderr.decode()} stirby')

        self.speech_stack.pop(0)

        if len(self.speech_stack) > 0:
            asyncio.create_task(self.speak_async())

    def add_to_speech_stack(self, command, priority=1):
        new_entry = {
            'command': command,
            'priority': priority,
            'process': None
        }
        self.speech_stack.append(new_entry)

        if len(self.speech_stack) == 1:
            asyncio.create_task(self.speak_async())

    def is_running_from_test(self):
        return hasattr(self.machine, "_ebb_running_from_test") and self.machine._ebb_running_from_test

    def speak(self, message):
        # turn off speaking during tests
        if self.is_running_from_test():
            return 

        command = []
        if PLATFORM_IS_LINUX:
            # command = ["espeak", "-v", "robot", "-m", "'{}'".format(message)]
            command = 'espeak -v robot -m "{}"'.format(message)
        else:
            command = ["C:\Program Files (x86)\eSpeak\command_line\espeak.exe", "-a", "200", "-v", "robot", "-m", "'{}'".format(message)]

        self.add_to_speech_stack(command)


