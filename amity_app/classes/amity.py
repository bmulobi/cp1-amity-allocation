# This class will contain most of the functionality
# required in the amity room allocation application


class Amity(object):
    """
    base class
    """

    
    def __init__(self):
        """

        :param person_name:
        """

        self.person_identifier = ""
        self.new_room_name = ""
        self.allocated_file_name = ""
        self.unallocated_file_name = ""
        self.room_name = ""
        self.source_db = ""
        self.destination_db = ""

    def reallocate_person(self, person_identifier, new_room_name):
        """

        :param person_identifier:
        :param new_room_name:
        :return:
        """
        return ("Person is: "+person_identifier+" and new room name is: "+new_room_name)

    def load_people(self):
        """

        :param file_path:
        :return:
        """

        return "load_people() was called successfully"

    def print_allocations(self, allocated_file_name=""):
        """

        :param file_name:
        :return:
        """

        return "print_allocations() was called successfully"

    def print_unallocated(self, unallocated_file_name=""):
        """

        :param file_name:
        :return:
        """

        return "print_unallocated() was called successfully"

    def print_room(self, room_name):
        """

        :param room_name:
        :return:
        """

        return "print_room() was called successfully with arg "+room_name

    def save_state(self, destination_db=""):
        """

        :param destination_db:
        :return:
        """
        return "save_state() was called successfully with arg "+destination_db

    def load_state(self, source_db):
        """

        :param source_db:
        :return:
        """

        return "load_state() was called successfully with arg "+source_db