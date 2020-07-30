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

    def handle_progress_change(self, **kwargs):
        self.player["wide_shot_advance_progress"] += 1
        self.update_lights()

    def update_lights(self):
        pos = self.player["wide_shot_position"]
        progress = self.player["wide_shot_progress"]
        for i in range(pos - progress, pos + progress + 1):
            shot = None
            if i == pos:
                shot = self.machine.shots["sh_wsl_{}".format(i)]
                shot.jump(ON)
            else: 
                adj_i = (i % NUM_TARGETS) + 1
                shot = self.machine.shots["sh_wsl_{}".format(adj_i)]
                shot.jump(FLASH)
            
            

    def handle_collected(self, **kwargs):
        
    
