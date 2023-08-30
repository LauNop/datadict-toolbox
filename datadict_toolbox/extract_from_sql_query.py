import re
import json

class SQLDeduce:
    def __init__(self,query):
        self.query = query
        print(self.is_correct())
        # self.query_split()
        print(self.query_type())
        self.keyword = self.keyword_table()
        print('keyword: ',self.keyword)


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

    def keyword_table(self):
        with open('datadict_toolbox/sql_keywords.json', 'r') as file:
            json_content = file.read()
            keywords_dict = json.loads(json_content)
        file.close()
        return keywords_dict
    def get_alias(self, input_str):
        last_as_index = input_str.rfind(" as ")
        colex = input_str[:last_as_index].strip()
        alias = input_str[last_as_index + 4:].strip()
        return alias, colex
            

if __name__=="__main__":
    print("Yes I try to extract info from select sql query")
