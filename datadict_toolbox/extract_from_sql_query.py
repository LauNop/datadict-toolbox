import os
import re
import json

import envVar as V

class SQLDeduce:
    def __init__(self,query):
        self.query = query
        self.clean()

    def clean(self):
        self.query = re.sub('\r?\n',' ',self.query)
        return

    def query_split(self):
        queries = self.query.split(';')
        return len(queries), queries

    def query_type(self):
        if re.match(r"(?i)select",self.query):
            return "SELECT QUERY"
        return
    
    def get_select_statement(self):
        pattern = r"(?i)select\s(.*?)\s+from"
        statements = re.findall(pattern,self.query,re.DOTALL)
        return len(statements), statements

    def get_from_statement(self):
        pattern = r"(?i)FROM\s+(\w+)(?:\s+WHERE|\s+JOIN|\s+INNER|\s+LEFT|\s+RIGHT|\s+OUTER|$)"
        statements = re.findall(pattern, self.query, re.IGNORECASE)
        return len(statements), statements

if __name__=="__main__":
    from ExtractFromDTSX import extract_erp_query

    folder_path = V.DTSX_FOLDER
    file_names = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    print("Nbr fichier: ",len(file_names))
    print(V.DASH_LINE)

    queries = extract_erp_query(file_names)["SQL_QUERY"]

    for query in queries[:4]:
    
        print("SQL QUERY:\n",query)
        print(V.DASH_LINE)

        deduce = SQLDeduce(query)
        print(deduce.query_split())
        print(V.DASH_LINE)
        deduce.query_type()
        print(V.DASH_LINE)
        print(deduce.get_select_statement())
        print(V.DASH_LINE)
        print(deduce.get_from_statement())
        print(V.DASH_LINE)

