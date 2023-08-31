import xml.etree.ElementTree as ET
import json
import pandas as pd
import os
import re


# Extract from tabular
def extract_cube_tabular_structure(file_path, src_database):
    # Structure de dictionnaire en sortie
    cube_struct = {"COLUMN_NAME": [], "NOM_EXPLICIT": [], "DATA_TYPE": [], "IS_CALCULATED": [], "IS_MEASURE": [],
                   "EXPRESSION": [], "IS_VISIBLE": [], "DIMENSION_NAME": [], "CUBE_NAME": [], "CATALOG_NAME": [],
                   "SOURCE": []}

    # Variable de manipulation
    data = ""
    new_values = []
    src_table = ""
    src_column = ""

    # Ouverture du fichier .xmla et récupération des données dans data
    with open(file_path, 'r', encoding='utf-8') as file:
        json_content = file.read()
        data = json.loads(json_content)
    file.close()

    # Etapes de récupération des différentes clé du dictionnaire

    # CATALOG_NAME
    catalog = data['create']['parentObject']['database']

    # CUBE_NAME
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

        if 'type' in keys:
            calculated = 1
        else:
            calculated = 0
        if 'isHidden' in keys:
            visible = 0
        else:
            visible = 1
        if 'expression' in keys:
            expression = column['expression']
            src = ""
        else:
            expression = ''
            src_column = column['sourceColumn']
            src = src_column + '/' + src_table + '/' + src_database

        new_values = [column['name'], "", column['dataType'], calculated, measure, expression, visible, dimension, cube,
                      catalog, src]
        for key, value in zip(cube_struct.keys(), new_values):
            cube_struct[key].append(value)

    # Récupération des colonnes Measures
    calculated = 0
    measure = 1
    if "measures" in list(table_dict.keys()):
        measures = table_dict['measures']
        for measure_ in measures:
            keys = list(measure_.keys())

            if 'isHidden' in keys:
                visible = 0
            else:
                visible = 1

            expression = measure_['expression']
            new_values = [measure_['name'], "", 'measure', calculated, measure, expression, visible, dimension, cube,
                          catalog, ""]
            for key, value in zip(cube_struct.keys(), new_values):
                cube_struct[key].append(value)

    return cube_struct


