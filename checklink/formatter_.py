class MessageFormatter:

    def __init__(self, temp):
        self.__temp = temp

    def __call__(self, *args):
        print(self.__temp.format(
            *args
        ))
