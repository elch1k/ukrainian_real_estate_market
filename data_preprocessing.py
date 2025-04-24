import pandas as pd
from save_load_functions import save_dataframe_to_json


def data_preprocessing(df):
    if df.duplicated().sum() > 0:
        df = df.drop_duplicates()
    
    # also can add another preprocessing things like text preprocessing or etc.
    return df


def main(temporary_file_path='lun_real_estate_data'):
    df = pd.read_json(f'{temporary_file_path}.json')
    df = data_preprocessing(df=df)
    save_dataframe_to_json(df, f'{temporary_file_path}.json')


if __name__=="__main__":
    main()