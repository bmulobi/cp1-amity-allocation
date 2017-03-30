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

    def test_confirms_person_identifier_as_valid(self):
        """
        test_confirms_person_identifier_as_valid():
        :return:
        """

        self.assertTrue(self.amity_object.confirm_person_identifier(1000000000),
                        msg="Method should return true if identifier exists")

    def test_confirms_room_name_as_valid(self):
        """
        test_confirms_room_name_as_valid():
        :return:
        """

        self.assertFalse(self.amity_object.confirm_room_name("*&&^%$EWQ%*&(_)^^$^%"),
                         msg="Method should return true if room name exists")
        self.office_object.create_room("Dragons")
        self.assertTrue(self.amity_object.confirm_room_name("Dragons"),
                        msg="Method should return true if room name exists")

    def test_confirms_specific_room_has_space(self):
        """
        test_confirms_specific_room_has_space():
        :return:
        """
        self.office_object.create_room("Pentagon")
        self.assertTrue(self.amity_object.confirm_specific_room_has_space("Pentagon"))

        for i in range(7):
            person_name = "John" + str(i)
            person_id, msg = self.staff_object.add_person(person_name)
            self.amity_object.reallocate_person(person_id, "Pentagon")

        person_id, msg = self.staff_object.add_person("Test Person")
        self.assertEqual(self.amity_object.reallocate_person(person_id, "Pentagon"),
                         "Pentagon is fully occupied",
                         msg="Could not reallocate person to fully occupied room")

        self.assertFalse(self.amity_object.confirm_specific_room_has_space("Pentagon"))

    def test_does_not_reallocate_staff_to_livingspace(self):
        """
        test_does_not_reallocate_staff_to_livingspace():
        :return:
        """

        self.living_space_object.create_room("Atom")
        person_id, msg = self.staff_object.add_person("Ben Man")
        self.assertEqual(self.amity_object.reallocate_person(person_id, "Atom"),
                         "Cannot reallocate staff member to a living space",
                         msg="Could not reallocate staff member to living space")

    def test_reallocates_person(self):
        """
        test_reallocates_person()
        :return:
        """
        Amity.rooms_list = [{}, {}]
        Amity.people_list = [{}, {}]

        self.living_space_object.create_room("TestRoom")
        person_id, msg = self.fellow_object.add_person("Test Person", "Y")
        self.living_space_object.create_room("TestRoomTwo")
        self.assertEqual(self.amity_object.reallocate_person(person_id, "TestRoomTwo"),
                         "Person with identifier " + person_id + " was reallocated to TestRoomTwo",
                         msg="Failed to reallocate person")

    def test_confirms_availability_of_space_in_amity(self):
        """
        test_confirms_availability_of_space_in_amity():
        :return:
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
        self.living_space_object.create_room("Atomic")
        self.office_object.create_room("Neutronic")
        self.amity_object.load_people()

        self.assertIn("f-1", Amity.rooms_list[0]["Atomic"])
        self.assertIn("f-1", Amity.rooms_list[1]["Neutronic"])
        self.assertIn("s-2", Amity.rooms_list[1]["Neutronic"])

    def test_confirms_existence_of_allocations_in_amity(self):
        """
        test_confirms_existence_of_allocations_in_amity():
        :return:
        """
        Amity.rooms_list = [{}, {}]
        Amity.people_list = [{}, {}]
        self.assertFalse(self.amity_object.confirm_existence_of_allocations(),
                         msg="Could not confirm existence of allocations")
        self.office_object.create_room("Test Room")
        person_id, msg = self.staff_object.add_person("Test Person")
        self.assertTrue(self.amity_object.confirm_existence_of_allocations(),
                        msg="Could not confirm existence of allocations")

    def test_it_prints_allocations(self):
        """
        test_it_prints_allocations():
        :return:
        """
        Amity.rooms_list = [{}, {}]
        Amity.people_list = [{}, {}]
        self.office_object.create_room("TestRoom")
        for i in range(7):
            name = "Test Person" + str(i)
            self.staff_object.add_person(name)
        self.assertIn("TestRoom\n" and
                      "-------------------------------------\n" and
                      "Test Person1, Test Person2, Test Person3, " +
                      "Test Person4, Test Person5, Test Person6\n",
                      self.amity_object.print_allocations()
                      )

        self.amity_object.print_allocations("../text_files/allocations_file.txt")

        try:
            file_object = open("../text_files/allocations_file.txt", "r")
            try:
                lines_list = file_object.readlines()

            finally:
                file_object.close()

        except IOError as e:
            print(str(e))
        self.assertIn(lines_list, "TestRoom\n" and
                      "-------------------------------------\n" and
                      "Test Person1, Test Person2, Test Person3, " +
                      "Test Person4, Test Person5, Test Person6\n")

    def test_it_confirms_existence_of_unallocated_people(self):
        """
        test_it_confirms_existence_of_unallocated_people():
        :return:
        """
        Amity.rooms_list = [{}, {}]
        Amity.people_list = [{}, {}]

        self.assertFalse(self.amity_object.confirm_existence_of_unallocated())

        for i in range(7):
            name = "Test Person" + str(i)
            self.staff_object.add_person(name)

        self.assertTrue(self.amity_object.confirm_existence_of_unallocated())

    def test_prints_unallocated_to_screen(self):
        """
        test_prints_unallocated():
        :return:
        """
        Amity.rooms_list = [{}, {}]
        Amity.people_list = [{}, {}]

        for i in range(7):
            name = "Test Person" + str(i)
            self.staff_object.add_person(name)

        with self.captured_output() as (out, err):
            self.amity_object.print_unallocated()

        output = out.getvalue().strip()
        self.assertEqual(output, "Test Person1, Test Person2, Test Person3," +
                                 " Test Person4, Test Person5, Test Person6")

    def test_prints_unallocated_to_file(self):
        """
        test_prints_unallocated_to_file():
        :return:
        """
        Amity.rooms_list = [{}, {}]
        Amity.people_list = [{}, {}]

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        filename = os.path.join(file_path, "text_files/unallocated_file.txt")

        for i in range(3):
            name = "Staff Person" + str(i)
            self.staff_object.add_person(name)
        for i in range(3):
            name = "Fellow Person" + str(i)
            self.fellow_object.add_person(name)

        self.amity_object.print_unallocated(filename)

        try:
            file_object = open(filename, "r+")

            try:
                lines_list = file_object.readlines()

            finally:
                file_object.close()

        except IOError as e:
            print(str(e))
        self.assertIn("Staff Person1\nStaff Person2\nFellow Person1\nFellow Person2\n", lines_list)

    def test_it_confirms_specific_room_has_allocations(self):
        """
        test_it_confirms_specific_room_has_allocations():
        :return:
        """
        Amity.rooms_list = [{}, {}]
        Amity.people_list = [{}, {}]

        self.office_object.create_room("Valhalla")

        self.assertFalse(self.amity_object.confirm_existence_of_allocations_for_particular_room("Valhalla"))

        self.staff_object.add_person("Code Dragon")
        self.fellow_object.add_person("Bau Meister")

        self.assertTrue(self.amity_object.confirm_existence_of_allocations_for_particular_room("Valhalla"))

    def test_it_prints_room(self):
        """
        test_it_prints_room():

        :return:
        """
        Amity.rooms_list = [{}, {}]
        Amity.people_list = [{}, {}]

        self.office_object.create_room("Krypton")
        for i in range(4):
            name = "Test Person" + str(i)
            self.staff_object.add_person(name)

        with self.captured_output() as (out, err):
            self.amity_object.print_room("Krypton")

        output = out.getvalue().strip()
        self.assertEqual(output, "Test Person1\nTest Person2\nTest Person3\n")

    def test_it_saves_state_to_default_db(self):
        """
        test_it_saves_state_to_default_db():

        :return:
        """
        if os.path.isfile("amity.db"):
            os.remove("amity.db")

        Amity.rooms_list = [{}, {}]
        Amity.people_list = [{}, {}]

        self.office_object.create_room("Mara")
        self.living_space_object.create_room("Serengeti")

        self.staff_object.add_person("Josh Jebs")
        self.fellow_object.add_person("Sarah Munene", "Y")

        self.amity_object.save_state()

        results_list = []

        try:
            connection = sqlite3.connect("amity.db")
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM tbl_people")
            connection.commit()
            results = cursor.fetchall()

            for row in results:
                results_list.append(results["person_iname"])
                results_list.append(results["person_identifier"])
                results_list.append(results["accommodation"])

            cursor.execute("SELECT * FROM tbl_rooms")
            connection.commit()
            results = cursor.fetchall()

            for row in results:
                results_list.append(results["room_name"])
                results_list.append(results["room_type"])

            cursor.execute("SELECT * FROM tbl_allocations")
            connection.commit()
            results = cursor.fetchall()

            for row in results:
                results_list.append(results["room_name"])
                results_list.append(results["person_id"])

        except sqlite3.Error as e:
            print("db access error - ", str(e))

        self.assertIn("Mara" and "Serengeti" and "Josh Jebs"
                      and "Sarah Munene" and "Y" and "s-1" and "f-2",
                      results_list,
                      msg="Could not verify database fetch results")

    def test_it_saves_state_to_specified_db(self):
        """
        test_it_saves_state_to_specified_db():

        :return:
        """
        if os.path.isfile("specified.db"):
            os.remove("specified.db")

        Amity.rooms_list = [{}, {}]
        Amity.people_list = [{}, {}]

        self.office_object.create_room("Mara")
        self.living_space_object.create_room("Serengeti")

        self.staff_object.add_person("Josh Jebs")
        self.fellow_object.add_person("Sarah Munene", "Y")

        self.amity_object.save_state("specified")

        results_list = []
        db_name = "specified." + "db"

        try:
            connection = sqlite3.connect(db_name)
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM tbl_people")
            connection.commit()
            results = cursor.fetchall()

            for row in results:
                results_list.append(results["person_name"])
                results_list.append(results["person_identifier"])
                results_list.append(results["accommodation"])

            cursor.execute("SELECT * FROM tbl_rooms")
            connection.commit()
            results = cursor.fetchall()

            for row in results:
                results_list.append(results["room_name"])
                results_list.append(results["room_type"])

            cursor.execute("SELECT * FROM tbl_allocations")
            connection.commit()
            results = cursor.fetchall()

            for row in results:
                results_list.append(results["room_name"])
                results_list.append(results["person_id"])

        except sqlite3.Error as e:
            print("db access error - ", str(e))

        self.assertIn("Mara" and "Serengeti" and "Josh Jebs"
                      and "Sarah Munene" and "Y" and "s-1" and "f-2",
                      results_list,
                      msg="Could not verify database fetch results")

    def test_it_confirms_existence_of_file(self):
        """
        test_it_confirms_existence_of_db_file():
        :return:
        """
        self.assertEqual(self.amity_object.load_state("fake_file.db"),
                         "File does not exist", "Could not find file")

    def test_load_state_confirms_file_extension(self):
        """
        test_load_state_confirms_file_extension():
        :return:
        """
        self.assertEqual(self.amity_object.load_state("my_file.txt"),
                         "File extension must be .db", "Not a database file")

    def test_it_loads_state(self):
        """
        test_it_loads_state():

        :return:
        """
        if os.path.isfile("test.db"):
            os.remove("test.db")

        try:
            connection = sqlite3.connect("test.db")
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            cursor.execute("""CREATE TABLE tbl_people (id INTEGER PRIMARY KEY NOT NULL,
                           person_name TEXT NOT NULL, person_identifier TEXT NOT NULL,
                           accommodation TEXT NOT NULL)""")
            cursor.execute("""CREATE TABLE tbl_rooms (id INTEGER PRIMARY KEY NOT NULL,
                           room_name TEXT NOT NULL, room_type TEXT NOT NULL)""")
            cursor.execute("""CREATE TABLE tbl_allocations (id INTEGER PRIMARY KEY NOT NULL,
                           room_name TEXT NOT NULL, person_id TEXT NO NULL)""")
            connection.commit()

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
                    ("Valhalla", "f-3"),
                   ]

            cursor.executemany("""INSERT INTO tbl_allocations (room_name, person_id) VALUES (?,?)""", rows)
            connection.commit()

        except sqlite3.Error as e:
            print("db access error - ", str(e))

        Amity.rooms_list = [{}, {}]
        Amity.people_list = [{}, {}]

        self.amity_object.load_state("test.db")

        fellows_names = Amity.people_list[0].values()
        self.assertIn("Big Ben" and "Harry Porter", fellows_names, msg="Name not found in dictionary")

        staff_names = Amity.people_list[0].values()
        self.assertIn("Sally Molly" and "Jim Harrigan", staff_names, msg="Name not found in dictionary")

        livingspaces_names = Amity.rooms_list[0].keys()
        self.assertIn("Upstairs", livingspaces_names, msg="Name not found in dictionary")

        offices_names = Amity.rooms_list[1].keys()
        self.assertIn("Valhalla", offices_names, msg="Name not found in dictionary")

        offices_allocations_list = Amity.rooms_list[1].values()
        self.assertIn("f-1" and "s-2" and "f-3", offices_allocations_list,
                      msg="Could not find the identifiers in dictionary")

        livingspaces_allocations_list = Amity.rooms_list[0].values()
        self.assertIn("f-1", livingspaces_allocations_list,
                      msg="Could not find the identifiers in dictionary")





