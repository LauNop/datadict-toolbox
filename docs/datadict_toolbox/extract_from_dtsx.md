extract_from_dtsx.py
This documentation file was created on 21 September 2023 at 14:00:37

## File path

.\datadict_toolbox\extract_from_dtsx.py

## Objectif du fichier

Ce fichier est utilisé pour extraire des informations spécifiques à partir de fichiers .dtsx (Data Transformation Services packages). Il contient plusieurs fonctions pour ouvrir les fichiers .dtsx, extraire des requêtes ERP, extraire des mappages SSIS, extraire des variables et enregistrer les résultats dans un fichier JSON.

## Codebase

### Imports: 

1. ```python 
   import xml.etree.ElementTree as ET
   ```
   Le module `xml.etree.ElementTree` est généralement utilisé pour analyser et créer des données XML. Dans ce fichier, il est utilisé pour analyser les fichiers .dtsx et extraire les informations nécessaires.

2. ```python 
   import os
   ```
   Le module `os` fournit une manière portable d'utiliser les fonctionnalités dépendantes du système d'exploitation. Dans ce fichier, il est utilisé pour obtenir des variables d'environnement et manipuler les chemins de fichiers.

3. ```python 
   import json
   ```
   Le module `json` est utilisé pour travailler avec des données JSON. Dans ce fichier, il est utilisé pour enregistrer les résultats extraits dans un fichier JSON.

4. ```python 
   import re
   ```
   Le module `re` est utilisé pour travailler avec des expressions régulières. Dans ce fichier, il est utilisé pour extraire des informations spécifiques à partir de chaînes de caractères.

***

### Variables:

#### Variable: DASH_LINE

Objectif: Cette variable est utilisée pour stocker une valeur d'environnement spécifique. Son but exact n'est pas clair dans ce fichier car elle n'est pas utilisée.

***

### Méthodes:  

#### Méthode: ```python dtsx_open(file_path) ```

Objectif: Cette fonction est utilisée pour ouvrir un fichier .dtsx et retourner sa racine et son espace de noms.

#### Méthode: ```python extract_erp_query(file_path_list,print_files=0) ```

Objectif: Cette fonction est utilisée pour extraire des requêtes ERP à partir d'une liste de fichiers .dtsx.

#### Méthode: ```python extract_ssis_mapping(file_path) ```

Objectif: Cette fonction est utilisée pour extraire des mappages SSIS à partir d'un fichier .dtsx.

#### Méthode: ```python extract_variable(file_path) ```

Objectif: Cette fonction est utilisée pour extraire toutes les variables de transformation à partir d'un fichier .dtsx.

#### Méthode: ```python saveAsJson(dictionary,json_file_name = "Queries.json") ```

Objectif: Cette fonction est utilisée pour enregistrer un dictionnaire de données dans un fichier JSON.

#### Méthode: ```python if __name__ == "__main__": ```

Objectif: Cette section du code est exécutée lorsque le fichier est exécuté directement. Elle appelle les fonctions définies précédemment pour extraire des informations à partir des fichiers .dtsx et les enregistrer dans un fichier JSON.
