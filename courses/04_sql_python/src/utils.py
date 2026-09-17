def read_csv(file_path):
    import pandas as pd
    return pd.read_csv(file_path)

def save_to_csv(dataframe, file_path):
    import pandas as pd
    dataframe.to_csv(file_path, index=False)

def clean_data(dataframe):
    # Example function to clean data
    return dataframe.dropna()

def print_dataframe_info(dataframe):
    print(dataframe.info())

def convert_to_datetime(dataframe, column_name):
    dataframe[column_name] = pd.to_datetime(dataframe[column_name])
    return dataframe