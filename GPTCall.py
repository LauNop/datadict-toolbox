import openai
import pandas as pd
import json
import os
from dotenv import load_dotenv
import time

load_dotenv()

openai.organization = "org-5wlnguNXWQIr7Jufj0TpmNXq"
openai.api_key = os.getenv("OPENAI_API_KEY")

DTSX_FOLDER = os.getenv("DTSX_FOLDER")
DASH_LINE = os.getenv("DASH_LINE")


model_name = "text-davinci-003"

def extract_from_json(path):
    with open(path) as f:
        return json.load(f)




# Function to interact with ChatGPT
def get_model_response(prompt, max_tokens=1500):
    response = openai.Completion.create(
        engine=model_name,  # You can also try "text-davinci-003" or other engines
        prompt=prompt,
        max_tokens=max_tokens,
    )
    print("Nbr TOKENS: ",response["usage"]["total_tokens"])
    return response.choices[0].text.strip()

def response_as_dict(model_response):
    print(model_response)
    print(DASH_LINE)
    model_response = model_response[model_response.index('{'):]
    print(model_response)
    print(DASH_LINE)
    return json.loads(model_response)  

def save_to_excel(dictionary,excel_repo = "erp_result.xlsx"):
    path = f"{excel_repo}"
    if(os.path.exists(path)):
        new_df = pd.DataFrame(dictionary)
        existing_df = pd.read_excel(path)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        combined_df.to_excel(path, index=False)
    else:
        df = pd.DataFrame(dictionary)
        df.to_excel(f"{excel_repo}", index=False)

def main(SQL_Query):
    # Fill in your question for ChatGPT here
    prompt = f"""
    Extract information from an SQL query as follows:

    Example 1:
    SQL Query :    
    select TABLE_NAME as Contenant, COLUMN_NAME, Cube 
    from INFORMATION_SCHEMA.COLUMNS
    .05
    I count 3 columns so the list length of each key must be 3 

    {{"COLUMN_NAME":["","",""],"NOM_EXPLICIT":["","",""],"DATA_TYPE":["","",""],"TABLE_NAME_CUBE":["","",""],"CUBE_NAME":["","",""],"CATALOG_NAME":["","",""],"VIEW_NAME":["","",""],"TABLE_NAME_INFOCENTRE":["","",""],"DATABASE_NAME_INFOCENTRE":["","",""],"SERVEUR_INFOCENTRE":["","",""],"COLUMN_NAME_ERP":["TABLE_NAME","COLUMN_NAME","Cube"],"TABLE_NAME_ERP":["COLUMNS","COLUMNS","COLUMNS"],"DATABASE_NAME_ERP":["INFORMATION_SCHEMA","INFORMATION_SCHEMA","INFORMATION_SCHEMA",],"ERP_NAME":["","",""],"EXPRESSION":["","",""],"DEFINITION":["","",""],"LIAISON":["","",""],"MAPPING":["Contenant","",""]}}
    
    Example 2:
    SQL Query :    
    select AvionID, Pilote as Employee, Cargo as nbr_passengers, APT as aeroport 
    from AVION

    I count 4 columns so the list length of each key must be 4 

    {{"COLUMN_NAME":["","","",""],"NOM_EXPLICIT":["","","",""],"DATA_TYPE":["","","",""],"TABLE_NAME_CUBE":["","","",""],"CUBE_NAME":["","","",""],"CATALOG_NAME":["","","",""],"VIEW_NAME":["","","",""],"TABLE_NAME_INFOCENTRE":["","","",""],"DATABASE_NAME_INFOCENTRE":["","","",""],"SERVEUR_INFOCENTRE":["","","",""],"COLUMN_NAME_ERP":["AvionID","Pilote","Cargo","APT"],"TABLE_NAME_ERP":["AVION","AVION","AVION","AVION"],"DATABASE_NAME_ERP":["Unknown","Unknown","Unknown","Unknown"],"ERP_NAME":["","","",""],"EXPRESSION":["","","",""],"DEFINITION":["","","",""],"LIAISON":["","","",""],,"MAPPING":["","Employee","nbr_passengers","aeroport]}}

    Complete this one
    SQL Query:
    {SQL_Query}

    
    """

 

    # Get response from ChatGPT
    data = response_as_dict(get_model_response(prompt))

    save_to_excel(data)

 

if __name__ == "__main__":
    import ExtractFromDTSX as EFD

    folder_path = DTSX_FOLDER
    file_names = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    #get_keys("Queries.json")["SQL_QUERY"]

    queries = EFD.extract_erp_query(file_names)["SQL_QUERY"]
    count = 0
    for query in queries:
        count+=1
        print(count)
        main(query)
        time.sleep(3)
        
    

 