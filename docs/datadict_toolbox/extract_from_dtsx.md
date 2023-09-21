extract_from_dtsx.py
This documentation file was created on 21 September 2023 at 14:00:37

## File path

.\datadict_toolbox\extract_from_dtsx.py

## Objectif du fichier

Ce fichier est utilis� pour extraire des informations sp�cifiques � partir de fichiers .dtsx (Data Transformation Services packages). Il contient plusieurs fonctions pour ouvrir les fichiers .dtsx, extraire des requ�tes ERP, extraire des mappages SSIS, extraire des variables et enregistrer les r�sultats dans un fichier JSON.

## Codebase

### Imports: 

1. ```python 
   import xml.etree.ElementTree as ET
   ```
   Le module `xml.etree.ElementTree` est g�n�ralement utilis� pour analyser et cr�er des donn�es XML. Dans ce fichier, il est utilis� pour analyser les fichiers .dtsx et extraire les informations n�cessaires.

2. ```python 
   import os
   ```
   Le module `os` fournit une mani�re portable d'utiliser les fonctionnalit�s d�pendantes du syst�me d'exploitation. Dans ce fichier, il est utilis� pour obtenir des variables d'environnement et manipuler les chemins de fichiers.

3. ```python 
   import json
   ```
   Le module `json` est utilis� pour travailler avec des donn�es JSON. Dans ce fichier, il est utilis� pour enregistrer les r�sultats extraits dans un fichier JSON.

4. ```python 
   import re
   ```
   Le module `re` est utilis� pour travailler avec des expressions r�guli�res. Dans ce fichier, il est utilis� pour extraire des informations sp�cifiques � partir de cha�nes de caract�res.

***

### Variables:

#### Variable: DASH_LINE

Objectif: Cette variable est utilis�e pour stocker une valeur d'environnement sp�cifique. Son but exact n'est pas clair dans ce fichier car elle n'est pas utilis�e.

***

### M�thodes:  

#### M�thode: ```python dtsx_open(file_path) ```

Objectif: Cette fonction est utilis�e pour ouvrir un fichier .dtsx et retourner sa racine et son espace de noms.

#### M�thode: ```python extract_erp_query(file_path_list,print_files=0) ```

Objectif: Cette fonction est utilis�e pour extraire des requ�tes ERP � partir d'une liste de fichiers .dtsx.

#### M�thode: ```python extract_ssis_mapping(file_path) ```

Objectif: Cette fonction est utilis�e pour extraire des mappages SSIS � partir d'un fichier .dtsx.

#### M�thode: ```python extract_variable(file_path) ```

Objectif: Cette fonction est utilis�e pour extraire toutes les variables de transformation � partir d'un fichier .dtsx.

#### M�thode: ```python saveAsJson(dictionary,json_file_name = "Queries.json") ```

Objectif: Cette fonction est utilis�e pour enregistrer un dictionnaire de donn�es dans un fichier JSON.

#### M�thode: ```python if __name__ == "__main__": ```

Objectif: Cette section du code est ex�cut�e lorsque le fichier est ex�cut� directement. Elle appelle les fonctions d�finies pr�c�demment pour extraire des informations � partir des fichiers .dtsx et les enregistrer dans un fichier JSON.
