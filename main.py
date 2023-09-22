import os
from env import envVar as V
from datadict_toolbox import SQLDeduce
from datadict_toolbox import ExtractorMultidimCubeCatalog as EMCC, ExtractorTabularCubeCatalog as ETCC
from datadict_toolbox import SelectGPTDeduce, extract_erp_query, extract_ssis_mapping
import re

def main(name):
    if name == "Exp":
        tab = list(range(5))
        print(tab)
        tab.insert(0,[0,1])
        print(tab)

    elif name == "Tabular":
        folder_path = V.TABULAR_FOLDER
        files_path = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
                      os.path.isfile(os.path.join(folder_path, f))]
        print("Nbr fichier: ", len(files_path))
        for file_path in files_path[:1]:
            etcc = ETCC(file_path)
            print("Database:", etcc.src_db)
            print("Serveur:", etcc.src_serv)
            print("Cube:", etcc.cube_name())
            etcc.save()
            etcc.save(V.EXCEL_REPO, 'tabular_save_test.xlsx')

    elif name == "Multidim":
        folder_path = V.MULTIDIM_FOLDER
        files_path = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
                      os.path.isfile(os.path.join(folder_path, f))]
        print("Nbr fichier: ", len(files_path))
        for file_path in files_path[:1]:
            emcc = EMCC(file_path)
            print(V.DASH_LINE)
            print(emcc.src_db)
            print(emcc.src_serv)
            # print("Namespace:", emcc.namespace)
            # print("Database:", emcc.src_db)
            # print("Serveur:", emcc.src_serv)
            # print("Dimensions du Catalogque:", emcc.dims_catalog_name())
            # print("Cubes du catalogue:", emcc.cubes_name())
            # print("Dictionnaire de donnée du catalogue:\n",emcc.cube_struct)
            emcc.save()
            emcc.save(V.EXCEL_REPO,'multidim_save_test.xlsx')

    elif name == "SQL":
        folder_path = V.DTSX_FOLDER
        print(folder_path)
        files_path = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
                      os.path.isfile(os.path.join(folder_path, f))]
        print("Nbr fichier:", len(files_path))
        print(V.DASH_LINE)

        queries_dict = extract_erp_query(files_path)["SQL_QUERY"]

        count = 1
        for element in queries_dict[3:4]:
            print(count)
            print('SQL QUERY:\n', element)
            print(V.DASH_LINE)

            deduce = SQLDeduce(element)
            print(V.DASH_LINE)

            # kw_pos = deduce.get_kw_pos()
            # print("Nbr keyword: ", len(kw_pos))
            # print(kw_pos)
            # print(V.DASH_LINE)
#
            # print('PARSE LIST:')
            # print(deduce.found_parse())
            # print(V.DASH_LINE)

            # kw_parse_pos = deduce.keyword_parse_pos()
            # print("Keyword and parse sequence:",len(kw_parse_pos),'\n',kw_parse_pos)
            # print(V.DASH_LINE)

            # kw_count = deduce.get_kw_count()
            # print(kw_count)
            # print(V.DASH_LINE)

            # nest_keyword = deduce.nest_keyword()
            # print('Nbr:',len(nest_keyword))
            # print(nest_keyword)
            # print(V.DASH_LINE)

            print(deduce.build_select_tree())
            print(V.DASH_LINE)

            print(deduce.deduce_from_tree())
            print(V.DASH_LINE)

            # print(deduce.get_kw_query())
            # print(V.DASH_LINE)

            # b_s_f = deduce.between_select_from()
            # print("Nbr de b_s_f:",len(b_s_f))
            # print(b_s_f)
            # print(V.DASH_LINE)

            # column_exp = deduce.split_column_expression()
            # print("Nbr de b_s_f",len(column_exp))
            # for key, value in column_exp.items():
            #     print(key,":")
            #     print("Nbr column expression:",len(value))
            #     print()
            #     for element in value:
            #         print(element)
            # print(V.DASH_LINE)

            # print("Result of ANALYSE_COLUMN_EXPRESSION:")
            # print(deduce.analyse_column_expression())
            # print(V.DASH_LINE)

            # print("Result of DEDUCE_COLUMN_EXPRESSION")
            # print(deduce.deduce_column_expression())
            # print(V.DASH_LINE)

            # print("IS SUBQUERIES:", deduce.get_is_got_subqueries())
            # print(V.DASH_LINE)

            # print("TABLES:")
            # table_exp = deduce.get_all_tables()
            # print("Nbr table exp:",len(table_exp))
            # print(table_exp)
            # print(V.DASH_LINE)

            # print('ANALYSE TABLES:')
            # deduce.analyse_tables()

            print(V.DASH_LINE)
            count += 1

    elif name == "GPT":
        folder_path = V.DTSX_FOLDER
        files_path = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
                      os.path.isfile(os.path.join(folder_path, f))]

        queries_dict = extract_erp_query(files_path)
        # print(queries_dict["DEST_TABLE"][43])

        length = len(queries_dict["SQL_QUERY"])
        length = 1

        for i in range(length):
            print(i, ":", files_path[i])
            deduce = SelectGPTDeduce(V.OPENAI_ORG_ID, V.OPENAI_API_KEY, queries_dict["SQL_QUERY"][i],
                                     response_file_name=queries_dict["DEST_TABLE"][i],
                                     destination_table=queries_dict["DEST_TABLE"][i])

            print(deduce.sql_query)
            print(V.DASH_LINE)

            # print("System:\n", deduce.system_message())
            # print(V.DASH_LINE)

            # print("Examples:\n", deduce.examples_message())
            # print(V.DASH_LINE)

            print(deduce.model_response)
            print(V.DASH_LINE)

            deduce.save_model_response()

            deduce.save()

            print(V.DASH_LINE)


    elif name == "Response":
        folder_path = "model_responses/"
        files_path = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
                      os.path.isfile(os.path.join(folder_path, f))]

        for file_path in [files_path[-1]]:
            print("File path:", file_path)

            last_border = len(file_path) - len('.txt')
            first_border = len(folder_path)
            table_name = file_path
            table_name = table_name[first_border:last_border]

            deduce = SelectGPTDeduce(V.OPENAI_ORG_ID, V.OPENAI_API_KEY, answer_file=file_path,
                                     destination_table=table_name)
            deduce.extract_data_from_model_response()
            deduce.save()

    elif name == "DTSX_TEST":
        folder_path = V.DTSX_FOLDER
        files_path = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
                      os.path.isfile(os.path.join(folder_path, f))]

        for file_path in files_path[:1]:
            print(extract_ssis_mapping(file_path))
    else:
        print("No case fit : Wrong number")
    return


if __name__ == "__main__":
    main("GPT")
    # main("Multidim")
