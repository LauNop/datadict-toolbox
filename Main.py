import os
from env import envVar as V
from datadict_toolbox import SQLDeduce
from datadict_toolbox import extract_erp_query
from datadict_toolbox import ExtractorMultidimCubeCatalog as EMCC, ExtractorTabularCubeCatalog as ETCC


def main(name):
    if name == "Exp":
        tab = list(range(10))
        print(tab[5:8])
        print(tab[:0])
        print(tab[:5])
        print(tab[5:5])
        print(tab[6:-1])
        tab += [20]
        print(tab)
    elif name == "Tabular":
        folder_path = V.TABULAR_FOLDER
        file_names = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
                      os.path.isfile(os.path.join(folder_path, f))]
        print("Nbr fichier: ", len(file_names))
        for file_path in file_names:
            etcc = ETCC(file_path)
            print("Database:", etcc.src_db)
            print("Serveur:", etcc.src_serv)
            print("Cube:",etcc.cube_name())
            print("Dictionnaire de donnée du catalogue:\n",etcc.cube_struct)
            excel_file_name = "tabular_datadict.xlsx"
            etcc.save()
            etcc.save(excel_file_name)



    elif name == "Multidim":
        folder_path = V.MULTIDIM_FOLDER
        file_names = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
                      os.path.isfile(os.path.join(folder_path, f))]
        print("Nbr fichier: ", len(file_names))
        for file_path in file_names:
            emcc = EMCC(file_path)
            print("Namespace:", emcc.namespace)
            print("Database:", emcc.src_db)
            print("Serveur:", emcc.src_serv)
            print("Dimensions du Catalogque:", emcc.dims_catalog_name())
            print("Cubes du catalogue:", emcc.cubes_name())
            print("Dictionnaire de donnée du catalogue:\n",emcc.cube_struct)
            emcc.save()

    elif name == "SQL":
        folder_path = V.DTSX_FOLDER
        print(folder_path)
        file_names = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
                      os.path.isfile(os.path.join(folder_path, f))]
        print("Nbr fichier:", len(file_names))
        print(V.DASH_LINE)

        queries = extract_erp_query(file_names)["SQL_QUERY"]

        count = 1
        for query in queries[:10]:
            print(count)
            print('SQL QUERY:\n', query)
            print(V.DASH_LINE)

            deduce = SQLDeduce(query)
            print(V.DASH_LINE)

            # kw_pos = deduce.get_kw_pos()
            # print("Nbr keyword: ", len(kw_pos))
            # print(kw_pos)
            # print(V.DASH_LINE)

            kw_count = deduce.get_kw_count()
            print(kw_count)
            print(V.DASH_LINE)

            print(deduce.get_kw_query())
            print(V.DASH_LINE)

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

            print("Result of DEDUCE_COLUMN_EXPRESSION")
            print(deduce.deduce_column_expression())
            print(V.DASH_LINE)

            print("IS SUBQUERIES:", deduce.get_is_got_subqueries())
            print(V.DASH_LINE)

            print("TABLES:")
            print(deduce.get_all_tables())
            print(V.DASH_LINE)

            print(V.DASH_LINE)
            count += 1

    else:
        print("No case fit : Wrong number")
    return


if __name__ == "__main__":
    main("Multidim")
