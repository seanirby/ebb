from mpf.core.mode import Mode

class Mball(Mode):
    def mode_start(self, **kwargs):
        self.init_drops()
        self.add_mode_event_handler("multiball_lock_scoop_upper_full", self.handle_ball_locked)
        self.add_mode_event_handler("s_drops_upper_3_active", self.handle_last_drop_down)

    def init_drops(self):
        drops_to_knock_down = self.player.mball_progress
        if self.is_ball_locked():
            drops_to_knock_down = 2

        for i in range(1, drops_to_knock_down + 1):
            event = "mball_deactivate_drop_{}".format(i)
            # self.machine.events.post(event)
            # adding a delay because it was necessary for vpx
            self.delay.add(500, self.machine.events.post, None, event=event)
        

    def is_ball_locked(self):
        return (self.machine.multiball_locks.scoop_upper.locked_balls > 0)

    def handle_last_drop_down(self, **kwargs):
        if self.is_ball_locked():
            self.machine.events.post("mball_main_start")

    def handle_ball_locked(self, **kwargs):
        event = "mball_activate_drop_3"
        self.machine.events.post(event)
