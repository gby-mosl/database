from database import insertInDatabase, searchInDatabase
from settings import getConfig


JOBS_LIST = getConfig("jobs")

# TODO: Gestion des erreurs


class People:
    def __init__(self, lastname: str, firstname: str, company_id: int, job: str = None, status: bool = True, id: int = None ):
        self.id: int = id or None
        self.lastname: str = lastname
        self.firstname: str = firstname
        self.company_id: int = company_id
        self.job: str = job
        self.status: bool = status
        self.company = searchInDatabase("companies", "id", self.company_id)[0][1]

    def __str__(self):
        return (
            f"id : {self.id}\n{self.lastname} {self.firstname}\n{self.company} | {self.job}\nActif: {'Oui' if self.status else 'Non'}\n{'-'*50}"
            if self.job
            else f"id : {self.id}\n{self.lastname} {self.firstname}\n{self.company}\nActif: {'Oui' if self.status else 'Non'}\n{'-'*50}"
        )

    def save(self) -> bool:
        if self.job:
            request = "INSERT INTO people (lastname, firstname, company_id, job) VALUES (%s, %s, %s, %s)"
            params = (self.lastname, self.firstname, self.company_id, self.job)
        else:
            request = "INSERT INTO people (lastname, firstname, company_id) VALUES (%s, %s, %s)"
            params = (self.lastname, self.firstname, self.company_id)
        insertInDatabase(request=request, params=params)
        return True

    def change_status(self):
        pass


class Staff(People):
    def __init__(self, lastname, firstname, job, company_id=1, status=True, id= None):
        super().__init__(lastname, firstname, company_id, job,  status, id)
        self.job: str = job


def getPersonByParam(column: str, searched_element: str | int) -> list[People | Staff]:
    people = []
    for elt in searchInDatabase(table="people", column=column, searched_element=searched_element):
        if elt[3] == 1:
            person = Staff(id=elt[0], lastname=elt[1], firstname=elt[2], job=elt[4], status=elt[5])
        else:
            person = People(id=elt[0], lastname=elt[1], firstname=elt[2], company_id=elt[3], job=elt[4], status=elt[5])
        people.append(person)
    return people


def getAllTechnicians() -> list[Staff]:
    technicians = []
    for t in searchInDatabase("technicians_vw"):
        technician = Staff(id=t[0], lastname=t[1], firstname=t[2], company_id=t[3], job=t[4], status=t[5])
        technicians.append(technician)
    return technicians
