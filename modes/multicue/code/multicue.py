from mpf.core.mode import Mode

MULTICUE_OFF = 0
MULTICUE_ON = 1
NUM_TARGETS = 7

class Multicue(Mode):
    def mode_start(self, **kwargs):
        self.add_mode_event_handler("s_left_flipper_active", self.handle_move, direction=-1)
        self.add_mode_event_handler("s_right_flipper_active", self.handle_move, direction=1)
        self.add_mode_event_handler("multicue_advance_progress", self.handle_progress_change)
        self.add_mode_event_handler("multicue_collected", self.handle_collected)

    def handle_move(self, **kwargs):
        direction = kwargs.get("direction")
        progress = self.player["multicue_progress"]
        position = self.player["multicue_position"]

        if progress > 0:
            self.player["multicue_position"] = (position + direction) % NUM_TARGETS
            self.update_lights()

    def handle_progress_change(self, **kwargs):
        self.player["multicue_progress"] = 1
        self.update_lights()

    def update_lights(self):
        pos = self.player["multicue_position"]
        progress = self.player["multicue_progress"]
        active = list(map(lambda x: x % NUM_TARGETS, list(range(pos-progress, pos+progress+1))))

        for i in range(0, NUM_TARGETS):
            shot = self.machine.shots["sh_multicue_{}".format(i)]
            if i in active:
                shot.jump(MULTICUE_ON)
            else:
                shot.jump(MULTICUE_OFF)
            
    def handle_collected(self, **kwargs):
        # reset progress
        self.player["multicue_progress"] = 0

        # TODO: Figure out why 'multicue_collected' doesn't avan
        # reset multicue target
        shot = self.machine.shots["sh_multicue"].jump(0)

        for i in range(0, NUM_TARGETS):
            self.machine.shots["sh_multicue_{}".format(i)].jump(MULTICUE_OFF)
