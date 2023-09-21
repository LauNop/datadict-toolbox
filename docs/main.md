main.py
This documentation file was created on 21 September 2023 at 13:59:06

## File path

.\main.py

## Objectif du fichier

Ce fichier est un script Python qui semble être utilisé pour extraire et analyser des informations à partir de différents types de fichiers et de bases de données. Il utilise plusieurs bibliothèques pour accomplir cela, y compris `os`, `env`, `datadict_toolbox` et `re`.

## Codebase

### Imports: 

1. ```python 
   import os
   ```
   Le module `os` est un module Python standard qui fournit des fonctions pour interagir avec le système d'exploitation. Dans ce fichier, il est utilisé pour manipuler les chemins de fichiers et lister les fichiers dans un répertoire.

2. ```python 
   from env import envVar as V
   ```
   Le module `env` semble être un module personnalisé qui contient des variables d'environnement. Il est utilisé pour accéder à des chemins de fichiers spécifiques et à d'autres constantes à travers le script.

3. ```python 
   from datadict_toolbox import SQLDeduce, ExtractorMultidimCubeCatalog as EMCC, ExtractorTabularCubeCatalog as ETCC, SelectGPTDeduce, extract_erp_query, extract_ssis_mapping
   ```
   Le module `datadict_toolbox` semble être une bibliothèque personnalisée qui contient plusieurs classes et fonctions pour extraire et analyser des informations à partir de bases de données et de fichiers. Les classes `SQLDeduce`, `ExtractorMultidimCubeCatalog`, `ExtractorTabularCubeCatalog` et `SelectGPTDeduce` sont utilisées pour extraire et analyser des informations à partir de différents types de bases de données et de fichiers. Les fonctions `extract_erp_query` et `extract_ssis_mapping` sont utilisées pour extraire des informations spécifiques à partir de fichiers.

4. ```python 
   import re
   ```
   Le module `re` est un module Python standard qui fournit des fonctions pour travailler avec des expressions régulières. Il n'est pas utilisé explicitement dans ce script, il est donc possible qu'il soit utilisé dans des parties du code qui ont été commentées.

***

### Méthodes:  

#### Méthode: ```python main(name) ```

Objectif: Cette méthode est le point d'entrée principal du script. Elle prend un argument `name` qui détermine quel type d'opération le script doit effectuer. Selon la valeur de `name`, le script peut extraire et analyser des informations à partir de différents types de fichiers et de bases de données.

#### Méthode: ```python if __name__ == "__main__": main("GPT") ```

Objectif: Cette ligne de code est un idiome courant en Python. Si le script est exécuté directement (plutôt que d'être importé comme un module), cette ligne de code appelle la fonction `main` avec l'argument `"GPT"`. Cela signifie que le script va extraire et analyser des informations à partir de fichiers ou de bases de données spécifiés par le cas "GPT" dans la fonction `main`.

***

### Variables:

#### Variable: `folder_path`

Objectif: Cette variable est utilisée pour stocker le chemin d'accès au répertoire contenant les fichiers à analyser. Sa valeur est déterminée par la valeur de `name` passée à la fonction `main`.

#### Variable: `files_path`

Objectif: Cette variable est une liste de tous les fichiers dans le répertoire spécifié par `folder_path`. Elle est utilisée pour itérer sur tous les fichiers dans le répertoire.

#### Variable: `V`

Objectif: Cette variable est un alias pour le module `envVar` importé du module `env`. Elle est utilisée pour accéder à des constantes spécifiques définies dans ce module, comme les chemins de fichiers et d'autres variables d'environnement.
