from amity_app.classes.person import Person
from amity_app.classes.amity import Amity

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
        self.amity_object = Amity()

    def add_person(self, name, wants_accommodation="N"):
        """

        :param name:
        :param wants_accommodation:
        :return:
        """

        Amity.person_identifier += 1
        self.person_id = "s-" + str(Amity.person_identifier)
        self.name = name
        Amity.people_list[1][self.person_id] = self.name

        if self.amity_object.confirm_availability_of_space_in_amity():
            offices_with_space_list, living_spaces_with_space_list = \
                self.amity_object.fetch_rooms_with_space()
            if offices_with_space_list:
                for room in offices_with_space_list:
                    if room[1] > 0:
                        Amity.rooms_list[1][room[0]].append(self.person_id)
                        room[1] -= 1
                        break

        return self.person_id, name + " was added successfully"
