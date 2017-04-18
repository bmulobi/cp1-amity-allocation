import os
from unittest import TestCase

from amity_app.classes.person import Person
from amity_app.classes.fellow import Fellow
from amity_app.classes.staff import Staff
from amity_app.classes.amity import Amity


class TestPerson(TestCase):
    """
    class holds tests for class person, class fellow and class staff
    """

    def setUp(self):
        """
        Method instantiates class objects
        that will be used in the test cases
        """

        self.amity_object = Amity()
        self.fellow_object = Fellow("Ben")
        self.staff_object = Staff("Sally")

        Amity.fellows = {}
        Amity.staff = {}
        Amity.offices = {}
        Amity.living_spaces = {}

    def tearDown(self):
        del self.amity_object
        del self.staff_object
        del self.fellow_object

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
            self.class_object = class_to_check("Ben")

        except TypeError:
            return False

        return True

    # Method tests if object is of class Fellow
    def test_isinstance_of_fellow_class(self):
        """
        test_isInstance_of_Fellow_class():
        Method uses assertIsInstance() to check whether
        given object belongs to class Fellow

        """

        self.assertIsInstance(self.fellow_object, Fellow)

    # Method tests if object is of class Staff
    def test_isinstance_of_staff_class(self):
        """
        test_isinstance_of_staff_class():
        Method uses assertIsInstance() to check whether
        given object belongs to class Staff

        """

        self.assertIsInstance(self.staff_object, Staff)

    # Method tests if object is a subclass of class person
    def test_fellow_is_subclass_of_person(self):
        """
        test_fellow_is_subclass_of_person():
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
    def test_staff_is_subclass_of_person(self):
        """
        test_staff_is_subclass_of_person():
        Method uses issubclass() to check whether
        Staff is a subclass of Person

        Returns
        -------
        Boolean

        True : if it is a subclass
        False : otherwise

        """
        self.assertTrue(issubclass(Staff, Person))

    # Method tests the type of the given object
    def test_fellow_object_type(self):
        """
        test_fellow_object_type():
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
    def test_staff_object_type(self):
        """
        test_Staff_object_type()
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
    def test_person_is_abstract_class(self):
        """
        test_person_is_abstract_class():
        Method uses helper method check_abstract_class_instantiation()
        to check whether class Person can be instantiated

        Returns
        -------
        Boolean

        True : if it is abstract
        False : otherwise

        """

        self.assertEqual(self.check_abstract_class_instantiation(Person), False)
