main.py
This documentation file was created on 21 September 2023 at 13:59:06

## File path

.\main.py

## Objectif du fichier

Ce fichier est un script Python qui semble �tre utilis� pour extraire et analyser des informations � partir de diff�rents types de fichiers et de bases de donn�es. Il utilise plusieurs biblioth�ques pour accomplir cela, y compris `os`, `env`, `datadict_toolbox` et `re`.

## Codebase

### Imports: 

1. ```python 
   import os
   ```
   Le module `os` est un module Python standard qui fournit des fonctions pour interagir avec le syst�me d'exploitation. Dans ce fichier, il est utilis� pour manipuler les chemins de fichiers et lister les fichiers dans un r�pertoire.

2. ```python 
   from env import envVar as V
   ```
   Le module `env` semble �tre un module personnalis� qui contient des variables d'environnement. Il est utilis� pour acc�der � des chemins de fichiers sp�cifiques et � d'autres constantes � travers le script.

3. ```python 
   from datadict_toolbox import SQLDeduce, ExtractorMultidimCubeCatalog as EMCC, ExtractorTabularCubeCatalog as ETCC, SelectGPTDeduce, extract_erp_query, extract_ssis_mapping
   ```
   Le module `datadict_toolbox` semble �tre une biblioth�que personnalis�e qui contient plusieurs classes et fonctions pour extraire et analyser des informations � partir de bases de donn�es et de fichiers. Les classes `SQLDeduce`, `ExtractorMultidimCubeCatalog`, `ExtractorTabularCubeCatalog` et `SelectGPTDeduce` sont utilis�es pour extraire et analyser des informations � partir de diff�rents types de bases de donn�es et de fichiers. Les fonctions `extract_erp_query` et `extract_ssis_mapping` sont utilis�es pour extraire des informations sp�cifiques � partir de fichiers.

4. ```python 
   import re
   ```
   Le module `re` est un module Python standard qui fournit des fonctions pour travailler avec des expressions r�guli�res. Il n'est pas utilis� explicitement dans ce script, il est donc possible qu'il soit utilis� dans des parties du code qui ont �t� comment�es.

***

### M�thodes:  

#### M�thode: ```python main(name) ```

Objectif: Cette m�thode est le point d'entr�e principal du script. Elle prend un argument `name` qui d�termine quel type d'op�ration le script doit effectuer. Selon la valeur de `name`, le script peut extraire et analyser des informations � partir de diff�rents types de fichiers et de bases de donn�es.

#### M�thode: ```python if __name__ == "__main__": main("GPT") ```

Objectif: Cette ligne de code est un idiome courant en Python. Si le script est ex�cut� directement (plut�t que d'�tre import� comme un module), cette ligne de code appelle la fonction `main` avec l'argument `"GPT"`. Cela signifie que le script va extraire et analyser des informations � partir de fichiers ou de bases de donn�es sp�cifi�s par le cas "GPT" dans la fonction `main`.

***

### Variables:

#### Variable: `folder_path`

Objectif: Cette variable est utilis�e pour stocker le chemin d'acc�s au r�pertoire contenant les fichiers � analyser. Sa valeur est d�termin�e par la valeur de `name` pass�e � la fonction `main`.

#### Variable: `files_path`

Objectif: Cette variable est une liste de tous les fichiers dans le r�pertoire sp�cifi� par `folder_path`. Elle est utilis�e pour it�rer sur tous les fichiers dans le r�pertoire.

#### Variable: `V`

Objectif: Cette variable est un alias pour le module `envVar` import� du module `env`. Elle est utilis�e pour acc�der � des constantes sp�cifiques d�finies dans ce module, comme les chemins de fichiers et d'autres variables d'environnement.
