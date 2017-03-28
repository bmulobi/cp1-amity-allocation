from amity_app.classes.room import Room
from amity_app.classes.amity import Amity

class LivingSpace(Room):
    """
    child class
    """


    def __init__(self):

        """

        :param room_type:
        """

        self.room_name = ""
        self.room_type = "living_space"
        self.room_capacity = 4

    def create_room(self, room_name):
        self.room_name = room_name
        Amity.rooms_list[0][self.room_name] = []

        return self.room_name + " was created successfully"
