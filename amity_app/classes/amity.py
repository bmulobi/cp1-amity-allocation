# This class will contain most of the functionality
# required in the amity room allocation application


class Amity(object):
    """
    base class
    """

    # class properties
    people_list = [{}, {}]
    rooms_list = [{}, {}]
    person_identifier = 0

    def __init__(self):
        """

        :param person_name:
        """

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
        self.matched_identifiers_list = []
        self.staff_identifiers_list = []
        self.fellows_identifiers_list = []

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

    # Confirms whether specific room has space for further allocations
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

    # Fetches room type
    def fetch_room_type(self, room_name):
        """
        """
        self.offices_list, self.living_spaces_list = self.search_rooms_list()
        if room_name in self.offices_list:
            return "office"
        if room_name in self.living_spaces_list:
            return "livingspace"

    # Alerts if we try to allocate person to the same room they are already allocated
    def confirm_person_not_doubly_reallocated_to_same_room(self,
                                                           person_identifier,
                                                           room_name):
        """
        Returns:
        True -  if we try to allocate person to a room
                where they are already allocated.
        False - otherwise.
        """

        if (self.fetch_room_type(room_name) == "office"):

            if person_identifier in Amity.rooms_list[1][room_name]:
                return True
        else:
            if person_identifier in Amity.rooms_list[0][room_name]:
                return True
        return False

    def fetch_person_identifier(self, person_name, role):
        """
        returns: uses name and role to
                 return associated person identifier
        """
        people_list = [{}, {}]
        self.matched_identifiers_list = []
        if role == "staff":
            self.staff_identifiers_list = Amity.people_list[1].keys()
            for identifier in self.staff_identifiers_list:
                if person_name in Amity.people_list[1][identifier]:
                    self.matched_identifiers_list.append(identifier)

        else:
            self.fellows_identifiers_list = Amity.people_list[0].keys()
            for identifier in self.fellows_identifiers_list:
                if person_name in Amity.people_list[0][identifier]:
                    self.matched_identifiers_list.append(identifier)

        return self.matched_identifiers_list

    def reallocate_person(self, person_identifier, new_room_name):
        """

        :param person_identifier:
        :param new_room_name:
        :return:
        """

        return "Person with identifier " + person_identifier + " was reallocated to " + new_room_name

    def confirm_availability_of_space_in_amity(self):
        """

        :return:
        """

        if len(Amity.rooms_list[0]) > 0:
            items_list = Amity.rooms_list[0].values()
            for item in items_list:
                if len(item) < 4:
                    return True
        if len(Amity.rooms_list[1]) > 0:
            items_list = Amity.rooms_list[1].values()
            for item in items_list:
                if len(item) < 6:
                    return True
        return False

    def fetch_rooms_with_space(self):
        """
        returns 2 lists: one for offices with space (if any)
        and one for livingspaces with space (if any) and
        the number of spaces available in each room
        """
        offices_list, living_spaces_list = self.search_rooms_list()
        offices_with_space = []
        living_spaces_with_space = []

        if len(offices_list):

            for room in offices_list:
                space = 0
                space = 6 - len(Amity.rooms_list[1][room])
                if space:
                    offices_with_space.append([room, space])

        if len(living_spaces_list):

            for room in living_spaces_list:
                space = 0
                space = 4 - len(Amity.rooms_list[0][room])
                if space:
                    living_spaces_with_space.append([room, space])
        return offices_with_space, living_spaces_with_space

    def load_people(self):
        """
        :param file_path:
        :return:
        """
        offices, living_spaces = self.fetch_rooms_with_space()
        if len(offices) or len(living_spaces):
            try:
                file_object = open("../text_files/test_file.txt", "r")
                try:
                    lines_list = file_object.readlines()
                    for line in lines_list:
                        Amity.person_identifier += 1
                        line_fragments = line.split()
                        if len(line_fragments) == 3:
                            if line_fragments[2] == "FELLOW":
                                Amity.people_list[0]\
                                    ["f-" + str(Amity.person_identifier)] \
                                    = [line_fragments[0]
                                       + " " + line_fragments[1]]
                                for room in offices:
                                    if room[1] > 0:
                                        Amity.rooms_list[1][room[0]].append("f-" + str(Amity.person_identifier))
                                        room[1] -= 1
                                        break
                            else:
                                Amity.people_list[1]\
                                    ["s-" + str(Amity.person_identifier)] \
                                    = [line_fragments[0]
                                       + " " + line_fragments[1]]
                                for room in offices:
                                    if room[1] > 0:
                                        Amity.rooms_list[1][room[0]].append("s-" + str(Amity.person_identifier))
                                        room[1] -= 1
                                        break
                        if len(line_fragments) == 4:
                            Amity.people_list[0]\
                                ["f-" + str(Amity.person_identifier)] \
                                = [line_fragments[0]
                                   + " " + line_fragments[1]]
                            for room in offices:
                                if room[1] > 0:
                                    Amity.rooms_list[1][room[0]].append("f-" + str(Amity.person_identifier))
                                    room[1] -= 1
                                    break
                            for room in living_spaces:
                                if room[1] > 0:
                                    Amity.rooms_list[0][room[0]].append("f-" + str(Amity.person_identifier))
                                    room[1] -= 1
                                    break

                finally:
                    file_object.close()

            except IOError as e:
                print(str(e))

        else:
            print("There is no free space currently, use the create_room \
                  command to create new space")

    def confirm_existence_of_allocations(self):
        """

        :return:
        """
        # rooms_list = [{},{}]
        if len(Amity.rooms_list[0]) > 0:
            items_list = Amity.rooms_list[0].values()
            for item in items_list:
                if len(item) > 0:
                    return True
        if len(Amity.rooms_list[1]) > 0:
            items_list = Amity.rooms_list[1].values()
            for item in items_list:
                if len(item) > 0:
                    return True
        return False

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

        return "print_room() was called successfully with arg " + room_name

    def save_state(self, destination_db=""):
        """

        :param destination_db:
        :return:
        """
        return "save_state() was called successfully with arg " + destination_db

    def load_state(self, source_db):
        """

        :param source_db:
        :return:
        """

        return "load_state() was called successfully with arg " + source_db
