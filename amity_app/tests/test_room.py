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
        set up some required properties for the tests
        """
        self.office_object = Office()
        self.livingspace_object = LivingSpace()

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
            self.class_object = class_to_check("John", "staff")

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

    def test_create_room_in_office(self):
        """
        test_create_room_in_office():
        tests whether create_room() in
         office creates a room properly
        """
        Amity.rooms_list = [{}, {}]

        self.office_object.create_room("Krypton")

        self.assertIn("Krypton", Amity.rooms_list[1].keys())

    def test_create_room_in_livingspace(self):
        """
        test_create_room_in_livingspace():
        tests whether create_room() in
        livingspace creates a room properly
        """
        Amity.rooms_list = [{}, {}]

        self.livingspace_object.create_room("Hostel")

        self.assertIn("Hostel", Amity.rooms_list[0].keys())

    def test_create_room_in_office_rejects_duplicate_room_names(self):
        """
        test_create_room_in_office_rejects_duplicate_room_names():
        check whether create room checks for duplicate room names
        """
        Amity.rooms_list = [{}, {}]

        self.office_object.create_room("Krypton")
        self.assertEqual(self.office_object.create_room("Krypton"),
                         "Room name already exists",
                         msg="Could not reject duplicate room name")

    def test_create_room_in_livingspace_rejects_duplicate_room_names(self):
        """
        test_create_room_in_livingspace_rejects_duplicate_room_names():
        check whether create room checks for duplicate room names
        """
        Amity.rooms_list = [{}, {}]

        self.livingspace_object.create_room("Hostel")
        self.assertEqual(self.office_object.create_room("Hostel"),
                         "Room name already exists",
                         msg="Could not reject duplicate room name")



