''' 
Program purpose: Replace user dialog acts in 'attraction-restaurant-taxi' with Hindi equivalents from database

Input: 1. Database File (in xlsx)
       2. Segregated MultiWOZ_2.1 dataset (with corrections from MultiWOZ_2.2)

Output:
1. JSON files from dataset with replaced user dialog-acts in 'hindi-dataset/attraction-restaurant-taxi'
2. 'hindi-dataset/not_found_attraction_hindi.json' with values that were not matched in database (hindi equivalent not found)

Running command syntax:
1. Set the ATTRACTION_EXCEL and DATASET_DIR, OUTPUT_DIR paths in the file (line 21, 22)
2. Install pandas using 'pip3 install pandas=1.2.0'
3. Run using 'python3 hindi.py'
'''

import os
import json
import pandas as pd

ATTRACTION_EXCEL = './Attraction_Database.xlsx' # Set the path of attraction_database excel file relative to the directory in which file is present
DATASET_DIR = './dataset/attraction-restaurant-taxi/'   # Set the path of 'attraction-restaurant-taxi' data (relative to the directory in which file is present)
OUTPUT_DIR = './' # Set the output directory relative to the directory in which file is present

# DO NOT CHANGE ANYTHING AFTER THIS LINE
# --- Setting location of the parent directory  ---
parent_dir = os.path.dirname(os.path.abspath(__file__))

output_path = os.path.join(parent_dir, OUTPUT_DIR)
excel_path = os.path.join(parent_dir, ATTRACTION_EXCEL)
dataset_directory = os.path.join(parent_dir, DATASET_DIR)

not_found = {}

def create_directory(output_path):
    '''
    Create folder for 'attraction-restaurant-taxi'
    '''
    path = os.path.join(output_path, 'hindi-dataset/attraction-restaurant-taxi/')
    
    try:
        os.makedirs(path)
        print("Created -> {}".format(path))
    
    except FileExistsError as exists:
        print("Already exists -> {}".format(exists.filename))

def fetch_data_from_excel(excel_path):
    '''
    Fetch data from Attraction Database excel file
    '''
    excel = pd.ExcelFile(excel_path)
    data_english = pd.read_excel(excel, 'english-attraction-original')
    data_hindi = pd.read_excel(excel, 'hindi-attraction-original')

    # Drop rows and columsn that contain only NaN values
    data_english = data_english.dropna(axis=0, how='all')
    data_english = data_english.dropna(axis=1, how='all')

    data_hindi = data_hindi.dropna(axis=0, how='all')
    data_hindi = data_hindi.dropna(axis=1, how='all')

    return data_english, data_hindi

def update_not_found(key):
    '''
    Update a global parameter 'not_found' to keep a track of entires that weren't found in database
    '''
    if key in not_found:
        not_found[key] += 1
    else:
        not_found[key] = 1

def get_hindi_value(data_english, data_hindi, key, english_value):
    '''
    Find the hindi equivalent of an english value from the database
    Returns hindi_value if found, otherwise return the original english_value
    '''
    # 'entrancefee' in dialog acts is 'entrance fee' in database
    if key == 'entrancefee':
        key =  'entrance fee'
    if key in data_english:
        try:
            index = data_english[data_english[key].str.contains(str(english_value))].index.values.astype(int)[0]
        except:
            index = None
        if index is not None:
            id = int(data_english.iloc[index].id)
            hindi_value = data_hindi[data_hindi.id == id][key].values[0]
            return hindi_value
        else:
            update_not_found('{} - {}'.format(key, english_value))
            return english_value
        
    else:
        update_not_found(key)
        return english_value

def write_to_file(json_data, path_to_file):
    '''
    Write the contents to a file
    '''
    f = open(path_to_file, 'w')
    json.dump(json_data, f, indent=2)
    f.close()

def replace_with_hindi(data_english, data_hindi, dataset_directory):
    '''
    Iterate over all dialog files present in 'attraction-restaurant-taxi' and replace user dialog act values with hindi
    '''
    print("Replacing user dialog act values with hindi...")

    for json_file in os.listdir(dataset_directory):
        # Skip non-json files as well has list.json file
        if json_file == 'list.json' or not json_file.endswith('.json'):
            continue
        
        # Read the english value from each file and replace with hindi
        path = os.path.join(dataset_directory, json_file)
        with open(path, 'r') as f:
            json_data = json.load(f)
            attraction_goal = json_data['goal']['attraction']
            info = attraction_goal['info']
            fail_info = attraction_goal['fail_info']
            for key in info:
                hindi_value = get_hindi_value(data_english, data_hindi, key, info[key])
                json_data['goal']['attraction']['info'][key] = hindi_value
            for key in fail_info:
                hindi_value = get_hindi_value(data_english, data_hindi, key, fail_info[key])
                json_data['goal']['attraction']['fail_info'][key] = hindi_value

            log = json_data['log']
            for dialog_index, dialog in enumerate(log):
                # Skip if system dialog act (even dialogues) - (odd in code because index starts from 0)
                if dialog_index % 2 == 1 :
                    continue
                dialog_act = dialog['dialog_act']
                for act in dialog_act:
                    if act.find('Attraction') == -1:
                        continue
                    slots = dialog_act[act]
                    for slot_index, slot in enumerate(slots):
                        key, value = slot
                        hindi_value = get_hindi_value(data_english, data_hindi, key, value)
                        json_data['log'][dialog_index]['dialog_act'][act][slot_index][1] = hindi_value

        # Write the hindi contents to a new file (copy)
        new_file_path = os.path.join(output_path, 'hindi-dataset/attraction-restaurant-taxi/' + json_file)
        write_to_file(json_data, new_file_path)

    print('Done :)')
    print('The words which could not be replaced are available in hindi-dataset/not_found_attraction_hindi.json')

create_directory(output_path)
data_english, data_hindi = fetch_data_from_excel(excel_path)
replace_with_hindi(data_english, data_hindi, dataset_directory)
write_to_file(not_found, os.path.join(output_path, 'hindi-dataset/not_found_attraction_hindi.json'))