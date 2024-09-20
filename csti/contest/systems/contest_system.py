from enum import Enum

from csti.contest.systems.ejudje import EjudjeAPI


class ContestSystem(Enum):
    """ Перечисление доступных систем. """

    ejudje = {
        "fullName": "Ejudje",
        "api": EjudjeAPI,
    }

    @property
    def fullName(self):
        return self.value["fullName"]
    
    @property
    def api(self):
        return self.value["api"]
