from amity_app.classes.person import Person

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

    def add_person(self, name):
        return self.person_id, name + " was added successfully"
