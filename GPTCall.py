import openai
import pandas as pd
import json


dash_line = "\n"+"-"*100+"\n"

def get_keys(path):
    with open(path) as f:
        return json.load(f)

# Retrieve SQL Query that will serve as input
#SQL_Query = get_keys("C:/Users/La_Nopoly/source/repos/ExtractFromDTSX/SQL_Query.json")["Query"]

# Set your OpenAI GPT-3 API key here
api_key = get_keys("C:/Users/La_Nopoly/Desktop/API.json")["DICO_KEY"]



# Function to interact with ChatGPT
def chat_with_gpt3(prompt, max_tokens=400):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can also try "text-davinci-003" or other engines
        prompt=prompt,
        max_tokens=max_tokens,
    )
    return response.choices[0].text.strip()

 

def main(SQL_Query):
    # Fill in your question for ChatGPT here
    prompt = f"""
    Extract information from an SQL query as follows:

    Example 1:
    SQL Query :    
    select TABLE_NAME as Contenant, COLUMN_NAME, Cube 
    from INFORMATION_SCHEMA.COLUMNS

    I count 3 columns so the list length of each keys must be 3 

    {{"Alias":["Contenant","",""],"COLUMN":["TABLE_NAME","COLUMN_NAME","Cube"],"TABLE":["COLUMNS","COLUMNS","COLUMNS"],"DATABASE":["INFORMATION_SCHEMA","INFORMATION_SCHEMA","INFORMATION_SCHEMA",]}}

    Example 2:
    SQL Query :    
    select AvionID, Pilote as Employee, Cargo as nbr_passengers, APT as aeroport 
    from AVION

    I count 4 columns so the list length of each keys must be 4 

    {{"Alias":["","Employee","nbr_passengers","aeroport],"COLUMN":["AvionID","Pilote","Cargo","APT"],"TABLE":["AVION","AVION","AVION","AVION"],"DATABASE":["Unknown","Unknown","Unknown","Unknown"]}}

    Complete this one
    SQL Query:
    {SQL_Query}

    
    """

 

    # Get response from ChatGPT
    model_response = chat_with_gpt3(prompt)

    print(model_response)
    print(dash_line)

    model_response = model_response[model_response.index('{'):]

    print(model_response)



    model_tab_response = json.loads(model_response)  

    # Save ChatGPT's response to an Excel file
    df = pd.DataFrame(model_tab_response)
    df.to_excel('chatgpt_response.xlsx', index=False)

 

if __name__ == "__main__":
    query = get_keys("C:/Users/La_Nopoly/source/repos/ExtractFromDTSX/ExtractFromDTSX/Query.json")["SQL_QUERY"][0]
    main(query)
    

 