import os
from sql_metadata import Parser

import envVar as V

if __name__=="__main__":
    from ExtractFromDTSX import extract_erp_query

    folder_path = V.DTSX_FOLDER
    file_names = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    print("Nbr fichier: ",len(file_names))
    print(V.DASH_LINE)

    queries = extract_erp_query(file_names)["SQL_QUERY"]

    for query in queries[:3]:
    
        print("SQL QUERY:\n",query)
        print(V.DASH_LINE)

        parser = Parser(query)

        print("COLUMNS:\n",parser.columns)
        print(V.DASH_LINE)
        print("COLUMNS_DICT:\n",parser.columns_dict)
        print(V.DASH_LINE)
        print("ALIASES:\n",parser.columns_aliases)
        print(V.DASH_LINE)
        print("TABLE:\n",parser.tables)
        print(V.DASH_LINE)
        print("SUB-QUERIES:\n",parser.subqueries)
        print(V.DASH_LINE)
