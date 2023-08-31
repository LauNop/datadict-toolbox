import re
import json


class SQLDeduce:
    def __init__(self, query):
        self.query = query
        print(self.is_correct())
        # self.query_split()
        print(self.query_type())
        self.clean()

        self.__keywords = self.keyword_table()
        self.__kw_pos_in_query = self.keywords_pos()
        self.__kw_count_in_query = self.keywords_count()
        self.__kw_in_query = self.keywords_used()

    # Getters
    def get_kw_pos(self):
        return self.__kw_pos_in_query

    def get_kw_count(self):
        return self.__kw_count_in_query

    def get_kw_query(self):
        return self.__kw_in_query

    # Methods
    def clean(self):
        self.query = re.sub('\r?\n', ' ', self.query)
        return

    def is_correct(self):
        if len(re.findall(r"(?i)select", self.query)) == len(re.findall(r"(?i)from", self.query)):
            return True
        else:
            print("select nbr: ", re.findall(r"(?i)select", self.query))
            print("from nbr: ", re.findall(r"(?i)from", self.query))
        return False

    def query_split(self):
        queries = self.query.split(';')
        return len(queries), queries

    def query_type(self):
        if re.match(r"(?i)select", self.query):
            return "SELECT QUERY"
        return

    def keyword_table(self):
        with open('datadict_toolbox/usefull.json', 'r') as file:
            json_content = file.read()
            usefull_dict = json.loads(json_content)
        file.close()
        return usefull_dict["Keywords"]

    def keywords_pos(self,string_to_match = None):
        if string_to_match is None:
            string_to_match = self.query
        search_pattern = "|".join(self.__keywords)
        search_pattern = r'\b('+search_pattern+r')\b'
        kw_pos_in_query = []
        match_iterator = re.finditer(search_pattern, string_to_match, re.IGNORECASE)
        for match in match_iterator:
            kw_pos_in_query.append((match.group(), match.span()))
        return kw_pos_in_query

    def keywords_count(self,string_to_match = None):
        if string_to_match is None:
            string_to_match = self.__kw_pos_in_query
        kw_dict = {key: [0,[]] for key in self.__keywords}
        for kw_element in string_to_match:
            keyword, span = kw_element
            for pattern in self.__keywords:
                if re.fullmatch(pattern,keyword,re.IGNORECASE):
                    kw_dict[pattern][0] += 1
                    kw_dict[pattern][1].append(span)
        kw_dict = {key: value for key, value in kw_dict.items() if value[0] > 0}
        return kw_dict

    def keywords_used(self, dict_to_filter = None):
        if dict_to_filter is None:
            dict_to_filter = self.__kw_count_in_query
        keywords_in_query = [key for key, value in dict_to_filter.items()]
        return keywords_in_query

    def between_2_keywords(self, keyword_before, keyword_after):
        b_s_f_list = []
        boundary_a = self.__kw_count_in_query[keyword_before][1]
        boundary_b = self.__kw_count_in_query[keyword_after][1]
        if len(boundary_a) == len(boundary_b):
            for i in range(len(boundary_a)):
                start_a, end_a = boundary_a[i]
                start_b, end_b = boundary_b[i]
                between_result = self.query[end_a:start_b]
                b_s_f_list.append(between_result)
        else:
            print("Length Problem")
        return b_s_f_list

    def between_select_from(self):
        return self.between_2_keywords("SELECT", "FROM")

    def split_column_expression(self):
        split_col_exp_dict = {}
        split_pattern = r',\s*(?![^()]*\))'
        elements_to_change = self.between_select_from()
        for i in range(len(elements_to_change)):
            elements = re.split(split_pattern,elements_to_change[i])
            elements = [elem.strip() for elem in elements]
            split_col_exp_dict[i] = elements
        return split_col_exp_dict

    def analyse_column_expression(self):
        dict_to_analyse = {}
        for key, value in self.split_column_expression().items():
            dict_to_analyse[key] = []
            for element in value:
                keys_by_element = self.keywords_pos(element)
                keys_by_element = self.keywords_count(keys_by_element)
                tab = [element,keys_by_element]
                dict_to_analyse[key].append(tab)
        return dict_to_analyse

    def define_for_column_expression(self,column_expression,keys_of_ce):
        if not keys_of_ce:
            return {'Column': column_expression}
        elif keys_of_ce.get('AS', None):
            as_start, as_end = keys_of_ce['AS'][1][-1]
            statement = column_expression[:as_start].strip()
            alias = column_expression[as_end:].strip()
            return {'Column': statement, 'Alias': alias}
        else:
            print('key word Not handle')

    def deduce_column_expression(self):
        deduce_dict = self.analyse_column_expression()
        analysed_dict = {}
        for select_key, select_value in deduce_dict.items():
            analysed_dict[select_key] = []
            for element in select_value:
                column_expression = element[0]
                keys_of_ce = element[1]
                analysed_dict[select_key].append(self.define_for_column_expression(column_expression, keys_of_ce))
        return analysed_dict


if __name__ == "__main__":
    print("Yes I try to extract info from select sql query")
