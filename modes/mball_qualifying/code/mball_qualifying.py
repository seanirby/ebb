from mpf.core.mode import Mode

class MballQualifying(Mode):
    def mode_start(self, **kwargs):
        print("IN MODE START WHOOPIEE")
        self.init_drops()

    def init_drops(self):
        drops_to_knock_down = self.player.mball_progress

        if drops_to_knock_down == 0:
            for i in range(1, 4):
                if not(self.machine.diverters["div_drops_upper_{}".format(i)].active):
                    event = "activate_upper_drop_{}".format(i)
                    self.delay.add(500, self.machine.events.post, None, event=event)
        else:
            # need to set UP drops too
            for i in range(1, drops_to_knock_down + 1):
                event = "deactivate_upper_drop_{}".format(i)
                self.delay.add(500, self.machine.events.post, None, event=event)
