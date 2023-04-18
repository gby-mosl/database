from datetime import datetime

from database import insertInDatabase, searchInDatabase
from settings import getConfig

STATUS = getConfig("plans_status")


class Plan:
    def __init__(self, project_number: str, plan_number: str, title: str, id: int = None):
        self.project_number: str = project_number
        self.plan_number: str = plan_number
        self.title: str = title
        self.id: int = id or None

    def __str__(self):
        return f"{self.project_number} - {self.plan_number} - {self.title} (id: {self.id})"

    def save(self) -> bool:
        request = "INSERT INTO plans (project_number, plan_number, title) VALUES (%s, %s, %s)"
        params = (self.project_number, self.plan_number, self.title)
        insertInDatabase(request=request, params=params)
        return True

    def addVersion(self, version: str, creation_date: datetime.date, modification: str, technician_id: int,
                      status: str = None):
        request = "INSERT INTO version (version, plan_id, creation_date, modification, technician_id, status) VALUES (%s, %s, %s, %s, %s, %s)"
        params = (version, self.id, creation_date, modification, technician_id, status)
        insertInDatabase(request=request, params=params)
        return True

    def change_status(self):
        pass


def getPlansByProjectNumber(project_number: str) -> list[Plan]:
    plans = []
    for elt in searchInDatabase("plans", "project_number", project_number):
        plan = Plan(project_number=project_number, plan_number=elt[1], title=elt[2], id=elt[3])
        plans.append(plan)
    return plans


def getPlanById(id: int) -> Plan:
    p = searchInDatabase("plans", "id", id)[0]
    return Plan(project_number=p[0], plan_number=p[1], title=p[2], id=id)
