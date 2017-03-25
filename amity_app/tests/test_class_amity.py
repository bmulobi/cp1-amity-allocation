from unittest import TestCase

from amity_app.classes.person import Person
from amity_app.classes.amity import Amity
from amity_app.classes.fellow import Fellow
from amity_app.classes.living_space import LivingSpace
from amity_app.classes.office import Office
from amity_app.classes.room import Room
from amity_app.classes.staff import Staff


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
        test_callable_reallocate_person_from_class_Amity():
        Method checks whether reallocate_person() from class
        Amity is called properly
        """
        self.assertEqual(self.amity_object.reallocate_person("Ben", "valhalla"),
                         "Person is: Ben and new room name is: valhalla")

        # test calling load_people() from class Amity

    def test_calls_load_people_from_class_amity(self):
        """
        test_callable_load_people_from_class_Amity():
        Method checks whether load_people() from class
        Amity is called properly
        """
        self.assertEqual(self.amity_object.load_people(),
                         "load_people() was called successfully")

        # test calling print_allocations() from class Amity

    def test_calls_print_allocations_from_class_amity(self):
        """
        test_callable_print_allocations_from_class_Amity():
        Method checks whether print_allocations() from class
        Amity is called properly
        """
        self.assertEqual(self.amity_object.print_allocations(),
                         "print_allocations() was called successfully")

        # test calling print_unallocated() from class Amity

    def test_calls_print_unallocated_from_class_amity(self):
        """
        test_callable_print_unallocated_from_class_Amity():
        Method checks whether print_unallocated() from class
        Amity is called properly
        """
        self.assertEqual(self.amity_object.print_unallocated(),
                         "print_unallocated() was called successfully")

        # test calling print_room() from class Amity

    def test_calls_print_room_from_class_amity(self):
        """
        test_callable_print_room_from_class_Amity():
        Method checks whether print_room() from class
        Amity is called properly
        """
        self.assertEqual(self.amity_object.print_room("Krypton"),
                         "print_room() was called successfully with arg Krypton")

        # test calling save_state() from class Amity

    def test_calls_save_state_from_class_amity(self):
        """
        test_callable_save_state_from_class_Amity():
        Method checks whether save_state() from class
        Amity is called properly
        """
        self.assertEqual(self.amity_object.save_state("mydb"),
                         "save_state() was called successfully with arg mydb")

        # test calling load_state() from class Amity

    def test_calls_load_state_from_class_amity(self):
        """
        test_callable_load_state_from_class_Amity():
        Method checks whether load_state() from class
        Amity is called properly
        """
        self.assertEqual(self.amity_object.load_state("source_db"),
                         "load_state() was called successfully with arg source_db")

    def test_confirms_person_identifier(self):
        """
        test_confirms_person_identifier():
        :return:
        """

        self.assertTrue(self.amity_object.confirm_person_identifier(1000000000),
                        msg="Method should return true if identifier exists")

    def test_confirms_room_name(self):
        """
        test_confirms_room_name():
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
        self.assertEqual(self.amity_object.reallocate_person(1, "Krypton"),
                         "Person with identifier 1 was reallocated to Krypton",
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

    def test_confirms_existence_of_allocations(self):
        """
        test_confirms_existence_of_allocations():
        :return:
        """
        self.is_empty = True
        self.assertEqual(self.amity_object.confirm_existence_of_allocations(), False)

    def test_it_prints_allocations(self):
        """
        test_it_prints_allocations():
        :return:
        """
        self.assertEqual(self.amity_object.print_allocations(), True)

    def test_it_confirms_existence_of_unallocated(self):
        """
        test_it_confirms_existence_of_unallocated():
        :return:
        """

        self.assertEqual(self.amity_object.confirm_existence_of_unallocated(), True)

    def test_prints_unallocated(self):
        """
        test_prints_unallocated():
        :return:
        """
        unallocated_people_list = ["Ben", "John", "Sharon"]
        self.assertIn("Ben", self.amity_object.print_unallocated())

    def test_prints_room(self):
        """
        test_prints_room():
        :return:
        """

        self.assertEqual(self.amity_object.print_room("Krypton"), True)