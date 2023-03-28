from threading import Timer


class UpdateTimer():
    def __init__(self):
        self.baseline_timer = None
        self.price_check_timer = None

    def set_baseline_timer_interval(self, time):
        self.baseline_timer = Timer(time, self.trigger_baseline_update)

    def set_price_check_timer(self, time):
        self.price_check_timer = Timer(time, self.trigger_price_check_update)

    def trigger_baseline_update(self):
        pass

    def trigger_price_check_update(self):
        pass

    def start_timers(self):
        self.baseline_timer.start()
        self.price_check_timer.start()

