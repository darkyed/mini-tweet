class Tweet(object):
    def __init__(self, text, author) -> None:
        self.text = text
        self.author = author

    def __repr__(self) -> str:
        return "<Tweet: by %s>" % self.author


class HashTag(object):
    def __init__(self, tag) -> None:
        self.tag = tag

    def __repr__(self) -> str:
        return "<HashTag: #%s>" % self.tag
