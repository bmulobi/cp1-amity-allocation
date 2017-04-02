from amity_app.classes.person import Person
from amity_app.classes.amity import Amity

import re


class Staff(Person):
    """
    inherits from Person
    """

    def __init__(self, role="STAFF"):

        """
        :type accommodation: str
        :type name: str
        :type role: str
        """

        self.name = ""
        self.person_role = role
        self.person_id = ""
        self.amity_object = ""
        self.regex_name = r'(\(|\+|\?|\.|\*|\^|\$|\)|\[|\]|\{|\}|\||\\|\d|\`|\~|\!|\@|\#|\%|\_|\=|\;|\:|\"|\,|\<|\>|\/)'
        self.return_message = ""

    def add_person(self, name):
        """

        :param name: Person's name
        :return: relevant message
        """

        self.name = name.upper()
        # ensure no illegal characters in name i.e any of
        # ( + ? . *  ^ $  ( ) \ [ ] { } | \ ) [0-9] ` ~ ! @ # % _ = ; : " , < . > /
        if re.search(self.regex_name, self.name):
            return 0, ("Avoid any of the following characters in name: + ? . *  ^ $ "
                       "( ) \ [ ] { } | \  [0-9] ` ~ ! @ # % _ = ; : \" , < . > /")

        # instantiate Amity class
        self.amity_object = Amity()
        # increment person identifier by 1
        Amity.person_identifier += 1
        # make unique identifier for new staff member
        self.person_id = "s-" + str(Amity.person_identifier)

        # insert new person into staff dictionary with id as key
        Amity.people_list[1][self.person_id] = [self.name]
        self.return_message += (self.name + " with ID " + self.person_id + " was added successfully as a Staff\n")

        # confirm availability of space in amity
        if self.amity_object.confirm_availability_of_space_in_amity():
            # fetch list of rooms with space
            offices_with_space_list, living_spaces_with_space_list = \
                self.amity_object.fetch_rooms_with_space()
            # if there's office with space, allocate to new staff member
            if offices_with_space_list:
                for room in offices_with_space_list:
                    if room[1] > 0:
                        Amity.rooms_list[1][room[0]].append(self.person_id)
                        room[1] -= 1
                        self.return_message += ("and allocated to office " + room[0] + "\n")
                        break

        return self.person_id, self.return_message
