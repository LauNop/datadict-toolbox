# Dictionary_ToolBox

Dictionary_ToolBox est un projet python contenant des outils pour consitiuer un dictionnaire de données.

## Contenu

### ExtractFromDTSX.py (Opérationel) 
ExtractFromDTSX permet de récupérer des informations d'un fichier .dtsx pour analyser des packages SSIS, récupérer leur mapping, leur requête SQL et leur variable de configuration

### ExtractFromXMLA.py (Opérationel)
ExtractFromXMLA permet de récupérer les informations d'un fichier .xmla afin de constituer le dictionnaire de donnée d'un cube tabulaire.

Il permet également de constituer le dictionnaire de données des cubes mutlidimensionnelle d'un catalogue de cubes.

### GPTCall.py (Non conlcuant)
Tentative de ICL (In Context Learning) avec les modèles de OpenAI text-davincii-03 et gpt-3.5-turbo afin de déterminer la structure d'une base de donnée depuis la requête SQL qui a permis la construire. (Retro-engineering)

## Configuration

Créer un fichier .env dans lequel vous devrez renseigner votre OPENAI_API_KEY, DTSX_FOLDER, XMLA_FOLDER, EXCEL_REPO
Dupliquer le fichier .env.example

## Project status

Développement de la solution pour que ExtractFromXMLA.py prenne en charge les cubes multidimensionnelle

To do :

		- Récupérer AttributeID et Column_NAME
		- Récupérer l'usage des dimensions par measure

## Roadmap

### En cours

### Prévu

### Fait

