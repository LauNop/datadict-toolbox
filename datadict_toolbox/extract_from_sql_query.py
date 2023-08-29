import os
import re
import json

import envVar as V

class SQLDeduce:
    def __init__(self,query):
        self.query = query
        #is_correct select query
        print(self.is_correct())

    def clean(self,string):
        string = re.sub('\r?\n',' ',string)
        return string

    def is_correct(self):
        if len(re.findall(r"(?i)select",self.query)) == len(re.findall(r"(?i)from",self.query)):
            return True
        else:
            print("select nbr: ",re.findall(r"(?i)select",self.query))
            print("from nbr: ",re.findall(r"(?i)from",self.query))
        return False

    def query_split(self):
        queries = self.query.split(';')
        return len(queries), queries

    def query_type(self):
        if re.match(r"(?i)select",self.query):
            return "SELECT QUERY"
        return
    
    def get_select2from(self):
        between_select_from_list = []
        pattern = r"(?i)select\s+(.*?)\s+from"
        match_iterator =  re.finditer(pattern_test,query,re.DOTALL)
        for match in match_iterator:
            string = match.group()
            start = re.match(r'(?i)select',string).end()
            end = re.search(r'(?i)from',string).start()
            string = self.clean(string[start:end])
            between_select_from_list.append(string)
        return between_select_from_list

    def get_colex(self,test_string):
        pattern = r',\s*(?![^()]*\))'
        colex_list = re.split(pattern,test_string)
        return colex_list

    def get_alias(self,input_str):
        last_as_index = input_str.rfind(" as ")
        colex = input_str[:last_as_index].strip()
        alias = input_str[last_as_index + 4:].strip()
        return alias, colex
            

if __name__=="__main__":
    from ExtractFromDTSX import extract_erp_query

    folder_path = V.DTSX_FOLDER
    file_names = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    print("Nbr fichier: ",len(file_names))
    print(V.DASH_LINE)

    queries = extract_erp_query(file_names)["SQL_QUERY"]

    pattern_test = r"(?i)select\s+(.*?)\s+from"

    for query in queries[:2]:
    
        print("SQL QUERY:\n",query)
        print(V.DASH_LINE)

        #test_iterator = re.finditer(pattern_test,query,re.DOTALL)
        #for match in test_iterator :
        #    print(match.span())
        #    print(type(match.group()),match.group())
        #    print(V.DASH_LINE)

        deduce = SQLDeduce(query)
        test = deduce.get_select2from()
        print("Nbr:\n",len(test))
        print(test)
        print(V.DASH_LINE)
        for string in test:
            colex_list = deduce.get_colex(string)
            print(len(colex_list))
            for colex in colex_list:
                print(colex)
                print(deduce.get_alias(colex))
            print(V.DASH_LINE)

