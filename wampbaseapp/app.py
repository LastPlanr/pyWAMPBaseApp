class App:
    def __init__(self, wamp_app, *args, **kwargs):
        self.wamp_app = wamp_app

        self.details = None
        self.current_step = 0
        self.total_steps_count = None

        self.init(*args, **kwargs)

    def init(self, *args, **kwargs):
        pass

    def advance_progress_print(self, step_name=None):
        print(self.current_step, self.total_steps_count, step_name or '')
        self.current_step += 1

    def advance_progress_send(self, step_name=None):
        try:
            self.details.progress((self.current_step, self.total_steps_count, step_name))
        except Exception as ex:
            print(ex)
            self.advance_progress = self.advance_progress_print
            return self.advance_progress(step_name)

        self.current_step += 1

    def advance_progress(self, step_name=None):
        self.original_advance_progress = self.advance_progress
        if self.details and self.details.progress:
            self.advance_progress = self.advance_progress_send
        else:
            self.advance_progress = self.advance_progress_print

        return self.advance_progress(step_name)
