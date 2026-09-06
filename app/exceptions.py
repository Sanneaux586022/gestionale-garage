class NotFoundResultError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        self.message = args[0]
        self.status_code = 404