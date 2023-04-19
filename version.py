from datetime import datetime

from plan import getPlansByProjectNumber, getPlanById, Plan
from database import searchInDatabase
from people import getPersonByParam


class Version:
    def __init__(self, version: str, plan_id: int, creation_date: datetime.date, modification: str, technician_id: int,
                 status: str, id: int = None):
        self.version: str = version
        self.plan_id: int = plan_id
        self.creation_date: datetime.date = creation_date
        self.modification: str = modification
        self.technician_id: int = technician_id
        self.status: str = status
        self.id: int = id or None

    def __str__(self):
        plan = getPlanById(self.plan_id)
        technician = getPersonByParam("id", self.technician_id)[0]
        return f"Plan n°{plan.plan_number} {plan.title} - Indice {self.version} du {self.creation_date} par {technician.lastname} -> {self.modification}."


def getVersionByProject(project_number: str) -> list[Version]:
    versions = []
    for plan in getPlansByProjectNumber(project_number):
        for elt in getVersionByPlan(plan):
            version = Version(elt[0], elt[1], elt[2], elt[3], elt[4], elt[5], elt[6])
            versions.append(version)
    return versions



def getVersionByPlan(plan: Plan) -> list[Version]:
    return searchInDatabase("versions", "plan_id", plan.id)


if __name__ == '__main__':
    for v in getVersionByProject('P.678910.D.12'):
        print(v)
