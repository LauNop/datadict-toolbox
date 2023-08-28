import os

import envVar as V

if __name__=="__main__":
    from ExtractFromDTSX import extract_erp_query

    folder_path = "C:/Users/La_Nopoly/Desktop/TestExtract/DTSX"
    file_names = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    print(len(file_names))
