import os
from unittest import TestCase

from amity_app.classes.room import Room
from amity_app.classes.office import Office
from amity_app.classes.living_space import LivingSpace
from amity_app.classes.amity import Amity

# class for testing room creation functionality


class TestRoom(TestCase):
    """
    class contains logic to test class Room, class
    Office and class LivingSpace
    """
    def setUp(self):
        """
        Method instantiates class objects
        that will be used in the test cases
        """

        self.amity_object = Amity()
        self.office_object = Office("Krypton")
        self.livingspace_object = LivingSpace("Hostel")

        Amity.fellows = {}
        Amity.staff = {}
        Amity.offices = {}
        Amity.living_spaces = {}

    def tearDown(self):
        del self.amity_object
        del self.office_object
        del self.livingspace_object

    # helper method for testing abstract classes
    def check_abstract_class_instantiation(self, class_to_check):
        """
        Method checks whether a base class is abstract

        Parameter
        ---------
        class_to_check : class to be checked

        Returns
        -------
        False : if class cannot be instantiated
        True : if class can be instantiated

        """

        try:
            self.class_object = class_to_check("Valhalla")

        except TypeError:
            return False

        return True

    # Method tests if object is of class LivingSpace
    def test_isinstance_of_livingspace_class(self):
        """
        test_isinstance_of_livingspace_class():
        Method uses assertIsInstance() to check whether
        given object belongs to class LivingSpace

        """

        self.assertIsInstance(self.livingspace_object, LivingSpace)

    # Method tests if object is of class Office
    def test_isinstance_of_office_class(self):
        """
        test_isinstance_of_office_class():
        Method uses assertIsInstance() to check whether
        given object belongs to class Office

        """

        self.assertIsInstance(self.office_object, Office)

    # Method tests if object is a subclass of class Room
    def test_livingspace_is_subclass_of_room(self):
        """
        test_livingspace_is_subclass_of_room():
        Method uses issubclass() to check whether
        LivingSpace is a subclass of Room

        Returns
        -------
        Boolean

        True : if it is a subclass
        False : otherwise

        """
        self.assertTrue(issubclass(LivingSpace, Room))

    # Method tests if object is a subclass of class Room
    def test_office_is_subclass_of_Room(self):
        """
        test_office_is_subclass_of_Room():
        Method uses issubclass() to check whether
        Office is a subclass of Room

        Returns
        -------
        Boolean

        True : if it is a subclass
        False : otherwise

        """
        self.assertTrue(issubclass(Office, Room))

    # Method tests the type of the given object
    def test_livingspace_object_type(self):
        """
        test_LivingSpace_object_type():
        Method uses type() to check whether
        given object is of type LivingSpace

        Returns
        -------
        Boolean

        True : if it is of type LivingSpace
        False : otherwise

        """

        self.assertTrue(type(self.livingspace_object) is LivingSpace)

    # Method tests the type of the given object
    def test_office_object_type(self):
        """
        test_Office_object_type():
        Method uses type() to check whether
        given object is of type Office

        Returns
        -------
        Boolean

        True : if it is of type Office
        False : otherwise

        """

        self.assertTrue(type(self.office_object) is Office)


    # Method tests if class Room is abstract
    def test_room_is_abstract_class(self):
        """
        test_Room_is_abstract_class():
        Method uses helper method check_abstract_class_instantiation()
        to check whether class Room can be instantiated

        Returns
        -------
        Boolean

        True : if it is abstract
        False : otherwise

        """

        self.assertEqual(self.check_abstract_class_instantiation(Room), False)
