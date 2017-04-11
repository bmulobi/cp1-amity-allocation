from amity_app.classes.room import Room


class Office(Room):
    """
    child class of class Room
    defines a room that is an office
    """

    def __init__(self, name):
        """
        :param room_type: office
        :param room_capacity: 6 per office
        """

        self.room_name = name.upper()
        self.room_type = "OFFICE"
        self.room_capacity = 6
        self.allocations = []


