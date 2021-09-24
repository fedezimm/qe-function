class TopicKey(object):
    def __init__(
        self,
        term,
        value
    ):
        self.key = {term: value}