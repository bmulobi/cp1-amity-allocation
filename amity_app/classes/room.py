from abc import ABCMeta, abstractmethod


class Room(metaclass=ABCMeta):
    """
    base class for class LivingSpace
    and class Office
    """

    # __metaclass__ = ABCMeta

    def __init__(self):
        """
        constructor to initialise room name
        """

        self.room_name = ""

    @abstractmethod
    # creates room (either office or living space)
    def create_room(self, name):
        """
        abstract method to be inplemented in child classes
        """
        pass
