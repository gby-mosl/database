from database import insertInDatabase,searchInDatabase

# TODO: Gestion des erreurs


class Company:
    def __init__(self, name: str, address: str, post_code: str, city: str, id: int = None):
        self.id: int = id or None
        self.name: str = name
        self.address: str = address
        self.post_code: str = post_code
        self.city: str = city

    def __str__(self):
        return f"{'-'*50}\nid: {self.id}\n{self.name}\n{self.address}\n{self.post_code} {self.city}\n{'-'*50}"

    def save(self) -> bool:
        request = "INSERT INTO companies (name, address, post_code, city) VALUES (%s, %s, %s, %s)"
        params = (self.name, self.address, self.post_code, self.city)
        insertInDatabase(request=request, params=params)
        return True


def getCompanies(column: str = None, searched_element: str | int = None) -> list[Company]:
    companies = []
    for elt in searchInDatabase(table="companies", column=column, searched_element=searched_element):
        company = Company(id=elt[0], name=elt[1], address=elt[2], post_code=elt[3], city=elt[4])
        companies.append(company)
    return companies


if __name__ == '__main__':
    for elt in getCompanies():
        print(elt)


