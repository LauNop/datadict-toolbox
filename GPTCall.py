import openai
import pandas as pd
import json
import os


dash_line = "\n"+"-"*100+"\n"

def get_keys(path):
    with open(path) as f:
        return json.load(f)

# Retrieve SQL Query that will serve as input
#SQL_Query = get_keys("C:/Users/La_Nopoly/source/repos/ExtractFromDTSX/SQL_Query.json")["Query"]

# Set your OpenAI GPT-3 API key here
api_key = get_keys("C:/Users/La_Nopoly/Desktop/API.json")["DICO_KEY"]



# Function to interact with ChatGPT
def get_model_response(prompt, max_tokens=500):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can also try "text-davinci-003" or other engines
        prompt=prompt,
        max_tokens=max_tokens,
    )
    return response.choices[0].text.strip()

def response_as_dict(model_response):
    print(model_response)
    print(dash_line)
    model_response = model_response[model_response.index('{'):]
    print(model_response)
    print(dash_line)
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

    I count 3 columns so the list length of each key must be 3 

    {{"COLUMN_NAME":["","",""],"NOM_EXPLICIT":["","",""],"DATA_TYPE":["","",""],"TABLE_NAME_CUBE":["","",""],"CUBE_NAME":["","",""],"CATALOG_NAME":["","",""],"VIEW_NAME":["","",""],"TABLE_NAME_INFOCENTRE":["","",""],"DATABASE_NAME_INFOCENTRE":["","",""],"SERVEUR_INFOCENTRE":["","",""],"MAPPING":["Contenant","",""],"COLUMN_NAME_ERP":["TABLE_NAME","COLUMN_NAME","Cube"],"TABLE_NAME_ERP":["COLUMNS","COLUMNS","COLUMNS"],"DATABASE_NAME_ERP":["INFORMATION_SCHEMA","INFORMATION_SCHEMA","INFORMATION_SCHEMA",],"ERP_NAME":["","",""],"EXPRESSION":["","",""],"DEFINITION":["","",""],"LIAISON":["","",""]}}
    
    Example 2:
    SQL Query :    
    select AvionID, Pilote as Employee, Cargo as nbr_passengers, APT as aeroport 
    from AVION

    I count 4 columns so the list length of each key must be 4 

    {{"COLUMN_NAME":["","","",""],"NOM_EXPLICIT":["","","",""],"DATA_TYPE":["","","",""],"TABLE_NAME_CUBE":["","","",""],"CUBE_NAME":["","","",""],"CATALOG_NAME":["","","",""],"VIEW_NAME":["","","",""],"TABLE_NAME_INFOCENTRE":["","","",""],"DATABASE_NAME_INFOCENTRE":["","","",""],"SERVEUR_INFOCENTRE":["","","",""],"MAPPING":["","Employee","nbr_passengers","aeroport],"COLUMN_NAME_ERP":["AvionID","Pilote","Cargo","APT"],"TABLE_NAME_ERP":["AVION","AVION","AVION","AVION"],"DATABASE_NAME_ERP":["Unknown","Unknown","Unknown","Unknown"],"ERP_NAME":["","","",""],"EXPRESSION":["","","",""],"DEFINITION":["","","",""],"LIAISON":["","","",""]}}

    Complete this one
    SQL Query:
    {SQL_Query}

    
    """

 

    # Get response from ChatGPT
    data = response_as_dict(get_model_response(prompt))

    save_to_excel(data)

 

if __name__ == "__main__":
    query = get_keys("C:/Users/La_Nopoly/source/repos/ExtractFromDTSX/ExtractFromDTSX/Query.json")["SQL_QUERY"][0]
    main(query)
    

 