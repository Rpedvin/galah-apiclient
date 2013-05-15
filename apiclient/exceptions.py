class PermissionError(Exception):
    def __init__(self, what):
        self.what = str(what)

    def __str__(self):
        return self.what
