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

        Amity.fellows = {}
        Amity.staff = {}
        Amity.offices = {}
        Amity.living_spaces = {}

        Amity.people_counter = 0

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        filename = os.path.join(file_path, 'text_files/sessions_file.txt')

        with open(filename, "r") as file_object:
            self.session_id = file_object.read()

    def tearDown(self):
        del self.amity_object

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
        :return:
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
        tests if confirm_person_identifier() works properly
        """

        self.assertFalse(self.amity_object.confirm_person_identifier_exists("s-1" + self.session_id),
                         msg="Method should return true if identifier exists")

        result = self.amity_object.add_person("Test Person", "STAFF")

        self.assertTrue(self.amity_object.confirm_person_identifier_exists(result[0]),
                        msg="Method should return true if identifier exists")

    # tests whether room name is verified
    def test_fetch_room_type_confirms_room_name_exists(self):
        """
        test_confirms_room_name_as_valid():
        tests if confirm_room_name() works properly
        """
        # verify room name when no rooms exist
        self.assertFalse(self.amity_object.fetch_room_type("VALHALLA"),
                         msg="Method should return true if room name exists")


    # tests whether given room is checked for space
    def test_confirms_specific_room_has_space(self):
        """
        test_confirms_specific_room_has_space():
        tests if confirm_specific_room_has_space() works properly
        """

        # create room pentagon
        self.amity_object.create_room("OFFICE", ["Pentagon"])
        # test if it has space
        self.assertTrue(self.amity_object.confirm_specific_room_has_space("PENTAGON"),
                        msg="Expected output was not matched")


        for i in ["-a", "-b", "-c", "-d", "-e", "-f"]:
            person_name = "John" + i
            self.amity_object.add_person(person_name, "STAFF")

        self.assertFalse(self.amity_object.confirm_specific_room_has_space("PENTAGON"),
                         msg="Expected output was not matched")

    # tests whether allocations to staff are to offices only
    def test_does_not_reallocate_staff_to_livingspace(self):
        """
        test_does_not_reallocate_staff_to_livingspace():
        tests whether reallocate_person() does not reallocate
        staff member to a living space
        """

        self.amity_object.create_room("OFFICE", ["Atom"])
        result = self.amity_object.add_person("Ben Man", "STAFF")
        self.amity_object.create_room("LIVINGSPACE", ["Hostel"])
        self.assertEqual(self.amity_object.reallocate_person(result[0], "HOSTEL"),
                         "\n Cannot reallocate a staff member to a living space",
                         msg="Could not reallocate staff member to living space")

    # tests whether does not reallocate

    # tests whether reallocate_person() is reallocating
    # properly
    def test_reallocates_person(self):
        """
        test_reallocates_person()
        tests reallocate_person() works properly
        """

        self.amity_object.create_room("LIVINGSPACE", ["TestRoom"])
        result = self.amity_object.add_person("TEST PERSON","FELLOW", "Y")
        self.amity_object.create_room("LIVINGSPACE", ["TESTROOMTWO"])
        self.assertEqual(self.amity_object.reallocate_person(result[0], "TESTROOMTWO"),
                         "\n Person with identifier " + result[0] + " and name TEST PERSON was reallocated to TESTROOMTWO",
                         msg="Failed to reallocate person")

    # tests for duplicate allocations to same room
    def test_reallocate_person_does_not_duplicate_allocations_to_same_room(self):
        """
        test_reallocate_person_does_not_duplicate_allocations_to_same_room():
        tests whether confirm_person_not_doubly_reallocated_to_same_room()
        works properly
        """

        self.amity_object.create_room("OFFICE", ["TEST ROOM"])
        result = self.amity_object.add_person("TEST PERSON", "STAFF")

        self.assertEqual(self.amity_object.reallocate_person(result[0], "TEST ROOM"),
                         "\n Person is already allocated to room TEST ROOM")

    # tests whether method confirms availability of space
    # before performing allocations
    def test_confirms_availability_of_space_in_amity(self):
        """
        test_confirms_availability_of_space_in_amity():
        tests confirm_availability_of_space_in_amity()
        """
        self.assertFalse(self.amity_object.confirm_availability_of_space_in_amity(),
                         msg="Could not confirm availability of space")
        self.amity_object.create_room("OFFICE", ["Test Room"])
        self.assertTrue(self.amity_object.confirm_availability_of_space_in_amity(),
                        msg="Could not confirm availability of space")

    # tests if load people is working
    def test_it_loads_people(self):
        """
        test_it_loads_people():
        Takes names from text file and allocates people
        rooms based on their role and availability of space
        """

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        filename = os.path.join(file_path, 'text_files/test_file.txt')

        try:

            file_object = open(filename, "w")
            try:
                file_object.write("BEN MULOBI FELLOW Y\n" +
                                  "ROGER TARACHA STAFF\n")
            finally:
                file_object.close()

        except IOError as e:
            print(str(e))


        self.amity_object.create_room("LIVINGSPACE", ["ATOMIC"])
        self.amity_object.create_room("OFFICE", ["NEUTRONIC"])

        self.assertEqual(self.amity_object.load_people("test_file.txt"),
                         "\n 2 people were loaded into the system successfully",
                         msg="Output not equal to expected output")

    # tests whether method confirms existence of allocations
    def test_print_allocations_confirms_existence_of_allocations_in_amity(self):
        """
        test_confirms_existence_of_allocations_in_amity():
        tests confirm_existence_of_allocations() works properly
        """
        with self.captured_output() as (out, err):
            self.amity_object.print_allocations()

            output = out.getvalue()

        self.assertEqual(output, "\n There are currently no allocations in the system\n")

    # tests if print_allocations works properly
    def test_it_prints_allocations_to_screen(self):
        """
        test_it_prints_allocations_to_screen():
        tests print_allocations()
        """

        self.amity_object.create_room("OFFICE", ["TestRoom"])

        for i in ["-a", "-b", "-c", "-d", "-e", "-f"]:
            name = "Test Person" + i
            self.amity_object.add_person(name.upper(), "STAFF")

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

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        filename = os.path.join(file_path, 'text_files/allocations_file.txt')

        if os.path.isfile(filename):
            os.remove(filename)

        self.amity_object.create_room("OFFICE", ["TestRoom"])
        for i in ["-a", "-b", "-c", "-d", "-e", "-f"]:
            name = "Test Person" + i
            self.amity_object.add_person(name.upper(), "FELLOW", "Y")

        self.amity_object.print_allocations(allocated_file_name="allocations_file.txt")

        try:
            file_object = open(filename, "r")
            try:
                lines_list = file_object.readlines()

            finally:
                file_object.close()

        except IOError as e:
            print(str(e))
        self.assertIn("\n" and "TESTROOM\n" and
                      "-------------------------------------\n" and
                      "TEST PERSON-A, TEST PERSON-B, TEST PERSON-C, " +
                      "TEST PERSON-D, TEST PERSON-E, TEST PERSON-F\n", lines_list)

    # tests whether method confirms existence of unallocated
    # people before attempting to print the list
    def test_fetch_list_of_unallocated_people_confirms_existence_of_unallocated_people(self):
        """
        test_it_confirms_existence_of_unallocated_people():
        tests confirm_existence_of_unallocated()
        """

        self.assertFalse(self.amity_object.fetch_list_of_unallocated_people())


    # tests whether print_unallocated() prints
    # to screen
    def test_prints_unallocated_to_screen(self):
        """
        test_prints_unallocated_to_screen():
        tests print_unallocated()
        """

        for i in ["-a", "-b", "-c", "-d", "-e", "-f"]:
            name = "Test Person" + i
            self.amity_object.add_person(name, "STAFF")

        with self.captured_output() as (out, err):
            self.amity_object.print_unallocated()

            output = out.getvalue()
            self.assertEqual(output, "\n TEST PERSON-A - not allocated office\n" +
                             "\n TEST PERSON-B - not allocated office\n" +
                             "\n TEST PERSON-C - not allocated office\n" +
                             "\n TEST PERSON-D - not allocated office\n" +
                             "\n TEST PERSON-E - not allocated office\n" +
                             "\n TEST PERSON-F - not allocated office\n")

    # tests whether print_unallocated() prints(writes)
    # to file
    def test_prints_unallocated_to_file(self):
        """
        test_prints_unallocated_to_file():
        tests print_unallocated(arg)
        """

        lines = []

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        filename = os.path.join(file_path, "text_files/unallocated_file.txt")

        for i in ["-a", "-b"]:
            name = "Staff Person" + i
            self.amity_object.add_person(name, "STAFF")
        for i in ["-a", "-b"]:
            name = "Fellow Person" + i
            self.amity_object.add_person(name, "FELLOW", "Y")

        self.amity_object.print_unallocated("unallocated_file.txt")

        try:
            file_object = open(filename, "r")

            try:
                lines = file_object.readlines()

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
                      lines)

    # tests check for allocations in given room
    def test_it_confirms_specific_room_has_allocations(self):
        """
        test_it_confirms_specific_room_has_allocations():
        tests if confirm_existence_of_allocations_for_particular_room()
        works properly
        """
        self.amity_object.create_room("OFFICE", ["Valhalla"])

        self.assertFalse(self.amity_object.confirm_existence_of_allocations_for_particular_room("VALHALLA"))

        self.amity_object.add_person("Code Dragon", "FELLOW")
        self.amity_object.add_person("Bau Meister", "STAFF")

        self.assertTrue(self.amity_object.confirm_existence_of_allocations_for_particular_room("VALHALLA"))

    # tests if print_room() prints to screen
    def test_it_prints_room(self):
        """
        test_it_prints_room():
        tests whether print_room() works properly
        """

        self.amity_object.create_room("OFFICE", ["Krypton"])
        for i in ["-a", "-b", "-c"]:
            name = "Test Person" + i
            self.amity_object.add_person(name, "STAFF")

        with self.captured_output() as (out, err):
            self.amity_object.print_room("KRYPTON")

            output = out.getvalue()
            self.assertEqual(output, "\n TEST PERSON-A\n\n TEST PERSON-B\n\n TEST PERSON-C\n")

    # tests data validation by print_room
    def test_print_room_validates_room_names(self):
        """
        test_print_room_validates_room_names():
        tests if print_room() validates room names
        :return:
        """

        with self.captured_output() as (out, err):

            self.amity_object.print_room("kjlhfvg(*&^&%$89665544")
            output = out.getvalue()

            self.assertEqual(output, "\n Use letters and/or digits only for room names\n",
                             msg="Output not equal to expected error message")

    # tests room name verification by print_room
    def test_print_room_rejects_non_existent_room_names(self):
        """
        test_print_room_rejects_non_existent_room_names():
        tests if print_room() validates room names
        :return:
        """
        with self.captured_output() as (out, err):

            self.amity_object.print_room("TEST ROOM")
            output = out.getvalue()

            self.assertEqual(output, "\n Room TEST ROOM does not exist in the system\n",
                             msg="Output not equal to expected error message")

    # tests save state to default db
    def test_it_saves_state_to_default_db(self):
        """
        test_it_saves_state_to_default_db():
        tests whether save state works correctly without
        a destination db argument
        """
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        filename = os.path.join(file_path, "db_files/amity.db")
        if os.path.isfile(filename):
            os.remove(filename)

        self.amity_object.create_room("OFFICE", ["Mara"])
        self.amity_object.create_room("LIVINGSPACE", ["Serengeti"])

        self.amity_object.add_person("Josh Jebs", "STAFF")
        self.amity_object.add_person("Sarah Munene", "FELLOW", "Y")

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

        self.assertIn("MARA" and "SERENGETI" and "JOSH JEBS"
                      and "SARAH MUNENE" and "Y" and "s-1" + Amity.session_id
                      and "f-2" + Amity.session_id,
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

        self.amity_object.create_room("OFFICE", ["Mara"])
        self.amity_object.create_room("LIVINGSPACE", ["Serengeti"])

        self.amity_object.add_person("Josh Jebs", "STAFF")
        self.amity_object.add_person("Sarah Munene","FELLOW", "Y")

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

        self.assertIn("MARA" and "SERENGETI" and "JOSH JEBS"
                      and "SARAH MUNENE" and "Y" and "s-1" + Amity.session_id
                      and "f-2" + Amity.session_id,
                      results_list,
                      msg="Could not verify database fetch results")

    # tests verification of file existence
    def test_load_state_confirms_existence_of_db_file(self):
        """
        test_load_state_confirms_existence_of_db_file():
        tests whether load state confirms existence of source db
        file before attempting to load state
        """

        self.assertEqual(self.amity_object.load_state("non_existent_file.db"),
                         "\n File does not exist", "Could not find file")

    # tests verification of file type
    def test_load_state_confirms_file_extension(self):
        """
        test_load_state_confirms_file_extension():

        """
        self.assertEqual(self.amity_object.load_state("my_file.txt"),
                         "\n File extension must be .db", msg="Not a database file")

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
                        ("BIG BEN", "f-1a", "Y", 0, 0),
                        ("SALLY MOLLY", "s-2a", "N", 0, 0),
                        ("HARRY PORTER", "f-3a", "N", 0, 0),
                        ("JIM HARRIGAN", "s-4a", "N", 0, 0)
                       ]

                cursor.executemany("""INSERT INTO tbl_people (person_name, person_identifier,
                               accommodation, has_office, has_livingspace) VALUES (?,?,?,?,?)""", rows)

                rows = [
                        ("VALHALLA", "office"),
                        ("UPSTAIRS", "livingspace")
                       ]
                cursor.executemany("""INSERT INTO tbl_rooms (room_name, room_type) VALUES (?,?)""", rows)

                rows = [
                        ("VALHALLA", "f-1a"),
                        ("UPSTAIRS", "f-1a"),
                        ("VALHALLA", "s-2a"),
                        ("VALHALLA", "f-3a"),
                        ("VALHALLA", "s-4a")
                       ]

                cursor.executemany("""INSERT INTO tbl_allocations (room_name, person_id) VALUES (?,?)""", rows)
                connection.commit()

            except sqlite3.Error as e:
                print("db access error - ", str(e))

            self.assertEqual(self.amity_object.load_state("test.db"),
                             "\n State was loaded successfully from " + filename)

    # test get_person_identifier() for data validation
    def test_get_person_identifier_validates_names(self):
        """
        test_get_person_identifier_validates_names()
        ensure names don't have illegal characters
        :return: relevant message
        """
        self.assertEqual(self.amity_object.get_person_identifier("ben", "man*&^%^$809", "fellow"),
                         "\n Use letters only for person name", msg="Could not verify output")

    # test get identifier for correctness
    def test_get_person_identifier_returns_correct_person_id(self):
        """
        test_get_person_identifier_returns_correct_person_id
        :return:
        """
        result = self.amity_object.add_person("Ben Man", "FELLOW", "y")

        self.assertIn(result[0], self.amity_object.get_person_identifier("Ben", "Man", "fellow"))





