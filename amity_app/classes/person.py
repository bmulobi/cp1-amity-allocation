from abc import ABCMeta, abstractmethod


class Person(metaclass=ABCMeta):
    """
    Base class for
    """

    # __metaclass__ = ABCMeta

    person_identifier = 0

    def __init__(self, name, role, accommodation="N"):
        self.name = name
        self.person_role = role
        self.accommodation = accommodation

    @abstractmethod
    def add_person(self):
        pass



