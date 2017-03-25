from amity_app.classes.room import Room

class Office(Room):
    """
    child class
    """

    def __init__(self, room_type="office", room_capacity=6):

        """

        :param room_name:
        :param room_type:
        """

        self.room_name = ""

    def create_room(self, name):

        """

        :return:
        """
        return "create_room() was called successfully from class Office"
 