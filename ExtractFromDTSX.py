# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import os
import json

repo = "C:/Users/La_Nopoly/Desktop/TestExtract/Excel/ExcelResults/"
dash_line = "\n"+"-"*100+"\n"


def dtsx_open(file_path):
    tree = ET.parse(file_path)
    return tree.getroot(),  "{www.microsoft.com/SqlServer/Dts}"

def extract_erp_query(file_path_list):
    erp_query = {"DEST_TABLE":[],"SQL_QUERY":[]}
    for file_path in file_path_list:
        root, namespace = dtsx_open(file_path)
        new_values = []

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

def extract_ssis_mapping(file_path):
    ssis_mapping = {"ALIAS_NAME":[],"NAME":[]}
    new_values = []

    root, namespace = dtsx_open(file_path)

    executables = root.find(".//{}Executables".format(namespace))
    executable = executables.find("{}Executable".format(namespace))
    subexecs = executable.find("{}Executables".format(namespace)).findall("{}Executable".format(namespace))
    component = ""
    for subexec in subexecs:
        if subexec.attrib.get("{}ObjectName".format(namespace))=="Tâche de flux de données":  
            component = subexec.find("{}ObjectData".format(namespace)).find("pipeline").find("components").find("component")

    col_alias = []
    input_ = component.find("inputs").find("input")
    inputColumns = input_.find("inputColumns")
    for inputCol in inputColumns.findall("inputColumn"):
        sourceColName = inputCol.attrib.get("cachedName")
        col_alias.append(sourceColName)

    col_dest = []
    outputColumns = input_.find("externalMetadataColumns")
    for outputCol in outputColumns.findall("externalMetadataColumn"):
        destinationColName = outputCol.attrib.get("name")
        col_dest.append(destinationColName)

    new_values = [col_alias,col_dest]
    for key, value in zip(ssis_mapping.keys(), new_values):
            ssis_mapping[key].append(value)

    return ssis_mapping

def extract_variable(file_path):
    root, namespace = dtsx_open(file_path)
    variable = {"VARIABLE":[]}

        # Rechercher toutes les variables de transformation dans le package dtsx
    for variables in root.findall(".//{}Variable".format(namespace)):
        variable["VARIABLE"].append(variables.attrib.get("{}ObjectName".format(namespace))) 

    return variable

def saveAsJson(dictionary,json_file_name):
    with open(json_file_name,"w",encoding="utf-8") as json_file :
        json.dump(dictionary, json_file,ensure_ascii=False,indent=4)

        return json.dumps(dictionary)
    
file1 = "C:/Users/La_Nopoly/Desktop/TestExtract/DTSX/DimActionCo.dtsx"
file2 = "C:/Users/La_Nopoly/Desktop/TestExtract/DTSX/DimArticles.dtsx"

# Appel de la fonction en fournissant le chemin vers le fichier .dtsx
if __name__ == "__main__":
    folder_path = "C:/Users/La_Nopoly/Desktop/TestExtract/DTSX"
    file_names = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    print(file_names)
    print(len(file_names))
    print(dash_line)
    print(extract_ssis_mapping(file_names[0]))
    print(extract_variable(file_names[0]))
    #dico = extract_erp_query(file_names)
    #print(dico)
    #print(len(dico))
    
         

