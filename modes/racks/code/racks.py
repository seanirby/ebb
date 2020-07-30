from mpf.core.mode import Mode

NUM_TARGETS = 7
MAX_PROGRESS = 4

OFF = 0
ON = 1
FLASH = 2

class Racks(Mode):
    def mode_start(self, **kwargs):
        self.init_lights()
        for i in range(1, NUM_TARGETS+1):
            self.add_mode_event_handler("sh_tl_{}_hit".format(i), self.handle_target_hit, target_number=i)

        self.add_mode_event_handler("sh_rack_collect_hit", self.handle_rack_collected)

    def init_lights(self):
        for i in range(1, NUM_TARGETS+1):
            progress = self.player["tl_{}_progress".format(i)]
            for j in range(1, MAX_PROGRESS+1):
                shot_name = "l_{}_{}".format(i, j)
                shot = self.machine.shots[shot_name]
                if j == 1 and progress == 0:
                    shot.jump(FLASH)
                elif progress >= j:
                    shot.jump(ON)
                else:
                    shot.jump(OFF)
    
    def handle_target_hit(self, **kwargs):
        target_number = kwargs.get("target_number")
        self.update_target_progress(target_number)
        self.update_show(target_number)
        self.update_if_rack_collected()

    def handle_rack_collected(self, **kwargs):
        # update score
        self.player.score += 1000000
        # reset players progress
        for i in range(1,NUM_TARGETS+1):
            self.player["tl_{}_progress".format(i)] = 0
        # update target lights
        self.init_lights()
        # disable rack collect shot
        self.machine.events.post("disable_rack_collect")

        # potentially update difficulty
        # play a show

    def update_target_progress(self, target_number):
        target_progress_var = "tl_{}_progress".format(target_number)
        current_progress = self.player[target_progress_var]
        self.player[target_progress_var] = min(current_progress + 1, MAX_PROGRESS)

    def update_show(self,target_number):
        progress = self.player["tl_{}_progress".format(target_number)]
        for i in range(1, progress+1):
            shot_name = "l_{}_{}".format(target_number, i)
            self.machine.shots[shot_name].jump(ON)

    def update_if_rack_collected(self):
        update = True
        for i in range(1, NUM_TARGETS+1):
            progress = self.player["tl_{}_progress".format(i)]
            if progress == 0:
                update = False
                break

        if update:
            self.machine.events.post("enable_rack_collect")
        
        

        
