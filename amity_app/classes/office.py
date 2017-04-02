from amity_app.classes.room import Room
from amity_app.classes.amity import Amity


class Office(Room):
    """
    child class of class Room
    defines a room that is an office
    """

    def __init__(self, room_type="office", room_capacity=6):
        """
        :param room_type: office
        :param room_capacity: 6 per office
        """

        self.room_name = ""
        self.room_type = room_type
        self.room_capacity = room_capacity

    # creates room of type office in amity
    def create_room(self, name):
        """
        :param name: room name
        :return: relevant message
        """

        self.room_name = name.upper()
        Amity.rooms_list[1][self.room_name] = []
        return "Office room " + self.room_name + " was created successfully"

