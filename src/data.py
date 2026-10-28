from pathlib import Path

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

def get_subset(df, n=12000, seed=40, out_path=None):
    if out_path is None:
        out_path = Path(__file__).resolve().parents[1] / "Data" / "supermarket_subset.csv"
    else:
        out_path = Path(out_path)

    if out_path.exists():
       return pd.read_csv(out_path)

    subset = df.sample(n=min(n, len(df)), random_state=seed)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    subset.to_csv(out_path, index=False)
    return subset
