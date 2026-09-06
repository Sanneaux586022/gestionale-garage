
class ServiceBase:
    def __init__(self, db_session, logger):
        self.session = db_session
        self.logger = logger
        