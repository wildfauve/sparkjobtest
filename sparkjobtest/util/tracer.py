import uuid
import pendulum

class Tracer():

    def __init__(self, env, job_id=None, context=None):
        self.env = env
        self.context = context
        self.job_id = uuid.uuid4() if not job_id else job_id

    def serialise(self):
        return {'env': self.env,
                'job_id': self.job_id_to_s(),
                'time': pendulum.now().to_iso8601_string()}

    def job_id_to_s(self):
        return str(self.job) if isinstance(self.job_id, uuid.UUID) else self.job_id


def init_tracing(env):
    return Tracer(env)
