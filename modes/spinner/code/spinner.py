from mpf.core.mode import Mode


class Spinner(Mode):

    def mode_start(self, **kwargs):
        # initialize to off
        self.change_spinner_shot_state(state=0)
        self.add_mode_event_handler("spinner_state_off_started", self.change_spinner_shot_state, state=0)
        self.add_mode_event_handler("spinner_state_qualified_started", self.change_spinner_shot_state, state=1)
        self.add_mode_event_handler("spinner_state_spinning_on_started", self.change_spinner_shot_state, state=2)
        self.add_mode_event_handler("spinner_state_spinning_off_started", self.change_spinner_shot_state, state=3)
        # TODO: Find out how to fix a bug where the spinner light will flash on/off when you drain with it qualified
        # The below line does not fix this bug
        self.add_mode_event_handler("mode_spinner_stopping", self.change_spinner_shot_state, state=0)

    def change_spinner_shot_state(self, **kwargs):
        state = kwargs.get("state")
        self.machine.shots["sh_spinner"].jump(state)