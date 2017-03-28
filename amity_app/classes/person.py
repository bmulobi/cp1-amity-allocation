from abc import ABCMeta, abstractmethod


class Person(metaclass=ABCMeta):
    """
    Base class for
    """

    # __metaclass__ = ABCMeta

    person_identifier = 0

    def __init__(self):
        self.name = ""
        self.person_role = ""
        self.person_id = ""

    @abstractmethod
    def add_person(self, name, wants_accommodation="N"):
        pass
