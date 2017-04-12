from abc import ABCMeta


class Room(metaclass=ABCMeta):
    """
    base class for class LivingSpace
    and class Office
    """

    def __init__(self):
        """
        constructor to initialise room name
        """

        self.room_name = ""
