import pandas as pd
import json

def save_data_to_csv(data, file_path):
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)


def save_data_to_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_csv_data(file_path: str):
    df = pd.read_csv(file_path)
    return df


def load_json_file(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return data


def save_dataframe_to_json(df, file_path):
    json_str = df.to_json(orient='records')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(json_str)