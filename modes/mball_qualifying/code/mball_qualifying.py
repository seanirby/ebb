from mpf.core.mode import Mode

class MballQualifying(Mode):
    def mode_start(self, **kwargs):
        self.init_drops()

    def init_drops(self):
        drops_to_knock_down = self.player.mball_progress

        for i in range(1, drops_to_knock_down + 1):
            event = "mball_deactivate_drop_{}".format(i)
            # self.machine.events.post(event)
            # adding a delay because it was necessary for vpx
            self.delay.add(500, self.machine.events.post, None, event=event)
