import os
import sqlite3
import re
import random

from amity_app.classes.fellow import Fellow
from amity_app.classes.staff import Staff
from amity_app.classes.office import Office
from amity_app.classes.living_space import LivingSpace


class Amity(object):
    """
    Class contains all the functionalities for
    amity
    """

    # class properties
    fellows = {}
    staff = {}
    offices = {}
    living_spaces = {}
    people_counter = 0
    session_id = ""

    def __init__(self):
        """
        initialise some properties
        """
        self.file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.filename = os.path.join(self.file_path, 'text_files/sessions_file.txt')
        self.alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                         "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

        if os.path.isfile(self.filename):
            file_mode = "r"
        else:
            file_mode = "w"

        if file_mode == "r":

            with open(self.filename, file_mode) as file_object:

                Amity.session_id = file_object.read()
                position = self.alphabet.index(Amity.session_id)

                if position == 25:

                    next_session_id = self.alphabet[0]
                else:
                    next_session_id = self.alphabet[position + 1]

            with open(self.filename, "w") as file_object:
                file_object.write(next_session_id)
        else:
            Amity.session_id = "a"
            with open(self.filename, file_mode) as file_object:
                file_object.write("b")

        self.new_room_name = ""
        self.allocated_file_name = ""
        self.unallocated_file_name = ""
        self.room_name = ""
        self.source_db = ""
        self.destination_db = ""
        self.return_message = ""

        self.fellows_list = []
        self.staff_list = []
        self.matched_identifiers_list = []
        self.staff_identifiers_list = []
        self.fellows_identifiers_list = []
        self.room_type = ""
        self.livingspaces_with_allocations = []
        self.offices_with_allocations = []

        self.regex_name = r'(\(|\+|\?|\.|\*|\^|\$|\)|\[|\]|\{|\}|\||\\|[0-9]|\`|\~|\!|\@|\#|\%|\_|\=|\;|\:|\"|\,|\<|\>|\/)'
        self.regex_person_id = r'^[s|f]-[1-9]{1,3}[a-z]{1}$'

        self.fetched_identifiers = []

    # verifies overall availability of space in amity
    def confirm_availability_of_space_in_amity(self):
        """
        :return: True if space is available
                 False otherwise
        """

        if len(Amity.living_spaces) > 0:
            living_spaces = Amity.living_spaces.keys()
            for room in living_spaces:
                if len(Amity.living_spaces[room].allocations) < Amity.living_spaces[room].room_capacity:
                    return True
        if len(Amity.offices) > 0:
            offices = Amity.offices.keys()
            for room in offices:
                if len(Amity.offices[room].allocations) < Amity.offices[room].room_capacity:
                    return True
        return False

    # get list of all rooms in amity
    def search_rooms_list(self):
        """
        :return: list of rooms in amity, if any
                 False otherwise
        """
        # return false if dictionaries are empty
        if not len(Amity.living_spaces) and not len(Amity.offices):
            return False

        living_space_rooms = []
        office_rooms = []

        # fetch living spaces names if any in system
        if len(Amity.living_spaces):
            living_space_rooms  = Amity.living_spaces.keys()

        # fetch offices names if any in system
        if len(Amity.offices):
            office_rooms  = Amity.offices.keys()

        # if at least one room was found, return in list
        if living_space_rooms or office_rooms:
            return [living_space_rooms, office_rooms]
        else:
            return False

    # fetches list of rooms with space
    def fetch_rooms_with_space(self):
        """
        returns 2 lists: one for offices with space (if any)
        and one for livingspaces with space (if any) and
        the number of spaces available in each room
        """

        # check if any rooms in system
        if self.search_rooms_list():

            offices_with_space = []
            living_spaces_with_space = []

            # get list of all rooms in system
            rooms = self.search_rooms_list()
            living_spaces = rooms[0]
            offices = rooms[1]

            # if any offices in system
            if len(offices):

                for room in offices:

                    # check if office has any space
                    if len(Amity.offices[room].allocations) < Amity.offices[room].room_capacity:
                        offices_with_space.append(room)

            # if any living spaces in system
            if len(living_spaces):

                for room in living_spaces:

                    # check if livingspace has any space
                    if len(Amity.living_spaces[room].allocations) < Amity.living_spaces[room].room_capacity:
                        living_spaces_with_space.append(room)

            return [living_spaces_with_space, offices_with_space]
        else:
            return False

    # adds a new person to amity
    def add_person(self, name, role, wants_accommodation="N"):
        """
        :param role: either staff or fellow
        :param name: Person's name
        :param wants_accommodation: default N, if Y allocate accommodation
        :return: relevant message
        """
        self.return_message = "\n"

        # ensure no illegal characters in name i.e any of
        # ( + ? . *  ^ $  ( ) \ [ ] { } | \ ) [0-9] ` ~ ! @ # % _ = ; : " , < . > /
        if re.search(self.regex_name, name):
            return [0, "Avoid any of the following characters in name: + ? . * " + \
                    "^ $ ( ) \ [ ] { } | \  [0-9] ` ~ ! @ # % _ = ; : \" , < . > /\n"]

        # ensure wants accommodation option is either (Y or N) or (y or n)
        if wants_accommodation not in ["Y", "N"]:
            return [0, "\nAccommodation option should be either y or n\n"]

        if role == "STAFF" and wants_accommodation == "Y":
            return [0, "\nStaff cannot be allocated living spaces\n"]

        # ensure role is either fellow or staff
        if role not in ["FELLOW", "STAFF"]:
            return [0, "\nRole must be either fellow or staff\n"]

        # increment people counter by 1
        Amity.people_counter += 1

        if role == "FELLOW":

            fellow_object = Fellow(name)
            if wants_accommodation and wants_accommodation in ["y", "Y"]:
                fellow_object.accommodation = "Y"
            # make unique identifier for new fellow
            fellow_object.person_id = "f-" + str(Amity.people_counter) + Amity.session_id

            # insert new fellow into fellows dictionary with id as key
            Amity.fellows[fellow_object.person_id] = fellow_object

            self.return_message += fellow_object.name + " with ID " + fellow_object.person_id + \
                                   " was added successfully as a fellow\n"

        if role == "STAFF":

            staff_object = Staff(name)

            # make unique identifier for new person
            staff_object.person_id = "s-" + str(Amity.people_counter) + Amity.session_id

            # insert new staff into staff dictionary with id as key
            Amity.staff[staff_object.person_id] = staff_object

            self.return_message += staff_object.name + " with ID " + staff_object.person_id + \
                                   " was added successfully as a member of staff\n"

        # confirm availability of space in amity
        if self.confirm_availability_of_space_in_amity():

            # fetch list of rooms with space
            rooms_with_space = self.fetch_rooms_with_space()
            livingspaces_with_space = rooms_with_space[0]
            offices_with_space = rooms_with_space[1]

            if role == "FELLOW":

                # if there's office with space, allocate to new fellow
                if offices_with_space:
                    random_room = random.choice(offices_with_space)

                    Amity.offices[random_room].allocations.append(fellow_object.person_id)
                    Amity.fellows[fellow_object.person_id].has_office = random_room

                    self.return_message += "and allocated to office " + random_room + "\n"

                # check if fellow wants accommodation
                if Amity.fellows[fellow_object.person_id].accommodation == "Y":

                    # if there's a living space with space, allocate to fellow
                    if livingspaces_with_space:

                        random_room = random.choice(livingspaces_with_space)
                        Amity.living_spaces[random_room].allocations.append(fellow_object.person_id)
                        Amity.fellows[fellow_object.person_id].has_accommodation = random_room

                        self.return_message += "and allocated to living space " + random_room + "\n"
            if role == "STAFF":
                # if there's office with space, allocate to new staff
                if offices_with_space:
                    random_room = random.choice(offices_with_space)

                    Amity.offices[random_room].allocations.append(staff_object.person_id)
                    Amity.staff[staff_object.person_id].has_office = random_room

                    self.return_message += "and allocated to office " + random_room + "\n"

        if role == "FELLOW":
            return [fellow_object.person_id, self.return_message]
        if role == "STAFF":
            return [staff_object.person_id, self.return_message]

    # creates rooms in amity
    def create_room(self, room_type, room_names):

        if room_type not in ["OFFICE", "LIVINGSPACE"]:
            return "\nRoom type must be office or livingspace"

        successfully_created_rooms = []
        format_error_room_names = []
        already_existing_rooms = []

        success_msg = ""
        error_msg = ""
        failure_msg = ""

        for name in room_names:

            name = name.upper()

            # ensure no illegal characters in room name i.e any of
            # ( + ? . *  ^ $  ( ) \ [ ] { } | \ ) [0-9] ` ~ ! @ # % _ = ; : " , < . > /
            if re.search(self.regex_name, name):
                format_error_room_names.append(name)
                continue
            if name in Amity.offices.keys() or name in Amity.living_spaces.keys():
                already_existing_rooms.append(name)
                continue

            if room_type == "OFFICE":

                Amity.offices[name] = Office(name)
                successfully_created_rooms.append(name)

            else:
                Amity.living_spaces[name] = LivingSpace(name)
                successfully_created_rooms.append(name)

        if len(successfully_created_rooms):
            success_msg = "\n Successfully created " + room_type.lower() + "s: " + \
                          str(len(successfully_created_rooms))\
                          + " ,\n " + " ".join(successfully_created_rooms) + "\n"

        if len(format_error_room_names):
            error_msg = "\n Room names rejected due to format errors: " + \
                        str(len(format_error_room_names)) + " ,\n "\
                        + " ".join(format_error_room_names) + "\n"

        if len(already_existing_rooms):
            failure_msg = "\n Room names rejected because they already exist: " + \
                          str(len(already_existing_rooms)) +\
                          " ,\n " + " ".join(already_existing_rooms) + "\n"

        return success_msg + error_msg + failure_msg

    # confirms whether user has entered a valid identifier
    def confirm_person_identifier(self, person_identifier):
        """
        :param person_identifier: person's identifier
        :return: True if identifier is valid
                 False otherwise
        """

        if not len(Amity.fellows) and not len(Amity.staff):
            return False

        fellows_ids = []
        staff_ids = []

        if len(Amity.fellows):
            fellows_ids = Amity.fellows.keys()
        if len(Amity.staff):
            staff_ids = Amity.staff.keys()

        return person_identifier in fellows_ids or person_identifier in staff_ids

    # check if room name exists in system
    def confirm_room_name(self, room_name):
        """
        :param room_name: name of room to confirm
        :return: True if name is valid,
                 False otherwise
        """
        if not len(Amity.living_spaces) and not len(Amity.offices):
            return False

        rooms = self.search_rooms_list()

        return room_name in rooms[0] or room_name in rooms[1]

    # Confirms whether specific room has space for further allocations
    def confirm_specific_room_has_space(self, room_name):
        """
        :param room_name: room name
        :return: True if space is available
                 False otherwise
        """
        room_name = room_name.upper()
        # first confirm overall availability of space
        if self.confirm_availability_of_space_in_amity():
            result = self.search_rooms_list()

            if room_name in result[0]:
                return len(Amity.living_spaces[room_name].allocations) < Amity.living_spaces[room_name].room_capacity
            if room_name in result[1]:
                return len(Amity.offices[room_name].allocations) < Amity.offices[room_name].room_capacity
        return False

    # Fetches room type
    def fetch_room_type(self, room_name):
        """
        """
        if self.search_rooms_list():

            room_name = room_name.upper()
            result = self.search_rooms_list()

            if room_name in result[1]:
                return "office"
            if room_name in result[0]:
                return "livingspace"
            return False

    # Alerts if we try to allocate person to the
    # same room they are already allocated
    def confirm_person_not_doubly_reallocated_to_same_room(self,
                                                           person_identifier,
                                                           room_name):
        """
        person_identifier: Person's unique ID
        room_name: room to reallocate to
        Returns:
        True -  if we try to allocate person to a room
                where they are already allocated.
        False - otherwise.
        """
        room_name = room_name.upper()

        if self.fetch_room_type(room_name) == "office":

            if person_identifier in Amity.offices[room_name].allocations:
                return True
        if self.fetch_room_type(room_name) == "livingspace":
            if person_identifier in Amity.living_spaces[room_name].allocations:
                return True
        return False

    # gets person's identifier given the name and role
    def fetch_person_identifier(self, person_name, role):
        """
        returns: uses name and role to
                 return associated person identifier
        """
        person_name = person_name.upper()
        self.matched_identifiers_list = []

        if role in ["staff", "STAFF"]:
            self.staff_identifiers_list = Amity.staff.keys()
            for identifier in self.staff_identifiers_list:
                if person_name == Amity.staff[identifier].name:
                    self.matched_identifiers_list.append(identifier)

        elif role in ["fellow", "FELLOW"]:
            self.fellows_identifiers_list = Amity.fellows.keys()
            for identifier in self.fellows_identifiers_list:
                if person_name == Amity.fellows[identifier].name:
                    self.matched_identifiers_list.append(identifier)
        else:
            return "Role must be staff or fellow"

        return self.matched_identifiers_list

    # reallocates a person to a new room
    def reallocate_person(self, person_identifier, new_room_name):
        """
        :param person_identifier: Person's unique ID
        :param new_room_name: room to reallocate to
        :return: relevant message
        """
        new_room_name = new_room_name.upper()

        # check room name format
        if re.search(self.regex_name, new_room_name):
            return "\n Room name should consist of letters only"

        # check id format
        if not re.match(self.regex_person_id, person_identifier):
            return "\n Person identifier looks something like s-1a or f-2a\nuse the <get_person_identifier> command" +\
                   " to get a valid ID"

        # verify person_identifier
        if not self.confirm_person_identifier(person_identifier):
            return "\n Person identifier does not exist in the system " + \
                   "\n use the <get_person_identifier> command to get a valid ID"

        # verify room name
        if not self.confirm_room_name(new_room_name):
            return "\n Room " + new_room_name + " does not exist in the system"

        # check if room has space
        if not self.confirm_specific_room_has_space(new_room_name):
            return new_room_name + " is fully occupied"

        if self.confirm_person_not_doubly_reallocated_to_same_room(person_identifier, new_room_name):
            return "\n Person is already allocated to room " + new_room_name

        # get room type
        self.room_type = self.fetch_room_type(new_room_name)

        if self.room_type == "livingspace":

            if person_identifier.startswith("s"):
                return "\n Cannot reallocate a staff member to a living space"
            else:
                Amity.living_spaces[new_room_name].allocations.append(person_identifier)
                Amity.fellows[person_identifier].has_accommodation = new_room_name

        if self.room_type == "office":
            Amity.offices[new_room_name].allocations.append(person_identifier)

            if person_identifier.startswith("s"):

                Amity.staff[person_identifier].has_office = new_room_name
            else:
                Amity.fellows[person_identifier].has_office = new_room_name

        # check if person was reallocated a room of similar type
        # before and cancel that allocation

        result = self.fetch_rooms_with_allocations()

        # if there are any allocations, then we continue
        if result and (result[0] or result[1]):

            # if person is staff, we cancel any previous allocation with no further checks
            if person_identifier.startswith("s"):
                for room in result[1]:

                    # make sure we cancel only a previous allocation
                    # not the latest reallocation
                    if room == new_room_name:
                        continue

                    if person_identifier in Amity.offices[room].allocations:
                        id_index = Amity.offices[room].allocations.index(person_identifier)
                        del(Amity.offices[room].allocations[id_index])
                        break
            # if person is fellow, we check whether new reallocation
            # is to office or living space before we cancel any previous allocation
            else:
                if self.room_type == "office":
                    # cancel previous office allocation
                    for room in result[1]:

                        # make sure we cancel only a previous allocation
                        # not the latest reallocation
                        if room == new_room_name:
                            continue

                        if person_identifier in Amity.offices[room].allocations:
                            id_index = Amity.offices[room].allocations.index(person_identifier)
                            del(Amity.offices[room].allocations[id_index])
                            break
                else:
                    # cancel previous living space allocation
                    for room in result[0]:

                        # make sure we cancel only a previous allocation
                        # not the latest reallocation
                        if room == new_room_name:
                            continue

                        if person_identifier in Amity.living_spaces[room].allocations:
                            id_index = Amity.living_spaces[room].allocations.index(person_identifier)
                            del(Amity.living_spaces[room].allocations[id_index])
                            break

            # return success message based on whether person is staff or fellow
            if person_identifier.startswith("s"):
                return "\n Person with identifier " + person_identifier + \
                       " and name " + Amity.staff[person_identifier].name + \
                       " was reallocated to " + new_room_name
            else:
                return "\n Person with identifier " + person_identifier + \
                       " and name " + Amity.fellows[person_identifier].name + \
                       " was reallocated to " + new_room_name

    # loads people from text file to system
    def load_people(self, source_file):
        """
        :param source_file: file with source data
        :return: relevant message
        """
        # get path to text files directory
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        filename = os.path.join(file_path, 'text_files/' + source_file)

        # make sure its a real file
        if not os.path.isfile(filename):
            return "\n Supply a real file in the text_files folder"

        # check file type
        if not source_file.endswith(".txt"):
            return "\n Source must be a txt file"

        # check if there's space to load people, exit with message otherwise
        if self.confirm_availability_of_space_in_amity() is not False:

            try:
                file_object = open(filename, "r")
                try:
                    lines_list = file_object.readlines()

                    for line in lines_list:

                        Amity.people_counter += 1
                        line_fragments = line.split()

                        if len(line_fragments) == 3:

                            self.add_person(line_fragments[0] + " " + line_fragments[1], line_fragments[2])

                        if len(line_fragments) == 4:
                            self.add_person(line_fragments[0] + " " + line_fragments[1],
                                                  line_fragments[2], line_fragments[3])

                    return "\n " + str(len(lines_list)) + " people were loaded into the system"

                finally:
                    file_object.close()

            except IOError as e:
                print(str(e))

        else:
            return "\n There is no free space currently, use the create_room command to create new space"

    # confirms whether there are allocations in the system
    def confirm_existence_of_allocations(self):
        """
        :return: True if allocations exist
                 False otherwise
        """
        if len(Amity.living_spaces) > 0:
            rooms = Amity.living_spaces.keys()
            for room in rooms:
                if len(Amity.living_spaces[room].allocations) > 0:
                    return True
        if len(Amity.offices) > 0:
            rooms = Amity.offices.keys()
            for room in rooms:
                if len(Amity.offices[room].allocations) > 0:
                    return True
        return False

    # fetches list of all rooms with allocations
    def fetch_rooms_with_allocations(self):
        """
        :return: list of rooms with allocations if any
                 False otherwise
        """
        self.livingspaces_with_allocations = []
        self.offices_with_allocations = []

        if self.search_rooms_list():

            result = self.search_rooms_list()
            for room in result[1]:
                if len(Amity.offices[room].allocations) > 0:
                    self.offices_with_allocations.append(room)
            for room in result[0]:
                if len(Amity.living_spaces[room].allocations) > 0:
                    self.livingspaces_with_allocations.append(room)
            return [self.livingspaces_with_allocations, self.offices_with_allocations]
        return False

    # prints all allocations in the system
    def print_allocations(self, allocated_file_name=""):
        """
        Prints allocations to the screen or
        writes to file if file name is given
        """

        # first check if there are any allocations
        if self.confirm_existence_of_allocations():

            result = self.fetch_rooms_with_allocations()

            # check if file name was given
            if allocated_file_name:

                # check file type
                if not allocated_file_name.endswith(".txt"):
                    return "\n Destination must be a txt file"

                file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
                filename = os.path.join(file_path, "text_files/" + allocated_file_name)

                try:
                    file_object = open(filename, "w")
                    try:
                        for room in result[1]:

                            file_object.write("\n" + room + "\n")
                            file_object.write("-------------------------------------\n")
                            list_length = len(Amity.offices[room].allocations)

                            i = 1
                            names_string = ""
                            for value in Amity.offices[room].allocations:


                                if i < list_length:
                                    if value.startswith("s"):
                                        names_string += Amity.staff[value].name + ", "
                                    else:
                                        names_string += Amity.fellows[value].name + ", "
                                else:
                                    if value.startswith("s"):
                                        names_string += Amity.staff[value].name + "\n"
                                    else:
                                        names_string += Amity.fellows[value].name + "\n"
                                i += 1

                            file_object.write(names_string)

                        for room in result[0]:

                            file_object.write("\n" + room + "\n")
                            file_object.write("-------------------------------------\n")
                            list_length = len(Amity.living_spaces[room].allocations)

                            i = 1
                            names_string = ""
                            for value in Amity.living_spaces[room].allocations:


                                if i < list_length:
                                        names_string += Amity.fellows[value].name + ", "
                                else:
                                        names_string += Amity.fellows[value].name + "\n"
                                i += 1

                            file_object.write(names_string)

                        print("\n Allocations were written successfully to ", filename)

                    finally:
                        file_object.close()
                except IOError as e:
                    print(str(e))

            else:

                for room in result[1]:

                    print("\n" + room)
                    print("-------------------------------------")
                    list_length = len(Amity.offices[room].allocations)

                    i = 1
                    names_string = ""
                    for value in Amity.offices[room].allocations:

                        if i < list_length:
                            if value.startswith("s"):
                                names_string += Amity.staff[value].name + ", "
                            else:
                                names_string += Amity.fellows[value].name + ", "

                        else:
                            if value.startswith("s"):
                                names_string += Amity.staff[value].name
                            else:
                                names_string += Amity.fellows[value].name

                        i += 1

                    print(names_string)

                for room in result[0]:

                    print("\n" + room)
                    print("-------------------------------------")
                    list_length = len(Amity.living_spaces[room].allocations)

                    i = 1
                    names_string = ""
                    for value in Amity.living_spaces[room].allocations:

                        if i < list_length:
                                names_string += Amity.fellows[value].name + ", "

                        else:
                                names_string += Amity.fellows[value].name

                        i += 1

                    print(names_string)
        else:
            print("\n There are currently no allocations in the system")

    # verifies whether unallocated people exist
    def confirm_existence_of_unallocated(self):
        """
        :return: True if unallocated people are found
                 False otherwise
        """
        # if there are any people in the system
        if len(Amity.fellows) > 0 or len(Amity.staff) > 0:
            # put their IDs into lists
            fellows_ids = Amity.fellows.keys()
            staff_ids = Amity.staff.keys()

            for person_id in fellows_ids:
                # check if any of the fellows has not been allocated an office
                if not Amity.fellows[person_id].has_office:
                    return True

                # check if any of the fellows who wanted a
                # living space has not been allocated one
                if Amity.fellows[person_id].accommodation == "Y" and \
                   not Amity.fellows[person_id].has_accommodation:

                    return True

            for person_id in staff_ids:
                # check if any of the staff has not been allocated an office
                if not Amity.staff[person_id].has_office:
                    return True
        return False

    # prints names of people without room allocations
    def print_unallocated(self, destination_file_name=""):
        """
        :param destination_file_name: file to write to
        :return:
        """
        # check if unallocated people exist
        if self.confirm_existence_of_unallocated():

            # if no file name given, print to screen
            if destination_file_name == "":
                # if there are any people in the system

                # put their IDs into lists
                fellows_ids = Amity.fellows.keys()
                staff_ids = Amity.staff.keys()

                for person_id in fellows_ids:
                    # check if any of the fellows has not been allocated an office
                    # and print name to screen
                    if not Amity.fellows[person_id].has_office:
                        print("\n " + Amity.fellows[person_id].name + " - not allocated office")

                    # check if any of the fellows who wanted a
                    # living space has not been allocated one
                    # and print name to screen
                    if Amity.fellows[person_id].accommodation == "Y" and \
                       not Amity.fellows[person_id].has_accommodation:

                        print("\n " + Amity.fellows[person_id].name + " - not allocated living space")

                for person_id in staff_ids:
                    # check if any of the staff has not been allocated an office
                    # and print name to screen
                    if not Amity.staff[person_id].has_office:
                        print("\n " + Amity.staff[person_id].name + " - not allocated office")

            else:
                file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
                filename = os.path.join(file_path, 'text_files/' + destination_file_name)

                try:
                    file_object = open(filename, "w")

                    try:

                        # put their IDs into lists
                        fellows_ids = Amity.fellows.keys()
                        staff_ids = Amity.staff.keys()

                        for person_id in fellows_ids:
                            # check if any of the fellows has not been allocated an office
                            # and write to file
                            if not Amity.fellows[person_id].has_office:
                                file_object.write(Amity.fellows[person_id].name + " - not allocated office\n")

                            # check if any of the fellows who wanted a
                            # living space has not been allocated one
                            # and write to file
                            if Amity.fellows[person_id].accommodation == "Y" and \
                                not Amity.fellows[person_id].has_accommodation:

                                file_object.write(Amity.fellows[person_id].name + " - not allocated living space\n")

                        for person_id in staff_ids:
                            # check if any of the staff has not been allocated an office
                            # and write to file
                            if not Amity.staff[person_id].has_office:
                                file_object.write(Amity.staff[person_id].name + " - not allocated office\n")

                        print("\n Unallocated people were written successfully to ", filename)

                    finally:
                        file_object.close()

                except IOError as e:
                    print("File access error - " + str(e))
        else:
            print("\n There are no unallocated people in the system")

    # verifies whether room has allocations
    def confirm_existence_of_allocations_for_particular_room(self, room_name):
        """
        :param room_name: name of room to check
        :return: True if allocations exist
                 False otherwise
        """

        room_type = self.fetch_room_type(room_name)
        if room_type and room_type == "office":
            if len(Amity.offices[room_name].allocations) > 0:
                return True
        if room_type and room_type == "livingspace":
            if len(Amity.living_spaces[room_name].allocations) > 0:
                return True
        return False

    # prints allocations for given room
    def print_room(self, room_name):
        """
        :param room_name: room to print allocations from
        :return: prints output to screen
        """

        # validate room name
        if re.search(self.regex_name, room_name):

            print("\n Use letters only for room names")

        else:

            room_name = room_name.upper()

            # verify existence of room name in system
            if self.confirm_room_name(room_name):

                if self.confirm_existence_of_allocations_for_particular_room(room_name):

                    if self.fetch_room_type(room_name) == "office":

                        for person_id in Amity.offices[room_name].allocations:

                            if person_id.startswith("s"):
                                print("\n " + Amity.staff[person_id].name)
                            else:
                                print("\n " + Amity.fellows[person_id].name)
                    else:

                        for person_id in Amity.living_spaces[room_name].allocations:

                            print("\n " + Amity.fellows[person_id].name)
                else:
                    print("\n " + room_name + " has no allocations currently")
            else:
                print("\n " + room_name + " does not exist in the system")

    # creates required database
    def create_database(self, dbname):
        """
        :param dbname: name of db to create
        :return: True on success
                 False otherwise
        """
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        filename = os.path.join(file_path, "db_files/" + dbname)

        # if db already exists, delete it
        if os.path.isfile(filename):
            os.remove(filename)

        try:
            connection = sqlite3.connect(filename)
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            cursor.execute("""CREATE TABLE tbl_people (id INTEGER PRIMARY KEY NOT NULL,
                           person_name TEXT NOT NULL, person_identifier TEXT NOT NULL,
                           accommodation TEXT NOT NULL DEFAULT 'N', has_office BOOLEAN NOT NULL DEFAULT 0,
                           has_livingspace BOOLEAN NOT NULL DEFAULT 0)""")
            cursor.execute("""CREATE TABLE tbl_rooms (id INTEGER PRIMARY KEY NOT NULL,
                           room_name TEXT NOT NULL, room_type TEXT NOT NULL)""")
            cursor.execute("""CREATE TABLE tbl_allocations (id INTEGER PRIMARY KEY NOT NULL,
                           room_name TEXT NOT NULL, person_id TEXT NO NULL)""")
            connection.commit()
            connection.close()
            return True

        except sqlite3.Error as e:

            return str(e)

    # writes data from memory to database
    def save_state(self, destination_db=""):
        """
        :param destination_db: database to save to
        :return: success message on success
                 failure message on failure
        """
        if destination_db:
            file_end = destination_db
        else:
            file_end = "amity.db"

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        filename = os.path.join(file_path, "db_files/" + file_end)
        if os.path.isfile(filename):
            os.remove(filename)

        # ensure there's some data to save
        if len(Amity.fellows) > 0 or len(Amity.staff) > 0 or \
           len(Amity.living_spaces) > 0 or len(Amity.offices) > 0:

            # ensure database has been created
            if self.create_database(file_end) is True:

                try:
                    connection = sqlite3.connect(filename)
                    cursor = connection.cursor()

                    # if any fellows in system
                    if len(Amity.fellows) > 0:

                        fellow_ids = Amity.fellows.keys()
                        # insert fellows into table
                        for item in fellow_ids:

                            has_office = 0
                            has_livingspace = 0

                            if Amity.fellows[item].has_office is not False:
                                has_office = 1
                            if Amity.fellows[item].has_accommodation is not False:
                                has_livingspace = 1

                            cursor.execute("""INSERT INTO tbl_people (person_name, person_identifier,
                                           accommodation, has_office, has_livingspace) VALUES (?,?,?,?,?)""",
                                           (
                                               Amity.fellows[item].name,
                                                item,
                                               Amity.fellows[item].accommodation,
                                                has_office,
                                                has_livingspace
                                           )
                                           )
                        connection.commit()

                    # if any staff in system
                    if len(Amity.staff) > 0:

                        staff_ids = Amity.staff.keys()
                        # insert staff into table
                        for item in staff_ids:

                            has_office = 0

                            if Amity.staff[item].has_office is not False:
                                has_office = 1

                            cursor.execute("""INSERT INTO tbl_people (person_name, person_identifier,
                                           has_office)VALUES (?,?,?)""",
                                           (
                                               Amity.staff[item].name,
                                               item,
                                               has_office
                                           )
                                           )
                        connection.commit()

                    # if any living spaces in system
                    if len(Amity.living_spaces) > 0:

                        living_space_names = Amity.living_spaces.keys()
                        # insert living spaces into table rooms
                        for item in living_space_names:

                            cursor.execute("""INSERT INTO tbl_rooms (room_name, room_type) VALUES (?,?)""",
                                           (
                                               item,
                                               "livingspace"
                                           )
                                           )

                            for person_id in Amity.living_spaces[item].allocations:
                                cursor.execute("""INSERT INTO tbl_allocations (room_name, person_id) VALUES (?,?)""",
                                               (
                                                   item,
                                                   person_id
                                               )
                                               )
                        connection.commit()

                    # if any offices in system
                    if len(Amity.offices) > 0:

                        office_names = Amity.offices.keys()
                        # insert offices into table rooms
                        for item in office_names:

                            cursor.execute("""INSERT INTO tbl_rooms (room_name, room_type) VALUES (?,?)""",
                                           (
                                               item,
                                               "office"
                                           )
                                           )

                            for person_id in Amity.offices[item].allocations:
                                cursor.execute("""INSERT INTO tbl_allocations (room_name, person_id) VALUES (?,?)""",
                                               (
                                                   item,
                                                   person_id
                                               )
                                               )
                        connection.commit()

                except sqlite3.Error as e:
                    return "An error occurred - " + str(e)

            return "State was saved successfully to " + filename

    # verifies existence of db file to be used by load_state()
    def confirm_existence_of_db_file(self, file_name):
        """
        :param file_name: file to search for
        :return: True if found
                 False otherwise
        """
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        file_name = os.path.join(file_path, "db_files/" + file_name)

        if os.path.isfile(file_name):
            return True
        return False

    # loads data from database to memory
    def load_state(self, source_db):
        """
        :param source_db: source database file
        :return: success message on success
                 error message otherwise
        """
        # reject files that are not sqlite3 database files
        if not source_db.endswith(".db"):
            return "\n File extension must be .db"
        # confirm existence of db source file
        if not self.confirm_existence_of_db_file(source_db):
            return "\n File does not exist"

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        filename = os.path.join(file_path, "db_files/" + source_db)

        try:
            connection = sqlite3.connect(filename)
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            # fetch all data from table people
            cursor.execute("SELECT * FROM tbl_people")
            rows = cursor.fetchall()

            for row in rows:

                office_name = False
                livingspace_name = False

                if row["has_office"] is not 0:
                    office_name = row["has_office"]

                if row["has_livingspace"] is not 0:
                    livingspace_name = row["has_livingspace"]

                # if person is staff, store in staff dictionary
                if row["person_identifier"].startswith("s"):

                    Amity.staff[row["person_identifier"]] = Staff(row["person_name"])
                    Amity.staff[row["person_identifier"]].has_office = office_name
                else:
                    # if person is fellow, store in fellow dictionary
                    Amity.fellows[row["person_identifier"]] = Fellow(row["person_name"])
                    Amity.fellows[row["person_identifier"]].accommodation = row["accommodation"]
                    Amity.fellows[row["person_identifier"]].has_office = office_name
                    Amity.fellows[row["person_identifier"]].has_accommodation = livingspace_name

            # fetch all data from table rooms
            cursor.execute("SELECT * FROM tbl_rooms")
            rows = cursor.fetchall()
            for row in rows:
                # if room is office, store in office dictionary
                if row["room_type"] == "office":
                    Amity.offices[row["room_name"]] = Office(row["room_name"])

                else:
                    # if room is living space, store in living space dictionary
                    Amity.living_spaces[row["room_name"]] = LivingSpace(row["room_name"])

            # fetch all data from table allocations
            cursor.execute("SELECT * FROM tbl_allocations")
            rows = cursor.fetchall()

            for row in rows:
                # if room is office
                if row["room_name"] in Amity.offices.keys():

                    Amity.offices[row["room_name"]].allocations.append(row["person_id"])

                # if room is living space
                if row["room_name"] in Amity.living_spaces.keys():

                    Amity.living_spaces[row["room_name"]].allocations.append(row["person_id"])


        except sqlite3.Error as e:
            print("DB access error - ", str(e))

        return "\n State was loaded successfully from " + filename

    # give name to fetch unique identifier
    def get_person_identifier(self, first_name, last_name, role):
        """Takes name and role and returns person identifier"""

        self.fetched_identifiers = []

        first_name = first_name.upper()
        last_name = last_name.upper()

        # check name format for illegal characters
        if re.search(self.regex_name, first_name + " " + last_name):
            return "\n Use letters only for person name"

        if role not in ["fellow", "staff", "FELLOW", "STAFF"]:
            return "\n Role must be either fellow or staff"

        # search in fellows dict
        if role in ["fellow", "FELLOW"]:

            self.fetched_identifiers = [person_id for person_id in Amity.fellows.keys() if \
                                        Amity.fellows[person_id].name == first_name + " " + last_name]

        else:
            # search in staff dict
            self.fetched_identifiers = [person_id for person_id in Amity.staff.keys() if \
                                        Amity.staff[person_id].name == first_name + " " + last_name]

        return self.fetched_identifiers

    # gets person's allocation details
    def see_person_allocations(self, person_id):
        """
        :param person_id:
        :return:
        """

        # check id format
        if not re.match(self.regex_person_id, person_id):
            return "\n Person identifier looks something like s-1a or f-2a\nuse the " +\
                   "<get_person_identifier> command to get a valid ID"

        # verify person_identifier
        if not self.confirm_person_identifier(person_id):
            return "\n Person identifier does not exist in the system " + \
                   "\n use the <get_person_identifier> command to get a valid ID"

        msg = ""

        # if person is staff, retrieve from staff dict
        if person_id.startswith("s-"):
            name = Amity.staff[person_id].name
            office = Amity.staff[person_id].has_office

            if office:
                msg = "\n Staff member " + name + " is allocated to office " + office

            else:
                msg = "\n Staff member " + name + " is not yet allocated an office"


        else:
            # if person is fellow, retrieve from fellow dict
            name = Amity.fellows[person_id].name
            office = Amity.fellows[person_id].has_office
            accommodation = Amity.fellows[person_id].has_accommodation
            wants_accommodation = Amity.fellows[person_id].accommodation

            msg += "\n Fellow " + name + " details:\n Office: " + str(office) + "\n Wants ccommodation: " + \
                   wants_accommodation+ "\n Accommodation: " + str(accommodation)

        return msg




