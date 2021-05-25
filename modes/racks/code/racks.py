import subprocess
from mpf.core.mode import Mode

NUM_TARGETS = 7
MAX_PROGRESS = 4
NUM_RACKS = 8

OFF = 0
ON = 1
FLASH = 2
MULTICUE_SIZE = 1


class Racks(Mode):
    def mode_start(self, **kwargs):
        self.init_lights()

        if self.player["ball"]==1:
            self.speak("Rack em up <break time='150ms'/> human")


        for i in range(0, NUM_TARGETS):
            self.add_mode_event_handler("sh_tl_{}_hit".format(i), self.handle_target_hit, target_number=i)

        self.add_mode_event_handler("timer_drops_lower_left_complete", self.update_if_rack_can_be_collected)
        self.add_mode_event_handler("saucer_rack_collect", self.handle_rack_collect_hit)

    def init_lights(self):
        self.update_status_lights()
        self.update_target_lights()

    def update_status_lights(self):
        rack_progress = self.player.racks
        for i in range(0, NUM_RACKS):
            status_shot_name = "sh_racks_status_{}".format(i)
            status_shot = self.machine.shots[status_shot_name]
            if i < rack_progress:
                # collected rack
                status_shot.jump(2)
            elif i == rack_progress:
                # current rack
                status_shot.jump(1)
            else:
                status_shot.jump(0)


    def update_target_lights(self):
        for i in range(0, NUM_TARGETS):
            progress = self.player["tl_{}_progress".format(i)]
            for j in range(0, MAX_PROGRESS):
                shot_name = "l_{}_{}".format(i, j)
                shot = self.machine.shots[shot_name]
                if progress == 0 and j == 0:
                    # current
                    shot.jump(FLASH)
                else:
                    if j < progress:
                        shot.jump(ON)
                    else:
                        shot.jump(OFF)
        
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
            self.update_target_progress(target)

        self.update_target_lights()
        self.update_if_rack_can_be_collected()

    def speak(self, message):
        # Create subprocess
        subprocess.Popen(["espeak", "-v", "robot", "-m", "'{}'".format(message)])

    def handle_speech(self, hit_target_number):
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

    def handle_rack_collect_hit(self, **kwargs):
        all_progress = []

        for i in range(0 ,NUM_TARGETS):
            all_progress.append(self.player["tl_{}_progress".format(i)])

        rack_progress_collecting = min(all_progress)
        self.machine.events.post("min_progress_is_{}".format(rack_progress_collecting))
        if rack_progress_collecting == 0:
            return
        
        if self.machine.shots["sh_racks_collect"].state_name=="unlit":
            return


        # kickoff async transition handler
        self.racks_collect_transition_start()

    def update_target_progress(self, target_number):
        target_progress_var = "tl_{}_progress".format(target_number)
        current_progress = self.player[target_progress_var]
        self.player[target_progress_var] = min(current_progress + 1, MAX_PROGRESS)

    def update_if_rack_can_be_collected(self, **kwargs):
        update = True
        for i in range(0, NUM_TARGETS):
            progress = self.player["tl_{}_progress".format(i)]
            if progress == 0:
                update = False
                break

        if update:
            self.machine.events.post("racks_enable_qualify_collect")

    def racks_collect_transition_start(self, **kwargs):
        # assign tick handler

        collected_targets = []
        for i in reversed(range(NUM_TARGETS)):
            progress = self.player["tl_{}_progress".format(i)]
            progress_status_shots = []
            if (progress > 0):
                for j in reversed(range(progress)):
                    shot = self.machine.shots["l_{}_{}".format(i, j)]
                    progress_status_shots.append(shot)
                collected_targets.append(progress_status_shots)

        assert(len(collected_targets) > 0)
        key = self.machine.events.add_handler('timer_racks_collect_transition_tick', self.racks_collect_transition_tick_handler, collected_targets=collected_targets)
        # kick things off

        self.machine.events.post("racks_collected_loop_start")
        self.machine.timers.racks_collect_transition.restart()
        # add in a fallback for removing our transition tick handler
        # TODO: not sure if this is needed
        self.delay.add(6000, self.remove_transition_handler_fallback, None, transition_handler_key=key)

    def racks_collect_transition_tick_handler(self, **kwargs):

        key = kwargs.get("transition_handler_key")
        ticks = kwargs.get("ticks")
        collected_targets = kwargs.get("collected_targets")
        # find first lit shot in collected_targets nested list
        shot_to_update = None
        for row in collected_targets:
            for shot in row:
                if shot.state == ON:
                    shot_to_update = shot
                    break
            else:
                continue
            break

        if not shot_to_update:
            # game logic
            self.player.racks += 1
            for i in range(0 ,NUM_TARGETS):
                self.player["tl_{}_progress".format(i)] = 0
            self.init_lights()
            self.machine.timers.racks_collect_transition.stop()
            self.machine.timers.racks_collect_transition.reset()
            self.machine.events.post("racks_rack_collected")
            self.machine.events.post("racks_collected_loop_stop")

            # # TODO: is there a way to remove this handler from within itself
            # self.machine.events.remove_handler_by_key(key)
        else:
            # TODO: fix scoring and updates here
            self.player.score += 100000
            shot.jump(OFF)

    def remove_transition_handler_fallback(self, **kwargs):
        key = kwargs.get('transition_handler_key')
        self.machine.events.remove_handler_by_key(key)
        

        
