from amity_app.classes.person import Person


class Fellow(Person):
    """
    Defines the attributes of a person who is a fellow
    """

    def __init__(self, name):

        self.name = name.upper()
        self.person_role = "FELLOW"
        self.accommodation = "N"
        self.person_id = ""
        self.has_office = False
        self.has_accommodation = False

