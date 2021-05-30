from modes.ebb_mode import EbbMode

class Announcer(EbbMode):
    def mode_start(self, **kwargs):
        if self.player["ball"]==1:
            self.delay.add(500, self.announce_game_start, None)


        for i in range(0, NUM_TARGETS):
            self.add_mode_event_handler("sh_tl_{}_hit".format(i), self.handle_target_hit, target_number=i)

        self.add_mode_event_handler("timer_drops_lower_left_complete", self.update_if_rack_can_be_collected)
        self.add_mode_event_handler("saucer_collect_rack_show_start", self.handle_rack_collect_hit)

    def announce_game_start(self, **kwargs):
        self.speak("Rack em up <break time='100ms'/> human")

    def handle_target_hit(self, **kwargs):
        target_number = kwargs.get("target_number")
        multicue = self.machine.shots["sh_multicue_{}".format(target_number)]

        targets=[target_number]

        if multicue.state_name == "lit":
            multicue_position = self.player["multicue_position"]
            self.machine.events.post("multicue_collected")
            # TODO: dedupe the formula below
            targets = list(map(lambda x: x % NUM_TARGETS, list(range(multicue_position-MULTICUE_SIZE, multicue_position+MULTICUE_SIZE+1))))

        for target in targets:
            self.handle_speech(target)

    def handle_target_speech(self, hit_target_number):
        hit_target_progress = self.player["tl_{}_progress".format(hit_target_number)]
        others_completed=True

        for target in range(NUM_TARGETS):
            if hit_target_number==target:
                continue
            else:
                progress = self.player["tl_{}_progress".format(target)]
                if progress==0:
                    others_completed = False
                    break

        if hit_target_progress==0:
            if others_completed:
                self.speak("{} Ball. Get <break time='30ms'> The <break time='100ms'> Eight <break time='150ms'> Ball".format(hit_target_number+1))
            else:
                self.speak("{} ball".format(hit_target_number+1))
