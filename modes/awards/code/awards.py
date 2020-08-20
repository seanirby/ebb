from mpf.core.mode import Mode

NUM_AWARDS = 7
AWARD_OFF = 0
AWARD_ON = 1
AWARD_FLASH = 2

AWARD_EVENTS = [
    "award_instant_million_collected",
    "award_multiplied_rack_collected",
    "award_super_spinner_collected",
    "award_lower_drops_collected",
    "award_mystery_collected",
    "award_spot_3_balls",
    "award_ball_saver_collected"
]

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
        awards = []

        for award in range(0, NUM_AWARDS):
            if not(self.is_award_collected(award)):
                awards.append(award)

        if len(awards) == 1:
            self.player["award_position"] = awards[0]
            return
        else:
            direction = kwargs["direction"]
            pos = self.award_position()

            # because this function could be called from 'handle_award_collected' we manually put in the active position into the awards array so it can be the basis for the next selection
            awards.append(pos)
            awards = list(set(awards))
            awards.sort()

            i = awards.index(pos)
            next_i = (i + direction) % len(awards)
            self.player["award_position"] = awards[next_i]
            self.init_lights()

    def are_all_awards_collected(self):
        for award in range(0, NUM_AWARDS):
            if not(self.is_award_collected(award)):
                return False
        return True

    def reset_awards(self):
        for award in range(0, NUM_AWARDS):
            self.player["award_{}_collected".format(award)] = 0

    def handle_award_collected(self, **kwargs):
        print("BAR")
        pos = self.award_position()
        print(pos)
        self.machine.events.post(AWARD_EVENTS[pos])

        self.player["award_{}_collected".format(pos)] = 1
        if self.are_all_awards_collected():
            self.player["award_position"] = 0
            self.reset_awards()
        else:
            self.handle_select_award(direction=1)

        self.init_lights()
        
        
