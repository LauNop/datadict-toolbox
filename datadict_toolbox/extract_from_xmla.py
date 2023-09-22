import xml.etree.ElementTree as ET
import json
import pandas as pd
import os
import re
from abc import ABC, abstractmethod

from datadict_toolbox.usefull import usefull_dict

class Extractor(ABC):
    def __init__(self, file_path):
        self.cube_struct = None
        self.file_path = file_path

    @abstractmethod
    def build_cube_dict(self,key):
        cube_struct = {key: [] for key in usefull_dict[key]}
        return cube_struct

    @abstractmethod
    def open_file(self):
        pass

    @abstractmethod
    def db_element(self):
        pass

    @abstractmethod
    def catalog_name(self):
        pass

    def cube_name(self):
        pass

    @abstractmethod
    def extract_from_connectionString(self, str_datasource):
        # Traitement de str_datasource pour récupérer l'IP serveur et l'Initial Catalog
        str_datasource = str_datasource.split(";")
        src_database, src_serv = "", ""
        for str_el in str_datasource:
            if re.match(r"^Data Source.*", str_el):
                src_serv = str_el[str_el.index("=") + 1:]
            if re.match(r"^Initial Catalog", str_el):
                src_database = str_el[str_el.index("=") + 1:]
        return src_database, src_serv

    @abstractmethod
    def datasource(self):
        pass

    @abstractmethod
    def insert_structure(self, values):
        for key, value in zip(self.cube_struct.keys(), values):
            self.cube_struct[key].append(value)
        return

    @abstractmethod
    def create_cube_struct(self):
        pass

    @abstractmethod
    def build_save_filename(self):
        pass

    @abstractmethod
    def save(self, save_path=None, filename=None):
        save_folder = "excel_result/"
        if save_path is None:
            save_path = "excel_result/"

        if not (os.path.exists(save_path) and os.path.isdir(save_path)):
            os.makedirs(save_path)

        if filename is None:
            filename_build = self.build_save_filename()
            filename = "_".join(filename_build) + ".xlsx"

        save_path = os.path.join(save_path, filename)

        if os.path.exists(save_path):
            new_df = pd.DataFrame(self.cube_struct)
            existing_df = pd.read_excel(save_path)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            combined_df.to_excel(save_path, index=False)
        else:
            df = pd.DataFrame(self.cube_struct)
            df.to_excel(save_path, index=False)
        return

    @abstractmethod
    def setup(self):
        pass


# Extract from tabular
class ExtractorTabularCubeCatalog(Extractor):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.cube_struct = self.build_cube_dict()
        self.root = self.open_file()
        self.db_element = self.db_element()
        self.src_db, self.src_serv = self.datasource()
        self.create_cube_struct()

    def build_cube_dict(self):
        return super().build_cube_dict("Tabular")

    def setup(self):
        pass

    def open_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            json_content = file.read()
        file.close()
        root = json.loads(json_content)
        return root

    def db_element(self):
        db_element = self.root['create']['database']
        return db_element

    def catalog_name(self):
        catalog = self.db_element['name']
        return catalog

    def model_element(self):
        cube = self.db_element['model']
        return cube

    def cube_name(self):
        cube_name = self.model_element()['name']
        return cube_name

    def extract_from_connectionString(self, str_datasource):
        return super().extract_from_connectionString(str_datasource)

    def datasource(self):
        str_datasource = self.model_element()['dataSources'][0]['connectionString']
        return self.extract_from_connectionString(str_datasource)

    def insert_structure(self, values):
        return super().insert_structure(values)

    def tables_element(self):
        tables_element = self.model_element()['tables']
        return tables_element

    def cube_table(self, dict_table):
        table_name = dict_table['name']
        is_measure = 0
        src_table = None
        for dict_annot in dict_table['annotations']:
            if dict_annot['name'] == "_TM_ExtProp_DbTableName":
                src_table = dict_annot['value']

        for dict_column in dict_table['columns']:
            column_name = dict_column['name']
            data_type = dict_column['dataType']
            if dict_column.get('isHidden'):
                is_visible = 0
            else:
                is_visible = 1
            print(dict_column.get('type'))
            if dict_column.get('type'):
                is_calculated = 1
                expression = dict_column["expression"]
                src = ""
            else:
                is_calculated = 0
                expression = ""
                src_column = dict_column['sourceColumn']
                src = f"{src_column}/{src_table}"

            new_values = [column_name, "", data_type, is_calculated, is_measure, expression, is_visible, table_name,
                          self.cube_name(), self.catalog_name(), src]
            self.insert_structure(new_values)

    def cube_measures(self, dict_table):
        table_name = dict_table["name"]
        data_type = "measure"
        is_calculated = 0
        is_measure = 1
        if dict_table.get('measures'):
            for dict_measure in dict_table['measures']:
                column_name = dict_measure['name']
                expression = dict_measure['expression']
                if dict_measure.get('isHidden'):
                    is_visible = 0
                else:
                    is_visible = 1

                new_values = [column_name, "", data_type, is_calculated, is_measure, expression, is_visible, table_name,
                              self.cube_name(), self.catalog_name(), ""]
                self.insert_structure(new_values)

    def create_cube_struct(self):
        for dict_table in self.tables_element():
            self.cube_table(dict_table)
            self.cube_measures(dict_table)

    def build_save_filename(self):
        return [self.catalog_name(), "tabular", self.cube_name()]

    def save(self, save_path=None,filename=None):
        super().save(save_path,filename)
        return


