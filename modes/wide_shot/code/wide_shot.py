from mpf.core.mode import Mode

WSL_OFF = 0
WSL_FLASH = 1
WSL_ON = 2
NUM_TARGETS = 7

class WideShot(Mode):
    def mode_start(self, **kwargs):
        self.add_mode_event_handler("s_left_flipper_active", self.handle_move, direction=-1)
        self.add_mode_event_handler("s_right_flipper_active", self.handle_move, direction=1)
        self.add_mode_event_handler("wide_shot_advance_progress", self.handle_progress_change)
        self.add_mode_event_handler("wide_shot_collected", self.handle_collected)

    def handle_move(self, **kwargs):
        direction = kwargs.get("direction")
        progress = self.player["wide_shot_progress"]
        position = self.player["wide_shot_position"]

        if progress > 0:
            self.player["wide_shot_position"] = (position + direction) % NUM_TARGETS
            self.update_lights()

    def handle_progress_change(self, **kwargs):
        self.player["wide_shot_progress"] = 1
        self.update_lights()

    def update_lights(self):
        pos = self.player["wide_shot_position"]
        progress = self.player["wide_shot_progress"]
        active = list(map(lambda x: x % NUM_TARGETS, list(range(pos-progress, pos+progress+1))))

        for i in range(0, NUM_TARGETS):
            shot = self.machine.shots["sh_wsl_{}".format(i)]
            if i == pos:
                shot.jump(WSL_ON)
            elif i in active: 
                shot.jump(WSL_FLASH)
            else:
                shot.jump(WSL_OFF)
            
    def handle_collected(self, **kwargs):
        # reset progress
        self.player["wide_shot_progress"] = 0

        # # reset wide shot target
        # shot = self.machine.shots["sh_wide_shot"].jump(0)

        # reset wsl indicators
        for i in range(0, NUM_TARGETS):
            self.machine.shots["sh_wsl_{}".format(i)].jump(WSL_OFF)
