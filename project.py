from datetime import datetime
from dateutil.relativedelta import relativedelta

from database import searchInDatabase, insertInDatabase

from settings import getConfig

ARCHIVING_TIME = getConfig("archiving_time")

# TODO: Gestion des erreurs


class Project:
    def __init__(self, number: str, ranking: str, name: str, archive_number: str = None,
                 archive_date: datetime.date = None):
        self.number: str = number
        self.ranking: str = ranking
        self.name: str = name
        self.archive_number: str = archive_number or None
        self.archive_date: datetime.date = archive_date or None

    def __str__(self):
        if self.archive_number:
            self.archive_txt = f" *** Archive N° {self.archive_number} (fin d'archivage: {self.archive_date + relativedelta(years=ARCHIVING_TIME)}) ***"
        return f"{self.ranking} - {self.number} - {self.name}{self.archive_txt if self.archive_number else ''}"

    def save(self) -> bool:
        request = "INSERT INTO projects (number, ranking, name) VALUES (%s, %s, %s)"
        params = (self.number, self.ranking, self.name)
        insertInDatabase(request=request, params=params)
        return True

    def archive(self):
        pass


def getProjects(project_type: str = None) -> list[Project]:
    projects = []
    table = ""
    if project_type is None:
        table = "projects"
    elif project_type == "Current":
        table = "current_projects_vw"
    elif project_type == "Archive":
        table = "archives_vw"

    for elt in searchInDatabase(table):
        project = Project(number=elt[0], ranking=elt[1], name=elt[2], archive_number=elt[3], archive_date=elt[4])
        projects.append(project)
    return projects


if __name__ == '__main__':
    for p in getProjects():
        print(p)
