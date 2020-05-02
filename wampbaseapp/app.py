class App:
    def __init__(self, wamp_app, *args, **kwargs):
        self.wamp_app = wamp_app

        self.details = None
        self.current_step = 1
        self.total_steps_count = None

        self.init(*args, **kwargs)

        self.topic = None

    def init(self, *args, **kwargs):
        pass

    async def call(self, method_name, *args, **kwargs):
        return await self.wamp_app.call(method_name, *args, **kwargs)

    def publish(self, message, topic=None, options=None):
        topic = topic or self.topic
        if topic:
            self.wamp_app.publish(topic, message, {}, options)

    def advance_progress_print(self, step_name=None):
        print(self.current_step, self.total_steps_count, step_name or '')
        self.current_step += 1

    def advance_progress_send(self, step_name=None):
        progress_data = (self.current_step, self.total_steps_count, step_name)
        try:
            self.details.progress(progress_data)
        except Exception as ex:
            print(ex)
            self.advance_progress = self.advance_progress_print
            return self.advance_progress(step_name)

        self.publish(progress_data)
        self.current_step += 1

    def advance_progress_notify(self, step_name):
        progress_data = (self.current_step, self.total_steps_count, step_name)
        self.publish(progress_data)
        self.current_step += 1

    def advance_progress(self, step_name=None):
        self.original_advance_progress = self.advance_progress
        if self.details and self.details.progress:
            self.advance_progress = self.advance_progress_send
        else:
            self.advance_progress = self.advance_progress_print

        return self.advance_progress(step_name)

    def inform_finish(self, step_name=None):
        self.current_step = 0
        self.advance_progress(step_name)
        self.current_step = 0