class ExtractorMultidimCubeCatalog(Extractor):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.cube_struct = self.build_cube_dict()
        self.root = self.open_file()
        self.namespace = self.setup()
        self.db_element = self.db_element()
        self.src_db, self.src_serv = self.datasource()
        self.create_cube_struct()

    def build_cube_dict(self):
        return super().build_cube_dict("Multidim")

    def open_file(self):
        # Ouverture du fichier .xmla et récupération des données dans data
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        return root

    def db_element(self):
        db_obj = self.root.find(".//" + self.balise_format("ObjectDefinition")).find(self.balise_format("Database"))
        return db_obj

    def catalog_name(self):
        # CATALOG_NAME
        catalog = self.db_element.find(self.balise_format("Name")).text
        return catalog

    def cube_name(self, cube):
        cube_name = cube.find(self.balise_format("Name")).text
        return cube_name

    def extract_from_connectionString(self, str_datasource):
        return super().extract_from_connectionString(str_datasource)

    def datasource(self):
        # Récupérer la datasource
        str_datasource = self.db_element.find(self.balise_format("DataSources")).find(
            self.balise_format("DataSource")).find(
            self.balise_format("ConnectionString")).text
        return self.extract_from_connectionString(str_datasource)

    def insert_structure(self, values):
        return super().insert_structure(values)

    def dims_catalog_name(self):
        dim_name_list = []
        dimensions = self.dim_catalog()
        for dimension in dimensions:
            dim_name = dimension.find(self.balise_format("Name")).text
            dim_name_list.append(dim_name)
        return dim_name_list

    def cubes_name(self):
        cubes_name_list = []
        for cube in self.cubes():
            cubes_name_list.append(self.cube_name(cube))
        return cubes_name_list

    def setup(self):
        pattern = r'{(.*)}'
        regex = re.match(pattern, self.root.tag)
        namespace = regex.group()
        return namespace

    def balise_format(self, balise_name):
        formatted = f"{self.namespace}{balise_name}"
        return formatted

    def dim_catalog(self):
        # Récupérer les dimensions à la source
        dimensions = self.db_element.find(self.balise_format("Dimensions")).findall(self.balise_format("Dimension"))
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
        cubes = self.db_element.find(self.balise_format("Cubes")).findall(self.balise_format("Cube"))
        return cubes

    def cube_dimensions_usage(self, cube):
        expression = ""
        is_measure = 0
        is_dimension = 1
        is_calculated = 0
        c_dims = cube.find(self.balise_format("Dimensions")).findall(self.balise_format("Dimension"))
        for c_dim in c_dims:
            group_name = c_dim.find(self.balise_format("Name")).text
            dimension_id = c_dim.find(self.balise_format("DimensionID")).text
            attributes = c_dim.find(self.balise_format("Attributes")).findall(self.balise_format("Attribute"))
            for attribute in attributes:
                is_visible = 1
                column_name = attribute.find(self.balise_format("AttributeID")).text
                if attribute.find(self.balise_format("AttributeHierarchyVisible")) is not None:
                    is_visible = 0
                dim_dict = self.dim_metadata()
                for i in range(len(dim_dict[dimension_id]["Attribute_id"])):

                    if dim_dict[dimension_id]["Attribute_id"][i] == column_name:
                        data_type = dim_dict[dimension_id]["Datatype"][i]
                        src_column = dim_dict[dimension_id]["Column"][i]
                        src_table = dim_dict[dimension_id]["Table"][i]
                        if re.match(r"dbo_",src_table):
                            src_table = src_table[4:]
                        new_values = [column_name, "", data_type, is_calculated, is_measure, is_dimension, expression,
                                      is_visible,
                                      group_name, self.cube_name(cube), self.catalog_name(),
                                      f"{src_column}/{src_table}"]
                        self.insert_structure(new_values)
        return

    def cube_measures(self, cube):
        expression = ""
        is_measure = 1
        is_dimension = 0
        is_calculated = 0
        is_visible = 1
        measure_groups = cube.find(self.balise_format("MeasureGroups")).findall(self.balise_format("MeasureGroup"))
        for measure_group in measure_groups:
            group_name = measure_group.find(self.balise_format("Name")).text
            measures = measure_group.find(self.balise_format("Measures")).findall(self.balise_format("Measure"))
            for measure in measures:
                column_name = measure.find(self.balise_format("Name")).text
                data_type = measure.find(self.balise_format("DataType")).text
                source = measure.find(self.balise_format("Source"))
                sub_source = source.find(self.balise_format("Source"))
                src_table = sub_source.find(self.balise_format("TableID")).text
                if re.match(r"dbo_", src_table):
                    src_table = src_table[4:]
                if sub_source.attrib.get("{http://www.w3.org/2001/XMLSchema-instance}type") == "ColumnBinding":
                    src_column = sub_source.find(self.balise_format("ColumnID")).text
                else:
                    src_column = ""
                new_values = [column_name, "", data_type, is_calculated, is_measure, is_dimension, expression,
                              is_visible, group_name,
                              self.cube_name(cube), self.catalog_name(),
                              f"{src_column}/{src_table}"]
                self.insert_structure(new_values)
        return

    def analyse_calculate(self, raw_text, cube):
        is_calculated = 1
        is_measure = 1
        is_dimension = 0
        group_name = 'Unknown'
        is_visible = 'Unknown'
        data_type = 'Unknown'
        src=''
        text = re.split('CALCULATE;', raw_text)
        calculates = re.split(r'CREATE', text[1].strip(), re.DOTALL)
        calculates = calculates[1:]
        # print("=============================")
        # print(len(calculates))
        # print("Calcultes QUERY:\n", calculates)
        # print("=============================")
        for element in calculates:
            element = re.split(r'\sAS\s', element)
            index = re.search(r'Measures', element[0]).end()
            calculate_name = element[0][index + 2:].strip()
            calculate_name = calculate_name[1:-1]
            # print("=============================")
            # print("CALCULATE NAME:", calculate_name)
            # print("=============================")
            split_pattern = r'(\b[A-Z_]+\s=.*,)'
            variables = re.split(split_pattern, element[1], re.DOTALL)
            # print("=============================")
            # print("VARIABLES", len(variables))
            # print(variables)
            # print("=============================")

            expression = variables[0]
            value_pattern = r'=\s+["\']? (\w)+["\']?"\s+[,;]$'
            for parameter in variables[1:]:
                if re.search(r'FORMAT_STRING', parameter):
                    data_type = parameter[parameter.index("=")+1:]
                    data_type = data_type.replace('"','')
                    data_type = data_type.replace(',','')
                    data_type = data_type.strip()
                    # print('data_type:', data_type)
                elif re.search(r'VISIBLE', parameter):
                    is_visible = parameter[parameter.index("=")+1:]
                    is_visible = is_visible.replace(',', '')
                    is_visible = is_visible.strip()
                    is_visible = int(is_visible)
                    # print('is_visible:', is_visible)
                elif re.search(r'ASSOCIATED_MEASURE_GROUP', parameter):
                    group_name = parameter[parameter.index("=")+1:]
                    group_name = group_name.replace("'", '')
                    group_name = group_name.replace(';', '')
                    group_name = group_name.strip()
                    # print('group_name:', group_name)
                else:
                    pass
                    # print('OTHER PARAMETER:',parameter)

            new_values = [calculate_name, '', data_type, is_calculated, is_measure, is_dimension, expression,
                          is_visible, group_name, self.cube_name(cube), self.catalog_name(), src]
            self.insert_structure(new_values)
        return

    def cube_calculate(self, cube):
        mdxscript = cube.find(self.balise_format("MdxScripts"))
        if mdxscript is not None:
            calculate_group = mdxscript.find(self.balise_format("MdxScript"))
            raw_text = calculate_group.find(self.balise_format("Commands")).find(self.balise_format("Command")).find(
                self.balise_format("Text")).text
            self.analyse_calculate(raw_text, cube)
        return

    def create_cube_struct(self):
        for cube in self.cubes():
            self.cube_dimensions_usage(cube)
            self.cube_measures(cube)
            self.cube_calculate(cube)

    def build_save_filename(self):
        return [self.catalog_name(), "mutldidim", str(len(self.cubes()))]

    def save(self, save_path=None, filename=None):
        super().save(save_path, filename)
        return


if __name__ == "__main__":
    print('Need to convert ETCC')
