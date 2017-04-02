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
        set up some required properties for the tests

        """
        self.fellow_object = Fellow()
        self.staff_object = Staff()

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

    # Method tests if add_person() works properly
    def test_add_person_in_class_fellow(self):
        """
        test_add_person_in_class_fellow():
        tests whether add_person() in fellow adds a
         fellow properly
        """

        Amity.person_identifier = 0
        Amity.people_list = [{}, {}]
        self.fellow_object.add_person("BEN MAN", "Y")

        self.assertIn("BEN MAN" and "Y", Amity.people_list[0]["f-1"])

    # Method tests if add_person() works properly
    def test_add_person_in_class_staff(self):
        """
        test_add_person_in_class_staff():
        tests whether add_person() in staff adds a
         staff member properly
        """

        Amity.person_identifier = 0
        Amity.people_list = [{}, {}]
        self.staff_object.add_person("JACKIE CHAN")

        self.assertIn("JACKIE CHAN", Amity.people_list[1]["s-1"])

    # ensure fellow's name is acceptable format
    def test_add_person_in_fellow_rejects_illegal_characters_in_person_name(self):
        """
        test_add_person_in_fellow_rejects_illegal_characters_in_person_name():
        test whether add_person() in class fellow rejects following characters
        in person name
        ( + ? . *  ^ $  ( ) \ [ ] { } | \ ) [0-9] ` ~ ! @ # % _ = ; : \" , < . > /
        """
        id, msg = self.fellow_object.add_person("BEn*&^%#W@^((_)(653132", "Y")
        self.assertEqual(msg, "Avoid any of the following characters in name: + ? . *  ^ $ "
                         "( ) \ [ ] { } | \  [0-9] ` ~ ! @ # % _ = ; : \" , < . > /",
                         msg="Output not equal to expected output")

    # ensure staff's name is acceptable format
    def test_add_person_in_staff_rejects_illegal_characters_in_person_name(self):
        """
        test_add_person_in_staff_rejects_illegal_characters_in_person_name():
        test whether add_person() in class fellow rejects following characters
        in person name
        ( + ? . *  ^ $  ( ) \ [ ] { } | \ ) [0-9] ` ~ ! @ # % _ = ; : \" , < . > /
        """
        id, msg = self.staff_object.add_person("BEn*&^%#W@^((_)(653132")
        self.assertEqual(msg, "Avoid any of the following characters in name: + ? . *  ^ $ "
                         "( ) \ [ ] { } | \  [0-9] ` ~ ! @ # % _ = ; : \" , < . > /",
                         msg="Output not equal to expected output")




