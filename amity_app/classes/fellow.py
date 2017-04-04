from amity_app.classes.person import Person
from amity_app.classes.amity import Amity

import re


class Fellow(Person):
    """
    inherits from Person
    Defines the attributes of a person who is a fellow
    """

    def __init__(self, role="FELLOW"):
        self.name = ""
        self.person_role = role
        self.accommodation = "N"
        self.person_id = ""
        self.amity_object = ""
        self.regex_name = r'(\(|\+|\?|\.|\*|\^|\$|\)|\[|\]|\{|\}|\||\\|\d|\`|\~|\!|\@|\#|\%|\_|\=|\;|\:|\"|\,|\<|\>|\/)'
        self.return_message = ""

    def add_person(self, name, wants_accommodation="N"):
        """
        :param name: Person's name
        :param wants_accommodation: default N if Y allocate accommodation
        :return: relevant message
        """

        self.name = name.upper()
        self.accommodation = wants_accommodation.upper()

        # ensure no illegal characters in name i.e any of
        # ( + ? . *  ^ $  ( ) \ [ ] { } | \ ) [0-9] ` ~ ! @ # % _ = ; : " , < . > /
        if re.search(self.regex_name, self.name):
            return 0, ("Avoid any of the following characters in name: + ? . *  ^ $ "
                       "( ) \ [ ] { } | \  [0-9] ` ~ ! @ # % _ = ; : \" , < . > /")

        # ensure wants accommodation option is either (Y or N) or (y or n)
        if self.accommodation not in["Y", "N", "y", "n"]:
            return 0, "Accommodation option should be either (Y or N) or (y or n)"

        # instantiate Amity class
        self.amity_object = Amity()
        # increment person identifier by 1
        Amity.person_identifier += 1
        # make unique identifier for new fellow
        self.person_id = "f-" + str(Amity.person_identifier)

        # insert new person into fellows dictionary with id as key
        Amity.people_list[0][self.person_id] = [self.name]
        self.return_message += self.name + " with ID " + self.person_id + " was added successfully as a fellow\n"
        # append accommodation preferences to list
        if self.accommodation == "Y":
            Amity.people_list[0][self.person_id].append("Y")
        else:
            Amity.people_list[0][self.person_id].append("N")

        # confirm availability of space in amity
        if self.amity_object.confirm_availability_of_space_in_amity():
            # fetch list of rooms with space
            offices_with_space_list, living_spaces_with_space_list = \
                self.amity_object.fetch_rooms_with_space()
            # if there's office with space, allocate to new fellow
            if offices_with_space_list:
                for room in offices_with_space_list:
                    if room[1] > 0:
                        Amity.rooms_list[1][room[0]].append(self.person_id)
                        room[1] -= 1
                        Amity.people_list[0][self.person_id].append("office")
                        self.return_message += "and allocated to office " + room[0] + "\n"
                        break
            # check if fellow wants accommodation
            if self.accommodation == "Y":
                # if there's a living space with space, allocate to fellow
                if living_spaces_with_space_list:
                    for room in living_spaces_with_space_list:
                        if room[1] > 0:
                            Amity.rooms_list[0][room[0]].append(self.person_id)
                            room[1] -= 1
                            Amity.people_list[0][self.person_id].append("livingspace")
                            self.return_message += "and living space " + room[0] + "\n"
                            break

        return self.person_id, self.return_message
