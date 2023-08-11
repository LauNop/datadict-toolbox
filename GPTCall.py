import openai
import pandas as pd
import json
import os
import time


dash_line = "\n"+"-"*100+"\n"
model_name = "gpt-3.5-turbo"

def get_keys(path):
    with open(path) as f:
        return json.load(f)

# Retrieve SQL Query that will serve as input
#SQL_Query = get_keys("C:/Users/La_Nopoly/source/repos/ExtractFromDTSX/SQL_Query.json")["Query"]

# Set your OpenAI GPT-3 API key here
api_key = get_keys("C:/Users/La_Nopoly/Desktop/API.json")["DICO_KEY"]



# Function to interact with ChatGPT
def get_model_response(prompt,dict_prompt,dict_resp, example_prompt,example_resp,expl2_p,expl2_r, max_tokens=1500):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=model_name,  # You can also try "text-davinci-003" or other engines
        messages=[
            {"role":"system","content":"You extract information from a SQL query"},
            {"role":"user","content":dict_prompt},
            {"role":"assistant","content":dict_resp}
            {"role":"user","content":example_prompt},
            {"role":"assistant","content":example_resp},
            {"role":"user","content":expl2_p},
            {"role":"assistant","content":expl2_r},
            {"role":"user","content":prompt}
        ],
    )
    print("Nbr TOKENS: ",response["usage"]["total_tokens"])
    return response["choices"][0]["message"]["content"]

def response_as_dict(model_response):
    print(model_response)
    print(dash_line)
    model_response = model_response[model_response.index('{'):model_response.index("}")+1]
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
    SQL Query:
    {SQL_Query}
    """

    dict_prompt = """
     Create a dictionary with the following Keys:"COLUMN_NAME","NOM_EXPLICIT","DATA_TYPE","TABLE_NAME_CUBE","CUBE_NAME","CATALOG_NAME","VIEW_NAME","TABLE_NAME_INFOCENTRE","DATABASE_NAME_INFOCENTRE","SERVEUR_INFOCENTRE","COLUMN_NAME_ERP","TABLE_NAME_ERP","DATABASE_NAME_ERP","ERP_NAME","EXPRESSION","DEFINITION","LIAISON". The keys' values should be empty lists.
    """
    dict_resp = """Here's the dictionary you requested with empty lists as values for each key:
    
    ```python
    empty_dict = {
        "COLUMN_NAME": [],
        "NOM_EXPLICIT": [],
        "DATA_TYPE": [],
        "TABLE_NAME_CUBE": [],
        "CUBE_NAME": [],
        "CATALOG_NAME": [],
        "VIEW_NAME": [],
        "TABLE_NAME_INFOCENTRE": [],
        "DATABASE_NAME_INFOCENTRE": [],
        "SERVEUR_INFOCENTRE": [],
        "COLUMN_NAME_ERP": [],
        "TABLE_NAME_ERP": [],
        "DATABASE_NAME_ERP": [],
        "ERP_NAME": [],
        "EXPRESSION": [],
        "DEFINITION": [],
        "LIAISON": []
    }
    ```
    
    You can use this dictionary as a starting point and populate the lists with values as needed in your code."""

    example_prompt = """Perfect, now I want you to fill each list with elements. Some lists will have values given from an SQL Query. The ones that do not, should still be filled with the same amount of elements but their values will be "".

    The extraction of values for these lists will take place as follows:
    
    Example 1:
    SQL Query :    
    select TABLE_NAME as Contenant, COLUMN_NAME, Cube 
    from INFORMATION_SCHEMA.COLUMNS"""

    example_resp = """
    I count 3 columns so the list length of each key must be 3 

    {"COLUMN_NAME":["","",""],"NOM_EXPLICIT":["","",""],"DATA_TYPE":["","",""],"TABLE_NAME_CUBE":["","",""],"CUBE_NAME":["","",""],"CATALOG_NAME":["","",""],"VIEW_NAME":["","",""],"TABLE_NAME_INFOCENTRE":["","",""],"DATABASE_NAME_INFOCENTRE":["","",""],"SERVEUR_INFOCENTRE":["","",""],"COLUMN_NAME_ERP":["TABLE_NAME","COLUMN_NAME","Cube"],"TABLE_NAME_ERP":["COLUMNS","COLUMNS","COLUMNS"],"DATABASE_NAME_ERP":["INFORMATION_SCHEMA","INFORMATION_SCHEMA","INFORMATION_SCHEMA",],"ERP_NAME":["","",""],"EXPRESSION":["","",""],"DEFINITION":["","",""],"LIAISON":["","",""],"MAPPING":["Contenant","",""]}

    """
    expl2_p="""
    SQL Query :    
    select AvionID, Pilote as Employee, Cargo as nbr_passengers, APT as aeroport 
    from AVION
    """
    expl2_r = """
    I count 4 columns so the list length of each key must be 4 

    {"COLUMN_NAME":["","","",""],"NOM_EXPLICIT":["","","",""],"DATA_TYPE":["","","",""],"TABLE_NAME_CUBE":["","","",""],"CUBE_NAME":["","","",""],"CATALOG_NAME":["","","",""],"VIEW_NAME":["","","",""],"TABLE_NAME_INFOCENTRE":["","","",""],"DATABASE_NAME_INFOCENTRE":["","","",""],"SERVEUR_INFOCENTRE":["","","",""],"MAPPING":["","Employee","nbr_passengers","aeroport],"COLUMN_NAME_ERP":["AvionID","Pilote","Cargo","APT"],"TABLE_NAME_ERP":["AVION","AVION","AVION","AVION"],"DATABASE_NAME_ERP":["Unknown","Unknown","Unknown","Unknown"],"ERP_NAME":["","","",""],"EXPRESSION":["","","",""],"DEFINITION":["","","",""],"LIAISON":["","","",""]}

    """

 

    # Get response from ChatGPT
    data = response_as_dict(get_model_response(prompt,example_prompt,example_resp,expl2_p,expl2_r))

    save_to_excel(data)

 

if __name__ == "__main__":

    #print( [f["id"] for f in get_keys("models.json")["data"]])

    queries = get_keys("Queries.json")["SQL_QUERY"]
    count = 0
    for query in queries:
        count+=1
        print(count)
        main(query)
        time.sleep(1)
        
    

 