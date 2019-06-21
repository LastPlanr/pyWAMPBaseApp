class App:
    def __init__(self, wamp_app, *args, **kwargs):
        self.wamp_app = wamp_app

        self.details = None
        self.current_step = 0
        self.total_steps_count = None

        self.init(*args, **kwargs)

    def init(self, *args, **kwargs):
        pass

    def advance_progress(self, step_name=None):
        if self.details and self.details.progress:
            self.details.progress((self.current_step, self.total_steps_count, step_name))
            self.current_step += 1
