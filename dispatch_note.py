from datetime import datetime

from database import insertInDatabase, searchInDatabase, updateInDataBase
from version import Version


class DispatchNote:
    def __init__(self, project_number: str, sender: int, recipient: int, sending_date: datetime.date, sending_status: str, id: int = None, dispatch_number: str = None,  plans_list: list[Version] = None):
        if plans_list is None:
            plans_list = []
        self.plans_list: list[Version] = plans_list
        self.dispatch_number: str = dispatch_number or None
        self.project_number: str = project_number
        self.sender: int = sender
        self.recipient: int = recipient
        self.sending_date: datetime.date = sending_date
        self.sending_status: str = sending_status
        self.id: int = id or None

    def addPlan(self, plan: Version) -> bool:
        self.plans_list.append(plan)
        return True

    def save(self):
        provisional_number = "__prov__"
        request = "INSERT INTO dispatch_notes (dispatch_number, project_number, sender, recipient, sending_date, sending_status) VALUES (%s, %s, %s, %s, %s, %s)"
        params = (provisional_number, self.project_number, self.sender, self.recipient, self.sending_date, self.sending_status)
        insertInDatabase(request=request, params=params)
        created_id = searchInDatabase("dispatch_notes", "dispatch_number", "__prov__")[0][0]
        self.id = created_id
        self.dispatch_number = f"{str(created_id).zfill(4)}-BE/OMX_NCY"
        updateInDataBase("dispatch_notes", "dispatch_number", self.dispatch_number, "dispatch_number", "'__prov__'")
        return True



if __name__ == '__main__':
    pass