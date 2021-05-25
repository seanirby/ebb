from mpf.core.mode import Mode

NUM_AWARDS = 7
AWARDS_OFF = 0
AWARDS_ON = 1
AWARDS_FLASH = 2

class Awards(Mode):
    def mode_start(self, **kwargs):
        self.init_lights()
        self.add_mode_event_handler("sh_awards_select_left_hit", self.handle_select_award, direction = -1)
        self.add_mode_event_handler("sh_awards_select_right_hit", self.handle_select_award, direction = 1)
        self.add_mode_event_handler("awards_award_collected", self.handle_award_collected)

        # ensure the right award mode is selected when mode starts
        for i in range(0, NUM_AWARDS):
            if i == self.award_selected():
                self.machine.events.post("award_{}_selected".format(i))
                break

    def init_lights(self, **kwargs):
        for award in range(0, NUM_AWARDS):
            light = self.machine.shots["sh_awards_{}".format(award)]
            if not(self.is_award_collected(award)):
                if self.award_selected() == award:
                    light.jump(AWARDS_FLASH)
                else:
                    light.jump(AWARDS_OFF)
            else:
                light.jump(AWARDS_ON)

    def is_award_collected(self, award):
        return self.player["award_{}_collected".format(award)] > 0

    def award_selected(self):
        return self.player["award_selected"]

    def handle_select_award(self, **kwargs):
        awards = []

        for award in range(0, NUM_AWARDS):
            if not(self.is_award_collected(award)):
                awards.append(award)

        next_i = None
        if len(awards) == 1:
            self.player["award_selected"] = awards[0]
            next_i = awards[0]
        else:
            direction = kwargs["direction"]
            pos = self.award_selected()

            # because this function could be called from 'handle_awards_collected' we manually put in the active position into the awards array so it can be the basis for the next selection
            awards.append(pos)
            awards = list(set(awards))
            awards.sort()

            i = awards.index(pos)
            next_i = (i + direction) % len(awards)

            self.machine.events.post("award_{}_unselected".format(pos))

            self.player["award_selected"] = awards[next_i]

        self.machine.events.post("award_{}_selected".format(next_i))
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
        # TODO: may need to add in logic so awards aren't always collected
        pos = self.award_selected()
        self.machine.events.post("award_{}_collected".format(pos))
        self.player["award_{}_collected".format(pos)] = 1

        if self.are_all_awards_collected():
            self.player["award_sets"] += 1
            self.player["award_selected"] = 0
            self.reset_awards()
        else:
            self.handle_select_award(direction=1)

        self.init_lights()
        
        
