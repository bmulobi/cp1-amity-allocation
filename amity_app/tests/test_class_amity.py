from unittest import TestCase

from amity_app.classes.person import Person
from amity_app.classes.amity import Amity
from amity_app.classes.fellow import Fellow
from amity_app.classes.living_space import LivingSpace
from amity_app.classes.office import Office
from amity_app.classes.room import Room
from amity_app.classes.staff import Staff

import sys
from contextlib import contextmanager
from io import StringIO

# Class contains all the logic to run model tests on
# the class definitions for the amity room allocation app

class TestAmity(TestCase):
    """
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

    # test calling reallocate_person() from class Amity
    def test_calls_reallocate_person_from_class_amity(self):
        """
        test_calls_reallocate_person_from_class_Amity():
        Method checks whether reallocate_person() from class
        Amity is called properly
        """
        self.assertEqual(self.amity_object.reallocate_person("Ben", "valhalla"),
                         "Person is: Ben and new room name is: valhalla")

        # test calling load_people() from class Amity

    def test_calls_load_people_from_class_amity(self):
        """
        test_calls_load_people_from_class_Amity():
        Method checks whether load_people() from class
        Amity is called properly
        """
        self.assertEqual(self.amity_object.load_people(),
                         "load_people() was called successfully")

        # test calling print_allocations() from class Amity

    def test_calls_print_allocations_from_class_amity(self):
        """
        test_calls_print_allocations_from_class_Amity():
        Method checks whether print_allocations() from class
        Amity is called properly
        """
        self.assertEqual(self.amity_object.print_allocations(),
                         "print_allocations() was called successfully")

        # test calling print_unallocated() from class Amity

    def test_calls_print_unallocated_from_class_amity(self):
        """
        test_calls_print_unallocated_from_class_Amity():
        Method checks whether print_unallocated() from class
        Amity is called properly
        """
        self.assertEqual(self.amity_object.print_unallocated(),
                         "print_unallocated() was called successfully")

        # test calling print_room() from class Amity

    def test_calls_print_room_from_class_amity(self):
        """
        test_calls_print_room_from_class_Amity():
        Method checks whether print_room() from class
        Amity is called properly
        """
        self.assertEqual(self.amity_object.print_room("Krypton"),
                         "print_room() was called successfully with arg Krypton")

        # test calling save_state() from class Amity

    def test_calls_save_state_from_class_amity(self):
        """
        test_calls_save_state_from_class_Amity():
        Method checks whether save_state() from class
        Amity is called properly
        """
        self.assertEqual(self.amity_object.save_state("mydb"),
                         "save_state() was called successfully with arg mydb")

        # test calling load_state() from class Amity

    def test_calls_load_state_from_class_amity(self):
        """
        test_calls_load_state_from_class_Amity():
        Method checks whether load_state() from class
        Amity is called properly
        """
        self.assertEqual(self.amity_object.load_state("source_db"),
                         "load_state() was called successfully with arg source_db")

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
        error_msg = ""

        try:
            file_object = open("../text_files/test_file.txt", "w")
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

        for i in range(3):
            name = "Staff Person" + str(i)
            self.staff_object.add_person(name)
        for i in range(3):
            name = "Fellow Person" + str(i)
            self.fellow_object.add_person(name)

        self.amity_object.print_unallocated("../text_files/unallocated_file.txt")

        try:
            file_object = open("../text_files/unallocated_file.txt", "r")

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




    def test_it_saves_state(self):
        """
        test_it_saves_state():

        :return:
        """
        pass

    def test_it_loads_state(self):
        """
        test_it_loads_state():

        :return:
        """
        pass