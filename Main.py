import os

"""
with open(".env", "r") as f:
    for line in f.readlines():
        try:
            key, value = line.split('=')
            os.putenv(key, value)
        except ValueError:
            # syntax error
            pass
"""

if __name__ == "__main__":
    print("Hello World")
    string = """
{"COLUMN_NAME":["","","","","",""],"NOM_EXPLICIT":["","","","","",""],"DATA_TYPE":["","","","","",""],"TABLE_NAME_CUBE":["","","","","",""],"CUBE_NAME":["","","","","",""],"CATALOG_NAME":["","","","","",""],"VIEW_NAME":["","","","","",""],"TABLE_NAME_INFOCENTRE":["","","","","",""],"DATABASE_NAME_INFOCENTRE":["","","","","",""],"SERVEUR_INFOCENTRE":["","","","","",""],"COLUMN_NAME_ERP":["1","ACO_tyori","ACO_cdac","ACO_AAAC","ACO_LBACCOM","ACO_DTDEBUT","ACO_DTFIN"],"TABLE_NAME_ERP":["MGACO","MGACO","MGACO",,"MGACO","MGACO"],"DATABASE_NAME_ERP":["SADECO","SADECO","SADECO","SADECO","SADECO","SADECO","SADECO"],,"ERP_NAME":["","","","","",""],"EXPRESSION":["","","","","",""],"DEFINITION":["","","","","",""],"LIAISON":["","","","","",""],"MAPPING":["Magasin","CodeActionCo1","CodeActionCo","LibelleActionCo","DateDebut","DateFin"]}    """
    print(string[500:520])


