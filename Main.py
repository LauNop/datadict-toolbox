import os
import Extract

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
    {{"COLUMN_NAME":["","","","","",""],"NOM_EXPLICIT":["","","","","",""],"DATA_TYPE":["","","","","",""],"TABLE_NAME_CUBE":["","","","","",""],"CUBE_NAME":["","","","","",""],"CATALOG_NAME":["","","","","",""],"VIEW_NAME":["","","","","",""],"TABLE_NAME_INFOCENTRE":["","","","","",""],"DATABASE_NAME_INFOCENTRE":["","","","","",""],"SERVEUR_INFOCENTRE":["","","","","",""],"MAPPING":["Magasin","CodeActionCo1","CodeActionCo","LibelleActionCo","DateDebut","DateFin"],"COLUMN_NAME_ERP":["1","cast(ACO_tyori||ACO_cdac||ACO_AAAC as nvarchar2(20))","case when ACO_AAAC='18' or ACO_AAAC='mb'  then cast(regexp_replace(cast(ACO_tyori||ACO_cdac||ACO_AAAC as nvarchar2(20)), '[abcdefghijklmnopqrstuvwxyz]', '*') as nvarchar2(20)) else cast(ACO_tyori||ACO_cdac||ACO_AAAC as nvarchar2(20)) end","cast(ACO_LBACCOM as nvarchar2(50))","ACO_DTDEBUT","ACO_DTFIN"],"TABLE_NAME_ERP":["MGACO","MGACO","MGACO","MGACO","MGACO","MGACO"],"DATABASE_NAME_ERP":["SADECO","SADECO","SADECO","SADECO","SADECO","SADECO"],"ERP_NAME":["","","","","",""],"EXPRESSION":["","","","","",""],"DEFINITION":["","","","","",""],"LIAISON":["","","","","",""]}}
    """
    print(string[900:1010])
