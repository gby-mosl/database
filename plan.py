from datetime import datetime

from database import insertInDatabase, searchInDatabase
from settings import getConfig


STATUS = getConfig("plans_status")


class Plan:
    def __init__(self, number: str, project_number: str, name: str, version: str, creation_date: datetime.date,
                 technician_id: int,
                 status: str = None):
        self.number: str = number
        self.project_number: str = project_number
        self.name: str = name
        self.version: str = version
        self.creation_date: datetime.date = creation_date
        self.technician_id: int = technician_id
        self.status: str = status

    def save(self) -> bool:
        request = "INSERT INTO plans (number, project_number, version, creation_date, name, technician_id) VALUES (%s, %s, %s, %s, %s, %s)"
        params = (self.number, self.project_number, self.version, self.creation_date, self.name, self.technician_id)
        insertInDatabase(request=request, params=params)
        return True

    def change_status(self):
        pass


if __name__ == '__main__':
    pass
