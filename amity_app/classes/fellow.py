from amity_app.classes.person import Person
from amity_app.classes.amity import Amity


class Fellow(Person):
    """
    inherits from Person
    """

    def __init__(self, role="FELLOW"):
        self.name = ""
        self.person_role = role
        self.accommodation = "N"
        self.person_id = ""
        self.amity_object = Amity()

    def add_person(self, name, wants_accommodation="N"):
        """

        :param name:
        :param wants_accommodation:
        :return:
        """
        self.accommodation = wants_accommodation
        Amity.person_identifier += 1

        self.person_id = "f-" + str(Amity.person_identifier)
        self.name = name
        Amity.people_list[0][self.person_id] = self.name

        if self.amity_object.confirm_availability_of_space_in_amity():
            offices_with_space_list, living_spaces_with_space_list = \
                self.amity_object.fetch_rooms_with_space()
            if offices_with_space_list:
                for room in offices_with_space_list:
                    if room[1] > 0:
                        Amity.rooms_list[1][room[0]].append(self.person_id)
                        room[1] -= 1
                        break

            if self.accommodation == "Y":

                if living_spaces_with_space_list:
                    for room in living_spaces_with_space_list:
                        if room[1] > 0:
                            Amity.rooms_list[0][room[0]].append(self.person_id)
                            room[1] -= 1
                            break

        return self.person_id, self.name + " was added successfully"
