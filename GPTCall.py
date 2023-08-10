import openai
import pandas as pd
import json


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
    chat_prompt = f"""
    Extract information from an SQL query as follows:

    Example 1:
    SQL Query :    
    select TABLE_NAME as Contenant, COLUMN_NAME, Cube 
    from INFORMATION_SCHEMA.COLUMNS

    structure = {{"Alias":["Contenant","",""],"COLUMN":["TABLE_NAME","COLUMN_NAME","Cube"],"TABLE":["COLUMNS","COLUMNS","COLUMNS"],"DATABASE":["INFORMATION_SCHEMA","INFORMATION_SCHEMA","INFORMATION_SCHEMA",]}}

    You should know that this data will become a pandas DataFrame. We want it to have these columns in order : COLUMN_NAME (Alias),	NOM_EXPLICIT (Empty),	DATA_TYPE (Empty),	TABLE_NAME_CUBE (Empty),	CUBE_NAME (Empty),	CATALOG_NAME (Empty),	VIEW_NAME (Empty),	TABLE_NAME_INFOCENTRE (Empty),	DATABASE_NAME_INFOCENTRE (Empty),	SERVEUR_INFOCENTRE (Empty),	COLUMN_NAME_ERP (COLUMN),	TABLE_NAME_ERP (TABLE),	DATABASE_NAME_ERP (DATABASE),	ERP_NAME (Empty),	EXPRESSION (Empty),	DEFINITION (Empty),	LIAISON (Alias)

    Complete this one
    SQL Query:
    {SQL_Query}

    
    """

 

    # Get response from ChatGPT
    gpt3_response = chat_with_gpt3(chat_prompt)

 

    # Print ChatGPT's response
    #print("ChatGPT:", gpt3_response)

 

    # Save ChatGPT's response to an Excel file
    data = {'Response': [gpt3_response]}
    df = pd.DataFrame(data)
    df.to_excel('chatgpt_response.xlsx', index=False)

 

if __name__ == "__main__":
    query = get_keys("C:/Users/La_Nopoly/source/repos/ExtractFromDTSX/ExtractFromDTSX/Query.json")["SQL_QUERY"][0]
    main(query)
    

 