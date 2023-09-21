extract_from_xmla.py
This documentation file was created on 21 September 2023 at 14:04:57

## File path

.\datadict_toolbox\extract_from_xmla.py

## Objectif du fichier

Ce fichier est destin� � extraire des informations structur�es � partir de fichiers de configuration de cubes de donn�es. Il d�finit deux classes principales, `ExtractorTabularCubeCatalog` et `ExtractorMultidimCubeCatalog`, qui h�ritent d'une classe abstraite `Extractor`. Ces classes sont utilis�es pour extraire des informations � partir de fichiers de configuration de cubes de donn�es tabulaires et multidimensionnels respectivement.

## Codebase

### Imports: 

1. ```python 
   import xml.etree.ElementTree as ET
   ```
   `xml.etree.ElementTree` est un module Python qui fournit des m�thodes pour analyser et cr�er des documents XML. Dans ce fichier, il est utilis� pour analyser les fichiers XML qui contiennent la configuration des cubes de donn�es multidimensionnels.

2. ```python 
   import json
   ```
   Le module `json` est utilis� pour travailler avec des donn�es JSON. Dans ce fichier, il est utilis� pour lire et analyser les fichiers JSON qui contiennent la configuration des cubes de donn�es tabulaires.

3. ```python 
   import pandas as pd
   ```
   `pandas` est une biblioth�que Python qui fournit des structures de donn�es et des fonctions d'analyse de donn�es. Dans ce fichier, il est utilis� pour cr�er des DataFrames � partir des donn�es extraites des fichiers de configuration des cubes de donn�es.

4. ```python 
   import os
   ```
   Le module `os` fournit une mani�re portable d'utiliser les fonctionnalit�s d�pendantes du syst�me d'exploitation. Dans ce fichier, il est utilis� pour v�rifier l'existence de dossiers et pour cr�er des dossiers si n�cessaire.

5. ```python 
   import re
   ```
   Le module `re` fournit des fonctions pour travailler avec des expressions r�guli�res. Dans ce fichier, il est utilis� pour analyser les cha�nes de connexion et pour extraire des informations � partir des commandes MDX.

6. ```python 
   from abc import ABC, abstractmethod
   ```
   Le module `abc` fournit le m�canisme de base pour d�finir les classes de base abstraites (ABC) en Python. Dans ce fichier, il est utilis� pour d�finir la classe `Extractor` comme une classe abstraite.

***

### Classes

#### Classe : Extractor 

Objectif : Cette classe est une classe de base abstraite qui d�finit l'interface pour les classes d'extraction de cubes de donn�es. Elle d�finit des m�thodes abstraites qui doivent �tre impl�ment�es par les classes d�riv�es.

##### M�thodes : m�thodes de la classe

1. ```python 
   __init__(self, file_path)
   ```
   Initialise la classe avec le chemin du fichier � analyser. Il initialise �galement `cube_struct` � None, qui sera utilis� pour stocker la structure du cube de donn�es.

   ##### Variables :
   - `self.cube_struct` : utilis� pour stocker la structure du cube de donn�es.
   - `self.file_path` : le chemin du fichier � analyser.

2. ```python 
   build_cube_dict(self)
   ```
   M�thode abstraite qui doit �tre impl�ment�e par les classes d�riv�es. Elle est destin�e � construire un dictionnaire qui repr�sente la structure du cube de donn�es.

3. ```python 
   open_file(self)
   ```
   M�thode abstraite qui doit �tre impl�ment�e par les classes d�riv�es. Elle est destin�e � ouvrir le fichier de configuration du cube de donn�es.

4. ```python 
   db_element(self)
   ```
   M�thode abstraite qui doit �tre impl�ment�e par les classes d�riv�es. Elle est destin�e � extraire l'�l�ment de base de donn�es � partir du fichier de configuration du cube de donn�es.

5. ```python 
   catalog_name(self)
   ```
   M�thode abstraite qui doit �tre impl�ment�e par les classes d�riv�es. Elle est destin�e � extraire le nom du catalogue � partir du fichier de configuration du cube de donn�es.

6. ```python 
   cube_name(self)
   ```
   M�thode qui peut �tre surcharg�e par les classes d�riv�es. Elle est destin�e � extraire le nom du cube � partir du fichier de configuration du cube de donn�es.

7. ```python 
   extract_from_connectionString(self, str_datasource)
   ```
   M�thode qui analyse une cha�ne de connexion et extrait le nom de la base de donn�es source et l'adresse IP du serveur.

8. ```python 
   datasource(self)
   ```
   M�thode abstraite qui doit �tre impl�ment�e par les classes d�riv�es. Elle est destin�e � extraire la cha�ne de connexion � la source de donn�es � partir du fichier de configuration du cube de donn�es.

9. ```python 
   insert_structure(self, values)
   ```
   M�thode abstraite qui doit �tre impl�ment�e par les classes d�riv�es. Elle est destin�e � ins�rer des valeurs dans la structure du cube de donn�es.

10. ```python 
    create_cube_struct(self)
    ```
    M�thode abstraite qui doit �tre impl�ment�e par les classes d�riv�es. Elle est destin�e � cr�er la structure du cube de donn�es � partir du fichier de configuration du cube de donn�es.

11. ```python 
    build_save_path(self)
    ```
    M�thode abstraite qui doit �tre impl�ment�e par les classes d�riv�es. Elle est destin�e � construire le chemin o� le cube de donn�es sera enregistr�.

12. ```python 
    save(self, path=None)
    ```
    M�thode qui enregistre la structure du cube de donn�es dans un fichier Excel. Si aucun chemin n'est fourni, elle construit le chemin en utilisant la m�thode `build_save_path`.

13. ```python 
    setup(self)
    ```
    M�thode abstraite qui doit �tre impl�ment�e par les classes d�riv�es. Elle est destin�e � effectuer toute configuration n�cessaire avant l'extraction des donn�es.

#### Classe : ExtractorTabularCubeCatalog 

Objectif : Cette classe est une classe d�riv�e de `Extractor` qui est utilis�e pour extraire des informations � partir de fichiers de configuration de cubes de donn�es tabulaires.

#### Classe : ExtractorMultidimCubeCatalog 

Objectif : Cette classe est une classe d�riv�e de `Extractor` qui est utilis�e pour extraire des informations � partir de fichiers de configuration de cubes de donn�es multidimensionnels.

***

### M�thodes:  

Il n'y a pas de m�thodes en dehors des classes dans ce fichier.

***

### Variables:

Il n'y a pas de variables globales en dehors des fonctions et des classes dans ce fichier.
