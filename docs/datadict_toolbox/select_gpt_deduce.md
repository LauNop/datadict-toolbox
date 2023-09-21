select_gpt_deduce.py
This documentation file was created on 21 September 2023 at 14:07:34

## File path

.\datadict_toolbox\select_gpt_deduce.py

## But du fichier

Ce fichier est utilisé pour interagir avec le modèle GPT-4 d'OpenAI afin de générer des réponses basées sur une requête SQL donnée. Il enregistre également les réponses du modèle et les sauvegarde dans un fichier Excel.

## Codebase

### Imports: 

1. ```python 
   import openai
   ```
   OpenAI est une bibliothèque Python qui permet d'interagir avec l'API d'OpenAI. Dans ce fichier, elle est utilisée pour interagir avec le modèle GPT-4 d'OpenAI.

2. ```python 
   import pandas as pd
   ```
   Pandas est une bibliothèque Python utilisée pour la manipulation et l'analyse des données. Dans ce fichier, elle est utilisée pour créer des DataFrames et sauvegarder les données dans un fichier Excel.

3. ```python 
   import json
   ```
   La bibliothèque json est utilisée pour travailler avec des données au format JSON. Dans ce fichier, elle est utilisée pour lire un fichier JSON et convertir une chaîne de caractères en liste.

4. ```python 
   import os
   ```
   La bibliothèque os fournit des fonctions pour interagir avec le système d'exploitation. Dans ce fichier, elle est utilisée pour vérifier l'existence de dossiers et de fichiers, et pour créer des dossiers si nécessaire.

5. ```python 
   import re
   ```
   La bibliothèque re est utilisée pour travailler avec des expressions régulières. Dans ce fichier, elle est utilisée pour extraire une liste d'une chaîne de caractères.

***

### Classes

#### Class: SelectGPTDeduce 

But: Cette classe est utilisée pour interagir avec le modèle GPT-4 d'OpenAI, générer des réponses basées sur une requête SQL donnée, et sauvegarder les réponses dans un fichier Excel.

##### Méthodes: 

1. ```python 
   __init__(self, openai_organization, openai_api_key, sql_query=None, model_name="gpt-4", response_file_name="model_response", answer_file=None, excel_name = "data_dict", destination_table = None)
   ```
   Initialise la classe avec les paramètres donnés. Il définit également certaines variables d'instance et appelle certaines méthodes pour préparer les données nécessaires.

   ##### Variables:
   - self.sql_query : La requête SQL à utiliser pour générer la réponse du modèle.
   - self.model_name : Le nom du modèle à utiliser pour générer la réponse.
   - self.response_file_name : Le nom du fichier où sauvegarder la réponse du modèle.
   - self.excel_name : Le nom du fichier Excel où sauvegarder les données.
   - self.select_data_dict : Un dictionnaire contenant les données à sauvegarder.
   - self.destination_table : La table de destination pour la requête SQL.
   - self.prompts_lines : Les lignes de l'invite à utiliser pour générer la réponse du modèle.
   - self.model_response : La réponse générée par le modèle.

2. ```python 
   load_prompts(self)
   ```
   Charge les lignes de l'invite à partir d'un fichier texte.

3. ```python 
   system_message(self)
   ```
   Retourne le message du système à utiliser pour générer la réponse du modèle.

4. ```python 
   examples_message(self)
   ```
   Génère et retourne le message d'exemple à utiliser pour générer la réponse du modèle.

5. ```python 
   prompt(self)
   ```
   Génère et retourne l'invite à utiliser pour générer la réponse du modèle.

6. ```python 
   get_model_response(self)
   ```
   Interagit avec le modèle GPT-4 d'OpenAI pour générer une réponse basée sur l'invite et les messages donnés.

7. ```python 
   build_data_dict(self)
   ```
   Construit et retourne un dictionnaire contenant les données à sauvegarder.

8. ```python 
   insert_structure(self, values)
   ```
   Insère les valeurs données dans le dictionnaire de données.

9. ```python 
   extract_data_from_model_response(self)
   ```
   Extrait les données de la réponse du modèle et les insère dans le dictionnaire de données.

10. ```python 
    save_model_response(self)
    ```
    Sauvegarde la réponse du modèle dans un fichier texte.

11. ```python 
    save(self)
    ```
    Sauvegarde les données du dictionnaire dans un fichier Excel.

***

### Méthodes:  

Il n'y a pas de méthodes en dehors des classes dans ce fichier.

***

### Variables:

Il n'y a pas de variables globales en dehors des fonctions et des classes dans ce fichier.
