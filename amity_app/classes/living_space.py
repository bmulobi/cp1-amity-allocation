from amity_app.classes.room import Room


class LivingSpace(Room):
    """
    child class
    """


    def __init__(self, room_type="living_space", room_capacity=4):

        """

        :param room_type:
        """

        self.room_name = ""
        self.room_type = room_type
        self.room_capacity = room_capacity

    def create_room(self, room_name):

        return room_name + " was created successfully"
