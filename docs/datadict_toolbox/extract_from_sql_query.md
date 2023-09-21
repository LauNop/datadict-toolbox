extract_from_sql_query.py
This documentation file was created on 21 September 2023 at 14:01:47

## File path

.\datadict_toolbox\extract_from_sql_query.py

## Objectif du fichier

Ce fichier est une tentative d'extraire des informations à partir d'une requête SQL SELECT. Il contient une classe principale `SQLDeduce` qui analyse une requête SQL et extrait des informations pertinentes, et une classe auxiliaire `Nester` qui aide à gérer les sous-requêtes imbriquées.

## Codebase

### Imports: 

1. ```python 
   import re
   ```
   Le module `re` est utilisé pour les expressions régulières. Il est utilisé dans ce fichier pour analyser la requête SQL et extraire des informations spécifiques.

2. ```python 
   import json
   ```
   Le module `json` est utilisé pour lire un fichier JSON qui contient des mots-clés SQL. Ces mots-clés sont utilisés pour analyser la requête SQL.

***

### Classes

#### Classe: SQLDeduce 

Objectif: Cette classe est utilisée pour analyser une requête SQL et extraire des informations pertinentes.

##### Méthodes: méthodes de la classe

1. ```python 
   __init__(self, query)
   ```
   
   Initialise la classe avec une requête SQL et effectue une série d'analyses sur cette requête.
   
   ##### Variables:
   
   - self.query : contient la requête SQL à analyser.
   - self.__keywords : contient les mots-clés SQL extraits d'un fichier JSON.
   - self.__kw_pos_in_query : contient les positions des mots-clés dans la requête.
   - self.__kw_count_in_query : contient le nombre d'occurrences de chaque mot-clé dans la requête.
   - self.__kw_in_query : contient les mots-clés utilisés dans la requête.
   - self.__is_got_subqueries : un booléen indiquant si la requête contient des sous-requêtes.
   - self.__all_tables : contient les noms de toutes les tables mentionnées dans la requête.
   - self.relation_list : une liste vide qui sera utilisée pour stocker les relations entre les tables.
   - self.inner_alias : une variable qui sera utilisée pour stocker un alias interne.

2. ```python 
   get_kw_pos(self)
   ```
   
   Retourne les positions des mots-clés dans la requête.
   
3. ```python 
   get_kw_count(self)
   ```
   
   Retourne le nombre d'occurrences de chaque mot-clé dans la requête.
   
4. ```python 
   get_kw_query(self)
   ```
   
   Retourne les mots-clés utilisés dans la requête.
   
5. ```python 
   get_is_got_subqueries(self)
   ```
   
   Retourne un booléen indiquant si la requête contient des sous-requêtes.
   
6. ```python 
   get_all_tables(self)
   ```
   
   Retourne les noms de toutes les tables mentionnées dans la requête.
   
7. ```python 
   clean(self)
   ```
   
   Nettoie la requête en supprimant les sauts de ligne.
   
8. ```python 
   is_correct(self)
   ```
   
   Vérifie si la requête est correcte en comparant le nombre de "select" et de "from".
   
9. ```python 
   query_split(self)
   ```
   
   Divise la requête en sous-requêtes en utilisant le point-virgule comme séparateur.
   
10. ```python 
    query_type(self)
    ```
    
    Détermine le type de la requête (actuellement, ne gère que les requêtes SELECT).
    
11. ```python 
    keyword_table(self)
    ```
    
    Charge les mots-clés SQL à partir d'un fichier JSON.
    
12. ```python 
    keyword_without_as(self)
    ```
    
    Retourne la liste des mots-clés sans le mot-clé "AS".
    
13. ```python 
    keywords_pos(self, string_to_match=None)
    ```
    
    Trouve les positions des mots-clés dans la requête.
    
14. ```python 
    found_parse(self)
    ```
    
    Trouve les parenthèses dans la requête.
    
15. ```python 
    useless_parse_pop(self, kw_parse_list)
    ```
    
    Supprime les parenthèses inutiles de la liste.
    
16. ```python 
    keyword_parse_pos(self)
    ```
    
    Trouve les positions des mots-clés et des parenthèses dans la requête.
    
17. ```python 
    keywords_count(self, string_to_match=None)
    ```
    
    Compte le nombre d'occurrences de chaque mot-clé dans la requête.
    
18. ```python 
    keywords_used(self, dict_to_filter=None)
    ```
    
    Retourne les mots-clés utilisés dans la requête.
    
19. ```python 
    nest_keyword(self, list_to_nest=None)
    ```
    
    Niche les mots-clés dans la requête.
    
20. ```python 
    build_select_tree(self)
    ```
    
    Construit un arbre à partir de la requête SELECT.
    
21. ```python 
    deduce_from_tree(self, start_key=0)
    ```
    
    Déduit des informations à partir de l'arbre de la requête.
    
22. ```python 
    decrypt_table_node(self, node)
    ```
    
    Déchiffre un nœud de table dans l'arbre de la requête.
    
23. ```python 
    decrypt_SF_node(self,node)
    ```
    
    Déchiffre un nœud SelectFrom dans l'arbre de la requête.
    
24. ```python 
    between_2_keywords(self, keyword_before, keyword_after)
    ```
    
    Trouve le texte entre deux mots-clés dans la requête.
    
25. ```python 
    between_select_from(self)
    ```
    
    Trouve le texte entre "select" et "from" dans la requête.
    
26. ```python 
    check_after_split(self, string_list)
    ```
    
    Vérifie la liste des chaînes après la division.
    
27. ```python 
    split_column_expression(self,start,end)
    ```
    
    Divise l'expression de colonne dans la requête.
    
28. ```python 
    analyse_column_expression(self)
    ```
    
    Analyse l'expression de colonne dans la requête.
    
29. ```python 
    deduce_column_expression(self, column_expression)
    ```
    
    Déduit l'expression de colonne dans la requête.
    
30. ```python 
    deduce_column_expression_list(self, list_column_exp)
    ```
    
    Déduit la liste des expressions de colonnes dans la requête.
    
31. ```python 
    is_got_subqueries(self)
    ```
    
    Vérifie si la requête contient des sous-requêtes.
    
32. ```python 
    table_statement(self)
    ```
    
    Trouve les déclarations de table dans la requête.
    
33. ```python 
    is_table_name(self, table_statement)
    ```
    
    Vérifie si une déclaration est un nom de table.
    
34. ```python 
    table_alias(self, table_statement)
    ```
    
    Trouve l'alias de la table dans la déclaration.
    
35. ```python 
    analyse_tables(self)
    ```
    
    Analyse les tables dans la requête.

#### Classe: Nester 

Objectif: Cette classe aide à gérer les sous-requêtes imbriquées.

##### Méthodes: méthodes de la classe

1. ```python 
   __init__(self)
   ```
   
   Initialise la classe avec une liste vide et un booléen indiquant si elle est en train de créer une sous-requête.
   
2. ```python 
   add(self, nester)
   ```
   
   Ajoute une sous-requête à la liste.
   
3. ```python 
   append(self, element)
   ```
   
   Ajoute un élément à la sous-requête en cours.
   
4. ```python 
   submit(self)
   ```
   
   Soumet la sous-requête en cours et la retire de la liste.

***

### Méthodes:  

Il n'y a pas de méthodes en dehors des classes dans ce fichier.

***

### Variables:

Il n'y a pas de variables globales en dehors des fonctions et des classes dans ce fichier.
