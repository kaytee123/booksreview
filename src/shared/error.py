class UserError:
    def __init__(self, message, code="", meta={}):
        self.message = message
        self.code = code
        self.meta = meta
