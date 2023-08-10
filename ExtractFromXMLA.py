import xml.etree.ElementTree as ET
import json
import pandas as pd
import os

repo = "C:/Users/La_Nopoly/Desktop/TestExtract/Excel/ExcelResults/"

def extract_cube_structure(file_path,tabular = True,src_database="MTQ_BRI_GCO"):
    cube_struct = {"COLUMN_NAME":[],"DATA_TYPE":[],"IS_CALCULATED":[],"IS_MEASURE":[],"EXPRESSION":[],"IS_VISIBLE":[],"DIMENSION_NAME":[],"CUBE_NAME":[],"CATALOG_NAME":[],"SOURCE":[]}
    data = ""
    new_values = []
    src_table = ""
    src_column = ""

    with open(file_path, 'r', encoding = 'utf-8') as file:
        json_content = file.read()
        data = json.loads(json_content)
    file.close()
    
    catalog = data['create']['parentObject']['database']

    if tabular:
        cube = 'Modèle'
    else:
        print('Problème')

    table_dict = data['create']['table']
    dimension = table_dict['name'] 

    annotations = table_dict['annotations']
    for annotation in annotations:
        if annotation['name'] == '_TM_ExtProp_DbTableName':
            src_table = annotation['value']
    
    measure = 0
    columns = table_dict['columns']
    for column in columns:
        keys = list(column.keys())
        
        if 'type' in keys :
            calculated = 1
        else:
            calculated = 0
        if 'isHidden' in keys :
            visible = 0
        else:
            visible = 1
        if 'expression' in keys :
            expression = column['expression']
            src = ""
        else:
            expression = 'None'
            src_column = column['sourceColumn']
            src = src_column+'/'+src_table+'/'+src_database
            
        new_values = [column['name'],column['dataType'],calculated,measure,expression,visible,dimension,cube,catalog,src]
        for key, value in zip(cube_struct.keys(), new_values):
            cube_struct[key].append(value)

    calculated = 0
    measure = 1
    if "measures" in list(table_dict.keys()):
        measures = table_dict['measures']
        for measure_ in measures:
            keys = list(measure_.keys())

            if 'isHidden' in keys :
                visible = 0
            else:
               visible = 1
            
            expression = measure_['expression']
            new_values = [measure_['name'],'measure',calculated,measure,expression,visible,dimension,cube,catalog,""]
            for key, value in zip(cube_struct.keys(), new_values):
                cube_struct[key].append(value)

    return cube_struct

def saveAsXLSX(dictionary,excel_file_name = 'cubes.xlsx'):
    path = f"{repo}{excel_file_name}"
    if(os.path.exists(path)):
        new_df = pd.DataFrame(dictionary)
        existing_df = pd.read_excel(path)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        combined_df.to_excel(path, index=False)
    else:
        df = pd.DataFrame(dictionary)
        df.to_excel(f"{repo}{excel_file_name}", index=False)

if __name__ == "__main__":

   folder_path = "C:/Users/La_Nopoly/Desktop/TestExtract/XMLA"
   file_names = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
   print(file_names)
   for file_path in file_names :
       saveAsXLSX(extract_cube_structure(file_path))