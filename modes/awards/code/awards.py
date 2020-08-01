from mpf.core.mode import Mode

NUM_AWARDS = 7
AWARD_OFF = 0
AWARD_ON = 1
AWARD_FLASH = 2

class Awards(Mode):
    def mode_start(self, **kwargs):
        self.init_lights()
        self.add_mode_event_handler("sh_award_select_up_hit", self.handle_select_award, direction = -1)
        self.add_mode_event_handler("sh_award_select_down_hit", self.handle_select_award, direction = 1)
        self.add_mode_event_handler("sh_award_collect_hit", self.handle_award_collected)

    def init_lights(self, **kwargs):
        for award in range(0, NUM_AWARDS):
            light = self.machine.shots["sh_award_{}".format(award)]
            if not(self.is_award_collected(award)):
                if self.award_position() == award:
                    light.jump(AWARD_FLASH)
                else:
                    light.jump(AWARD_ON)
            else:
                light.jump(AWARD_OFF)

    def is_award_collected(self, award):
        return self.player["award_{}_collected".format(award)] > 0

    def award_position(self):
        return self.player["award_position"]

    def handle_select_award(self, **kwargs):
        direction = kwargs["direction"]
        self.player["award_position"] = (self.award_position() + direction) % NUM_AWARDS
        self.init_lights()

    def handle_award_collected(self, **kwargs):
        print('bar')

