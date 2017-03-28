from abc import ABCMeta, abstractmethod


class Room(metaclass=ABCMeta):
    """
    base class
    """

    # __metaclass__ = ABCMeta

    def __init__(self):
        """

        :param room_name:
        """

        self.room_name = ""

    @abstractmethod
    def create_room(self):
        """

        :return:
        """

        pass
