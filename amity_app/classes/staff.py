from amity_app.classes.person import Person


class Staff(Person):
    """
    Defines the attributes of a person who is a staff
    """

    def __init__(self, name):

        self.name = name.upper()
        self.person_role = "STAFF"
        self.person_id = ""
        self.has_office = False
