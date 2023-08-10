# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import os
import json

repo = "C:/Users/La_Nopoly/Desktop/TestExtract/Excel/ExcelResults/"

def extract_erp_query(file_path_list):
    erp_query = {"DEST_TABLE":[],"SQL_QUERY":[]}
    for file_path in file_path_list:
        tree = ET.parse(file_path)
        root = tree.getroot()
        new_values = []

        # Namespace pour les tâches SSIS
        namespace = "{www.microsoft.com/SqlServer/Dts}"

        executables = root.findall(".//{}Executables".format(namespace))[0]
        executable = executables.find("{}Executable".format(namespace))
        subexecs = executable.find("{}Executables".format(namespace)).findall("{}Executable".format(namespace))
        component = ""
        for subexec in subexecs:
            if subexec.attrib.get("{}ObjectName".format(namespace))=="Tâche de flux de données":
            
                component = subexec.find("{}ObjectData".format(namespace)).find("pipeline").find("components").find("component")

        properties = component.find("properties")
        for property_ in properties.findall("property"):
            if(property_.attrib.get("name") == "OpenRowset"):
                tab_db_dest = property_.text
                tab_db_dest = tab_db_dest[len("[dbo]."):]
                tab_db_dest = tab_db_dest[1:-1]

        # Rechercher toutes les variables de transformation dans le package
        for variables in root.findall(".//{}Variable".format(namespace)):
            Object_name = variables.attrib.get("{}ObjectName".format(namespace))
            if Object_name == "RequêteRécupération" :
                SQLQuery = variables.find("{}VariableValue".format(namespace)).text

        new_values = [tab_db_dest,SQLQuery]
        for key, value in zip(erp_query.keys(), new_values):
                erp_query[key].append(value)

    return erp_query

def extraire_erp_structure(file_path):
    erp_struct = {"TEMP_COLUMN":[],"EXPRESSION":[],"DEST_COLUMN":[],"DEST_TABLE":[],"DATABASE_PLAN":[],"MAGASIN":[]}
    new_values = []

    tree = ET.parse(file_path)
    root = tree.getroot()
    dash_line = "\n"+"-"*100+"\n"

    # Namespace pour les tâches SSIS
    namespace = "{www.microsoft.com/SqlServer/Dts}"

    # Rechercher toutes les variables de transformation dans le package
    for variables in root.findall(".//{}Variable".format(namespace)):
        Object_name = variables.attrib.get("{}ObjectName".format(namespace))
        print("Object_name: {}".format(Object_name))
        if Object_name == "RequêteRécupération" :
            SQLQuery = variables.find("{}VariableValue".format(namespace)).text
            print("RequêteRécupération/requête SQL: {}".format(SQLQuery))

    print(dash_line)


    executables = root.findall(".//{}Executables".format(namespace))[0]
    executable = executables.find("{}Executable".format(namespace))
    print("Executable/refId: {}".format(executable.attrib.get("{}refId".format(namespace))))
    print("Executable/ObjectName: {}".format(executable.attrib.get("{}ObjectName".format(namespace))))
    subexecs = executable.find("{}Executables".format(namespace)).findall("{}Executable".format(namespace))
    component = ""
    for subexec in subexecs:
        print("Executable/refId: {}".format(subexec.attrib.get("{}refId".format(namespace))))
        print("Executable/ObjectName: {}".format(subexec.attrib.get("{}ObjectName".format(namespace))))
        print(dash_line)
        if subexec.attrib.get("{}ObjectName".format(namespace))=="Tâche de flux de données":
            
            component = subexec.find("{}ObjectData".format(namespace)).find("pipeline").find("components").find("component")

    properties = component.find("properties")
    for property_ in properties.findall("property"):
        if(property_.attrib.get("name") == "OpenRowset"):
            tab_db_dest = property_.text
            tab_db_dest = tab_db_dest[len("[dbo]."):]
            tab_db_dest = tab_db_dest[1:-1]
            print("Property/OpenRowset: {}".format(tab_db_dest))

    print(dash_line)

    sourceColAliasName = []
    input_ = component.find("inputs").find("input")
    inputColumns = input_.find("inputColumns")
    for inputCol in inputColumns.findall("inputColumn"):
        sourceColName = inputCol.attrib.get("cachedName")
        sourceColAliasName.append(sourceColName)
        print("InputColumn NAME: {}".format(sourceColName))

    print(dash_line)

    col_dest = []
    outputColumns = input_.find("externalMetadataColumns")
    for outputCol in outputColumns.findall("externalMetadataColumn"):
        destinationColName = outputCol.attrib.get("name")
        col_dest.append(destinationColName)
        print("OutputColumn NAME: {}".format(destinationColName))

    print(dash_line)

def saveAsXLSX(dictionary,excel_file_name = 'erp.xlsx'):
    path = f"{repo}{excel_file_name}"
    if(os.path.exists(path)):
        new_df = pd.DataFrame(dictionary)
        existing_df = pd.read_excel(path)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        combined_df.to_excel(path, index=False)
    else:
        df = pd.DataFrame(dictionary)
        df.to_excel(f"{repo}{excel_file_name}", index=False)

def saveAsJson(dictionary,json_file_name):
    with open(json_file_name,"w",encoding="utf-8") as json_file :
        json.dump(dictionary, json_file,ensure_ascii=False,indent=4)

        return json.dumps(dictionary)
    
file1 = "C:/Users/La_Nopoly/Desktop/TestExtract/DTSX/DimActionCo.dtsx"
file2 = "C:/Users/La_Nopoly/Desktop/TestExtract/DTSX/DimArticles.dtsx"

# Appel de la fonction en fournissant le chemin vers le fichier .dtsx
if __name__ == "__main__":
    dash_line = "\n"+"-"*100+"\n"
    folder_path = "C:/Users/La_Nopoly/Desktop/TestExtract/DTSX"
    file_names = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    print(file_names)
    print(len(file_names))
    print(dash_line)
    dico = extract_erp_query(file_names)
    print(dico)
    print(len(dico))
    saveAsJson(dico,"Query.json")
         

