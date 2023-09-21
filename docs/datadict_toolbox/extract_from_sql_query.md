extract_from_sql_query.py
This documentation file was created on 21 September 2023 at 14:01:47

## File path

.\datadict_toolbox\extract_from_sql_query.py

## Objectif du fichier

Ce fichier est une tentative d'extraire des informations � partir d'une requ�te SQL SELECT. Il contient une classe principale `SQLDeduce` qui analyse une requ�te SQL et extrait des informations pertinentes, et une classe auxiliaire `Nester` qui aide � g�rer les sous-requ�tes imbriqu�es.

## Codebase

### Imports: 

1. ```python 
   import re
   ```
   Le module `re` est utilis� pour les expressions r�guli�res. Il est utilis� dans ce fichier pour analyser la requ�te SQL et extraire des informations sp�cifiques.

2. ```python 
   import json
   ```
   Le module `json` est utilis� pour lire un fichier JSON qui contient des mots-cl�s SQL. Ces mots-cl�s sont utilis�s pour analyser la requ�te SQL.

***

### Classes

#### Classe: SQLDeduce 

Objectif: Cette classe est utilis�e pour analyser une requ�te SQL et extraire des informations pertinentes.

##### M�thodes: m�thodes de la classe

1. ```python 
   __init__(self, query)
   ```
   
   Initialise la classe avec une requ�te SQL et effectue une s�rie d'analyses sur cette requ�te.
   
   ##### Variables:
   
   - self.query : contient la requ�te SQL � analyser.
   - self.__keywords : contient les mots-cl�s SQL extraits d'un fichier JSON.
   - self.__kw_pos_in_query : contient les positions des mots-cl�s dans la requ�te.
   - self.__kw_count_in_query : contient le nombre d'occurrences de chaque mot-cl� dans la requ�te.
   - self.__kw_in_query : contient les mots-cl�s utilis�s dans la requ�te.
   - self.__is_got_subqueries : un bool�en indiquant si la requ�te contient des sous-requ�tes.
   - self.__all_tables : contient les noms de toutes les tables mentionn�es dans la requ�te.
   - self.relation_list : une liste vide qui sera utilis�e pour stocker les relations entre les tables.
   - self.inner_alias : une variable qui sera utilis�e pour stocker un alias interne.

2. ```python 
   get_kw_pos(self)
   ```
   
   Retourne les positions des mots-cl�s dans la requ�te.
   
3. ```python 
   get_kw_count(self)
   ```
   
   Retourne le nombre d'occurrences de chaque mot-cl� dans la requ�te.
   
4. ```python 
   get_kw_query(self)
   ```
   
   Retourne les mots-cl�s utilis�s dans la requ�te.
   
5. ```python 
   get_is_got_subqueries(self)
   ```
   
   Retourne un bool�en indiquant si la requ�te contient des sous-requ�tes.
   
6. ```python 
   get_all_tables(self)
   ```
   
   Retourne les noms de toutes les tables mentionn�es dans la requ�te.
   
7. ```python 
   clean(self)
   ```
   
   Nettoie la requ�te en supprimant les sauts de ligne.
   
8. ```python 
   is_correct(self)
   ```
   
   V�rifie si la requ�te est correcte en comparant le nombre de "select" et de "from".
   
9. ```python 
   query_split(self)
   ```
   
   Divise la requ�te en sous-requ�tes en utilisant le point-virgule comme s�parateur.
   
10. ```python 
    query_type(self)
    ```
    
    D�termine le type de la requ�te (actuellement, ne g�re que les requ�tes SELECT).
    
11. ```python 
    keyword_table(self)
    ```
    
    Charge les mots-cl�s SQL � partir d'un fichier JSON.
    
12. ```python 
    keyword_without_as(self)
    ```
    
    Retourne la liste des mots-cl�s sans le mot-cl� "AS".
    
13. ```python 
    keywords_pos(self, string_to_match=None)
    ```
    
    Trouve les positions des mots-cl�s dans la requ�te.
    
