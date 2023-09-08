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
        self.__is_got_subqueries = self.is_got_subqueries()
        self.__all_tables = self.table_statement()
        self.relation_list = []
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

    # Usefull
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

    # Usefull
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

    # Usefull
    def found_parse(self):
        parse_list = []
        search_pattern = r'(\(|\))'
        match_iterator = re.finditer(search_pattern, self.query)
        for match in match_iterator:
            parse_list.append((match.group(), match.span()))
        return parse_list

    def useless_parse_pop(self, kw_parse_list):
        i = 0
        for i in range(1, len(kw_parse_list)):
            previous = kw_parse_list[i - 1]
            str_previous, span_previous = previous
            str_, span = kw_parse_list[i]
            if re.match(r'\(', str_previous) and re.match(r'\)', str_):
                del kw_parse_list[i - 1:i + 1]
                break
        if i == len(kw_parse_list) - 1:
            return kw_parse_list
        return self.useless_parse_pop(kw_parse_list)

    # Usefull
    def keyword_parse_pos(self):
        through_list = self.__kw_pos_in_query.copy()
        output_list = through_list.copy()
        parse_list = self.found_parse()
        for element in parse_list:
            _, span = element
            start_p, _ = span
            for i in range(len(through_list)):
                _, key_span = through_list[i]
                start_k, _ = key_span
                if start_k > start_p:
                    through_list.insert(i, element)
                    break
        return self.useless_parse_pop(through_list)

    # Usefull
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

    # Usefull
    def nest_keyword(self, list_to_nest=None):
        nest = Nester()
        if list_to_nest is None:
            list_to_nest = self.keyword_parse_pos()
        kw_with_nester = []
        for i in range(1, len(list_to_nest)):
            previous = list_to_nest[i - 1]
            actual = list_to_nest[i]
            str_, _ = actual
            str_previous, _ = previous
            if re.match(r'\(', str_):
                nest.add(previous)
            elif re.match(r'\)', str_):
                if not re.match(r'\)', str_previous):
                    nest.append(previous)
                result = nest.submit()
                if result is not None:
                    kw_with_nester.append(result)
            elif nest.is_nesting:
                if re.match(r'\(', str_previous) or re.match(r'\)', str_previous):
                    pass
                else:
                    nest.append(previous)
            else:
                if re.match(r'\(', str_previous) or re.match(r'\)', str_previous):
                    pass
                else:
                    kw_with_nester.append(previous)
                if i == len(list_to_nest) - 1:
                    kw_with_nester.append(actual)
        return kw_with_nester

    def build_select_tree(self):
        list_for_tree = self.nest_keyword()
        node_dict = {}
        mother_node_list = []
        depth = 0

        def add_node(node_):
            num_key = len(node_dict)
            node_dict[num_key] = node_
            return

        def add_table_node(index, list_for_sub_tree, element):
            if index == len(list_for_tree) - 1:
                next_element = 'end'
            else:
                next_element = self.__kw_pos_in_query[self.__kw_pos_in_query.index(element)+1]
                if isinstance(next_element, dict):
                    next_element = next_element['Nester']
            parent_key_ = mother_node_list[-1]
            new_node = {'type': 'TABLE', 'content': [element, next_element], 'parent': parent_key_}
            add_node(new_node)
            return

        def tree_per_list(list_for_sub_tree):
            for i in range(len(list_for_sub_tree)):
                element = list_for_sub_tree[i]
                if isinstance(element, tuple):
                    str_, span = element
                    if re.search(r'SELECT', str_, re.IGNORECASE):
                        if mother_node_list:
                            parent_key = mother_node_list[-1]
                        else:
                            parent_key = None
                        node = {'type': 'SelectFrom', 'content': [element], 'parent': parent_key}
                        add_node(node)

                    elif re.search(r'FROM', str_, re.IGNORECASE):
                        node_dict_key = list(node_dict.keys())[-1]
                        node_dict[node_dict_key]['content'].append(element)
                        mother_node_list.append(node_dict_key)
                        add_table_node(i, list_for_sub_tree, element)

                    elif re.search(r'JOIN', str_, re.IGNORECASE):
                        parent_key = mother_node_list[-1]
                        node = {'type': 'JOIN', 'parent': parent_key}
                        add_node(node)
                        node_dict_key = list(node_dict.keys())[-1]
                        mother_node_list.append(node_dict_key)
                        add_table_node(i, list_for_sub_tree, element)

                elif isinstance(element, dict):
                    nester = element['Nester']
                    str_nester, span_nester = nester
                    if re.search(r'FROM', str_nester, re.IGNORECASE):
                        node_dict_key = list(node_dict.keys())[-1]
                        node_dict[node_dict_key]['content'].append(nester)
                        mother_node_list.append(node_dict_key)

                    elif re.search(r'JOIN', str_nester, re.IGNORECASE):
                        parent_key = mother_node_list[-1]
                        node = {'type': 'JOIN', 'parent': parent_key}
                        add_node(node)
                        node_dict_key = list(node_dict.keys())[-1]
                        mother_node_list.append(node_dict_key)

                    nested = element['Nested']
                    tree_per_list(nested)

            return

        def parent_to_child():
            for node_k, node_v in node_dict.items():
                node_dict[node_k]['child'] = []
                parent_key = node_v['parent']
                if parent_key is not None:
                    node_dict[parent_key]['child'].append(node_k)
            return

        tree_per_list(list_for_tree)
        parent_to_child()

        return node_dict

    def deduce_from_tree(self, start_key=0):
        tree_dict = self.build_select_tree()
        if isinstance(start_key, int):
            node = tree_dict[start_key]
            children = node['child']
            if node['type'] == 'SelectFrom':
                sub_output = self.deduce_from_tree(children)
                output = self.decrypt_SF_node(node)
                sub_output.append(output)
                return sub_output
            elif node['type'] == 'TABLE':
                return self.decrypt_table_node(node)
            elif node['type'] == 'JOIN':
                sub_output = self.deduce_from_tree(children)
                return sub_output
            return
            # Analyse le noeud actuelle soit un SF soit un JOIN
        elif isinstance(start_key, list):
            sub_outputs = []
            if start_key:
                for key in start_key:
                    sub_outputs.append(self.deduce_from_tree(key))
                return sub_outputs
            return


        return

    def decrypt_table_node(self, node):
        boundaries = node['content']
        _, boundary_1 = boundaries[0]
        _, boundary_2 = boundaries[1]
        _, start = boundary_1
        if boundary_2 == 'end':
            end = len(self.query)-1
        else:
            end, _ = boundary_2
        statement = self.query[start:end].strip()
        statement_list = statement.split(' ')
        if len(statement_list) == 2:
            alias = statement_list[-1]
        else:
            alias = None
        table_statement = statement_list[0].split('.')
        if len(table_statement) == 2:
            database = table_statement[0]
            table = table_statement[1]
        else:
            database = None
            table = table_statement[0]

        output = {'database_name': database, 'table_name': table, 'table_alias': alias}
        return output
        # Usefull

    def decrypt_SF_node(self,node):
        boundaries = node['content']
        _, boundary_1 = boundaries[0]
        _, boundary_2 = boundaries[1]
        _, start = boundary_1
        end, _ = boundary_2
        column_expressions = self.split_column_expression(start,end)
        output = self.deduce_column_expression_list(column_expressions)
        return output

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

    # Usefull
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

    # Usefull
    def split_column_expression(self,start,end):
        split_pattern = r',\s*(?![^()]*\))'
        # split_pattern = r',\s*'
        elements_to_change = self.query[start:end]
        elements = re.split(split_pattern, elements_to_change)
        elements = [elem.strip() for elem in elements]
        output = self.check_after_split(elements)
        return output

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

    # Usefull
    def deduce_column_expression(self, column_expression):
        keys_of_ce = self.keywords_count(self.keywords_pos(column_expression))
        if keys_of_ce.get('AS',None):
            as_start, as_end = keys_of_ce['AS'][1][-1]
            column = column_expression[:as_start].strip()
            alias = column_expression[as_end:].strip()
        else:
            alias = None
            column = column_expression
        return {'column_name': column, 'column_alias': alias}

    # Usefull
    def deduce_column_expression_list(self, list_column_exp):
        deduce_dict = {'columns_name': [],'columns_alias':[]}
        for column_expression in list_column_exp:
            ce_dict = self.deduce_column_expression(column_expression)
            deduce_dict['columns_name'].append(ce_dict['column_name'])
            deduce_dict['columns_alias'].append(ce_dict['column_alias'])
        return deduce_dict

    # Usefull
    def is_got_subqueries(self):
        if len(self.between_select_from()) > 1:
            return True
        else:
            return False

    # Usefull
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
                            or re.fullmatch('SELECT', kw_temp, re.IGNORECASE)
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

    # Usefull
    def is_table_name(self, table_statement):
        keywords_without_as = self.keyword_without_as()
        search_pattern = "|".join(keywords_without_as)
        search_pattern = r'\b(' + search_pattern + r')\b'
        if re.search(search_pattern, table_statement, re.IGNORECASE):
            return False
        return True

    # Usefull
    def table_alias(self, table_statement):
        if self.is_table_name(table_statement):
            statement_to_analyse = re.split(r'\s+', table_statement)
            print(statement_to_analyse)

        return

    # Usefull
    def analyse_tables(self):
        for statement in self.__all_tables:
            self.table_alias(statement)
        return


class Nester:
    def __init__(self):
        self.dict_list = []
        self.is_nesting = False

    def add(self, nester):
        self.is_nesting = True
        output = {'Nester': nester, 'Nested': []}
        self.dict_list.append(output)
        return

    def append(self, element):
        dict_to_append = self.dict_list[-1]
        dict_to_append['Nested'].append(element)
        return

    def submit(self):
        length = len(self.dict_list)
        if length == 0:
            # Error
            print("Can't submit something empty")
        elif length == 1:
            self.is_nesting = False
            output = self.dict_list[0]
            self.dict_list = []
            return output
        else:
            finished_dict = self.dict_list[-1]
            self.dict_list.pop()
            self.append(finished_dict)
        return


if __name__ == "__main__":
    print("Yes I try to extract info from select sql query")
