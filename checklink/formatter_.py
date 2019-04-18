class MessageFormatter:

    def __init__(self, temp):
        self.__temp = temp

    def __call__(self, *args):
        return self.__temp.format(*args)
