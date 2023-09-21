extract_from_xmla.py
This documentation file was created on 21 September 2023 at 14:04:57

## File path

.\datadict_toolbox\extract_from_xmla.py

## Objectif du fichier

Ce fichier est destiné à extraire des informations structurées à partir de fichiers de configuration de cubes de données. Il définit deux classes principales, `ExtractorTabularCubeCatalog` et `ExtractorMultidimCubeCatalog`, qui héritent d'une classe abstraite `Extractor`. Ces classes sont utilisées pour extraire des informations à partir de fichiers de configuration de cubes de données tabulaires et multidimensionnels respectivement.

## Codebase

### Imports: 

1. ```python 
   import xml.etree.ElementTree as ET
   ```
   `xml.etree.ElementTree` est un module Python qui fournit des méthodes pour analyser et créer des documents XML. Dans ce fichier, il est utilisé pour analyser les fichiers XML qui contiennent la configuration des cubes de données multidimensionnels.

2. ```python 
   import json
   ```
   Le module `json` est utilisé pour travailler avec des données JSON. Dans ce fichier, il est utilisé pour lire et analyser les fichiers JSON qui contiennent la configuration des cubes de données tabulaires.

3. ```python 
   import pandas as pd
   ```
   `pandas` est une bibliothèque Python qui fournit des structures de données et des fonctions d'analyse de données. Dans ce fichier, il est utilisé pour créer des DataFrames à partir des données extraites des fichiers de configuration des cubes de données.

4. ```python 
   import os
   ```
   Le module `os` fournit une manière portable d'utiliser les fonctionnalités dépendantes du système d'exploitation. Dans ce fichier, il est utilisé pour vérifier l'existence de dossiers et pour créer des dossiers si nécessaire.

5. ```python 
   import re
   ```
   Le module `re` fournit des fonctions pour travailler avec des expressions régulières. Dans ce fichier, il est utilisé pour analyser les chaînes de connexion et pour extraire des informations à partir des commandes MDX.

6. ```python 
   from abc import ABC, abstractmethod
   ```
   Le module `abc` fournit le mécanisme de base pour définir les classes de base abstraites (ABC) en Python. Dans ce fichier, il est utilisé pour définir la classe `Extractor` comme une classe abstraite.

***

### Classes

#### Classe : Extractor 

Objectif : Cette classe est une classe de base abstraite qui définit l'interface pour les classes d'extraction de cubes de données. Elle définit des méthodes abstraites qui doivent être implémentées par les classes dérivées.

##### Méthodes : méthodes de la classe

1. ```python 
   __init__(self, file_path)
   ```
   Initialise la classe avec le chemin du fichier à analyser. Il initialise également `cube_struct` à None, qui sera utilisé pour stocker la structure du cube de données.

   ##### Variables :
   - `self.cube_struct` : utilisé pour stocker la structure du cube de données.
   - `self.file_path` : le chemin du fichier à analyser.

2. ```python 
   build_cube_dict(self)
   ```
   Méthode abstraite qui doit être implémentée par les classes dérivées. Elle est destinée à construire un dictionnaire qui représente la structure du cube de données.

3. ```python 
   open_file(self)
   ```
   Méthode abstraite qui doit être implémentée par les classes dérivées. Elle est destinée à ouvrir le fichier de configuration du cube de données.

4. ```python 
   db_element(self)
   ```
   Méthode abstraite qui doit être implémentée par les classes dérivées. Elle est destinée à extraire l'élément de base de données à partir du fichier de configuration du cube de données.

5. ```python 
   catalog_name(self)
   ```
   Méthode abstraite qui doit être implémentée par les classes dérivées. Elle est destinée à extraire le nom du catalogue à partir du fichier de configuration du cube de données.

6. ```python 
   cube_name(self)
   ```
   Méthode qui peut être surchargée par les classes dérivées. Elle est destinée à extraire le nom du cube à partir du fichier de configuration du cube de données.

7. ```python 
   extract_from_connectionString(self, str_datasource)
   ```
   Méthode qui analyse une chaîne de connexion et extrait le nom de la base de données source et l'adresse IP du serveur.

8. ```python 
   datasource(self)
   ```
   Méthode abstraite qui doit être implémentée par les classes dérivées. Elle est destinée à extraire la chaîne de connexion à la source de données à partir du fichier de configuration du cube de données.

9. ```python 
   insert_structure(self, values)
   ```
   Méthode abstraite qui doit être implémentée par les classes dérivées. Elle est destinée à insérer des valeurs dans la structure du cube de données.

10. ```python 
    create_cube_struct(self)
    ```
    Méthode abstraite qui doit être implémentée par les classes dérivées. Elle est destinée à créer la structure du cube de données à partir du fichier de configuration du cube de données.

11. ```python 
    build_save_path(self)
    ```
    Méthode abstraite qui doit être implémentée par les classes dérivées. Elle est destinée à construire le chemin où le cube de données sera enregistré.

12. ```python 
    save(self, path=None)
    ```
    Méthode qui enregistre la structure du cube de données dans un fichier Excel. Si aucun chemin n'est fourni, elle construit le chemin en utilisant la méthode `build_save_path`.

13. ```python 
    setup(self)
    ```
    Méthode abstraite qui doit être implémentée par les classes dérivées. Elle est destinée à effectuer toute configuration nécessaire avant l'extraction des données.

#### Classe : ExtractorTabularCubeCatalog 

Objectif : Cette classe est une classe dérivée de `Extractor` qui est utilisée pour extraire des informations à partir de fichiers de configuration de cubes de données tabulaires.

#### Classe : ExtractorMultidimCubeCatalog 

Objectif : Cette classe est une classe dérivée de `Extractor` qui est utilisée pour extraire des informations à partir de fichiers de configuration de cubes de données multidimensionnels.

***

### Méthodes:  

Il n'y a pas de méthodes en dehors des classes dans ce fichier.

***

### Variables:

Il n'y a pas de variables globales en dehors des fonctions et des classes dans ce fichier.
