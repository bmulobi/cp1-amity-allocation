from unittest import TestCase

from amity_app.classes.amity import Amity
from amity_app.classes.fellow import Fellow
from amity_app.classes.living_space import LivingSpace
from amity_app.classes.office import Office
from amity_app.classes.staff import Staff

import os
import sys
from contextlib import contextmanager
from io import StringIO

import sqlite3

# Class is used to test class Amity


class TestAmity(TestCase):
    """
       class contains logic to test all functionalities
       of the class Amity
    """

    def setUp(self):
        """
        Method instantiates class objects
        that will be used in the test cases

        """

        self.amity_object = Amity()
        self.living_space_object = LivingSpace()
        self.office_object = Office()
        self.staff_object = Staff()
        self.fellow_object = Fellow()

    # helper method to check print() output
    @contextmanager
    def captured_output(self):
        """
        method is used to capture the output
        of print() statements from other methods
        for purposes of testing with assert statements
        it does this by temporarily substituting in built
        stdout and stderr with instances of StringIO class

        """
        new_out, new_err = StringIO(), StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield sys.stdout, sys.stderr
        finally:
            sys.stdout, sys.stderr = old_out, old_err

    # Method tests if object is of class Amity
    def test_isinstance_of_amity_class(self):
        """
        test_isinstance_of_Amity_class():
        Method uses assertIsInstance() to check whether
        given object belongs to class Amity

        """

        self.assertIsInstance(self.amity_object, Amity)

    # Method tests the type of the given object
    def test_amity_object_type(self):
        """
        test_amity_object_type():
        Method uses type() to check whether
        given object is of type Amity

        Returns
        -------
        Boolean

        True : if it is of type Amity
        False : otherwise

        """

        self.assertTrue(type(self.amity_object) is Amity)

    # tests whether person identifier is verified properly
    def test_confirms_person_identifier_as_valid(self):
        """
        test_confirms_person_identifier_as_valid():

        """
        Amity.people_list = [{}, {}]

        self.assertFalse(self.amity_object.confirm_person_identifier("s-1"),
                         msg="Method should return true if identifier exists")

        person_identifier, message = self.staff_object.add_person("Test Person")
        self.assertTrue(self.amity_object.confirm_person_identifier(person_identifier),
                        msg="Method should return true if identifier exists")

    # tests whether room name is verified
    def test_confirms_room_name_as_valid(self):
        """
        test_confirms_room_name_as_valid():

        """
        # clear rooms list
        Amity.rooms_list = [{}, {}]
        # verify room name when no rooms exist
        self.assertFalse(self.amity_object.confirm_room_name("VALHALLA"),
                         msg="Method should return true if room name exists")
        # create room VALHALLA
        self.office_object.create_room("VALHALLA")
        # verify room name after room creation
        self.assertTrue(self.amity_object.confirm_room_name("VALHALLA"),
                        msg="Method should return true if room name exists")

    # tests whether given room is checked for space
    def test_confirms_specific_room_has_space(self):
        """
        test_confirms_specific_room_has_space():

        """
        # empty rooms list
        Amity.rooms_list = [{}, {}]
        # create room pentagon
        self.office_object.create_room("Pentagon")
        # test if it has space
        self.assertTrue(self.amity_object.confirm_specific_room_has_space("PENTAGON"))

        for i in ["-a", "-b", "-c", "-d", "-e", "-f"]:
            person_name = "John" + i
            self.staff_object.add_person(person_name)

        person_id, msg = self.staff_object.add_person("Test Person")
        self.assertEqual(self.amity_object.reallocate_person(person_id, "PENTAGON"),
                         "PENTAGON is fully occupied",
                         msg="Expected output was not matched")

        self.assertFalse(self.amity_object.confirm_specific_room_has_space("PENTAGON"))

    # tests whether allocations to staff are to offices only
    def test_does_not_reallocate_staff_to_livingspace(self):
        """
        test_does_not_reallocate_staff_to_livingspace():
        tests whether reallocate_person() does not reallocate
        staff member to a living space
        """
        Amity.people_list = [{}, {}]
        Amity.rooms_list = [{}, {}]

        self.office_object.create_room("Atom")
        person_id, msg = self.staff_object.add_person("Ben Man")
        self.living_space_object.create_room("Hostel")
        self.assertEqual(self.amity_object.reallocate_person(person_id, "HOSTEL"),
                         "Cannot reallocate a staff member to a living space",
                         msg="Could not reallocate staff member to living space")

    # tests whether does not reallocate

    # tests whether reallocate_person() is reallocating
    # properly
    def test_reallocates_person(self):
        """
        test_reallocates_person()
        tests reallocate_person()
        """
        Amity.rooms_list = [{}, {}]
        Amity.people_list = [{}, {}]

        self.living_space_object.create_room("TestRoom")
        person_id, msg = self.fellow_object.add_person("TEST PERSON", "Y")
        self.living_space_object.create_room("TestRoomTwo")
        self.assertEqual(self.amity_object.reallocate_person(person_id, "TESTROOMTWO"),
                         "Person with identifier " + person_id + " and name TEST PERSON was reallocated to TESTROOMTWO",
                         msg="Failed to reallocate person")

    # tests whether method confirms availability of space
    # before performing allocations
    def test_confirms_availability_of_space_in_amity(self):
        """
        test_confirms_availability_of_space_in_amity():
        tests confirm_availability_of_space_in_amity()
        """

        Amity.rooms_list = [{}, {}]
        self.assertFalse(self.amity_object.confirm_availability_of_space_in_amity(),
                         msg="Could not confirm availability of space")
        self.office_object.create_room("Test Room")
        self.assertTrue(self.amity_object.confirm_availability_of_space_in_amity(),
                        msg="Could not confirm availability of space")

    # tests if load people is working
    def test_it_loads_people(self):
        """
        test_it_loads_people():
        NOTE: in order for this test method to work properly
              you must navigate to the project tests
              folder before running the nosetests -v command
        Takes names from text file and allocates people
        rooms based on their role and availability of space
        """

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        filename = os.path.join(file_path, 'text_files/test_file.txt')

        try:
            error_msg = ""
            file_object = open(filename, "w")
            try:
                file_object.write("BEN MULOBI FELLOW Y\n" +
                                  "ROGER TARACHA STAFF\n")
            finally:
                file_object.close()

        except IOError as e:
            error_msg = str(e)
            error_msg += " - run this test from project tests directory"

        Amity.rooms_list = [{}, {}]
        Amity.people_list = [{}, {}]
        Amity.person_identifier = 0
        self.living_space_object.create_room("ATOMIC")
        self.office_object.create_room("NEUTRONIC")
        self.amity_object.load_people()

        self.assertIn("f-1", Amity.rooms_list[0]["ATOMIC"])
        self.assertIn("f-1", Amity.rooms_list[1]["NEUTRONIC"])
        self.assertIn("s-2", Amity.rooms_list[1]["NEUTRONIC"])

    # tests whether method confirms existence of allocatioins
    def test_confirms_existence_of_allocations_in_amity(self):
        """
        test_confirms_existence_of_allocations_in_amity():
        tests confirm_existence_of_allocations()
        """
        Amity.rooms_list = [{}, {}]
        Amity.people_list = [{}, {}]
        self.assertFalse(self.amity_object.confirm_existence_of_allocations(),
                         msg="Could not confirm existence of allocations")
        self.office_object.create_room("Test Room")
        person_id, msg = self.staff_object.add_person("Test Person")
        self.assertTrue(self.amity_object.confirm_existence_of_allocations(),
                        msg="Could not confirm existence of allocations")

    # tests if print_allocations works properly
    def test_it_prints_allocations_to_screen(self):
        """
        test_it_prints_allocations_to_screen():
        tests print_allocations()
        """
        Amity.person_identifier = 0
        Amity.rooms_list = [{}, {}]
        Amity.people_list = [{}, {}]

        self.office_object.create_room("TestRoom")
        for i in ["-a", "-b", "-c", "-d", "-e", "-f"]:
            name = "Test Person" + i
            self.staff_object.add_person(name)

        with self.captured_output() as (out, err):
            self.amity_object.print_allocations()

            output = out.getvalue()

        self.assertEqual(output, "\nTESTROOM\n-------------------------------------\n" +
                                 "TEST PERSON-A, TEST PERSON-B, TEST PERSON-C, " +
                                 "TEST PERSON-D, TEST PERSON-E, TEST PERSON-F\n"
                         )

    def test_it_writes_allocations_to_file(self):
        """
        test_it_writes_allocations_to_file():
        tests print_allocations(allocated_file_name="file.txt")
        with destination file argument given
        """
        Amity.person_identifier = 0
        Amity.rooms_list = [{}, {}]
        Amity.people_list = [{}, {}]

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        filename = os.path.join(file_path, 'text_files/allocations_file.txt')

        if os.path.isfile(filename):
            os.remove(filename)

        self.office_object.create_room("TestRoom")
        for i in ["-a", "-b", "-c", "-d", "-e", "-f"]:
            name = "Test Person" + i
            self.staff_object.add_person(name)

        self.amity_object.print_allocations(allocated_file_name="allocations_file.txt")

        try:
            file_object = open(filename, "r")
            try:
                lines_list = file_object.readlines()

            finally:
                file_object.close()

        except IOError as e:
            print(str(e))
        self.assertIn("TESTROOM\n" and
                      "-------------------------------------\n" and
                      "TEST PERSON-A, TEST PERSON-B, TEST PERSON-C, " +
                      "TEST PERSON-D, TEST PERSON-E, TEST PERSON-F", lines_list)

    # tests whether method confirms existence of unallocated
    # people before attempting to print the list
    def test_it_confirms_existence_of_unallocated_people(self):
        """
        test_it_confirms_existence_of_unallocated_people():
        tests confirm_existence_of_unallocated()
        """
        Amity.rooms_list = [{}, {}]
        Amity.people_list = [{}, {}]

        self.assertFalse(self.amity_object.confirm_existence_of_unallocated())

        for i in ["-a", "-b", "-c", "-d", "-e", "-f"]:
            name = "Test Person" + i
            self.staff_object.add_person(name)

        self.assertTrue(self.amity_object.confirm_existence_of_unallocated())

    # tests whether print_unallocated() prints
    # to screen
    def test_prints_unallocated_to_screen(self):
        """
        test_prints_unallocated_to_screen():
        tests print_unallocated()
        """
        Amity.rooms_list = [{}, {}]
        Amity.people_list = [{}, {}]

        for i in ["-a", "-b", "-c", "-d", "-e", "-f"]:
            name = "Test Person" + i
            self.staff_object.add_person(name)

        with self.captured_output() as (out, err):
            self.amity_object.print_unallocated()

            output = out.getvalue()
            self.assertEqual(output, "TEST PERSON-A - not allocated office\n" +
                             "TEST PERSON-B - not allocated office\n" +
                             "TEST PERSON-C - not allocated office\n" +
                             "TEST PERSON-D - not allocated office\n" +
                             "TEST PERSON-E - not allocated office\n" +
                             "TEST PERSON-F - not allocated office\n")

    # tests whether print_unallocated() prints(writes)
    # to file
    def test_prints_unallocated_to_file(self):
        """
        test_prints_unallocated_to_file():
        tests print_unallocated(arg)
        """
        Amity.rooms_list = [{}, {}]
        Amity.people_list = [{}, {}]
        lines_list = []

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        filename = os.path.join(file_path, "text_files/unallocated_file.txt")

        for i in ["-a", "-b"]:
            name = "Staff Person" + i
            self.staff_object.add_person(name)
        for i in ["-a", "-b"]:
            name = "Fellow Person" + i
            self.fellow_object.add_person(name, "Y")

        self.amity_object.print_unallocated("unallocated_file.txt")

        try:
            file_object = open(filename, "r")

            try:
                lines_list = file_object.readlines()

            finally:
                file_object.close()

        except IOError as e:
            print("File access error - ", str(e))

        self.assertIn("STAFF PERSON-A - not allocated office\n" and
                      "STAFF PERSON-B - not allocated office\n" and
                      "FELLOW PERSON-A - not allocated office\n" and
                      "FELLOW PERSON-A - not allocated living space\n" and
                      "FELLOW PERSON-B - not allocated office\n" and
                      "FELLOW PERSON-B - not allocated living space\n",
                      lines_list)

    # tests check for allocations in given room
    def test_it_confirms_specific_room_has_allocations(self):
        """
        test_it_confirms_specific_room_has_allocations():
        tests if confirm_existence_of_allocations_for_particular_room()
        works properly
        """
        Amity.rooms_list = [{}, {}]
        Amity.people_list = [{}, {}]

        self.office_object.create_room("Valhalla")

        self.assertFalse(self.amity_object.confirm_existence_of_allocations_for_particular_room("VALHALLA"))

        self.staff_object.add_person("Code Dragon")
        self.fellow_object.add_person("Bau Meister")

        self.assertTrue(self.amity_object.confirm_existence_of_allocations_for_particular_room("VALHALLA"))

    # tests if print_room() prints to screen
    def test_it_prints_room(self):
        """
        test_it_prints_room():
        tests whether print_room() works properly
        """
        Amity.rooms_list = [{}, {}]
        Amity.people_list = [{}, {}]

        self.office_object.create_room("Krypton")
        for i in ["-a", "-b", "-c"]:
            name = "Test Person" + i
            self.staff_object.add_person(name)

        with self.captured_output() as (out, err):
            self.amity_object.print_room("KRYPTON")

            output = out.getvalue()
            self.assertEqual(output, "TEST PERSON-A\nTEST PERSON-B\nTEST PERSON-C\n")

    # tests save state to default db
    def test_it_saves_state_to_default_db(self):
        """
        test_it_saves_state_to_default_db():

        """
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        filename = os.path.join(file_path, "db_files/amity.db")
        if os.path.isfile(filename):
            os.remove(filename)

        Amity.person_identifier = 0
        Amity.rooms_list = [{}, {}]
        Amity.people_list = [{}, {}]

        self.office_object.create_room("Mara")
        self.living_space_object.create_room("Serengeti")

        self.staff_object.add_person("Josh Jebs")
        self.fellow_object.add_person("Sarah Munene", "Y")

        self.amity_object.save_state()

        results_list = []

        try:
            connection = sqlite3.connect(filename)
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM tbl_people")
            connection.commit()
            results = cursor.fetchall()

            for row in results:
                results_list.append(row["person_name"])
                results_list.append(row["person_identifier"])
                results_list.append(row["accommodation"])

            cursor.execute("SELECT * FROM tbl_rooms")
            connection.commit()
            results = cursor.fetchall()

            for row in results:
                results_list.append(row["room_name"])
                results_list.append(row["room_type"])

            cursor.execute("SELECT * FROM tbl_allocations")
            connection.commit()
            results = cursor.fetchall()

            for row in results:
                results_list.append(row["room_name"])
                results_list.append(row["person_id"])

        except sqlite3.Error as e:
            print("db access error - ", str(e))

        self.assertIn("Mara" and "Serengeti" and "Josh Jebs"
                      and "Sarah Munene" and "Y" and "s-1" and "f-2",
                      results_list,
                      msg="Could not verify database fetch results")

    # tests save state to specified db
    def test_it_saves_state_to_specified_db(self):
        """
        test_it_saves_state_to_specified_db():

        """
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        filename = os.path.join(file_path, "db_files/specified.db")
        if os.path.isfile(filename):
            os.remove(filename)

        Amity.person_identifier = 0
        Amity.rooms_list = [{}, {}]
        Amity.people_list = [{}, {}]

        self.office_object.create_room("Mara")
        self.living_space_object.create_room("Serengeti")

        self.staff_object.add_person("Josh Jebs")
        self.fellow_object.add_person("Sarah Munene", "Y")

        self.amity_object.save_state(destination_db="specified.db")

        results_list = []

        try:
            connection = sqlite3.connect(filename)
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM tbl_people")
            connection.commit()
            results = cursor.fetchall()

            for row in results:
                results_list.append(row["person_name"])
                results_list.append(row["person_identifier"])
                results_list.append(row["accommodation"])

            cursor.execute("SELECT * FROM tbl_rooms")
            connection.commit()
            results = cursor.fetchall()

            for row in results:
                results_list.append(row["room_name"])
                results_list.append(row["room_type"])

            cursor.execute("SELECT * FROM tbl_allocations")
            connection.commit()
            results = cursor.fetchall()

            for row in results:
                results_list.append(row["room_name"])
                results_list.append(row["person_id"])

        except sqlite3.Error as e:
            print("db access error - ", str(e))

        self.assertIn("Mara" and "Serengeti" and "Josh Jebs"
                      and "Sarah Munene" and "Y" and "s-1" and "f-2",
                      results_list,
                      msg="Could not verify database fetch results")

    # tests verification of file existence
    def test_it_confirms_existence_of_db_file(self):
        """
        test_it_confirms_existence_of_db_file():
        tests whether load state confirms existence of source db
        file before attempting to load state
        """

        self.assertEqual(self.amity_object.load_state("non_existent_file.db"),
                         "File does not exist", "Could not find file")

    # tests verification of file type
    def test_load_state_confirms_file_extension(self):
        """
        test_load_state_confirms_file_extension():

        """
        self.assertEqual(self.amity_object.load_state("my_file.txt"),
                         "File extension must be .db", msg="Not a database file")

    # tests load_state()
    def test_it_loads_state(self):
        """
        test_it_loads_state():
        tests whether load state works properly
        """
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        filename = os.path.join(file_path, "db_files/test.db")
        if os.path.isfile(filename):
            os.remove(filename)

        if self.amity_object.create_database("test.db") is True:

            try:
                connection = sqlite3.connect(filename)
                connection.row_factory = sqlite3.Row
                cursor = connection.cursor()

                rows = [
                        ("Big Ben", "f-1", "Y"),
                        ("Sally Molly", "s-2", "N"),
                        ("Harry Porter", "f-3", "N"),
                        ("Jim Harrigan", "s-4", "N")
                       ]

                cursor.executemany("""INSERT INTO tbl_people (person_name, person_identifier,
                               accommodation) VALUES (?,?,?)""", rows)

                rows = [
                        ("Valhalla", "office"),
                        ("Upstairs", "livingspace")
                       ]
                cursor.executemany("""INSERT INTO tbl_rooms (room_name, room_type) VALUES (?,?)""", rows)

                rows = [
                        ("Valhalla", "f-1"),
                        ("Upstairs", "f-1"),
                        ("Valhalla", "s-2"),
                        ("Valhalla", "f-3")
                       ]

                cursor.executemany("""INSERT INTO tbl_allocations (room_name, person_id) VALUES (?,?)""", rows)
                connection.commit()

            except sqlite3.Error as e:
                print("db access error - ", str(e))

            Amity.rooms_list = [{}, {}]
            Amity.people_list = [{}, {}]
            fellows_names = []
            staff_names = []

            self.amity_object.load_state("test.db")

            fellows_ids = Amity.people_list[0].keys()
            for key in fellows_ids:
                fellows_names.append(Amity.people_list[0][key][0])

            self.assertIn("Big Ben" and "Harry Porter", fellows_names, msg="Name not found in dictionary")

            staff_ids = Amity.people_list[1].keys()
            for key in staff_ids:
                staff_names.append(Amity.people_list[1][key][0])

            self.assertIn("Sally Molly" and "Jim Harrigan", staff_names, msg="Name not found in dictionary")

            livingspaces_names = Amity.rooms_list[0].keys()
            self.assertIn("Upstairs", livingspaces_names, msg="Name not found in dictionary")

            offices_names = Amity.rooms_list[1].keys()
            self.assertIn("Valhalla", offices_names, msg="Name not found in dictionary")

            offices_allocations_list = []
            for name in offices_names:
                offices_allocations_list += Amity.rooms_list[1][name]

            self.assertIn("f-1" and "s-2" and "f-3", offices_allocations_list,
                          msg="Could not find the identifiers in dictionary")

            livingspaces_allocations_list = []

            for name in livingspaces_names:
                livingspaces_allocations_list += Amity.rooms_list[0][name]
            self.assertIn("f-1", livingspaces_allocations_list,
                          msg="Could not find the identifiers in dictionary")





