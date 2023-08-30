import openai
import pandas as pd
import json
import os
import time

from env import envVar as V

openai.organization = "org-5wlnguNXWQIr7Jufj0TpmNXq"
openai.api_key = os.getenv("OPENAI_API_KEY")

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

def get_data_from_response(model_response):
    print("MODEL RESPONSE :\n",model_response)
    print(V.DASH_LINE)
    column = model_response[model_response.index('['):model_response.index('{')]
    print(type(column),column)
    print(V.DASH_LINE)
    column = column.replace("\n","")
    print("After strip:",column)
    column = json.loads(column)
    print(type(column),column)
    col_nbr = len(column)
    print("Nbr_column:",col_nbr)
    print(V.DASH_LINE)
    model_response = model_response[model_response.index('{'):]
    data = json.loads(model_response)
    print("Model dict :", model_response)
    print(V.DASH_LINE)
    if len(data["COLUMN_NAME_ERP"])!= col_nbr: data['COLUMN_NAME_ERP']=data['COLUMN_NAME_ERP'][:col_nbr]
    if len(data["MAPPING"])!= col_nbr: data['MAPPING']=data['MAPPING'][:col_nbr]
    data["TABLE_NAME_ERP"]= [data["TABLE_NAME_ERP"] for i in range(col_nbr)]
    data["DATABASE_NAME_ERP"]= [data["DATABASE_NAME_ERP"] for i in range(col_nbr)]
    print(data)
    return data, col_nbr

def save_to_excel(dictionary,excel_repo = "{}erp_result.xlsx".format(V.EXCEL_REPO)):
    path = f"{excel_repo}"
    if os.path.exists(path):
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
    
    ["TABLE_NAME","COLUMN_NAME","Cube"]

    {{"COLUMN_NAME_ERP":["TABLE_NAME","COLUMN_NAME","Cube"],"TABLE_NAME_ERP":"COLUMNS","DATABASE_NAME_ERP":"INFORMATION_SCHEMA","MAPPING":["Contenant","",""]}}
    
    Example 2:
    SQL Query :    
    select AvionID, Pilote as Employee, Cargo as nbr_passengers, APT as aeroport 
    from AVION

    ["AvionID","Pilote","Cargo","APT"]

    {{"COLUMN_NAME_ERP":["AvionID","Pilote","Cargo","APT"],"TABLE_NAME_ERP":"AVION","DATABASE_NAME_ERP":"Unknown","MAPPING":["","Employee","nbr_passengers","aeroport"]}}

    Example 3:
    SQL Query :
    select cast(VIP||ECO||INTERMED as nvarchar2(20)) as Passenger, Train, cast(MotMod as nvarchar2(50))as Moteur
    from CARGO.INTERN_DATA

    ["cast(VIP||ECO||INTERMED as nvarchar2(20))","Train","cast(MotMod as nvarchar2(50))"]

    {{"COLUMN_NAME_ERP":["cast(VIP||ECO||INTERMED as nvarchar2(20))","Train","cast(MotMod as nvarchar2(50))"],"TABLE_NAME_ERP":"INTERN_DATA","DATABASE_NAME_ERP":"CARGO","MAPPING":["Passenger","","Moteur"]}}

    Complete this one
    SQL Query:
    {SQL_Query}
    """

    print("SQL QUERY :\n",SQL_Query)
    print(V.DASH_LINE)

    # Get response from ChatGPT
    data, col_nbr =get_data_from_response(get_model_response(prompt))

    print(V.DASH_LINE)

    dictionary = dict.fromkeys(["COLUMN_NAME","NOM_EXPLICIT","DATA_TYPE","TABLE_NAME_CUBE","CUBE_NAME","CATALOG_NAME","VIEW_NAME","TABLE_NAME_INFOCENTRE","DATABASE_NAME_INFOCENTRE","SERVER_INFOCENTRE","COLUMN_NAME_ERP","TABLE_NAME_ERP","DATABASE_NAME_ERP","SERVER_NAME_ERP","EXPRESSION","DEFINITION","LIAISON","MAPPING"],["" for i in range(col_nbr)])
    for key,value in data.items():
        dictionary[key] = value
    print(dictionary)


    save_to_excel(dictionary)

 

if __name__ == "__main__":
    import ExtractFromDTSX as EFD

    folder_path = V.DTSX_FOLDER
    file_names = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    #get_keys("Queries.json")["SQL_QUERY"]

    queries = EFD.extract_erp_query(file_names)["SQL_QUERY"]
    count = 0
    for query in queries:
        count+=1
        print(count,":",file_names[count-1])
        main(query)
        print(V.DASH_LINE)
        time.sleep(3)
        
    

 