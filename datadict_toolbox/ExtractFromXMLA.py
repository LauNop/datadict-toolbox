﻿from cgitb import text
import xml.etree.ElementTree as ET
import json
import pandas as pd
import os
import re

import envVar as V


# Extract from tabular
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

def getCatalog(database_elmt, namespace):
    # CATALOG_NAME
    catalog  = database_elmt.find("{}Name".format(namespace)).text
    
    return catalog

def getDatasource(database_elmt,namespace):
    # Récupérer la datasource
    str_datasource = database_elmt.find("{}DataSources".format(namespace)).find("{}DataSource".format(namespace)).find("{}ConnectionString".format(namespace)).text

    # Traitement de str_datasource pour récupérer l'IP serveur et l'Initial Catalog
    str_datasource = str_datasource.split(";")
    for str_el in str_datasource:
        if re.match(r"^Data Source.*",str_el):
            src_serv = str_el[str_el.index("=")+1:]
        if re.match(r"^Initial Catalog",str_el):
            src_database = str_el[str_el.index("=")+1:]
    return src_database, src_serv

def getDimCatalog(database_elmt,namespace):
    # Récupérer les dimensions à la source
    dimensions = database_elmt.find("{}Dimensions".format(namespace)).findall("{}Dimension".format(namespace))

    return dimensions

def getDimMetadata(database_elmt,namespace):
    dictionary = {}
    for dimension in getDimCatalog(database_elmt,namespace):
        dim_name = dimension.find("{}ID".format(namespace)).text
        sub_dict = {"Attribute_name":[],"Attribute_id":[],"Column":[],"Datatype":[],"Table":[]}
        dictionary[dim_name] = sub_dict

        for attribute in dimension.find("{}Attributes".format(namespace)).findall("{}Attribute".format(namespace)):
            attribute_name = attribute.find("{}Name".format(namespace)).text
            attribute_id = attribute.find("{}ID".format(namespace)).text
            source = attribute.find("{}NameColumn".format(namespace))
            sub_source = source.find("{}Source".format(namespace))
            column_name = sub_source.find("{}ColumnID".format(namespace)).text
            table_name = sub_source.find("{}TableID".format(namespace)).text
            data_type = source.find("{}DataType".format(namespace)).text
            dictionary[dim_name]["Attribute_name"].append(attribute_name)
            dictionary[dim_name]["Attribute_id"].append(attribute_id)
            dictionary[dim_name]["Column"].append(column_name)
            dictionary[dim_name]["Datatype"].append(data_type)
            dictionary[dim_name]["Table"].append(table_name)

    return dictionary

def getCubes(database_elmt,namespace):
    # Récupérer les cubes
    cubes = database_elmt.find("{}Cubes".format(namespace)).findall("{}Cube".format(namespace))
    
    return cubes

def insertStructure(dictionary,values):
    for key, value in zip(dictionary.keys(), values):
        dictionary[key].append(value)

    return dictionary

def getCubeName(cube,namespace):
    cube_name = cube.find("{}Name".format(namespace)).text

    return cube_name

def cubeDimensionsUsage(cube, catalog, cube_struct, namespace,src_database,src_serv,database_elmt):
    expression = ""
    cube_name = getCubeName(cube,namespace)
    print("CUBE: ",cube_name)
    is_measure = 0
    is_dimension = 1
    c_dims = cube.find("{}Dimensions".format(namespace)).findall("{}Dimension".format(namespace))
    for c_dim in c_dims:
        group_name = c_dim.find("{}Name".format(namespace)).text
        dimension_id = c_dim.find("{}DimensionID".format(namespace)).text
        attribs = c_dim.find("{}Attributes".format(namespace)).findall("{}Attribute".format(namespace))
        for attrib in attribs:
            column_name = attrib.find("{}AttributeID".format(namespace)).text
            dim_dict = getDimMetadata(database_elmt,namespace)
            for i in range(len(dim_dict[dimension_id]["Attribute_id"])):
                print(dim_dict[dimension_id]["Attribute_id"][i],":",group_name,":", column_name,":",dim_dict[dimension_id]["Attribute_id"][i] == column_name)
                
                if dim_dict[dimension_id]["Attribute_id"][i] == column_name:
                    data_type = dim_dict[dimension_id]["Datatype"][i]
                    src_column = dim_dict[dimension_id]["Column"][i]
                    src_table = dim_dict[dimension_id]["Table"][i]
                    new_values = [column_name,"",data_type,"wip",is_measure,is_dimension,expression,"wip",group_name,cube_name,catalog,f"{src_column}/{src_table}/{src_database}/{src_serv}"]
                    cube_struct = insertStructure(cube_struct, new_values)

    return cube_struct

