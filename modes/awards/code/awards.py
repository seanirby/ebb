import pdb
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
        for i in range(NUM_AWARDS):
            if i == self.award_selected():
                self.machine.events.post("award_{}_selected".format(i))
                break

    def init_lights(self, **kwargs):
        for award in range(NUM_AWARDS):
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
        pos = self.award_selected()

        for award in range(0, NUM_AWARDS):
            if not(self.is_award_collected(award)):
                awards.append(award)

        j = None
        if len(awards) == 1:
            self.player["award_selected"] = awards[0]
            j = awards[0]
        else:
            direction = kwargs["direction"]
            j = pos + direction

            while True:
                if 0 <= j < NUM_AWARDS:
                    if self.player["award_{}_collected".format(j)] > 0:
                        j += direction
                    else:
                        break
                elif j < 0:
                    j = NUM_AWARDS-1
                else:
                    j = 0

            self.player["award_selected"] = j

        if j != pos:
            self.machine.events.post("award_{}_unselected".format(pos))
            
        self.machine.events.post("award_{}_selected".format(j))
        self.init_lights()

    def are_all_awards_collected(self):
        for award in range(0, NUM_AWARDS):
            if not(self.is_award_collected(award)):
                return False
        return True


    def handle_award_collected(self, **kwargs):
        # TODO: may need to add in logic so awards aren't always collected
        pos = self.award_selected()
        self.player["award_{}_collected".format(pos)] = 1

        if self.are_all_awards_collected():
            self.player["award_sets"] += 1
            self.player["award_selected"] = 3
            self.machine.events.post("award_{}_selected".format(3))
            self.machine.events.post("award_{}_unselected".format(pos))

            for award in range(0, NUM_AWARDS):
                self.player["award_{}_collected".format(award)] = 0

        else:
            self.handle_select_award(direction=1)

        self.init_lights()
        
        
