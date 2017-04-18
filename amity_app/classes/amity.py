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
    amity room allocation app
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

            with open(self.filename, "r") as file_object:

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

            with open(self.filename, "w") as file_object:
                file_object.write("b")

        # self.new_room_name = ""
        # self.allocated_file_name = ""
        # self.unallocated_file_name = ""
        # self.room_name = ""
        # self.source_db = ""
        # self.destination_db = ""
        #
        #
        # self.fellows_list = []
        # self.staff_list = []

        self.regex_name = r'(\(|\+|\?|\.|\*|\^|\$|\)|\[|\]|\{|\}|\||\\|[0-9]|\`|\&|\~|\!|\@|\#|\%|\_|\=|\;|\:|\"|\,|\<|\>|\/)'
        self.regex_room_name = r'(\(|\+|\?|\.|\*|\^|\$|\)|\&|\[|\]|\{|\}|\||\\|\`|\~|\!|\@|\#|\%|\_|\=|\;|\:|\"|\,|\<|\>|\/)'
        self.regex_person_id = r'^[s|f]-[1-9]{1,3}[a-z]{1}$'

    # verifies overall availability of space in amity
    def confirm_availability_of_space_in_amity(self):
        """
        :return: True if space is available
                 False otherwise
        """

        # check if any living space is not full
        if len([room for room in Amity.living_spaces if len(Amity.living_spaces[room].allocations)
                < Amity.living_spaces[room].room_capacity]):
            return True

        # check if any office is not full
        if len([room for room in Amity.offices if len(Amity.offices[room].allocations)
                < Amity.offices[room].room_capacity]):
            return True

        # all rooms are full
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

        # fetch living spaces names if any in system
        living_space_rooms  = Amity.living_spaces.keys()

        # fetch offices names if any in system
        office_rooms  = Amity.offices.keys()

        return [living_space_rooms, office_rooms]


    # fetches list of rooms with space
    def fetch_rooms_with_space(self):
        """
        :return: a list of 2 lists - empty or populated: one for offices with space (if any)
                 and one for livingspaces with space (if any)
        """

        # check if any rooms in system
        if Amity.offices or Amity.living_spaces:

            # populate list of offices with space if any
            offices_with_space = [room for room in Amity.offices
                                  if len(Amity.offices[room].allocations) < \
                                  Amity.offices[room].room_capacity]

            # populate list of living spaces with space if any
            living_spaces_with_space = [room for room in Amity.living_spaces
                                        if len(Amity.living_spaces[room].allocations) < \
                                        Amity.living_spaces[room].room_capacity]

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

        return_message = "\n "

        # ensure no illegal characters in name i.e any of
        # ( + ? . *  ^ $  ( ) \ [ ] { } | \ ) [0-9] ` ~ ! @ # % _ = ; : " , < . > /
        if re.search(self.regex_name, name):
            return [0, "\n Avoid any of the following characters in name: + ? . * " + \
                    "^ $ ( ) \ [ ] { } | \  [0-9] & ` ~ ! @ # % _ = ; : \" , < . > /\n"]

        # ensure role is staff or fellow
        if role not in ["staff", "STAFF", "fellow", "FELLOW"]:
            return [0,"\n role must be staff or fellow"]

        if role == "STAFF" and wants_accommodation == "Y":
            return [0, "\n Staff cannot be allocated living spaces\n"]

        # increment people counter by 1
        Amity.people_counter += 1

        if role == "FELLOW":

            fellow_object = Fellow(name)
            if wants_accommodation and wants_accommodation == "Y":
                fellow_object.accommodation = "Y"
            # make unique identifier for new fellow
            fellow_object.person_id = "f-" + str(Amity.people_counter) + Amity.session_id

            # insert new fellow into fellows dictionary with id as key
            Amity.fellows[fellow_object.person_id] = fellow_object

            return_message += fellow_object.name + " with ID " + fellow_object.person_id + \
                                   " was added successfully as a fellow\n"

        if role == "STAFF":

            staff_object = Staff(name)

            # make unique identifier for new person
            staff_object.person_id = "s-" + str(Amity.people_counter) + Amity.session_id

            # insert new staff into staff dictionary with id as key
            Amity.staff[staff_object.person_id] = staff_object

            return_message += staff_object.name + " with ID " + staff_object.person_id + \
                                   " was added successfully as a member of staff\n"

        # fetch list of rooms with space
        rooms_with_space = self.fetch_rooms_with_space()

        if rooms_with_space:

            livingspaces_with_space = rooms_with_space[0]
            offices_with_space = rooms_with_space[1]

            if role == "FELLOW":

                # if there's office with space, allocate to new fellow
                if offices_with_space:
                    random_room = random.choice(offices_with_space)

                    Amity.offices[random_room].allocations.append(fellow_object.person_id)
                    Amity.fellows[fellow_object.person_id].has_office = random_room

                    return_message += "\n and allocated to the office " + random_room + "\n"
                else:
                    return_message += "\n and was not allocated an office due to lack of space\n"

                    # check if fellow wants accommodation
                if Amity.fellows[fellow_object.person_id].accommodation == "Y":

                    # if there's a living space with space, allocate to fellow
                    if livingspaces_with_space:

                        random_room = random.choice(livingspaces_with_space)
                        Amity.living_spaces[random_room].allocations.append(fellow_object.person_id)
                        Amity.fellows[fellow_object.person_id].has_accommodation = random_room

                        return_message += "\n and allocated to the living space " + random_room + "\n"
                    else:
                        return_message += "\n and was not allocated a living space due to lack of space\n"

            if role == "STAFF":
                # if there's office with space, allocate to new staff
                if offices_with_space:
                    random_room = random.choice(offices_with_space)

                    Amity.offices[random_room].allocations.append(staff_object.person_id)
                    Amity.staff[staff_object.person_id].has_office = random_room

                    return_message += "\n and allocated to the office " + random_room + "\n"
                else:
                    return_message += "\n and was not allocated an office due to lack of space\n"

        else:

            if role == "STAFF":

                return_message += "\n But was not allocated an office due to lack of space\n"
            else:
                return_message += "\n But was not allocated an office or living space due to lack of space\n"

        if role == "FELLOW":
            return [fellow_object.person_id, return_message]
        if role == "STAFF":
            return [staff_object.person_id, return_message]

    # creates rooms in amity
    def create_room(self, room_type, room_names):

        successfully_created_rooms = []
        format_error_room_names = []
        already_existing_rooms = []

        success_msg = ""
        error_msg = ""
        failure_msg = ""

        for name in room_names:

            name = name.upper()

            # ensure no illegal characters in room name i.e any of
            # ( + ? . *  ^ $  ( ) \ [ ] { } | \ ) ` ~ ! @ # % _ = ; : " , < . > /
            if re.search(self.regex_room_name, name):
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

        if successfully_created_rooms:
            success_msg = "\n Successfully created " + room_type.lower() + "s: " + \
                          str(len(successfully_created_rooms))\
                          + " ,\n " + " ".join(successfully_created_rooms) + "\n"

        if format_error_room_names:
            error_msg = "\n Room names rejected due to format errors: " + \
                        str(len(format_error_room_names)) + " ,\n "\
                        + " ".join(format_error_room_names) + "\n"

        if already_existing_rooms:
            failure_msg = "\n Room names rejected because they already exist: " + \
                          str(len(already_existing_rooms)) +\
                          " ,\n " + " ".join(already_existing_rooms) + "\n"

        return success_msg + error_msg + failure_msg

    # confirms whether user has entered a valid identifier
    def confirm_person_identifier_exists(self, person_identifier):
        """
        :param person_identifier: person's identifier
        :return: True if identifier is valid
                 False otherwise
        """

        if not Amity.fellows and not Amity.staff:
            return False

        fellows_ids = Amity.fellows.keys()
        staff_ids = Amity.staff.keys()

        return person_identifier in fellows_ids or person_identifier in staff_ids

    # Confirms whether specific room has space for further allocations
    def confirm_specific_room_has_space(self, room_name):
        """
        :param room_name: room name
        :return: True if space is available
                 False otherwise
        """
        room_name = room_name.upper()
        result = self.search_rooms_list()

        # first confirm there are rooms
        if result:

            if room_name in result[0]:
                return len(Amity.living_spaces[room_name].allocations) < Amity.living_spaces[room_name].room_capacity
            if room_name in result[1]:
                return len(Amity.offices[room_name].allocations) < Amity.offices[room_name].room_capacity
        return False

    # Fetches room type given room name
    def fetch_room_type(self, room_name):
        """
        :param room_name: name of room to identify
        :return: room type if room exists
                 false otherwise
        """
        result = self.search_rooms_list()
        if result:
            room_name = room_name.upper()

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

    # reallocates a person to a new room
    def reallocate_person(self, person_identifier, new_room_name):
        """
        :param person_identifier: Person's unique ID
        :param new_room_name: room to reallocate to
        :return: relevant message
        """
        new_room_name = new_room_name.upper()

        # check room name format
        if re.search(self.regex_room_name, new_room_name):
            return "\n Room name should consist of letters and/or digits only"

        # check id format
        if not re.match(self.regex_person_id, person_identifier):
            return "\n Person identifier looks something like s-1a or f-2a\nuse the <get_person_identifier> command" +\
                   " to get a valid ID"

        # verify person_identifier
        if not self.confirm_person_identifier_exists(person_identifier):
            return "\n Person identifier does not exist in the system " + \
                   "\n use the <get_person_identifier> command to get a valid ID"

        # verify room name
        if new_room_name not in Amity.offices and new_room_name not in Amity.living_spaces:
            return "\n Room " + new_room_name + " does not exist in the system"

        # check if room has space
        if not self.confirm_specific_room_has_space(new_room_name):
            return "\n Room " + new_room_name + " is fully occupied"

        # check if person is already allocated to the room
        if self.confirm_person_not_doubly_reallocated_to_same_room(person_identifier, new_room_name):
            return "\n Person is already allocated to room " + new_room_name

        # get room type
        room_type = self.fetch_room_type(new_room_name)

        if room_type == "livingspace":

            if person_identifier.startswith("s"):
                return "\n Cannot reallocate a staff member to a living space"
            else:
                Amity.living_spaces[new_room_name].allocations.append(person_identifier)
                Amity.fellows[person_identifier].has_accommodation = new_room_name

        if room_type == "office":
            Amity.offices[new_room_name].allocations.append(person_identifier)

            if person_identifier.startswith("s"):

                Amity.staff[person_identifier].has_office = new_room_name
            else:
                Amity.fellows[person_identifier].has_office = new_room_name

        # check if person was allocated a room of similar type
        # before and cancel that allocation

        result = self.fetch_rooms_with_allocations()

        # if there are any allocations, then we continue
        if result:

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
                if room_type == "office":
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
        if self.confirm_availability_of_space_in_amity():

            try:
                file_object = open(filename, "r")
                try:

                    lines_list = file_object.readlines()
                    successfull_loads = 0
                    failed_loads = 0
                    success_msg = ""
                    failure_msg = ""

                    # check if file has any contents
                    if len(lines_list):

                        for line in lines_list:

                            line_fragments = line.split()

                            # check for first valid format i.e first name, last name, role
                            if len(line_fragments) == 3:

                                result = self.add_person(line_fragments[0] + " " + line_fragments[1], line_fragments[2])

                                # count how many failed loads we got if any
                                if result[0] == 0:
                                    failed_loads += 1

                                # count how many successful loads we got if any
                                else:
                                    successfull_loads += 1

                            # check for second valid format i.e first name, last name, role, wants_accommodation
                            elif len(line_fragments) == 4:
                                result = self.add_person(line_fragments[0] + " " + line_fragments[1],
                                                      line_fragments[2], line_fragments[3])
                                # count how many failed loads we got if any
                                if result[0] == 0:
                                    failed_loads += 1

                                # count how many successful loads we got if any
                                else:
                                    successfull_loads += 1

                            # none of the two valid formats was found
                            else:
                                return "\n Contents of text file are not in the correct format"
                    else:
                        return "\n File is empty, has no contents"

                    if successfull_loads:
                        # format success message
                        if successfull_loads > 1:
                            msg_string = " people were"
                        else:
                            msg_string = " person was"

                        success_msg = "\n " + str(successfull_loads) + msg_string + \
                                       " loaded into the system successfully"

                    if failed_loads:
                        # format failure message
                        if failed_loads > 1:
                            msg_string = " people were"
                        else:
                            msg_string = " person was"

                        failure_msg = "\n " + str(failed_loads) + msg_string +\
                                      " not loaded into the system due to errors in name and/or role formats"

                    return success_msg + failure_msg

                finally:
                    file_object.close()

            except IOError as e:
                return str(e)

        else:
            return "\n There is no free space currently, use the create_room command to create new space"

    # fetches list of all rooms with allocations
    def fetch_rooms_with_allocations(self):
        """
        :return: list of rooms with allocations if any
                 False otherwise
        """
        # get occupied offices if any
        offices_with_allocations = [room for room in Amity.offices if len(Amity.offices[room].allocations) > 0]
        # get occupied living spaces if any
        livingspaces_with_allocations = [room for room in Amity.living_spaces
                                             if len(Amity.living_spaces[room].allocations) > 0]

        if offices_with_allocations or livingspaces_with_allocations:
            return [livingspaces_with_allocations, offices_with_allocations]

        return False

    # prints all allocations in the system
    def print_allocations(self, allocated_file_name=""):
        """
        Prints allocations to the screen or
        writes to file if file name is given
        """

        result = self.fetch_rooms_with_allocations()

        # first check if there are any allocations
        if result:

            # check if file name was given
            if allocated_file_name:

                # check file type
                if not allocated_file_name.endswith(".txt"):
                    return "\n Destination must be a txt file"

                # set file path
                file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
                filename = os.path.join(file_path, "text_files/" + allocated_file_name)

                try:
                    file_object = open(filename, "w")
                    try:

                        for room in result[1]:

                            # write current room name (office) to file
                            file_object.write("\n" + room + "\n")
                            file_object.write("-------------------------------------\n")
                            list_length = len(Amity.offices[room].allocations)

                            i = 1
                            names_string = ""

                            # build string of people names in current office
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

                            # write string of people names in current office to file
                            file_object.write(names_string)

                        for room in result[0]:

                            # write current room name (living space) to file
                            file_object.write("\n" + room + "\n")
                            file_object.write("-------------------------------------\n")
                            list_length = len(Amity.living_spaces[room].allocations)

                            i = 1
                            names_string = ""

                            # build string of people names in current livingspace
                            for value in Amity.living_spaces[room].allocations:


                                if i < list_length:
                                        names_string += Amity.fellows[value].name + ", "
                                else:
                                        names_string += Amity.fellows[value].name + "\n"
                                i += 1

                            # write string of people names in current living space to file
                            file_object.write(names_string)

                        print("\n Allocations were written successfully to ", filename)

                    finally:
                        file_object.close()
                except IOError as e:
                    print(str(e))

            else:

                for room in result[1]:

                    # print current room name (office) to screen
                    print("\n" + room)
                    print("-------------------------------------")
                    list_length = len(Amity.offices[room].allocations)

                    i = 1
                    names_string = ""

                    # build string of people names in current office
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

                    # print string of people names in current office to screen
                    print(names_string)

                for room in result[0]:

                    # print current room name (living space) to screen
                    print("\n" + room)
                    print("-------------------------------------")
                    list_length = len(Amity.living_spaces[room].allocations)

                    i = 1
                    names_string = ""

                    # build string of people names in current livingspace
                    for value in Amity.living_spaces[room].allocations:

                        if i < list_length:
                                names_string += Amity.fellows[value].name + ", "

                        else:
                                names_string += Amity.fellows[value].name

                        i += 1
                    # print string of people names in current living space to screen
                    print(names_string)
        else:
            print("\n There are currently no allocations in the system")

    # returns list of unallocated people if any
    def fetch_list_of_unallocated_people(self):
        """
        :return: list of unallocated people if any
                 False otherwise
        """
        # if there are any people in the system
        if Amity.fellows or Amity.staff:

            # put their IDs into lists
            fellows_ids = Amity.fellows.keys()
            staff_ids = Amity.staff.keys()

            # fetch any of the fellows who has not been allocated an office
            fellows_without_offices = [person_id for person_id in fellows_ids
                                       if Amity.fellows[person_id].has_office == False]

            # fetch any of the fellows who wanted a
            # living space and has not been allocated one
            fellows_without_livingspaces = [person_id for person_id in fellows_ids if
                                            Amity.fellows[person_id].accommodation == "Y" and
                                            Amity.fellows[person_id].has_accommodation == False]

            # fetch any of the staff who has not been allocated an office
            staff_without_offices = [person_id for person_id in staff_ids if Amity.staff[person_id].has_office == False]

            # if any unallocated people, return them in list
            if fellows_without_offices or fellows_without_livingspaces or staff_without_offices:

                return [fellows_without_livingspaces, fellows_without_offices, staff_without_offices]

        return False

    # prints names of people without room allocations
    def print_unallocated(self, destination_file_name=""):
        """
        :param destination_file_name: file to write to
        :return: prints message to screen
        """
        # check if unallocated people exist
        result = self.fetch_list_of_unallocated_people()

        if result:

            # if no file name given, print to screen
            if destination_file_name == "":

                # print names of fellows who wanted living spaces and were not allocated if any
                for person_id in result[0]:

                    print("\n " + Amity.fellows[person_id].name + " - not allocated living space")

                # print names of fellows without offices if any
                for person_id in result[1]:
                    print("\n " + Amity.fellows[person_id].name + " - not allocated office")

                # print names of staff without offices if any
                for person_id in result[2]:
                    print("\n " + Amity.staff[person_id].name + " - not allocated office")

            else:

                # check file type
                if not destination_file_name.endswith(".txt"):

                    print("\n Destination must be a txt file")
                    return

                file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
                filename = os.path.join(file_path, 'text_files/' + destination_file_name)

                try:
                    file_object = open(filename, "w")

                    try:

                        # write to file names of fellows who wanted living spaces and were not allocated if any
                        for person_id in result[0]:
                            file_object.write(Amity.fellows[person_id].name + " - not allocated living space\n")

                        # write to file names of fellows without offices if any
                        for person_id in result[1]:
                            file_object.write(Amity.fellows[person_id].name + " - not allocated office\n")

                        # write to file names of staff without offices if any
                        for person_id in result[2]:
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

        if room_type:
            room_name = room_name.upper()

            if room_type == "office":
                if len(Amity.offices[room_name].allocations) > 0:
                    return True
            if room_type == "livingspace":
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
        if re.search(self.regex_room_name, room_name):

            print("\n Use letters and/or digits only for room names")

        else:

            room_name = room_name.upper()

            # verify existence of room name in system
            if room_name in Amity.offices or room_name in Amity.living_spaces:

                # check if room has any allocations
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
                    print("\n Room " + room_name + " has no allocations currently")
            else:
                print("\n Room " + room_name + " does not exist in the system")

    # creates required database
    def create_database(self, dbname):
        """
        :param dbname: name of db to create
        :return: True on success
                 False otherwise
        """
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        filename = os.path.join(file_path, "db_files/" + dbname)

        # if db already exists, return true
        if os.path.isfile(filename):
            return True

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

            return False

    # writes data from memory to database
    def save_state(self, destination_db=""):
        """
        :param destination_db: database to save to
        :return: success message on success
                 failure message on failure
        """

        if destination_db:
            # user given db name
            file_end = destination_db
        else:
            # default db name if user did not indicate
            file_end = "amity.db"

        # set file path
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        filename = os.path.join(file_path, "db_files/" + file_end)

        # flag to indicate if db was created successfully
        db_created = False

        # if db doesn't exist, we create it
        if not os.path.isfile(filename):
            db_created = self.create_database(file_end)

            if not db_created:
                return "\n Failed to create database"

        # ensure there's some data to save
        if Amity.fellows or Amity.staff or Amity.living_spaces or Amity.offices:

            # ensure database has been created or already existed
            if db_created or os.path.isfile(filename):

                try:
                    connection = sqlite3.connect(filename)
                    cursor = connection.cursor()

                    # if any fellows in system
                    if Amity.fellows:

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
                    if Amity.staff:

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
                    if Amity.living_spaces:

                        living_space_names = Amity.living_spaces.keys()
                        # insert living spaces into table rooms
                        for item in living_space_names:

                            cursor.execute("""INSERT INTO tbl_rooms (room_name, room_type) VALUES (?,?)""",
                                           (
                                               item,
                                               "livingspace"
                                           )
                                           )

                            # if livingspace has any allocations, insert into table allocations
                            for person_id in Amity.living_spaces[item].allocations:
                                cursor.execute("""INSERT INTO tbl_allocations (room_name, person_id) VALUES (?,?)""",
                                               (
                                                   item,
                                                   person_id
                                               )
                                               )
                        connection.commit()

                    # if any offices in system
                    if Amity.offices:

                        office_names = Amity.offices.keys()
                        # insert offices into table rooms
                        for item in office_names:

                            cursor.execute("""INSERT INTO tbl_rooms (room_name, room_type) VALUES (?,?)""",
                                           (
                                               item,
                                               "office"
                                           )
                                           )

                            # if office has any allocations, insert into table allocations
                            for person_id in Amity.offices[item].allocations:
                                cursor.execute("""INSERT INTO tbl_allocations (room_name, person_id) VALUES (?,?)""",
                                               (
                                                   item,
                                                   person_id
                                               )
                                               )
                        connection.commit()

                except sqlite3.Error as e:
                    return "\n An error occurred during insertions - " + str(e)

                return "\n State was saved successfully to " + filename

        else:
            return "\n There is no data in the system to save"

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

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        filename = os.path.join(file_path, "db_files/" + source_db)

        # confirm existence of db source file
        if not os.path.isfile(filename):
            return "\n File does not exist"

        try:
            connection = sqlite3.connect(filename)
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

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

            # fetch all data from table people
            cursor.execute("SELECT * FROM tbl_people")
            rows = cursor.fetchall()

            for row in rows:

                office_name = False
                livingspace_name = False

                if row["has_office"] is not 0:
                    office_name = [name for name in Amity.offices.keys() if row["person_identifier"]
                                   in Amity.offices[name].allocations][0]

                if row["has_livingspace"] is not 0:
                    livingspace_name = [name for name in Amity.living_spaces.keys() if row["person_identifier"]
                                        in Amity.living_spaces[name].allocations][0]

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


        except sqlite3.Error as e:
            return "\n DB access error - " + str(e)

        return "\n State was loaded successfully from " + filename

    # give name to fetch unique identifier
    def get_person_identifier(self, first_name, last_name, role):
        """Takes name and role and returns person identifier"""

        # check name format for illegal characters
        if re.search(self.regex_name, first_name) or re.search(self.regex_name, last_name):
            return "\n Use letters only for person name"

        person_name = first_name.upper() + " " + last_name.upper()

        if role == "fellow":
            # search in fellows dict
            fetched_identifiers = [person_id for person_id in Amity.fellows if
                                   Amity.fellows[person_id].name == person_name]

        else:
            # search in staff dict
            fetched_identifiers = [person_id for person_id in Amity.staff if
                                   Amity.staff[person_id].name == person_name]
        if fetched_identifiers:
            return fetched_identifiers

        return "\n Person does not exist in the system"

    # gets person's allocation details
    def see_person_allocations(self, person_id):
        """
        :param person_id: ID of person whose allocations we seek
        :return: person's allocations on success, error message otherwise
        """

        # check id format
        if not re.match(self.regex_person_id, person_id):
            return "\n Person identifier looks something like s-1a or f-2a\nuse the " +\
                   "<get_person_identifier> command to get a valid ID"

        # verify person_identifier
        if not self.confirm_person_identifier_exists(person_id):
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

            msg += "\n Fellow " + name + " details:\n Office: " + str(office) + "\n Wants accommodation: " + \
                   wants_accommodation+ "\n Accommodation: " + str(accommodation)

        return msg

    # displays rooms that have available space
    def see_rooms_with_space(self, room_type=""):
        """
        :param room_type: either offices or livingspaces
        :return:
        """
        rooms = self.fetch_rooms_with_space()

        if rooms:
            living_spaces = rooms[0]
            offices = rooms[1]

            if room_type == "offices":
                return offices
            if room_type == "livingspaces":
                return living_spaces

            return rooms

        return "\n There are no rooms with space"

    # displays names of all people in the system
    def see_all_people(self, role=""):
        """
        :param role: either staff or fellow
        :return: list of people if any
        """
        # fetch all staff
        if role == "staff":
            return ["\n " + person_id + " " + Amity.staff[person_id].name + " staff" for person_id in Amity.staff]

        # fetch all fellows
        elif role == "fellow":
            return ["\n " + person_id + " " + Amity.fellows[person_id].name + " fellow" for person_id in Amity.fellows]

        # fetch all people
        else:
            return [["\n " + person_id + " " + Amity.fellows[person_id].name + " fellow" for person_id in Amity.fellows],
                    ["\n " + person_id + " " + Amity.staff[person_id].name + " staff" for person_id in Amity.staff]]

    # displays names of all rooms in the system
    def see_all_rooms(self, type=""):
        """
        :param type: either office or livingspace
        :return: names of all rooms
        """