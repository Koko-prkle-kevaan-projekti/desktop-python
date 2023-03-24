

class ServerError(AttributeError):
    def __init__(self, msg: str):
        super().__init__(self, msg)

class WindowsError(AttributeError):
    def __init__(self, msg: str):
        super().__init__(self, msg)
