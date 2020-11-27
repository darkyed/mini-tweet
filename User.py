class User(object):
    def __init__(self, name, handle) -> None:
        self.name = name
        self.handle = handle

    def __repr__(self) -> str:
        return "<User: %s>" % self.handle

    def __iter__(self):
        return iter((self.name, self.handle))
