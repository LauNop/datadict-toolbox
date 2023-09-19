import openai
import pandas as pd
import json
import os
import re
import ast

import env.envVar as V

openai.organization = "org-5wlnguNXWQIr7Jufj0TpmNXq"
openai.api_key = V.OPENAI_API_KEY
model_name = "gpt-4"


class SelectGPTDeduce:
    def __init__(self, openai_organization, openai_api_key, sql_query = None, model_name="gpt-4",
                 response_file_name="model_response", answer_file = None):
        self.openai_organization = openai_organization
        self.openai_api_key = openai_api_key
        self.sql_query = sql_query
        self.model_name = model_name
        self.response_file_name = response_file_name

        self.prompts_lines = self.load_prompts()
        print(self.prompts_lines)
        print(len(self.prompts_lines))
        # if answer_file is None:
        #     self.model_response = self.get_model_response()
        # else:
        #     with open(answer_file,'r') as file:
        #         self.model_response = file.read()
        #         file.close()

    def load_prompts(self):
        with open('datadict_toolbox/prompt_components.txt', 'r') as file:
             lines = file.readlines()
        file.close()
        return lines

    def system_message(self):
        return self.prompts_lines[1]

    def examples_message(self):
        example_prompt = ""
        count = 0
        for i in range(4, len(self.prompts_lines), 2):
            count += 1
            example_prompt += "Example " + str(count) + ":\nSQL Query:\n"
            example_prompt += self.prompts_lines[i]
            print(self.prompts_lines[i])
            example_prompt += "\nOutput:\n"
            example_prompt += self.prompts_lines[i+1]
            example_prompt += '\n\n'
        return example_prompt

    def prompt(self):
        prompt = f"""
                SQL Query:
                {self.sql_query}
                """
        return prompt

    # Function to interact with ChatGPT
    def get_model_response(self):
        response = openai.ChatCompletion.create(
            model=self.model_name,  # You can also try "text-davinci-003" or other engines
            messages=[
                {"role": "system", "content": self.system_message()},
                {"role": "user", "content": self.examples_message()},
                {"role": "assistant", "content": "Ok, I get it give the sql query"},
                {"role": "user", "content": self.prompt()}
            ]
        )
        print("Nbr TOKENS:\n", response["usage"])
        return response.choices[0].message["content"]

    def extract_data_from_model_response(self):
        string = self.model_response
        list_to_format = re.search(r'\[.*?\]$',string,).group()
        print(type(list_to_format),list_to_format)
        list_to_format = list_to_format.replace("\n", "").strip()
        computable_list = json.loads('{"Section":' + list_to_format + '}')
        print(computable_list)
        return

    def save_model_response(self):
        dossier = "model_responses/"
        if not (os.path.exists(dossier) and os.path.isdir(dossier)):
            os.makedirs(dossier)
        with open(dossier + self.response_file_name + '.txt', 'w') as file:
            file.write(self.model_response)
            file.close()
        return

    def save(self, path=None):
        dossier = "excel_result/"
        if not (os.path.exists(dossier) and os.path.isdir(dossier)):
            os.makedirs(dossier)

        if path is None:
            path_build = self.build_save_path()
            path = "_".join(path_build) + ".xlsx"
            path = dossier + path
        else:
            path = dossier + path

        if os.path.exists(path):
            new_df = pd.DataFrame(self.cube_struct)
            existing_df = pd.read_excel(path)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            combined_df.to_excel(path, index=False)
        else:
            df = pd.DataFrame(self.cube_struct)
            df.to_excel(path, index=False)
        return

    def main(self, SQL_Query):
        # Fill in your question for the text model LLM
        SQL_Query = SQL_Query.replace("\n", " ")

        prompt = f"""
        SQL Query:
        {SQL_Query}
        """

        examples_prompt = """
        Extract information from an SQL query as the example below and will give you the SQL query to process:
    
        Example 1:
        SQL Query :    
        select TABLE_NAME as Contenant, COLUMN_NAME, Cube 
        from INFORMATION_SCHEMA.COLUMNS
    
        Column :
        ["TABLE_NAME","COLUMN_NAME","Cube"]
    
        Dictionary :
        {"COLUMN_NAME_ERP":["TABLE_NAME","COLUMN_NAME","Cube"],"TABLE_NAME_ERP":"COLUMNS","DATABASE_NAME_ERP":"INFORMATION_SCHEMA","MAPPING":["Contenant","",""]}
    
        Example 2:
        SQL Query :    
        select AvionID, Pilote as Employee, Cargo as nbr_passengers, APT as aeroport 
        from AVION
    
        Column :
        ["AvionID","Pilote","Cargo","APT"]
    
        Dictionary :
        {"COLUMN_NAME_ERP":["AvionID","Pilote","Cargo","APT"],"TABLE_NAME_ERP":"AVION","DATABASE_NAME_ERP":"Unknown","MAPPING":["","Employee","nbr_passengers","aeroport"]}
    
        Example 3:
        SQL Query :
        select cast(VIP||ECO||INTERMED as nvarchar2(20)) as Passenger, 3 as Train, cast(MotMod as nvarchar2(50))as Moteur
        from CARGO.INTERN_DATA
    
        Column :
        ["cast(VIP||ECO||INTERMED as nvarchar2(20))","3","cast(MotMod as nvarchar2(50))"]
    
        Dictionary :
        {"COLUMN_NAME_ERP":["cast(VIP||ECO||INTERMED as nvarchar2(20))","3","cast(MotMod as nvarchar2(50))"],"TABLE_NAME_ERP":"INTERN_DATA","DATABASE_NAME_ERP":"CARGO","MAPPING":["Passenger","Train","Moteur"]}
    
        """

        standby_resp = """ Okay, give me the sql query to complete"""

        print("SQL QUERY :\n", SQL_Query)

        # Get response from ChatGPT
        data, col_nbr = self.get_model_response(prompt, examples_prompt, standby_resp)

        dictionary = dict.fromkeys(
            ["COLUMN_NAME", "NOM_EXPLICIT", "DATA_TYPE", "TABLE_NAME_CUBE", "CUBE_NAME", "CATALOG_NAME", "VIEW_NAME",
             "TABLE_NAME_INFOCENTRE", "DATABASE_NAME_INFOCENTRE", "SERVER_INFOCENTRE", "COLUMN_NAME_ERP",
             "TABLE_NAME_ERP",
             "DATABASE_NAME_ERP", "SERVER_NAME_ERP", "EXPRESSION", "DEFINITION", "LIAISON", "MAPPING"],
            ["" for i in range(col_nbr)])
        for key, value in data.items():
            dictionary[key] = value
        print("Final DICT:\n", dictionary)

        # save_to_excel(dictionary)


if __name__ == "__main__":
    print("In the main.py")
