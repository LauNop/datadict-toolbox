import re
import json


class SQLDeduce:
    def __init__(self, query):
        self.query = query
        print(self.is_correct())
        # self.query_split()
        print(self.query_type())
        self.clean()
        print(self.query)

        self.__keywords = self.keyword_table()
        self.__kw_pos_in_query = self.keywords_pos()
        self.__kw_count_in_query = self.keywords_count()
        self.__kw_in_query = self.keywords_used()
        self.__is_got_subqueries = self.is_got_subqueries()
        self.__all_tables = self.table_statement()
        self.inner_alias = None

    # Getters
    def get_kw_pos(self):
        return self.__kw_pos_in_query

    def get_kw_count(self):
        return self.__kw_count_in_query

    def get_kw_query(self):
        return self.__kw_in_query

    def get_is_got_subqueries(self):
        return self.__is_got_subqueries

    def get_all_tables(self):
        return self.__all_tables

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

    def keyword_without_as(self):
        keywords_without_as = self.__keywords.copy()
        keywords_without_as.pop(keywords_without_as.index('AS'))
        return keywords_without_as

    def keywords_pos(self, string_to_match=None):
        matches_list = self.__keywords.copy()
        if string_to_match is None:
            string_to_match = self.query
        search_pattern = "|".join(matches_list)
        search_pattern = r'\b(' + search_pattern + r')\b'
        kw_pos_in_query = []
        match_iterator = re.finditer(search_pattern, string_to_match, re.IGNORECASE)
        for match in match_iterator:
            kw_pos_in_query.append((match.group(), match.span()))
        return kw_pos_in_query

    def found_parse(self):
        parse_list = []
        search_pattern = r'(\(|\))'
        match_iterator = re.finditer(search_pattern, self.query)
        for match in match_iterator:
            parse_list.append((match.group(), match.span()))
        return parse_list

    def keyword_parse_pos(self):
        through_list = self.__kw_pos_in_query.copy()
        output_list = through_list.copy()
        parse_list = self.found_parse()
        for element in parse_list:
            _, span = element
            start_p, _ = span
            for i in range(len(through_list)):
                _, key_span = through_list[i]
                start_k,_ = key_span
                if start_k > start_p:
                    through_list.insert(i, element)
                    break

        return through_list

    def keywords_count(self, string_to_match=None):
        if string_to_match is None:
            string_to_match = self.__kw_pos_in_query
        kw_dict = {key: [0, []] for key in self.__keywords}
        for kw_element in string_to_match:
            keyword, span = kw_element
            for pattern in self.__keywords:
                if re.fullmatch(pattern, keyword, re.IGNORECASE):
                    kw_dict[pattern][0] += 1
                    kw_dict[pattern][1].append(span)
        kw_dict = {key: value for key, value in kw_dict.items() if value[0] > 0}
        return kw_dict

    def keywords_used(self, dict_to_filter=None):
        if dict_to_filter is None:
            dict_to_filter = self.__kw_count_in_query
        keywords_in_query = [key for key, value in dict_to_filter.items()]
        return keywords_in_query

    def nest_keyword(self):
        kw_parse_pos = self.keyword_parse_pos()
        key = 'Nested'
        kw_with_nest_pos = []
        is_nested = False
        nest_dict = {}
        for i in range(len(kw_parse_pos)):
            string, span = kw_parse_pos[i]
            if re.match(r'\(',string) and not is_nested:
                is_nested = True
                nest_dict = {key: []}
            elif re.match(r'\)',string):
                kw_with_nest_pos.append(nest_dict)
                is_nested = False
                nest_dict = {}
            elif is_nested:
                nest_dict[key].append(kw_parse_pos[i])
            else:
                kw_with_nest_pos.append(kw_parse_pos[i])
        return kw_with_nest_pos

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

    def check_after_split(self, string_list):
        parentheses_list = []
        all_fusion = []
        element_to_fuse = []
        new_string_list = []
        last_index_reach = 0
        for i in range(len(string_list)):
            string_element = string_list[i]
            for character in string_element:
                if character == '(':
                    parentheses_list.append(character)
                if character == ')':
                    parentheses_list.pop()
            if parentheses_list:
                element_to_fuse.append(i)
            elif not parentheses_list and element_to_fuse:
                element_to_fuse.append(i)
                if len(element_to_fuse) == 1:
                    element_to_fuse.append(i + 1)
                all_fusion.append(element_to_fuse)
                element_to_fuse = []
            else:
                continue
        if all_fusion:
            for fusion in all_fusion:
                start = fusion[0]
                end = fusion[-1]
                if not last_index_reach:
                    new_string_list = string_list[:start]
                else:
                    new_string_list += string_list[last_index_reach + 1:start]
                new_element = ', '.join(string_list[start:end])
                new_string_list.append(new_element)
                last_index_reach = end
            if not last_index_reach == len(string_list) - 1:
                new_string_list += string_list[last_index_reach + 1:]
        else:
            new_string_list = string_list
        return new_string_list

    def split_column_expression(self):
        split_col_exp_dict = {}
        split_pattern = r',\s*(?![^()]*\))'
        # split_pattern = r',\s*'
        elements_to_change = self.between_select_from()
        for i in range(len(elements_to_change)):
            elements = re.split(split_pattern, elements_to_change[i])
            elements = [elem.strip() for elem in elements]
            elements = self.check_after_split(elements)
            split_col_exp_dict[i] = elements
        return split_col_exp_dict

    def analyse_column_expression(self):
        dict_to_analyse = {}
        for key, value in self.split_column_expression().items():
            dict_to_analyse[key] = []
            for element in value:
                keys_by_element = self.keywords_pos(element)
                keys_by_element = self.keywords_count(keys_by_element)
                tab = [element, keys_by_element]
                dict_to_analyse[key].append(tab)
        return dict_to_analyse

    def define_for_column_expression(self, column_expression, keys_of_ce):
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

    def deduce_subqueries_relation(self):
        '''
        Hello there I'm Mario and I'm Luigi,... WE ARE THE CREEPING SAME PEOPLE, MOUAAAAAAAAAHHHHHHHHHHHHHHHHHHH ah AH
        MAKE RELATION WITH FROM SELECT JOIN
        SELECT-0 FROM SELECT-1
        '''

        return

    def is_got_subqueries(self):
        if len(self.between_select_from()) > 1:
            return True
        else:
            return False

    def table_statement(self):
        length = len(self.__kw_pos_in_query)
        table_statement_list = []
        for i in range(length):
            kw_element = self.__kw_pos_in_query[i]
            keyword, span = kw_element
            if re.fullmatch('FROM', keyword, re.IGNORECASE):
                start_a, end_a = span
                if i != length - 1:
                    i_temp = i + 1
                    kw_temp, span_temp = self.__kw_pos_in_query[i_temp]
                    while ((re.fullmatch('AS', kw_temp, re.IGNORECASE)
                           or re.fullmatch('SELECT', kw_temp,re.IGNORECASE)
                           or re.fullmatch('FROM', kw_temp, re.IGNORECASE))
                           and i_temp != length - 1):
                        i_temp += 1
                        kw_temp, span_temp = self.__kw_pos_in_query[i_temp]
                    start_b, end_b = span_temp
                    statement = self.query[end_a:start_b].strip()
                    table_statement_list.append(statement)
                else:
                    statement = self.query[end_a:].strip()
                    table_statement_list.append(statement)
        return table_statement_list

    def is_table_name(self,table_statement):
        keywords_without_as = self.keyword_without_as()
        search_pattern = "|".join(keywords_without_as)
        search_pattern = r'\b(' + search_pattern + r')\b'
        if re.search(search_pattern, table_statement,re.IGNORECASE):
            return False
        return True

    def table_alias(self, table_statement):
        if self.is_table_name(table_statement):
            statement_to_analyse = re.split(r'\s+',table_statement)
            print(statement_to_analyse)

        return

    def analyse_tables(self):
        for statement in self.__all_tables:
            self.table_alias(statement)
        return

if __name__ == "__main__":
    print("Yes I try to extract info from select sql query")
