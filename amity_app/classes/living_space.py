from amity_app.classes.room import Room


class LivingSpace(Room):
    """
    child class of class Room
    defines a room that is a living space
    Contains create_room() the creates a room of type
    living space
    """

    def __init__(self, name):
        """
        :param name: name of room
        """

        self.room_name = name.upper()
        self.room_type = "LIVINGSPACE"
        self.room_capacity = 4
        self.allocations = []

