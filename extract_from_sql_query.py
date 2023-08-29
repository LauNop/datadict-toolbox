import os
import re

import envVar as V

class SQLDeduce:
    def __init__(self,query):
        self.query = query

    def query_sep(self):
        queries = self.query.split(';')
        return len(queries), queries

    def query_type(self):
        if re.match(r"(?i)^select",self.query):
            print("It's a select query")
            return "SELECT"
        return
    

    def get_keywords(self):
        
        return

    def get_select_statement(self):
        pattern = r"(?i)select\s(.*?)\s+from"
        re.search(pattern,self.query,re.DOTALL)
        
        return

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

        deduce = SQLDeduce(query)
        deduce.query_sep()
        print(V.DASH_LINE)
        deduce.query_type()
        print(V.DASH_LINE)
        deduce.get_select_statement()
        print(V.DASH_LINE)
