import pdb
from modes.ebb_mode import EbbMode, NUM_TARGETS, MAX_PROGRESS, NUM_PLANETS, PLANETS

OFF = 0
ON = 1
FLASH = 2
MULTICUE_SIZE = 1

class Racks(EbbMode):
    def mode_start(self, **kwargs):
        self.add_mode_event_handler("sh_racks_collect_hit", self.handle_rack_collect_hit)

    def handle_rack_collect_hit(self, **kwargs):
        planet_finished_number = self.player["planets"] - 1
        planet_finished = PLANETS[planet_finished_number]

        if planet_finished=="mars" and self.player["mars_earth_enabled"]==1:
            planet_finished="mars_earth"

        self.machine.events.post("racks_rack_collected")
        self.machine.events.post("racks_rack_collected_{}".format(planet_finished_number))



        self.racks_collect_transition_start(planet_finished)
    
    def reset_progress_vars(self):
        # TODO: clean this up
        # reset all progress vars
        for planet in PLANETS:
            for i in range(NUM_TARGETS):
                self.player["{}_{}_progress".format(planet, i)] = 0

        # reset mars earth too
        for i in range(NUM_TARGETS):
            self.player["mars_earth_{}_progress".format(planet, i)] = 0

    def racks_collect_transition_start(self, planet):
        if planet=="mars":
            self.machine.events.post("racks_collect_show_complete")
            self.machine.events.post("racks_collected_loop_stop")
            self.reset_progress_vars()
            return
        
        collected_targets = []
        for i in reversed(range(NUM_TARGETS)):
            # TODO: need to actually get the active mode instead of using the hardcoded 'tl'
            progress = self.player["{}_{}_progress".format(planet, i)]
            progress_status_shots = []
            if (progress > 0):
                for j in reversed(range(progress)):
                    # TODO: need to actually get the active mode instead of using the hardcoded 'tl'
                    shot = self.machine.shots["sh_{}_l_{}_{}".format(planet, i, j)]
                    progress_status_shots.append(shot)
                collected_targets.append(progress_status_shots)

        assert(len(collected_targets) > 0)
        key = self.machine.events.add_handler('timer_racks_collect_transition_tick', self.racks_collect_transition_tick_handler, collected_targets=collected_targets, planet=planet)
        # kick things off

        self.machine.events.post("racks_collected_loop_start")
        self.machine.timers.racks_collect_transition.restart()
        # add in a fallback for removing our transition tick handler
        # TODO: not sure if this is needed
        self.delay.add(6000, self.remove_transition_handler_fallback, None, transition_handler_key=key)

    
    def racks_collect_transition_tick_handler(self, **kwargs):
        # TODO: need to get shots from active mode, not hardcode tl_{} lights
        key = kwargs.get("transition_handler_key")
        ticks = kwargs.get("ticks")
        collected_targets = kwargs.get("collected_targets")
        planet = kwargs.get("planet")

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
                self.player["{}_{}_progress".format(planet, i)] = 0
            self.update_target_lights(planet)
            self.machine.timers.racks_collect_transition.stop()
            self.machine.timers.racks_collect_transition.reset()
            self.machine.events.post("racks_collect_show_complete")
            self.machine.events.post("racks_collected_loop_stop")
            self.reset_progress_vars()
            # # TODO: is there a way to remove this handler from within itself
            # self.machine.events.remove_handler_by_key(key)
        else:
            # TODO: fix scoring and updates here
            self.player.score += 100000
            shot.jump(OFF)

    def update_target_lights(self, planet):
        for i in range(0, NUM_TARGETS):
            progress = self.player["{}_{}_progress".format(planet, i)]
            for j in range(0, MAX_PROGRESS):
                shot_name = "sh_{}_l_{}_{}".format(planet, i, j)
                shot = self.machine.shots[shot_name]
                if progress == 0 and j == 0:
                    # current
                    shot.jump(FLASH)
                else:
                    if j < progress:
                        shot.jump(ON)
                    else:
                        shot.jump(OFF)

    def remove_transition_handler_fallback(self, **kwargs):
        key = kwargs.get('transition_handler_key')
        self.machine.events.remove_handler_by_key(key)