14. ```python 
    found_parse(self)
    ```
    
    Trouve les parenth�ses dans la requ�te.
    
15. ```python 
    useless_parse_pop(self, kw_parse_list)
    ```
    
    Supprime les parenth�ses inutiles de la liste.
    
16. ```python 
    keyword_parse_pos(self)
    ```
    
    Trouve les positions des mots-cl�s et des parenth�ses dans la requ�te.
    
17. ```python 
    keywords_count(self, string_to_match=None)
    ```
    
    Compte le nombre d'occurrences de chaque mot-cl� dans la requ�te.
    
18. ```python 
    keywords_used(self, dict_to_filter=None)
    ```
    
    Retourne les mots-cl�s utilis�s dans la requ�te.
    
19. ```python 
    nest_keyword(self, list_to_nest=None)
    ```
    
    Niche les mots-cl�s dans la requ�te.
    
20. ```python 
    build_select_tree(self)
    ```
    
    Construit un arbre � partir de la requ�te SELECT.
    
21. ```python 
    deduce_from_tree(self, start_key=0)
    ```
    
    D�duit des informations � partir de l'arbre de la requ�te.
    
22. ```python 
    decrypt_table_node(self, node)
    ```
    
    D�chiffre un n�ud de table dans l'arbre de la requ�te.
    
23. ```python 
    decrypt_SF_node(self,node)
    ```
    
    D�chiffre un n�ud SelectFrom dans l'arbre de la requ�te.
    
24. ```python 
    between_2_keywords(self, keyword_before, keyword_after)
    ```
    
    Trouve le texte entre deux mots-cl�s dans la requ�te.
    
25. ```python 
    between_select_from(self)
    ```
    
    Trouve le texte entre "select" et "from" dans la requ�te.
    
26. ```python 
    check_after_split(self, string_list)
    ```
    
    V�rifie la liste des cha�nes apr�s la division.
    
27. ```python 
    split_column_expression(self,start,end)
    ```
    
    Divise l'expression de colonne dans la requ�te.
    
28. ```python 
    analyse_column_expression(self)
    ```
    
    Analyse l'expression de colonne dans la requ�te.
    
29. ```python 
    deduce_column_expression(self, column_expression)
    ```
    
    D�duit l'expression de colonne dans la requ�te.
    
30. ```python 
    deduce_column_expression_list(self, list_column_exp)
    ```
    
    D�duit la liste des expressions de colonnes dans la requ�te.
    
31. ```python 
    is_got_subqueries(self)
    ```
    
    V�rifie si la requ�te contient des sous-requ�tes.
    
32. ```python 
    table_statement(self)
    ```
    
    Trouve les d�clarations de table dans la requ�te.
    
33. ```python 
    is_table_name(self, table_statement)
    ```
    
    V�rifie si une d�claration est un nom de table.
    
34. ```python 
    table_alias(self, table_statement)
    ```
    
    Trouve l'alias de la table dans la d�claration.
    
35. ```python 
    analyse_tables(self)
    ```
    
    Analyse les tables dans la requ�te.

#### Classe: Nester 

Objectif: Cette classe aide � g�rer les sous-requ�tes imbriqu�es.

##### M�thodes: m�thodes de la classe

1. ```python 
   __init__(self)
   ```
   
   Initialise la classe avec une liste vide et un bool�en indiquant si elle est en train de cr�er une sous-requ�te.
   
2. ```python 
   add(self, nester)
   ```
   
   Ajoute une sous-requ�te � la liste.
   
3. ```python 
   append(self, element)
   ```
   
   Ajoute un �l�ment � la sous-requ�te en cours.
   
4. ```python 
   submit(self)
   ```
   
   Soumet la sous-requ�te en cours et la retire de la liste.

***

### M�thodes:  

Il n'y a pas de m�thodes en dehors des classes dans ce fichier.

***

### Variables:

Il n'y a pas de variables globales en dehors des fonctions et des classes dans ce fichier.
