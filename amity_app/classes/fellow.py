from amity_app.classes.person import Person


class Fellow(Person):
    """
    inherits from Person
    """

    def __init__(self, name, role, accommodation="N"):
        self.name = name
        self.person_role = role
        self.accommodation = accommodation

    def add_person(self):
        return "add_person() was called successfully from class Fellow"