class ExtractorMultidimCubeCatalog:
    def __init__(self, file_path):
        self.__cube_struct = self.build_cube_dict()
        self.__file_path = file_path
        self.__root = self.open_file()
        self.__namespace = self.setup()
        self.__db_element = self.db_element()
        self.__src_db, self.__src_serv = self.datasource()
        self.create_cube_struct()

    # Getters
    def get_file_path(self):
        return self.__file_path

    def get_root(self):
        return self.__root

    def get_namespace(self):
        return self.__namespace

    def get_src_db(self):
        return self.__src_db

    def get_src_serv(self):
        return self.__src_serv

    def get_dims_catalog_name(self):
        dim_name_list = []
        dimensions = self.dim_catalog()
        for dimension in dimensions:
            dim_name = dimension.find(self.balise_format("Name")).text
            dim_name_list.append(dim_name)
        return dim_name_list

    def get_cubes_name(self):
        cubes_name_list = []
        for cube in self.cubes():
            cubes_name_list.append(self.cube_name(cube))
        return cubes_name_list

    def get_data_dict(self):
        return self.__cube_struct

    # Methods
    def build_cube_dict(self):
        with open('datadict_toolbox/usefull.json', 'r') as file:
            json_content = file.read()
            usefull_dict = json.loads(json_content)
        file.close()
        cube_struct = {key: [] for key in usefull_dict["Multidim"]}
        return cube_struct

    def open_file(self):
        # Ouverture du fichier .xmla et récupération des données dans data
        tree = ET.parse(self.__file_path)
        root = tree.getroot()
        return root

    def setup(self):
        pattern = r'{(.*)}'
        regex = re.match(pattern, self.__root.tag)
        namespace = regex.group()
        return namespace

    def balise_format(self, balise_name):
        formatted = f"{self.__namespace}{balise_name}"
        return formatted

    def db_element(self):
        db_obj = self.__root.find(".//" + self.balise_format("ObjectDefinition")).find(self.balise_format("Database"))
        return db_obj

    def catalog_name(self):
        # CATALOG_NAME
        catalog = self.__db_element.find(self.balise_format("Name")).text
        return catalog

    def datasource(self):
        # Récupérer la datasource
        str_datasource = self.__db_element.find(self.balise_format("DataSources")).find(self.balise_format("DataSource")).find(
            self.balise_format("ConnectionString")).text

        # Traitement de str_datasource pour récupérer l'IP serveur et l'Initial Catalog
        str_datasource = str_datasource.split(";")
        for str_el in str_datasource:
            if re.match(r"^Data Source.*", str_el):
                src_serv = str_el[str_el.index("=") + 1:]
            if re.match(r"^Initial Catalog", str_el):
                src_database = str_el[str_el.index("=") + 1:]
        return src_database, src_serv

    def dim_catalog(self):
        # Récupérer les dimensions à la source
        dimensions = self.__db_element.find(self.balise_format("Dimensions")).findall(self.balise_format("Dimension"))
        return dimensions

    def dim_metadata(self):
        dictionary = {}
        for dimension in self.dim_catalog():
            dim_name = dimension.find(self.balise_format("ID")).text
            sub_dict = {"Attribute_name": [], "Attribute_id": [], "Column": [], "Datatype": [], "Table": []}

            for attribute in dimension.find(self.balise_format("Attributes")).findall(self.balise_format("Attribute")):
                attribute_id = attribute.find(self.balise_format("ID")).text
                attribute_name = attribute.find(self.balise_format("Name")).text

                source = attribute.find(self.balise_format("NameColumn"))
                data_type = source.find(self.balise_format("DataType")).text

                sub_source = source.find(self.balise_format("Source"))
                table_name = sub_source.find(self.balise_format("TableID")).text
                column_name = sub_source.find(self.balise_format("ColumnID")).text

                sub_dict["Attribute_name"].append(attribute_name)
                sub_dict["Attribute_id"].append(attribute_id)
                sub_dict["Column"].append(column_name)
                sub_dict["Datatype"].append(data_type)
                sub_dict["Table"].append(table_name)

            dictionary[dim_name] = sub_dict
        return dictionary

    def cubes(self):
        # Récupérer les cubes
        cubes = self.__db_element.find(self.balise_format("Cubes")).findall(self.balise_format("Cube"))
        return cubes

    def insert_structure(self,values):
        for key, value in zip(self.__cube_struct.keys(), values):
            self.__cube_struct[key].append(value)
        return

    def cube_name(self, cube):
        cube_name = cube.find(self.balise_format("Name")).text
        return cube_name

    def cube_dimensions_usage(self,cube):
        expression = ""
        print("CUBE: ", self.cube_name(cube))
        is_measure = 0
        is_dimension = 1
        is_calculated = "wip"
        is_visible = "wip"
        c_dims = cube.find(self.balise_format("Dimensions")).findall(self.balise_format("Dimension"))
        for c_dim in c_dims:
            group_name = c_dim.find(self.balise_format("Name")).text
            dimension_id = c_dim.find(self.balise_format("DimensionID")).text
            attributes = c_dim.find(self.balise_format("Attributes")).findall(self.balise_format("Attribute"))
            for attribute in attributes:
                column_name = attribute.find(self.balise_format("AttributeID")).text
                dim_dict = self.dim_metadata()
                for i in range(len(dim_dict[dimension_id]["Attribute_id"])):

                    if dim_dict[dimension_id]["Attribute_id"][i] == column_name:
                        data_type = dim_dict[dimension_id]["Datatype"][i]
                        src_column = dim_dict[dimension_id]["Column"][i]
                        src_table = dim_dict[dimension_id]["Table"][i]
                        new_values = [column_name, "", data_type, is_calculated, is_measure, is_dimension, expression, is_visible,
                                      group_name, self.cube_name, self.catalog_name, f"{src_column}/{src_table}/{self.__src_db}/{self.__src_serv}"]
                        self.insert_structure(new_values)
        return

    def cube_measures(self, cube):
        expression = ""
        is_measure = 1
        is_dimension = 0
        is_calculated = "wip"
        is_visible = "wip"
        measure_groups = cube.find(self.balise_format("MeasureGroups")).findall(self.balise_format("MeasureGroup"))
        for measure_group in measure_groups:
            group_name = measure_group.find(self.balise_format("Name")).text
            print(" GROUP : ", group_name)
            measures = measure_group.find(self.balise_format("Measures")).findall(self.balise_format("Measure"))
            for measure in measures:
                column_name = measure.find(self.balise_format("Name")).text
                print("     Attribut : ", column_name)
                data_type = measure.find(self.balise_format("DataType")).text
                source = measure.find(self.balise_format("Source"))
                sub_source = source.find(self.balise_format("Source"))
                src_table = sub_source.find(self.balise_format("TableID")).text
                if sub_source.attrib.get("{http://www.w3.org/2001/XMLSchema-instance}type") == "ColumnBinding":
                    src_column = sub_source.find(self.balise_format("ColumnID")).text
                else:
                    src_column = ""
                new_values = [column_name, "", data_type, is_calculated, is_measure, is_dimension, expression, is_visible, group_name,
                              self.cube_name(cube), self.catalog_name(), f"{src_column}/{src_table}/{self.__src_db}/{self.__src_serv}"]
                self.insert_structure(new_values)
        return

    def create_cube_struct(self):
        for cube in self.cubes():
            self.cube_dimensions_usage(cube)
            self.cube_measures(cube)

    def save(self,path = None):
        if path is None:
            path_build = [self.catalog_name(),"multidim",str(len(self.cubes()))]
            path = "_".join(path_build)+".xlsx"

        if os.path.exists(path):
            new_df = pd.DataFrame(self.__cube_struct)
            existing_df = pd.read_excel(path)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            combined_df.to_excel(path, index=False)
        else:
            df = pd.DataFrame(self.__cube_struct)
            df.to_excel(path, index=False)




if __name__ == "__main__":
    print('Need to convert ETCC')