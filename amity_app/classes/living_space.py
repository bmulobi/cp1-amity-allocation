from amity_app.classes.room import Room
from amity_app.classes.amity import Amity


class LivingSpace(Room):
    """
    child class of class Room
    defines a room that is a living space
    Contains create_room() the creates a room of type
    living space
    """

    def __init__(self, room_type="livingspace", room_capacity=4):
        """
        :param room_type: sets the room type
        :param room_capacity: sets the room capacity
        """

        self.room_name = ""
        self.room_type = room_type
        self.room_capacity = room_capacity

    def create_room(self, room_name):
        self.room_name = room_name.upper()

        if self.room_name in Amity.rooms_list[0].keys() or\
           self.room_name in Amity.rooms_list[1].keys():

            return "Room name " + self.room_name + " already exists in the system"

        Amity.rooms_list[0][self.room_name] = []

        return "Living space room " + self.room_name + " was created successfully"
