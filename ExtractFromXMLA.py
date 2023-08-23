import xml.etree.ElementTree as ET
import json
import pandas as pd
import os

import envVar as V

def extract_cube_tabular_structure(file_path,src_database):

    # Structure de dictionnaire en sortie
    cube_struct = {"COLUMN_NAME":[],"NOM_EXPLICIT":[],"DATA_TYPE":[],"IS_CALCULATED":[],"IS_MEASURE":[],"EXPRESSION":[],"IS_VISIBLE":[],"DIMENSION_NAME":[],"CUBE_NAME":[],"CATALOG_NAME":[],"SOURCE":[]}

    # Variable de manipulation
    data = ""
    new_values = []
    src_table = ""
    src_column = ""

    # Ouverture du fichier .xmla et récupération des données dans data
    with open(file_path, 'r', encoding = 'utf-8') as file:
        json_content = file.read()
        data = json.loads(json_content)
    file.close()

    # Etapes de récupération des différentes clé du dictionnaire
    
    # CATALOG_NAME
    catalog = data['create']['parentObject']['database']

    #CUBE_NAME
    cube = 'Modèle'

    table_dict = data['create']['table']

    # DIMENSION_NAME
    dimension = table_dict['name'] 

    annotations = table_dict['annotations']
    for annotation in annotations:
        if annotation['name'] == '_TM_ExtProp_DbTableName':
            # src_table portion de SOURCE
            src_table = annotation['value']
    
    # Récupération des colonnes classiques
    measure = 0
    # COLUMN_NAME, DATA_TYPE, IS_CALCULATED, IS_MEASURE, EXPRESSION, IS_VISIBLE
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
            expression = ''
            src_column = column['sourceColumn']
            src = src_column+'/'+src_table+'/'+src_database
        
         
        new_values = [column['name'],"",column['dataType'],calculated,measure,expression,visible,dimension,cube,catalog,src]
        for key, value in zip(cube_struct.keys(), new_values):
            cube_struct[key].append(value)
    
    # Récupération des colonnes Measures
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
            new_values = [measure_['name'],"",'measure',calculated,measure,expression,visible,dimension,cube,catalog,""]
            for key, value in zip(cube_struct.keys(), new_values):
                cube_struct[key].append(value)

    return cube_struct

def extract_cube_multidim_structure(file_path):
    # Structure de dictionnaire en sortie
    cube_struct = {"COLUMN_NAME":[],"NOM_EXPLICIT":[],"DATA_TYPE":[],"IS_CALCULATED":[],"IS_MEASURE":[],"EXPRESSION":[],"IS_VISIBLE":[],"DIMENSION_NAME":[],"CUBE_NAME":[],"CATALOG_NAME":[],"SOURCE":[]}

    # Variable de manipulation
    data = ""
    new_values = []
    src_table = ""
    src_column = ""

    # Ouverture du fichier .xmla et récupération des données dans data
    tree = ET.parse(file_path)
    root = tree.getroot()
    namespace = "{http://schemas.microsoft.com/analysisservices/2003/engine}"
    database_elmt = root.find(".//{}ObjectDefinition".format(namespace)).find("{}Database".format(namespace))
    print(database_elmt.find("{}Name".format(namespace)).text)

    # CATALOG_NAME
    #catalog = xml_object.find("Name").text
    #
    #dim = xml_object.find("Dimensions").find("Dimension")
    #
    #print(catalog,dim.find("ID").text)

def saveAsXLSX(dictionary,excel_file_name = 'cubes.xlsx'):
    path = f"{V.EXCEL_REPO}{excel_file_name}"
    if(os.path.exists(path)):
        new_df = pd.DataFrame(dictionary)
        existing_df = pd.read_excel(path)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        combined_df.to_excel(path, index=False)
    else:
        df = pd.DataFrame(dictionary)
        df.to_excel(f"{V.EXCEL_REPO}{excel_file_name}", index=False)

if __name__ == "__main__":

   folder_path = V.XMLA_FOLDER
   file_names = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
   print(file_names)
   for file_path in file_names :
   #    saveAsXLSX(extract_cube_structure(file_path,"MTQ_BRI_CAI"))
        extract_cube_multidim_structure(file_path)

