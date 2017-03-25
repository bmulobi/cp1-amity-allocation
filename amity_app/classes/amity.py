# This class will contain most of the functionality
# required in the amity room allocation application


class Amity(object):
    """
    base class
    """

    # class properties
    people_list = [{}, {}]
    rooms_list = [{},{}]
    space_is_available_flag = False

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

        self.living_spaces_list = []
        self.offices_list = []
        self.fellows_list = []
        self.staff_list = []

    def confirm_person_identifier(self, person_identifier):
        """

        :param person_identifier:
        :return:
        """
        if not len(Amity.people_list):
            return False

        if len(Amity.people_list[0]):
            self.fellows_list = Amity.people_list[0].keys()
        if len(Amity.people_list[1]):
            self.staff_list = Amity.people_list[1].keys()

        return person_identifier in self.fellows_list or person_identifier in self.staff_list

    def search_rooms_list(self):
        """

        :return:
        """
        if not len(Amity.rooms_list):
            return False

        if len(Amity.rooms_list[0]):
            self.living_spaces_list = Amity.rooms_list[0].keys()


        if len(Amity.rooms_list[1]):
            self.offices_list = Amity.rooms_list[1].keys()

        return self.offices_list, self.living_spaces_list

    def confirm_room_name(self, new_room_name):
        """

        :param new_room_name:
        :return:
        """
        self.offices_list, self.living_spaces_list = self.search_rooms_list()

        return new_room_name in self.living_spaces_list or new_room_name in self.offices_list

    def confirm_specific_room_has_space(self, room_name):
        """

        :param room_name:
        :return:
        """
        self.offices_list, self.living_spaces_list = self.search_rooms_list()

        if room_name in self.offices_list:
            return len(Amity.rooms_list[1][room_name]) < 6

        if room_name in self.living_spaces_list:
            return len(Amity.rooms_list[0][room_name]) < 4

    def reallocate_person(self, person_identifier, new_room_name):
        """

        :param person_identifier:
        :param new_room_name:
        :return:
        """

        return "Person identifier is : "+str(person_identifier)+" and new room name is: "+new_room_name

    def confirm_availability_of_space_in_amity(self):
        """

        :return:
        """

        if len(Amity.rooms_list[0]) > 0:
            for item in Amity.rooms_list[0].iteritems():
                if len(item) < 4:
                    return True
        if len(Amity.rooms_list[1]) > 0:
            for item in Amity.rooms_list[1].iteritems():
                if len(item) < 6:
                    return True
        return False

    def load_people(self):
        """

        :param file_path:
        :return:
        """

        return "load_people() was called successfully "

    def confirm_existence_of_allocations(self):
        """

        :return:
        """
        return True


    def print_allocations(self, allocated_file_name=""):


        return "print_allocations() was called successfully"

    def confirm_existence_of_unallocated(self):
        """

        :return:
        """
        return False

    def print_unallocated(self, unallocated_file_name=""):
 
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
 