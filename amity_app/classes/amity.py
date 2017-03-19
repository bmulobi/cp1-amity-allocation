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
        pass


    def load_people(self):
        """

        :param file_path:
        :return:
        """

        pass

    def print_allocations(self, allocated_file_name=""):
        """

        :param file_name:
        :return:
        """

        pass

    def print_unallocated(self, unallocated_file_name=""):
        """

        :param file_name:
        :return:
        """

        pass

    def print_room(self, room_name):
        """

        :param room_name:
        :return:
        """

        pass

    def save_state(self, destination_db=""):
        """

        :param destination_db:
        :return:
        """
        pass

    def load_state(self, source_db):
        """

        :param source_db:
        :return:
        """

        pass