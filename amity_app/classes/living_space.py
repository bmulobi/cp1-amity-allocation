from amity_app.classes.room import Room
from amity_app.classes.amity import Amity


class LivingSpace(Room):
    """
    child class of class Room
    defines a room that is a living space
    """

    def __init__(self, room_type="livingspace", room_capacity=4):

        """

        :param room_type:
        """

        self.room_name = ""
        self.room_type = room_type
        self.room_capacity = room_capacity

    def create_room(self, room_name):
        self.room_name = room_name
        Amity.rooms_list[0][self.room_name] = []

        return "Living space room " + self.room_name + " was created successfully"
