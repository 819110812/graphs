from abc import ABCMeta


class BaseAdapter:
    __metaclass__ = ABCMeta

    def __init__(self, path):
        self.path = path
        pass

    def get_data(self):
        pass
