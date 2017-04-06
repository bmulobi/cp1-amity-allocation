# This class will contain most of the functionality
# required in the amity room allocation application
import os
import sqlite3


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
        self.room_type = ""
        self.livingspaces_with_allocations = []
        self.offices_with_allocations = []

    # confirms whether user has entered a valid identifier
    def confirm_person_identifier(self, person_identifier):
        """
        :param person_identifier: person's identifier
        :return: True if identifier is valid
                 False otherwise
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
        :return: list of rooms in amity, if any
                 False otherwise
        """
        if not len(Amity.rooms_list):
            return False

        self.living_spaces_list = []
        self.offices_list = []

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
        if not len(Amity.rooms_list[0]) and not len(Amity.rooms_list[1]):
            return False

        self.offices_list, self.living_spaces_list = self.search_rooms_list()

        return new_room_name in self.living_spaces_list or new_room_name in self.offices_list

    # Confirms whether specific room has space for further allocations
    def confirm_specific_room_has_space(self, room_name):
        """
        :param room_name: room name
        :return: True if space is available
                 False otherwise
        """
        # first confirm overall availability of space
        if self.confirm_availability_of_space_in_amity():
            self.offices_list, self.living_spaces_list = self.search_rooms_list()

            if room_name in self.offices_list:
                return len(Amity.rooms_list[1][room_name]) < 6

            if room_name in self.living_spaces_list:
                return len(Amity.rooms_list[0][room_name]) < 4
        return False

    # Fetches room type
    def fetch_room_type(self, room_name):
        """
        """
        if self.search_rooms_list():

            self.offices_list, self.living_spaces_list = self.search_rooms_list()
            if room_name in self.offices_list:
                return "office"
            if room_name in self.living_spaces_list:
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

        if self.fetch_room_type(room_name) == "office":

            if person_identifier in Amity.rooms_list[1][room_name]:
                return True
        else:
            if person_identifier in Amity.rooms_list[0][room_name]:
                return True
        return False

    # gets person's identifier given the name and role
    def fetch_person_identifier(self, person_name, role):
        """
        returns: uses name and role to
                 return associated person identifier
        """

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

    # reallocates a person to a new room
    def reallocate_person(self, person_identifier, new_room_name):
        """
        :param person_identifier: Person's unique ID
        :param new_room_name: room to reallocate to
        :return: relevant message
        """
        # verify person_identifier
        if not self.confirm_person_identifier(person_identifier):
            return "Person identifier does not exist in the system"
        # verify room name
        if not self.confirm_room_name(new_room_name):
            return "Room " + new_room_name + " does not exist in the system"
        # check if room has space
        if not self.confirm_specific_room_has_space(new_room_name):
            return new_room_name + " is fully occupied"

        if self.confirm_person_not_doubly_reallocated_to_same_room(person_identifier, new_room_name):
            return "Person is already allocated to room " + new_room_name

        # get room type
        self.room_type = self.fetch_room_type(new_room_name)

        if self.room_type == "livingspace":

            if person_identifier.startswith("s"):
                return "Cannot reallocate a staff member to a living space"
            else:
                Amity.rooms_list[0][new_room_name].append(person_identifier)
        else:
            Amity.rooms_list[1][new_room_name].append(person_identifier)

        # check if person was reallocated a room of similar type
        # before and cancel that allocation

        livingspaces_list, offices_list = self.fetch_rooms_with_allocations()

        # if person is staff, we cancel any previous allocation with no further checks
        if person_identifier.startswith("s"):
            for room in offices_list:
                if person_identifier in Amity.rooms_list[1][room]:
                    id_index = Amity.rooms_list[1][room].index(person_identifier)
                    del(Amity.rooms_list[1][room][id_index])
                    break
        # if person is fellow, we check whether new reallocation
        # is to office or living space before we cancel any previous allocation
        else:
            if self.room_type == "office":
                # cancel previous office allocation
                for room in offices_list:
                    if person_identifier in Amity.rooms_list[1][room]:
                        id_index = Amity.rooms_list[1][room].index(person_identifier)
                        del(Amity.rooms_list[1][room][id_index])
                        break
            else:
                # cancel previous living space allocation
                for room in livingspaces_list:
                    if person_identifier in Amity.rooms_list[0][room]:
                        id_index = Amity.rooms_list[0][room].index(person_identifier)
                        del(Amity.rooms_list[0][room][id_index])
                        break

        # return success message based on whether person is staff or fellow
        if person_identifier.startswith("s"):
            return "Person with identifier " + person_identifier + \
                   " and name " + Amity.people_list[1][person_identifier][0] + \
                   " was reallocated to " + new_room_name
        else:
            return "Person with identifier " + person_identifier + \
                   " and name " + Amity.people_list[0][person_identifier][0] + \
                   " was reallocated to " + new_room_name

    # verifies overall availability of space in amity
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

    # fetches list of roomswith space
    def fetch_rooms_with_space(self):
        """
        returns 2 lists: one for offices with space (if any)
        and one for livingspaces with space (if any) and
        the number of spaces available in each room
        """
        if self.search_rooms_list() is not False:
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
        else:
            return False

    # loads people from text file to system
    def load_people(self):
        """
        :param file_path:
        :return:
        """

        if self.fetch_rooms_with_space() is not False:
            offices, living_spaces = self.fetch_rooms_with_space()
            if len(offices) or len(living_spaces):

                file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
                filename = os.path.join(file_path, 'text_files/test_file.txt')

                try:
                    file_object = open(filename, "r")
                    try:
                        lines_list = file_object.readlines()
                        print(lines_list)
                        for line in lines_list:
                            Amity.person_identifier += 1
                            line_fragments = line.split()
                            if len(line_fragments) == 3:
                                if line_fragments[2].rstrip() == "FELLOW":
                                    Amity.people_list[0]\
                                        ["f-" + str(Amity.person_identifier)] \
                                        = [line_fragments[0]
                                           + " " + line_fragments[1]]
                                    for room in offices:
                                        if room[1] > 0:
                                            Amity.rooms_list[1][room[0]].\
                                            append("f-" +
                                                   str(Amity.person_identifier))
                                            room[1] -= 1
                                            break
                                else:
                                    Amity.people_list[1]\
                                        ["s-" + str(Amity.person_identifier)] \
                                        = [line_fragments[0]
                                           + " " + line_fragments[1]]
                                    for room in offices:
                                        if room[1] > 0:
                                            Amity.rooms_list[1][room[0]].\
                                            append("s-" +
                                                   str(Amity.person_identifier))
                                            room[1] -= 1
                                            break
                            if len(line_fragments) == 4:
                                Amity.people_list[0]\
                                    ["f-" + str(Amity.person_identifier)] \
                                    = [line_fragments[0]
                                       + " " + line_fragments[1]]
                                for room in offices:
                                    if room[1] > 0:
                                        Amity.rooms_list[1][room[0]].\
                                        append("f-" +
                                               str(Amity.person_identifier))
                                        room[1] -= 1
                                        break
                                for room in living_spaces:
                                    if room[1] > 0:
                                        Amity.rooms_list[0][room[0]].\
                                        append("f-" +
                                               str(Amity.person_identifier))
                                        room[1] -= 1
                                        break

                    finally:
                        file_object.close()

                except IOError as e:
                    print(str(e))

            else:
                print("There is no free space currently, use the create_room \
                      command to create new space")

        else:
            print("There is no free space currently, use the create_room \
                  command to create new space")

    # confirms whether there are allocations in the system
    def confirm_existence_of_allocations(self):
        """
        :return: True if allocations exist
                 False otherwise
        """
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

    # fetches list of all rooms with allocations
    def fetch_rooms_with_allocations(self):
        """
        :return: list of rooms with allocations if any
        """
        offices_list, living_spaces_list = self.search_rooms_list()
        for room in offices_list:
            if len(Amity.rooms_list[1][room]) > 0:
                self.offices_with_allocations.append(room)
        for room in living_spaces_list:
            if len(Amity.rooms_list[0][room]) > 0:
                self.livingspaces_with_allocations.append(room)
        return self.livingspaces_with_allocations, self.offices_with_allocations

    # prints all allocations in the system
    def print_allocations(self, allocated_file_name=""):
        """
        Prints allocations to the screen or
        writes to file if file name is given
        """

        # first check if there are any allocations
        if self.confirm_existence_of_allocations():

            living_spaces_list, offices_list = self.fetch_rooms_with_allocations()

            # check if file name was given
            if allocated_file_name:
                file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
                filename = os.path.join(file_path, "text_files/" + allocated_file_name)

                try:
                    file_object = open(filename, "w")
                    try:
                        for key in offices_list:

                            file_object.write(key + "\n")
                            file_object.write("-------------------------------------\n")
                            list_length = len(Amity.rooms_list[1][key])

                            i = 1
                            for value in Amity.rooms_list[1][key]:

                                names_string = ""
                                if i < list_length:
                                    if value.startswith("s"):
                                        names_string += Amity.people_list[1][value][0] + ", "
                                    else:
                                        names_string += Amity.people_list[0][value][0] + ", "
                                else:
                                    if value.startswith("s"):
                                        names_string += Amity.people_list[1][value][0]
                                    else:
                                        names_string += Amity.people_list[0][value][0]
                                i += 1

                                file_object.write(names_string)

                    finally:
                        file_object.close()
                except IOError as e:
                    print(str(e))

            else:

                for key in offices_list:

                    print("\n" + key)
                    print("-------------------------------------")
                    list_length = len(Amity.rooms_list[1][key])

                    i = 1
                    names_string = ""
                    for value in Amity.rooms_list[1][key]:

                        if i < list_length:
                            if value.startswith("s"):
                                names_string += Amity.people_list[1][value][0] + ", "
                            else:
                                names_string += Amity.people_list[0][value][0] + ", "

                        else:
                            if value.startswith("s"):
                                names_string += Amity.people_list[1][value][0]
                            else:
                                names_string += Amity.people_list[0][value][0]

                        i += 1

                    print(names_string)

    # verifies whether unallocated people exist
    def confirm_existence_of_unallocated(self):
        """
        :return: True if unallocated people are found
                 False otherwise
        """
        # if there are any people in the system
        if len(Amity.people_list[0]) > 0 or len(Amity.people_list[1]) > 0:
            # put their IDs into lists
            fellows_list = Amity.people_list[0].keys()
            staff_list = Amity.people_list[1].keys()

            for person_id in fellows_list:
                # check if any of the fellows has not been allocated an office
                if "office" not in Amity.people_list[0][person_id]:
                    return True

                # check if any of the fellows who wanted a
                # living space has not been allocated one
                if ("Y" in Amity.people_list[0][person_id] and
                    "livingspace" not in Amity.people_list[0][person_id]):
                    return True

            for person_id in staff_list:
                # check if any of the staff has not been allocated an office
                if "office" not in Amity.people_list[1][person_id]:
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
                if len(Amity.people_list[0]) > 0 or len(Amity.people_list[1]) > 0:
                    # put their IDs into lists
                    fellows_list = Amity.people_list[0].keys()
                    staff_list = Amity.people_list[1].keys()

                    for person_id in fellows_list:
                        # check if any of the fellows has not been allocated an office
                        # and print name to screen
                        if "office" not in Amity.people_list[0][person_id]:
                            print(Amity.people_list[0][person_id][0] + " - not allocated office")

                        # check if any of the fellows who wanted a
                        # living space has not been allocated one
                        # and print name to screen
                        if ("Y" in Amity.people_list[0][person_id] and
                            "livingspace" not in Amity.people_list[0][person_id]):
                            print(Amity.people_list[0][person_id][0] + " - not allocated living space")

                    for person_id in staff_list:
                        # check if any of the staff has not been allocated an office
                        # and print name to screen
                        if "office" not in Amity.people_list[1][person_id]:
                            print(Amity.people_list[1][person_id][0] + " - not allocated office")

            else:
                file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
                filename = os.path.join(file_path, 'text_files/' + destination_file_name)

                try:
                    file_object = open(filename, "w")

                    try:
                        # if there are any people in the system
                        if len(Amity.people_list[0]) > 0 or len(Amity.people_list[1]) > 0:
                            # put their IDs into lists
                            fellows_list = Amity.people_list[0].keys()
                            staff_list = Amity.people_list[1].keys()

                            for person_id in fellows_list:
                                # check if any of the fellows has not been allocated an office
                                # and write to file
                                if "office" not in Amity.people_list[0][person_id]:
                                    file_object.write(Amity.people_list[0][person_id][0] +
                                                      " - not allocated office\n")

                                # check if any of the fellows who wanted a
                                # living space has not been allocated one
                                # and write to file
                                if ("Y" in Amity.people_list[0][person_id] and
                                            "livingspace" not in Amity.people_list[0][person_id]):
                                    file_object.write(Amity.people_list[0][person_id][0] +
                                                      " - not allocated living space\n")

                            for person_id in staff_list:
                                # check if any of the staff has not been allocated an office
                                # and write to file
                                if "office" not in Amity.people_list[1][person_id]:
                                    file_object.write(Amity.people_list[1][person_id][0] +
                                                      " - not allocated office\n")
                            print("Unallocated people were written successfully to ", filename)

                    finally:
                        file_object.close()

                except IOError as e:
                    print("File access error - " + str(e))
        else:
            print("There are no unallocated people in the system")

    # verifies whether room has allocations
    def confirm_existence_of_allocations_for_particular_room(self, room_name):
        """
        :param room_name: name of room to check
        :return: True if allocations exist
                 False otherwise
        """

        room_type = self.fetch_room_type(room_name)
        if room_type and room_type == "office":
            if len(Amity.rooms_list[1][room_name]) > 0:
                return True
        if room_type and room_type == "livingspace":
            if len(Amity.rooms_list[0][room_name]) > 0:
                return True
        return False

    # prints allocations for given room
    def print_room(self, room_name):
        """
        :param room_name: room to print allocations from
        :return: prints output to screen
        """
        if self.confirm_room_name(room_name):

            if self.confirm_existence_of_allocations_for_particular_room(room_name):

                if self.fetch_room_type(room_name) == "office":

                    for name in Amity.rooms_list[1][room_name]:

                        if name.startswith("s"):
                            print(Amity.people_list[1][name][0])
                        else:
                            print(Amity.people_list[0][name][0])
                else:

                    for name in Amity.rooms_list[0][room_name]:

                        print(Amity.people_list[0][name][0])
            else:
                print(room_name, " has no allocations currently")
        else:
            print(room_name, " does not exist in the system")







        return "print_room() was called successfully with arg " + room_name

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
        if (len(Amity.people_list[0]) > 0 or len(Amity.people_list[1]) > 0 or
           len(Amity.rooms_list[0]) > 0 or len(Amity.rooms_list[1]) > 0):

            # ensure database has been created
            if self.create_database(file_end) is True:

                try:
                    connection = sqlite3.connect(filename)
                    cursor = connection.cursor()

                    # if any fellows in system
                    if len(Amity.people_list[0]) > 0:

                        fellow_ids = Amity.people_list[0].keys()
                        # insert fellows into table
                        for item in fellow_ids:

                            has_office = 0
                            has_livingspace = 0

                            if Amity.people_list[0][item][2] == "office":
                                has_office = 1
                            if Amity.people_list[0][item][3] == "livingspace":
                                has_livingspace = 1
                            cursor.execute("""INSERT INTO tbl_people (person_name, person_identifier,
                                           accommodation, has_office, has_livingspace) VALUES (?,?,?,?,?)""",
                                           (
                                                Amity.people_list[0][item][0],
                                                item,
                                                Amity.people_list[0][item][1],
                                                has_office,
                                                has_livingspace
                                           )
                                           )
                        connection.commit()

                    # if any staff in system
                    if len(Amity.people_list[1]) > 0:

                        staff_ids = Amity.people_list[1].keys()
                        # insert staff into table
                        for item in staff_ids:

                            has_office = 0

                            if Amity.people_list[1][item][1] == "office":
                                has_office = 1

                            cursor.execute("""INSERT INTO tbl_people (person_name, person_identifier,
                                           has_office)VALUES (?,?,?)""",
                                           (
                                               Amity.people_list[1][item][0],
                                               item,
                                               has_office
                                           )
                                           )
                        connection.commit()

                    # if any living spaces in system
                    if len(Amity.rooms_list[0]) > 0:

                        living_space_names = Amity.rooms_list[0].keys()
                        # insert living spaces into table rooms
                        for item in living_space_names:

                            cursor.execute("""INSERT INTO tbl_rooms (room_name, room_type) VALUES (?,?)""",
                                           (
                                               item,
                                               "livingspace"
                                           )
                                           )

                            for person_id in Amity.rooms_list[0][item]:
                                cursor.execute("""INSERT INTO tbl_allocations (room_name, person_id) VALUES (?,?)""",
                                               (
                                                   item,
                                                   person_id
                                               )
                                               )
                        connection.commit()

                    # if any offices in system
                    if len(Amity.rooms_list[1]) > 0:

                        office_names = Amity.rooms_list[1].keys()
                        # insert offices into table rooms
                        for item in office_names:

                            cursor.execute("""INSERT INTO tbl_rooms (room_name, room_type) VALUES (?,?)""",
                                           (
                                               item,
                                               "office"
                                           )
                                           )

                            for person_id in Amity.rooms_list[1][item]:
                                cursor.execute("""INSERT INTO tbl_allocations (room_name, person_id) VALUES (?,?)""",
                                               (
                                                   item,
                                                   person_id
                                               )
                                               )
                        connection.commit()

                except sqlite3.Error as e:
                    return "An error occurred - " + e

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
            return "File extension must be .db"
        # confirm existence of db source file
        if not self.confirm_existence_of_db_file(source_db):
            return "File does not exist"

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        filename = os.path.join(file_path, "db_files/" + source_db)
        offices_list = []
        livingspaces_list = []

        try:
            connection = sqlite3.connect(filename)
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            # fetch all data from table people
            cursor.execute("SELECT * FROM tbl_people")
            rows = cursor.fetchall()

            for row in rows:
                # if person is staff, store in staff dictionary
                if row["person_identifier"].startswith("s"):
                    Amity.people_list[1][row["person_identifier"]] = [row["person_name"]]
                else:
                    # if person is fellow, store in fellow dictionary
                    Amity.people_list[0][row["person_identifier"]] = [row["person_name"], row["accommodation"]]

            # fetch all data from table rooms
            cursor.execute("SELECT * FROM tbl_rooms")
            rows = cursor.fetchall()
            for row in rows:
                # if room is office, store in office dictionary
                if row["room_type"] == "office":
                    Amity.rooms_list[1][row["room_name"]] = []
                    offices_list.append(row["room_name"])

                else:
                    # if room is living space, store in living space dictionary
                    Amity.rooms_list[0][row["room_name"]] = []
                    livingspaces_list.append(row["room_name"])

            # fetch all data from table allocations
            cursor.execute("SELECT * FROM tbl_allocations")
            rows = cursor.fetchall()
            for row in rows:
                # if room is office
                if row["room_name"] in offices_list:
                    if row["room_name"] not in Amity.rooms_list[1].keys():
                        Amity.rooms_list[1][row["room_name"]] = [row["person_id"]]
                    else:
                        Amity.rooms_list[1][row["room_name"]].append(row["person_id"])
                if row["room_name"] in livingspaces_list:
                    if row["room_name"] not in Amity.rooms_list[0].keys():
                        Amity.rooms_list[0][row["room_name"]] = [row["person_id"]]
                    else:
                        Amity.rooms_list[0][row["room_name"]].append(row["person_id"])

        except sqlite3.Error as e:
            print("DB access error - ", str(e))

        return "State was loaded successfully from " + filename