def cubeMeasures(cube, catalog, cube_struct, namespace, src_database,src_serv):
    expression = ""
    cube_name = getCubeName(cube,namespace)
    is_measure = 1
    is_dimension = 0
    measure_groups = cube.find("{}MeasureGroups".format(namespace)).findall("{}MeasureGroup".format(namespace))
    for measure_group in measure_groups :
        group_name = measure_group.find("{}Name".format(namespace)).text
        print(" GROUP : ",group_name)
        measures = measure_group.find("{}Measures".format(namespace)).findall("{}Measure".format(namespace))
        for measure in measures :
            column_name = measure.find("{}Name".format(namespace)).text
            print("     Attribut : ",column_name)
            data_type = measure.find("{}DataType".format(namespace)).text
            source= measure.find("{}Source".format(namespace))
            sub_source = source.find("{}Source".format(namespace))
            src_table = sub_source.find("{}TableID".format(namespace)).text
            print("         SRC_TABLE : ",src_table)
            if sub_source.attrib.get("{http://www.w3.org/2001/XMLSchema-instance}type") == "ColumnBinding":
                src_column = sub_source.find("{}ColumnID".format(namespace)).text
            else:
                src_column = ""
            print("         SRC_COLUMN : ",src_column)
            new_values = [column_name,"",data_type,"wip",is_measure,is_dimension,expression,"wip",group_name,cube_name,catalog,f"{src_column}/{src_table}/{src_database}/{src_serv}"]
            insertStructure(cube_struct, new_values)

    return cube_struct

def cubesStructure(database_elmt, cube_struct, namespace):
    cubes = getCubes(database_elmt, namespace)
    catalog = getCatalog(database_elmt, namespace)
    src_database, src_serv = getDatasource(database_elmt, namespace)

    # Récupérer les infos des dimensions utilisées par chaque cube
    expression = ""
    for cube in cubes:
        cube_struct = cubeDimensionsUsage(cube, catalog, cube_struct, namespace,src_database,src_serv,database_elmt)
        cube_struct = cubeMeasures(cube, catalog, cube_struct, namespace,src_database,src_serv)

    return cube_struct

# Extract from multidim
def extractCubeMultidimStructure(file_path):
    # Structure de dictionnaire en sortie
    cube_struct = {"ATTRIBUTE_NAME":[],"NOM_EXPLICIT":[],"DATA_TYPE":[],"IS_CALCULATED":[],"IS_MEASURE":[],"IS_DIMENSION":[],"EXPRESSION":[],"IS_VISIBLE":[],"GROUP":[],"CUBE_NAME":[],"CATALOG_NAME":[],"SOURCE":[]}

    # Ouverture du fichier .xmla et récupération des données dans data
    tree = ET.parse(file_path)
    root = tree.getroot()
    namespace = "{http://schemas.microsoft.com/analysisservices/2003/engine}"
    database_elmt = root.find(".//{}ObjectDefinition".format(namespace)).find("{}Database".format(namespace))

    dims = getDimCatalog(database_elmt, namespace)
    
    cube_struct = cubesStructure(database_elmt, cube_struct, namespace)

    return cube_struct
    

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
        saveAsXLSX(extractCubeMultidimStructure(file_path),"cubes_multidim.xlsx")
