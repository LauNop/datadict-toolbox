import os
from env import envVar as V
from datadict_toolbox import SQLDeduce
from datadict_toolbox import extract_erp_query
from datadict_toolbox import ExtractorMultidimCubeCatalog as EMCC


def main(num):
    if num == 1:
        path = None
        if path:
            print("Pass")
        else:
            print("None")
    elif num == 2:
        folder_path = V.XMLA_FOLDER
        file_names = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
                      os.path.isfile(os.path.join(folder_path, f))]
        print("Nbr fichier: ", len(file_names))
        for file_path in file_names:
            emcc = EMCC(file_path)
            print("Namespace:", emcc.get_namespace())
            print("Database:", emcc.get_src_db())
            print("Serveur:", emcc.get_src_serv())
            print("Dimensions du Catalogque:", emcc.get_dims_catalog_name())
            print("Cubes du catalogue:",emcc.get_cubes_name())
            print("Dictionnaire de donnée du catalogue:\n",emcc.get_data_dict())
            excel_file_name = "multidim_datadict.xlsx"
            emcc.save()
            emcc.save(excel_file_name)

    elif num == 3:
        folder_path = V.DTSX_FOLDER
        print(folder_path)
        file_names = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
                      os.path.isfile(os.path.join(folder_path, f))]
        print("Nbr fichier:", len(file_names))
        print(V.DASH_LINE)

        queries = extract_erp_query(file_names)["SQL_QUERY"]

        for query in queries[:2]:
            print('SQL QUERY:\n', query)
            print(V.DASH_LINE)
            deduce = SQLDeduce(query)
            print(V.DASH_LINE)
            kw_pos = deduce.get_kw_pos()
            print("Nbr keyword: ", len(kw_pos))
            print(kw_pos)
            print(V.DASH_LINE)
            kw_count = deduce.get_kw_count()
            print(kw_count)
            print(V.DASH_LINE)
    else:
        print("No case fit : Wrong number")
    return


if __name__ == "__main__":
    main(2)
