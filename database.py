import json

import mysql.connector

from settings import getConfig

# TODO: Gestion des erreurs


def insertInDatabase(request: str, params: tuple) -> bool:
    with mysql.connector.connect(**getConfig("db_params")) as db:
        with db.cursor() as c:
            c.execute(request, params)
        db.commit()
    return True


def searchInDatabase(table: str, column: str = None, searched_element: str | int = None) -> list[tuple]:
    if searched_element and column:
        if isinstance(searched_element, int):
            request = f"SELECT * FROM {table} WHERE {column} = {searched_element}"
        else:
            request = f"SELECT * FROM {table} WHERE {column} = '{searched_element}'"
    else:
        request = f"SELECT * FROM {table}"
    with mysql.connector.connect(**getConfig("db_params")) as db:
        with db.cursor() as c:
            c.execute(request)
            result = c.fetchall()
    return result
