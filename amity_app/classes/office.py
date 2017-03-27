from amity_app.classes.room import Room
from amity_app.classes.amity import Amity

class Office(Room):
    """
    child class
    """

    def __init__(self, room_type="office",room_capacity=6):
        """

        :param room_name:
        :param room_type:
        """

        self.room_name = ""
        self.room_type = room_type
        self.room_capacity = room_capacity


    def create_room(self, name):
        """

        :return:
        """
        self.room_name = name
        Amity.rooms_list[1][self.room_name] = []
        return "create_room() was called successfully from class Office"