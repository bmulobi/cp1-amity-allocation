from amity_app.classes.person import Person


class Fellow(Person):
    """
    inherits from Person
    """

    def __init__(self, role="FELLOW", accommodation="N"):
        self.name = ""
        self.person_role = role
        self.accommodation = accommodation

    def add_person(self, name):
        return person_id, name + " was added successfully"
