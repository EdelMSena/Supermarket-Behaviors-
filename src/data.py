import pandas as pd

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: A DataFrame containing the loaded data.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.") #catches the file not found error
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        print(f"Error: The file at {file_path} is empty.") #catches the empty file error
        return pd.DataFrame()
    except pd.errors.ParserError:
        print(f"Error: The file at {file_path} could not be parsed.") #catches the parsing error
        return pd.DataFrame()