from amity_app.classes.room import Room

class Office(Room):
    """
    child class
    """

    def __init__(self, room_name, room_type="office"):
        """

        :param room_name:
        :param room_type:
        """

        self.room_name = room_name
        self.room_type = room_type


    def create_room(self):
        """

        :return:
        """
        pass