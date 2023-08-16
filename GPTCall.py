import openai
import pandas as pd
import json
import os
import time

from ExtractFromDTSX import extract_erp_query, saveAsJson


dash_line = "\n"+"-"*100+"\n"
model_name = "text-davinci-003"

def extract_from_json(path):
    with open(path) as f:
        return json.load(f)

# Retrieve SQL Query that will serve as input
#SQL_Query = get_keys("C:/Users/La_Nopoly/source/repos/ExtractFromDTSX/SQL_Query.json")["Query"]

# Set your OpenAI GPT-3 API key here
api_key = extract_from_json("C:/Users/La_Nopoly/Desktop/API.json")["DICO_KEY"]



# Function to interact with ChatGPT
def get_model_response(prompt, max_tokens=1500):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine=model_name,  # You can also try "text-davinci-003" or other engines
        prompt=prompt,
        max_tokens=max_tokens,
    )
    print("Nbr TOKENS: ",response["usage"]["total_tokens"])
    return response.choices[0].text.strip()

def get_data_from_response(model_response):
    print("MODEL RESPONSE :\n",model_response)
    print(dash_line)
    column = model_response[model_response.index('['):model_response.index('{')]
    print(type(column),column)
    print(dash_line)
    model_response = model_response[model_response.index('{'):]
    print(model_response)
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
    # Fill in your question for the text model LLM
    prompt = f"""
    Extract information from an SQL query as follows:

    Example 1:
    SQL Query :    
    select TABLE_NAME as Contenant, COLUMN_NAME, Cube 
    from INFORMATION_SCHEMA.COLUMNS
    
    [TABLE_NAME,COLUMN_NAME,Cube]

    {{"COLUMN_NAME_ERP":["TABLE_NAME","COLUMN_NAME","Cube"],"TABLE_NAME_ERP":["COLUMNS","COLUMNS","COLUMNS"],"DATABASE_NAME_ERP":["INFORMATION_SCHEMA","INFORMATION_SCHEMA","INFORMATION_SCHEMA",],"MAPPING":["Contenant","",""]}}
    
    Example 2:
    SQL Query :    
    select AvionID, Pilote as Employee, Cargo as nbr_passengers, APT as aeroport 
    from AVION

    [AvionID,Pilote,Cargo,APT]

    {{"COLUMN_NAME_ERP":["AvionID","Pilote","Cargo","APT"],"TABLE_NAME_ERP":["AVION","AVION","AVION","AVION"],"DATABASE_NAME_ERP":["Unknown","Unknown","Unknown","Unknown"],"MAPPING":["","Employee","nbr_passengers","aeroport]}}

    Complete this one
    SQL Query:
    {SQL_Query}
    """

    print("SQL QUERY :\n",SQL_Query)
    print(dash_line)

    # Get response from ChatGPT
    data =get_data_from_response(get_model_response(prompt))

    #save_to_excel(data)

 

if __name__ == "__main__":
    import ExtractFromDTSX as EFD

    folder_path = "C:/Users/La_Nopoly/Desktop/TestExtract/DTSX"
    file_names = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    #get_keys("Queries.json")["SQL_QUERY"]

    queries = EFD.extract_erp_query(file_names)["SQL_QUERY"][0]
    print()
    main(queries)
    #count = 0
    #for query in queries:
    #    count+=1
    #    print(count)
    #    main(query)
    #    time.sleep(3)
        
    

 