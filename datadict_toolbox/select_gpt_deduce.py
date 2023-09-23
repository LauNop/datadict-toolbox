import openai
import pandas as pd
import json
import os
import re

from datadict_toolbox.usefull import usefull_dict

class SelectGPTDeduce:
    def __init__(self, openai_organization, openai_api_key, sql_query=None, model_name="gpt-4",
                 response_file_name="model_response", answer_file=None, excel_name="data_dict", destination_table=None):
        openai.api_key = openai_api_key
        openai.organization = openai_organization
        self.sql_query = sql_query
        self.model_name = model_name
        self.response_file_name = response_file_name
        self.excel_name = excel_name
        self.select_data_dict = self.build_data_dict()
        self.destination_table = destination_table
        if answer_file is None:
            self.model_response = self.get_model_response()
        else:
            with open(answer_file,'r') as file:
                self.model_response = file.read()
                file.close()
        self.extract_data_from_model_response()

    def system_message(self):
        return usefull_dict["System_message"]

    def examples_message(self):
        example_prompt = ""
        count = 0
        prompts_dict = usefull_dict["Example_prompts"]
        for i in range(len(prompts_dict["query"])):
            count += 1
            example_prompt += "Example " + str(count) + ":\nSQL Query:\n"
            example_prompt += prompts_dict["query"][i]
            example_prompt += "\nOutput:\n"
            example_prompt += prompts_dict["solutions"][i]
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
        select_data_dict = {key: [] for key in usefull_dict["Select_Dict"]}
        return select_data_dict

    def insert_structure(self, values):
        for key, value in zip(self.select_data_dict.keys(), values):
            self.select_data_dict[key].append(value)
        return

    def extract_data_from_model_response(self):
        string = self.model_response
        computable_list = []
        try:
            list_to_format = re.search(r'\[.*?\]$',string,re.DOTALL).group()
            print(type(list_to_format), list_to_format)
            list_to_format = list_to_format.replace("\n", "").strip()
            computable_list = json.loads(list_to_format)
        except AttributeError:
            print(
                "No match found in the string.",
                "Python library:re fail to match the list of dictionnary in model response",
                  )
            self.save_model_response(True)
            print("Model response saved for inspection")
            return
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            self.save_model_response(True)
            print("Model response saved for inspection")
            return
        for dict_ in computable_list:
            alias = dict_['alias']
            column = dict_['column']
            table = dict_['table']
            new_values = [alias, column, table, self.destination_table]
            self.insert_structure(new_values)
        return computable_list

    def save_model_response(self,save_for_error=False):
        if save_for_error:
            dossier="model_responses/error/"
        else:
            dossier = "model_responses/"
        if not (os.path.exists(dossier) and os.path.isdir(dossier)):
            os.makedirs(dossier)
        with open(dossier + self.response_file_name + '.txt', 'w') as file:
            file.write(self.model_response)
            file.close()
        return

    def check_data_dict_status(self):
        num_element = len(self.select_data_dict['ALIAS_NAME'])
        print(f"There is {str(num_element)} element in data dict ")
        return num_element

    def save(self):
        if self.check_data_dict_status():
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
        else:
            print("Nothing to save. Extraction may have fail")
        return


if __name__ == "__main__":
    print("In the main.py")
