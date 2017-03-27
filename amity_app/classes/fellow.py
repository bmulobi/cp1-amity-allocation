from amity_app.classes.person import Person
from amity_app.classes.amity import Amity


class Fellow(Person):
    """
    inherits from Person
    """

    def __init__(self, role="FELLOW", accommodation="N"):
        self.name = ""
        self.person_role = role
        self.accommodation = accommodation
        self.person_id = ""

    def add_person(self, name, wants_accomodation):
        Amity.person_identifier += 1
        self.person_id = "f" + str(Amity.person_identifier)
        self.name = name
        return self.person_id, self.name + " was added successfully"
