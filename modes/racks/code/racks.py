from mpf.core.mode import Mode

NUM_TARGETS = 7
MAX_PROGRESS = 4
NUM_RACKS = 8

OFF = 0
ON = 1
FLASH = 2

class Racks(Mode):
    def mode_start(self, **kwargs):
        self.init_lights()
        for i in range(0, NUM_TARGETS):
            self.add_mode_event_handler("sh_tl_{}_hit".format(i), self.handle_target_hit, target_number=i)

        self.add_mode_event_handler("timer_base_drop_left_complete", self.update_if_rack_can_be_collected)
        self.add_mode_event_handler("sh_saucer_debounced_hit", self.handle_rack_collect_hit)

    def init_lights(self):
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

        self.update_target_lights()

    def update_target_lights(self):
        for i in range(0, NUM_TARGETS):
            progress = self.player["tl_{}_progress".format(i)]
            for j in range(0, MAX_PROGRESS):
                shot_name = "l_{}_{}".format(i, j)
                shot = self.machine.shots[shot_name]
                if j < progress:
                    # complete
                    shot.jump(ON)
                elif j == progress:
                    # current
                    shot.jump(FLASH)
                else:
                    # incomplete
                    shot.jump(OFF)
        
    def handle_target_hit(self, **kwargs):
        target_number = kwargs.get("target_number")
        wide_shot = self.machine.shots["sh_wsl_{}".format(target_number)]

        targets=[target_number]

        if wide_shot.state_name == "on":
            progress = self.player["wide_shot_progress"]
            self.machine.events.post("wide_shot_collected")
            # TODO: dedupe the formula below
            targets = list(map(lambda x: x % NUM_TARGETS, list(range(target_number-progress, target_number+progress+1))))

        for target in targets:
            self.update_target_progress(target)

        self.update_target_lights()

        self.update_if_rack_can_be_collected()

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

        # TODO: differentiate between racks collecting and score collecting
        # In each planet i'm only ever collecting 1 rack but I will get 
        self.player.racks += 1
        self.player.score += 1000000 * rack_progress_collecting

        for i in range(0 ,NUM_TARGETS):
            self.player["tl_{}_progress".format(i)] = 0

        self.init_lights()
        self.machine.events.post("racks_rack_collected")

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
        
        

        
