﻿import openai
import pandas as pd
import json
import os
import re


class SelectGPTDeduce:
    def __init__(self, openai_organization, openai_api_key, sql_query=None, model_name="gpt-4",
                 response_file_name="model_response", answer_file=None, excel_name = "data_dict", destination_table = None):
        openai.api_key = openai_api_key
        openai.organization = openai_organization
        self.sql_query = sql_query
        self.model_name = model_name
        self.response_file_name = response_file_name
        self.excel_name = excel_name
        self.select_data_dict = self.build_data_dict()
        self.destination_table = destination_table
        self.prompts_lines = self.load_prompts()
        if answer_file is None:
            self.model_response = self.get_model_response()
        else:
            with open(answer_file,'r') as file:
                self.model_response = file.read()
                file.close()
        # self.extract_data_from_model_response()

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

    def build_data_dict(self):
        with open('datadict_toolbox/usefull.json', 'r') as file:
            json_content = file.read()
            usefull_dict = json.loads(json_content)
        file.close()
        select_data_dict = {key: [] for key in usefull_dict["Select_Dict"]}
        return select_data_dict

    def insert_structure(self, values):
        for key, value in zip(self.select_data_dict.keys(), values):
            self.select_data_dict[key].append(value)
        return

    def extract_data_from_model_response(self):
        string = self.model_response
        list_to_format = re.search(r'\[.*?\]$',string,re.DOTALL).group()
        print(type(list_to_format),list_to_format)
        list_to_format = list_to_format.replace("\n", "").strip()
        computable_list = json.loads(list_to_format)
        for dict_ in computable_list:
            alias = dict_['alias']
            column = dict_['column']
            table = dict_['table']
            new_values = [alias, column, table, self.destination_table]
            self.insert_structure(new_values)
        return computable_list

    def save_model_response(self):
        dossier = "model_responses/"
        if not (os.path.exists(dossier) and os.path.isdir(dossier)):
            os.makedirs(dossier)
        with open(dossier + self.response_file_name + '.txt', 'w') as file:
            file.write(self.model_response)
            file.close()
        return

    def save(self):
        dossier = "excel_result/"
        if not (os.path.exists(dossier) and os.path.isdir(dossier)):
            os.makedirs(dossier)

        file_name = self.excel_name + ".xlsx"
        file_path = dossier + file_name

        if os.path.exists(file_path):
            new_df = pd.DataFrame(self.select_data_dict)
            existing_df = pd.read_excel(file_path)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            combined_df.to_excel(file_path, index=False)
        else:
            df = pd.DataFrame(self.select_data_dict)
            df.to_excel(file_path, index=False)
        return



if __name__ == "__main__":
    print("In the main.py")
