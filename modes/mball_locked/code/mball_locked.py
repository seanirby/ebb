from mpf.core.mode import Mode

NUM_DROPS = 3

class MballLocked(Mode):
    def mode_start(self, **kwargs):
        self.init_drops()

    def init_drops(self):
        for i in range(0, NUM_DROPS - 1):
            event = "deactivate_upper_drop_{}".format(i)
            # self.machine.events.post(event)
            # adding a delay because it was necessary for vpx
            self.delay.add(500, self.machine.events.post, None, event=event)

        event = "activate_upper_drop_2"
        self.delay.add(500, self.machine.events.post, None, event=event)

        
