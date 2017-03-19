from abc import ABCMeta, abstractmethod


class Room(metaclass=ABCMeta):
    """
    base class
    """

    #__metaclass__ = ABCMeta

    def __init__(self, room_name, room_type=""):
        """

        :param room_name:
        """

        self.room_name = room_name
        self.room_type = room_type

    @abstractmethod
    def create_room(self):
        """

        :return:
        """

        pass
