# Dictionary_ToolBox (v1.0.1)

Dictionary_ToolBox is a python package containing classes for building a tabular, multidimensional cube data dictionary and SQL select queries using OpenAI's GPT templates.

This package processes `.xmla` files generated by MS SQL SERVER software. 

Extracts SQL queries from `.dtsx` files.

Generates a partial data dictionary from a SQL select query.

## Installation
***
You can install `datadict_toolbox` using `pip` from the Python Package Index (PyPI).

```bash
pip install datadict_toolbox
```

The package is hosted on PyPI and can be found at <https://pypi.org/project/datadict-toolbox/>. You can visit the link for more information about the package and its available versions.

## Setup
***
Before you start using DataDict Toolbox, you need to set up a suitable Python environment. We recommend using a virtual environment (venv). Here's how you can set this up:

1. Install a Python  Interpreter (3.9) minimum. You can download it from the official Python website. Make sure to allow the installer to set the PATH variables for you.

2. Check your Python version by running `python --version` or `python3 --version` from the command line.

3. Once you have Python, you can create a virtual environment or it's automatically generated in IDE as Pycharm. To do this, run the following command in the root directory of the project:

   ```bash
   python -m venv venv
   ```

   This command creates a new directory named `venv` in your project. This directory will contain the Python executable files and a copy of the pip library which you can use to install other packages within this environment.

4. To start using this environment, you have to activate it.

   On Unix or MacOS, run:

   ```bash
   source venv/bin/activate
   ```

   On Windows, run:

   ```bash
   venv\Scripts\activate
   ```

5. Once the virtual environment is activated, you can install the necessary dependencies. To do this, run the following command:

   ```bash
   pip install -r requirements.txt
   ```

6. Now you should be all set! Remember to activate the venv environment every time you work on the project.

7. Finally, ensure you have an OpenAI API key and organization ID. The API key is necessary for making requests to the OpenAI service. To use them safely you must write them in a `.env` file and use the `python-dotenv` Python Package to get the key and id.

## Usage
***
### Importing the package

The easiest way to use the package is to copy the following codes in your `main.py` file to use the different classes :

#### Class: ExtractorTabularCubeCatalog
##### Create a tabular cube data dictionary from one .xmla file

```python
from datadict_toolbox import ExtractorTabularCubeCatalog
file_path = "paste the path of your .xmla file"
etcc = ExtractorTabularCubeCatalog(file_path) # Generate the data dictionary at the Instance of the class
print(etcc.cube_struct) # Display the python dictionary that contain your data dictionary
etcc.save() # By default it will create a "catalog_name_tabular_nbrtable.xslx" in a "excel_result/" folder automatically created in the root path of your running .py file
```

##### Create several tabular cube data dictionary from a folder of .xmla files

```python
import os
from datadict_toolbox import ExtractorTabularCubeCatalog
folder_path = "paste the path of the folder containing your .xmla files"
files_path = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
                      os.path.isfile(os.path.join(folder_path, f))]
print("Nbr fichier: ", len(files_path))
for file_path in files_path:
    etcc = ExtractorTabularCubeCatalog(file_path) # Generate the data dictionary at the Instance of the class
    print(etcc.cube_struct) # Display the python dictionary that contain your data dictionary
    etcc.save() # By default it will create a "catalog_name_tabular_nbrtable.xslx" in a "excel_result/" folder automatically created in the root path of your running .py file
```
You can change the save path and the filename of the `.xlsx` file by changing the `save_path` and `filename` parameters.

#### Class: ExtractorMultidimCubeCatalog
##### Create a multidimensional cube data dictionary from one .xmla file

```python
from datadict_toolbox import ExtractorMultidimCubeCatalog
file_path = "paste the path of your .xmla file"
emcc = ExtractorMultidimCubeCatalog(file_path) # Generate the data dictionary at the Instance of the class
print(emcc.cube_struct) # Display the python dictionary that contain your data dictionary
emcc.save() # By default it will create a "catalog_name_tabular_nbrtable.xslx" in a "excel_result/" folder automatically created in the root path of your running .py file
```

##### Create several multidimensional cube data dictionary from a folder of .xmla files

```python
import os
from datadict_toolbox import ExtractorMultidimCubeCatalog
folder_path = "paste the path of the folder containing your .xmla files"
files_path = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
                      os.path.isfile(os.path.join(folder_path, f))]
print("Nbr fichier: ", len(files_path))
for file_path in files_path:
    emcc = ExtractorMultidimCubeCatalog(file_path) # Generate the data dictionary at the Instance of the class
    print(emcc.cube_struct) # Display the python dictionary that contain your data dictionary
    emcc.save() # By default it will create a "catalog_name_tabular_nbrtable.xslx" in a "excel_result/" folder automatically created in the root path of your running .py file
```
You can change the save path and the filename of the `.xlsx` file by changing the `save_path` and `filename` parameters.

#### Class: SelectGPTDeduce
```python
import os
from dotenv import load_dotenv
from datadict_toolbox import SelectGPTDeduce

load_dotenv("path of your .env file relative to your root path")  # load .env file
openai_api_key = os.getenv("OPENAI_API_KEY")  # get OPENAI_KEY value from .env file{}
openai_org_id = os.getenv("OPENAI_ORG_ID")
select_query="paste your SQL select query here"

deduce = SelectGPTDeduce(openai_org_id, openai_api_key, select_query)
print(deduce.select_data_dict) # Display the python dictionary that contain your data dictionary
deduce.save()
```
The `save()` method is not configurable in this version.

#### File: extract_from_dtsx.py

The most usefull function is the `extract_erp_query` which extract the SQL query from a `.dtsx` file.
```python
import os
from datadict_toolbox import extract_erp_query
folder_path = "paste the path of the folder containing your .xmla files"
files_path = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
                      os.path.isfile(os.path.join(folder_path, f))]
queries = extract_erp_query(files_path)['SQL_QUERY']
```
This function takes a list as argument and outputs a dictionary of 2 key `DEST_TABLE` and `SQL_QUERY`.
You can fill in the `SelectGPTDeduce` class the outputs of the `extract_erp_query`.

### CLI
***
No command for this package

## Configuration
***
if you don't have a `.env` file create it and put 2 important variables
```txt
OPENAI_API_KEY="your api key"
OPENAI_ORG_ID="your organization id"
```


The assessment aims to provide comprehensive information that can help a new developer understand the purpose and functionality of the code, as well as areas that could potentially be refactored or optimized.

## Goal
***
This package was done for a internship project. It will probably not be maintained in the future.

## License
***
This project is licensed under the MIT License. See the LICENSE file for details.


