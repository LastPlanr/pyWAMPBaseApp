from time import sleep

import psutil


class MachineStatsMixin:
    @property
    def memory(self):
        return self.get_memory()

    def get_memory(self):
        return psutil.virtual_memory().percent

    @property
    def cpu(self):
        return self.get_cpu()

    def get_cpu(self):
        return psutil.cpu_percent()

    @property
    def load(self):
        return self.get_load()

    def get_load(self):
        return psutil.getloadavg()

    def await_something(self, method, limit, time_limit=60):
        if time_limit is None:
            wait_time = 1
        else:
            wait_time = max(min(time_limit / 20, 5), 1)

        total_time = 0
        while True:
            current_value = method()
            if current_value <= limit:
                return current_value

            if time_limit is not None and total_time > time_limit:
                return current_value

            total_time += wait_time
            sleep(wait_time)

    def await_memory(self, limit, time_limit=60):
        return self.await_something(self.get_memory, limit, time_limit)

    def await_cpu(self, limit, time_limit=60):
        return self.await_something(self.get_cpu, limit, time_limit)
