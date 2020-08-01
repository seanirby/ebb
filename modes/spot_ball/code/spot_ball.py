from mpf.core.mode import Mode

NUM_TARGETS = 7
MAX_PROGRESS = 4

class SpotBall(Mode):
    def mode_start(self, **kwargs):
        self.add_mode_event_handler("sh_spot_ball_hit", self.spot_ball)

    def spot_ball(self, **kwargs):
        for i in range(0, MAX_PROGRESS):
            for j in range(0, NUM_TARGETS):
                var = "tl_{}_progress".format(j)
                progress = self.player[var]
                if (progress-1) < i:
                    self.machine.events.post("spot_ball_{}".format(j))
                    return
                    
                
        
                
