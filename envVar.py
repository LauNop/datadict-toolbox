import os
from dotenv import load_dotenv

load_dotenv(".env")

DTSX_FOLDER = os.getenv("DTSX_FOLDER")
XMLA_FOLDER = os.getenv("XMLA_FOLDER")
EXCEL_REPO = os.getenv("EXCEL_REPO")

# Setting the 

DASH_LINE = os.getenv("DASH_LINE")

# Setting conn

OPENAI_API_KEY = os.getenv("OPEN_AI_KEY")