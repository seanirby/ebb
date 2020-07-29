from mpf.core.mode import Mode

class MballLocked(Mode):
    def mode_start(self, **kwargs):
        self.init_drops()

    def init_drops(self):
        for i in range(1, 3):
            event = "deactivate_upper_drop_{}".format(i)
            # self.machine.events.post(event)
            # adding a delay because it was necessary for vpx
            self.delay.add(500, self.machine.events.post, None, event=event)

        event = "activate_upper_drop_3"
        self.delay.add(500, self.machine.events.post, None, event=event)

        
