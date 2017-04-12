from abc import ABCMeta


class Person(metaclass=ABCMeta):
    """
    Base class for Staff and Fellow
    defines common attributes of a person
    """

    def __init__(self):

        self.name = ""
        self.person_role = ""
        self.person_id = ""
        self.has_office = 0

