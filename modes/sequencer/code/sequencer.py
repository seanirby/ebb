from modes.ebb_mode import EbbMode, NUM_TARGETS

class Sequencer(EbbMode):
    def mode_start(self, **kwargs):
        # get active mode
        self.add_mode_event_handler("sequencer_delayed_audio_init", self.handle_delayed_audio_init)

    def handle_delayed_audio_init(self, **kwargs):
        self.machine.events.post("sequencer_play_earth")
        planet = self.player["planets"]
        layers_to_play = []

        for i in range(NUM_TARGETS):
            variable = "earth_{}_progress".format(i)
            if self.player[variable] > 0:
                layers_to_play.append(i)

        for i in layers_to_play:
            self.machine.events.post("sequencer_play_earth_{}_with_fade".format(i))
