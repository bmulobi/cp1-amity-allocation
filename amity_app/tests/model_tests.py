import unittest

from amity_app.classes.person import Person
from amity_app.classes.amity import Amity
from amity_app.classes.fellow import Fellow
from amity_app.classes.living_space import LivingSpace
from amity_app.classes.office import Office
from amity_app.classes.room import Room
from amity_app.classes.staff import Staff

# Class contains all the logic to run model tests on
# the class definitions for the amity room allocation app


class TestModels(unittest.TestCase):
    """
    class contains a setUp() method to initialise
    required attributes for the tests. It also has
    got a helper function - check_abstract_class_instantiation()
    to help run tests for abstract classes. The other methods
    perform the actual model testing functions
    """

    # test cases set up method
    def setUp(self):
        """
        Method instantiates class objects
        that will be used in the test cases

        """

        self.amity_object = Amity()
        self.fellow_object = Fellow("Ben", "fellow")
        self.livingSpace_object = LivingSpace("mara")
        self.office_object = Office("samburu")
        self.staff_object = Staff("Sally", "staff")

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

    # Method tests if object is of class Amity
    def test_isInstance_of_Amity_class(self):
        """
        test_isInstance_of_Amity_class():
        Method uses assertIsInstance() to check whether
        given object belongs to class Amity

        """

        self.assertIsInstance(self.amity_object, Amity)

    # Method tests if object is of class Fellow
    def test_isInstance_of_Fellow_class(self):
        """
        test_isInstance_of_Fellow_class():
        Method uses assertIsInstance() to check whether
        given object belongs to class Fellow

        """

        self.assertIsInstance(self.fellow_object, Fellow)

    # Method tests if object is of class LivingSpace
    def test_isInstance_of_livingSpace_class(self):
        """
        test_isInstance_of_livingSpace_class():
        Method uses assertIsInstance() to check whether
        given object belongs to class LivingSpace

        """

        self.assertIsInstance(self.livingSpace_object, LivingSpace)

    # Method tests if object is of class Office
    def test_isInstance_of_Office_class(self):
        """
        test_isInstance_of_Office_clas():
        Method uses assertIsInstance() to check whether
        given object belongs to class Office

        """

        self.assertIsInstance(self.staff_object, Staff)

    # Method tests if object is of class Staff
    def test_isInstance_of_Staff_class(self):
        """
        test_isInstance_of_Staff_class():
        Method uses assertIsInstance() to check whether
        given object belongs to class Staff

        """

        self.assertIsInstance(self.staff_object, Staff)

    # Method tests if object is a subclass of class person
    def test_Fellow_is_subclass_of_Person(self):
        """
        test_Fellow_is_subclass_of_Person():
        Method uses issubclass() to check whether
        Fellow is a subclass of Person

        Returns
        -------
        Boolean
        True : if it is a subclass
        False : otherwise

        """
        self.assertTrue(issubclass(Fellow, Person))

    # Method tests if object is a subclass of class person
    def test_Staff_is_subclass_of_Person(self):
        """
        test_Staff_is_subclass_of_Person():
        Method uses issubclass() to check whether
        Staff is a subclass of Person

        Returns
        -------
        Boolean

        True : if it is a subclass
        False : otherwise

        """
        self.assertTrue(issubclass(Staff, Person))

    # Method tests if object is a subclass of class Room
    def test_LivingSpace_is_subclass_of_Room(self):
        """
        test_LivingSpace_is_subclass_of_Room():
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
    def test_Office_is_subclass_of_Room(self):
        """
        test_Office_is_subclass_of_Room():
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
    def test_Amity_object_type(self):
        """
        test_Amity_object_type():
        Method uses type() to check whether
        given object is of type Amity

        Returns
        -------
        Boolean

        True : if it is of type Amity
        False : otherwise

        """

        self.assertTrue(type(self.amity_object) is Amity)

    # Method tests the type of the given object
    def test_Fellow_object_type(self):
        """
        test_Fellow_object_type():
        Method uses type() to check whether
        given object is of type Fellow

        Returns
        -------
        Boolean

        True : if it is of type Fellow
        False : otherwise

        """

        self.assertTrue(type(self.fellow_object) is Fellow)

    # Method tests the type of the given object
    def test_LivingSpace_object_type(self):
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

        self.assertTrue(type(self.livingSpace_object) is LivingSpace)

    # Method tests the type of the given object
    def test_Office_object_type(self):
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

    # Method tests the type of the given object
    def test_Staff_object_type(self):
        """
        test_Staff_object_type():
        Method uses type() to check whether
        given object is of type Staff

        Returns
        -------
        Boolean

        True : if it is of type Staff
        False : otherwise

        """

        self.assertTrue(type(self.staff_object) is Staff)

    # Method tests if class Person is abstract
    def test_Person_is_abstract_class(self):
        """
        test_Person_is_abstract_class():
        Method uses helper method check_abstract_class_instantiation()
        to check whether class Person can be instantiated

        Returns
        -------
        Boolean

        True : if it is abstract
        False : otherwise

        """

        self.assertEqual(self.check_abstract_class_instantiation(Person), False)

    # Method tests if class Room is abstract
    def test_Room_is_abstract_class(self):
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


if __name__ == "__main__":
    unittest.main()



