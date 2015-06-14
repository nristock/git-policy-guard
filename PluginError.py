class PluginError(BaseException):
    def __init__(self, stop_operation, message):
        self.stop_operation = stop_operation
        self.message = message
