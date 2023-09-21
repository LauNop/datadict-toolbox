select_gpt_deduce.py
This documentation file was created on 21 September 2023 at 14:07:34

## File path

.\datadict_toolbox\select_gpt_deduce.py

## But du fichier

Ce fichier est utilis� pour interagir avec le mod�le GPT-4 d'OpenAI afin de g�n�rer des r�ponses bas�es sur une requ�te SQL donn�e. Il enregistre �galement les r�ponses du mod�le et les sauvegarde dans un fichier Excel.

## Codebase

### Imports: 

1. ```python 
   import openai
   ```
   OpenAI est une biblioth�que Python qui permet d'interagir avec l'API d'OpenAI. Dans ce fichier, elle est utilis�e pour interagir avec le mod�le GPT-4 d'OpenAI.

2. ```python 
   import pandas as pd
   ```
   Pandas est une biblioth�que Python utilis�e pour la manipulation et l'analyse des donn�es. Dans ce fichier, elle est utilis�e pour cr�er des DataFrames et sauvegarder les donn�es dans un fichier Excel.

3. ```python 
   import json
   ```
   La biblioth�que json est utilis�e pour travailler avec des donn�es au format JSON. Dans ce fichier, elle est utilis�e pour lire un fichier JSON et convertir une cha�ne de caract�res en liste.

4. ```python 
   import os
   ```
   La biblioth�que os fournit des fonctions pour interagir avec le syst�me d'exploitation. Dans ce fichier, elle est utilis�e pour v�rifier l'existence de dossiers et de fichiers, et pour cr�er des dossiers si n�cessaire.

5. ```python 
   import re
   ```
   La biblioth�que re est utilis�e pour travailler avec des expressions r�guli�res. Dans ce fichier, elle est utilis�e pour extraire une liste d'une cha�ne de caract�res.

***

### Classes

#### Class: SelectGPTDeduce 

But: Cette classe est utilis�e pour interagir avec le mod�le GPT-4 d'OpenAI, g�n�rer des r�ponses bas�es sur une requ�te SQL donn�e, et sauvegarder les r�ponses dans un fichier Excel.

##### M�thodes: 

1. ```python 
   __init__(self, openai_organization, openai_api_key, sql_query=None, model_name="gpt-4", response_file_name="model_response", answer_file=None, excel_name = "data_dict", destination_table = None)
   ```
   Initialise la classe avec les param�tres donn�s. Il d�finit �galement certaines variables d'instance et appelle certaines m�thodes pour pr�parer les donn�es n�cessaires.

   ##### Variables:
   - self.sql_query : La requ�te SQL � utiliser pour g�n�rer la r�ponse du mod�le.
   - self.model_name : Le nom du mod�le � utiliser pour g�n�rer la r�ponse.
   - self.response_file_name : Le nom du fichier o� sauvegarder la r�ponse du mod�le.
   - self.excel_name : Le nom du fichier Excel o� sauvegarder les donn�es.
   - self.select_data_dict : Un dictionnaire contenant les donn�es � sauvegarder.
   - self.destination_table : La table de destination pour la requ�te SQL.
   - self.prompts_lines : Les lignes de l'invite � utiliser pour g�n�rer la r�ponse du mod�le.
   - self.model_response : La r�ponse g�n�r�e par le mod�le.

2. ```python 
   load_prompts(self)
   ```
   Charge les lignes de l'invite � partir d'un fichier texte.

3. ```python 
   system_message(self)
   ```
   Retourne le message du syst�me � utiliser pour g�n�rer la r�ponse du mod�le.

4. ```python 
   examples_message(self)
   ```
   G�n�re et retourne le message d'exemple � utiliser pour g�n�rer la r�ponse du mod�le.

5. ```python 
   prompt(self)
   ```
   G�n�re et retourne l'invite � utiliser pour g�n�rer la r�ponse du mod�le.

6. ```python 
   get_model_response(self)
   ```
   Interagit avec le mod�le GPT-4 d'OpenAI pour g�n�rer une r�ponse bas�e sur l'invite et les messages donn�s.

7. ```python 
   build_data_dict(self)
   ```
   Construit et retourne un dictionnaire contenant les donn�es � sauvegarder.

8. ```python 
   insert_structure(self, values)
   ```
   Ins�re les valeurs donn�es dans le dictionnaire de donn�es.

9. ```python 
   extract_data_from_model_response(self)
   ```
   Extrait les donn�es de la r�ponse du mod�le et les ins�re dans le dictionnaire de donn�es.

10. ```python 
    save_model_response(self)
    ```
    Sauvegarde la r�ponse du mod�le dans un fichier texte.

11. ```python 
    save(self)
    ```
    Sauvegarde les donn�es du dictionnaire dans un fichier Excel.

***

### M�thodes:  

Il n'y a pas de m�thodes en dehors des classes dans ce fichier.

***

### Variables:

Il n'y a pas de variables globales en dehors des fonctions et des classes dans ce fichier.
