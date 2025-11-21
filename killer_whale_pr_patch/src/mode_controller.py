import time

class ModeController:
    def __init__(self, config):
        self.current_mode = config.get('mode','dynamic')
        self.last_switch = time.time()
        self.hysteresis = config['thresholds'].get('hysteresis_seconds', 180)

    def decide_mode(self, V, L, T, W):
        now = time.time()
        if now - self.last_switch < self.hysteresis:
            return self.current_mode

        V_high = 0.8; V_low = 0.3; T_trend = 0.6; L_min = 1000; W_spike = 0.7
        if T >= T_trend and V <= V_high and L >= L_min:
            candidate = "single_source"
        elif V <= V_low and T < T_trend:
            candidate = "dual_confirmation"
        elif V >= V_high or W >= W_spike:
            candidate = "hybrid"
        else:
            candidate = "hybrid"

        if candidate != self.current_mode:
            self.current_mode = candidate
            self.last_switch = now
        return self.current_mode
