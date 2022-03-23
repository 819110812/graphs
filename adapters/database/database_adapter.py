from abc import ABCMeta


class Database:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    def _connect(self):
        raise NotImplementedError

    def _disconnect(self):
        raise NotImplementedError






