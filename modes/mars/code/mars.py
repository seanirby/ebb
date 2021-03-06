import pdb
from modes.ebb_mode import EbbMode, NUM_TARGETS, MAX_PROGRESS, MULTICUE_SIZE

OFF = 0
ON = 1
FLASH = 2

class Mars(EbbMode):
    def mode_start(self, **kwargs):
        self.add_mode_event_handler("mars_enable_earth_rules", self.handle_earth_rules_enabled)
        self.add_mode_event_handler("mars_disable_earth_rules", self.handle_earth_rules_disabled)
        self.add_mode_event_handler("timer_drops_lower_left_complete", self.update_if_rack_can_be_collected)
        self.add_mode_event_handler("sh_mars_hurry_up_flash_four_hit", self.handle_hurry_up_completed)
        
        for i in range(0, NUM_TARGETS):
            self.add_mode_event_handler("sh_mars_earth_{}_hit".format(i), self.handle_target_hit, target_number=i)

    def handle_hurry_up_completed(self, **kwargs):
        for i in range(NUM_TARGETS):
            self.player["mars_{}_progress"] = MAX_PROGRESS

    def handle_earth_rules_enabled(self, **kwargs):
        self.update_target_lights()
        self.update_if_rack_can_be_collected()

    def handle_earth_rules_disabled(self, **kwargs):
        self.update_if_rack_can_be_collected()

    def update_target_lights(self):
        for i in range(0, NUM_TARGETS):
            progress = self.player["mars_earth_{}_progress".format(i)]
            for j in range(0, MAX_PROGRESS):
                shot_name = "sh_mars_earth_l_{}_{}".format(i, j)
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
        # multicue = self.machine.shots["sh_multicue_{}".format(target_number)]

        targets=[target_number]

        # if multicue.state_name == "lit":
        #     multicue_position = self.player["multicue_position"]
        #     self.machine.events.post("multicue_collected")
        #     # TODO: dedupe the formula below
        #     targets = list(map(lambda x: x % NUM_TARGETS, list(range(multicue_position-MULTICUE_SIZE, multicue_position+MULTICUE_SIZE+1))))

        for target in targets:
            self.handle_speech(target)
            self.update_target_progress(target)

        self.update_target_lights()
        self.update_if_rack_can_be_collected()

    def handle_speech(self, hit_target_number):
        hit_target_progress = self.player["mars_earth_{}_progress".format(hit_target_number)]
        others_completed=True

        for target in range(NUM_TARGETS):
            if hit_target_number==target:
                continue
            else:
                progress = self.player["mars_earth_{}_progress".format(target)]
                if progress==0:
                    others_completed = False
                    break

        if hit_target_progress==0:
            if others_completed:
                self.machine.events.post("announce_ball_collected", hit_target_number=hit_target_number, is_rack_ready=True)
            else:
                self.machine.events.post("announce_ball_collected", hit_target_number=hit_target_number, is_rack_ready=False)

    def update_target_progress(self, target_number):
        target_progress_var = "mars_earth_{}_progress".format(target_number)
        current_progress = self.player[target_progress_var]
        self.player[target_progress_var] = min(current_progress + 1, MAX_PROGRESS)

    def update_if_rack_can_be_collected(self, **kwargs):
        if not self.player["mars_earth_enabled"]:
            if self.machine.shots["sh_mars_hurry_up"].state_name == "complete":
                self.machine.events.post("racks_enable_qualify_collect")
        else:
            update = True
            for i in range(NUM_TARGETS):
                progress = self.player["mars_earth_{}_progress".format(i)]
                if progress == 0:
                    update = False
                    # pdb.set_trace()
                    break
    
            if update:
                self.machine.events.post("racks_enable_qualify_collect")
