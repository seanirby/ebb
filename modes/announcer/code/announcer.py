from modes.ebb_mode import EbbMode

class Announcer(EbbMode):
    def mode_start(self, **kwargs):
        # TODO: only do this for player 1
        if self.player["ball"]==1:
            self.delay.add(500, self.announce_game_start, None)

        self.add_mode_event_handler("announce_message", self.announce_message)
        self.add_mode_event_handler("announce_ball_collected", self.announce_ball_collected)

    def announce_message(self, **kwargs):
        message = kwargs.get("message")
        self.speak(message)

    def announce_ball_collected(self, **kwargs):
        hit_target_number = kwargs.get("hit_target_number")
        is_rack_ready = kwargs.get("is_rack_ready")

        if is_rack_ready:
            self.speak("{} Ball. Get <break time='30ms'> The <break time='100ms'> Eight <break time='150ms'> Ball".format(hit_target_number+1))
        else:
            self.speak("{} Ball".format(hit_target_number+1))

    def announce_game_start(self, **kwargs):
        self.speak("Rackum up <break time='100ms'/> human")
