from mpf.core.mode import Mode

MULTICUE_OFF = 0
MULTICUE_ON = 1
NUM_TARGETS = 7
MULTICUE_SIZE = 1

class Multicue(Mode):
    def mode_start(self, **kwargs):
        self.add_mode_event_handler("s_flipper_left_active", self.handle_move, direction=-1)
        self.add_mode_event_handler("s_flipper_right_active", self.handle_move, direction=1)
        self.add_mode_event_handler("multicue_collected", self.handle_collected)

    def handle_move(self, **kwargs):
        direction = kwargs.get("direction")
        position = self.player["multicue_position"]

        if not self.machine.shots["sh_multicue"].state == 1:
            self.player["multicue_position"] = (position + direction) % NUM_TARGETS
            self.update_lights()

    def update_lights(self):
        pos = self.player["multicue_position"]
        active = list(map(lambda x: x % NUM_TARGETS, list(range(pos-MULTICUE_SIZE, pos+MULTICUE_SIZE+1))))

        for i in range(0, NUM_TARGETS):
            shot = self.machine.shots["sh_multicue_{}".format(i)]
            if i in active:
                shot.jump(MULTICUE_ON)
            else:
                shot.jump(MULTICUE_OFF)
            
    def handle_collected(self, **kwargs):
        # TODO: Figure out why 'multicue_collected' doesn't avan
        # reset multicue target
        shot = self.machine.shots["sh_multicue"].jump(0)

        for i in range(0, NUM_TARGETS):
            self.machine.shots["sh_multicue_{}".format(i)].jump(MULTICUE_OFF)
