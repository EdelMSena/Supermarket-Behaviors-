from pathlib import Path
from typing import Dict, Any, Union
import pandas as pd

def load_data(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Load data safely from a CSV file into a pandas DataFrame.
    """
    path = Path(file_path)
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        print(f"Error: The file at '{path}' was not found.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file at '{path}' is empty.")
    except pd.errors.ParserError:
        print(f"Error: The file at '{path}' could not be parsed.")
    except Exception as e:
        print(f"An unexpected error occurred while reading '{path}': {e}")
        
    return pd.DataFrame()


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform standard data cleaning operations:
    - Standardize column names (lowercase, snake_case, alphanumeric/underscores only)
    - Remove duplicate rows
    - Strip leading/trailing whitespace from string columns
    - Handle missing values (numeric -> median, categorical -> 'Unknown')
    """
    if df.empty:
        print("Warning: Input DataFrame is empty. Skipping cleaning.")
        return df

    df_cleaned = df.copy()

    df_cleaned.columns = (
        df_cleaned.columns
        .str.strip()
        .str.lower()
        .str.replace(r'\s+', '_', regex=True)
        .str.replace(r'[^a-z0-9_]', '', regex=True)
    )

    initial_rows = len(df_cleaned)
    df_cleaned = df_cleaned.drop_duplicates()
    dropped_duplicates = initial_rows - len(df_cleaned)
    if dropped_duplicates > 0:
        print(f"Dropped {dropped_duplicates} duplicate rows.")

    string_cols = df_cleaned.select_dtypes(include=['object', 'string']).columns
    for col in string_cols:
        df_cleaned[col] = df_cleaned[col].str.strip()

    for col in df_cleaned.columns:
        if df_cleaned[col].isnull().sum() > 0:
            if pd.api.types.is_numeric_dtype(df_cleaned[col]):
                median_val = df_cleaned[col].median()
                df_cleaned[col] = df_cleaned[col].fillna(median_val)
                print(f"Imputed missing values in numeric column '{col}' with median: {median_val}")
            else:
                df_cleaned[col] = df_cleaned[col].fillna("Unknown")
                print(f"Imputed missing values in categorical column '{col}' with 'Unknown'")

    return df_cleaned


def get_subset(
    df: pd.DataFrame, 
    n: int = 12000, 
    seed: int = 40, 
    out_path: Union[str, Path, None] = None
) -> pd.DataFrame:
    """
    Extract a random subset from a DataFrame and cache it to CSV.
    """
    if out_path is None:
        base_dir = Path(__file__).resolve().parents[1] if "__file__" in globals() else Path.cwd()
        out_path = base_dir / "Data" / "supermarket_subset.csv"
    else:
        out_path = Path(out_path)

    if out_path.exists():
        return pd.read_csv(out_path)

    if df.empty:
        print("Warning: Input DataFrame is empty. Returning empty subset.")
        return pd.DataFrame()

    sample_size = min(n, len(df))
    subset = df.sample(n=sample_size, random_state=seed)
    
    out_path.parent.mkdir(parents=True, exist_ok=True)
    subset.to_csv(out_path, index=False)
    
    return subset


def check_data_quality(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate a concise quality report summarizing shape, missing values, and duplicate rows.
    """
    if df.empty:
        return {"shape": (0, 0), "missing_values": pd.Series(dtype=int), "duplicated_values": 0}

    missing_series = df.isnull().sum()
    
    return {
        "shape": df.shape,
        "missing_values": missing_series[missing_series > 0],
        "duplicated_values": int(df.duplicated().sum())
    }


if __name__ == "__main__":
    file_path = "path/to/your/supermarket_data.csv"
    raw_df = load_data(file_path)
    
    if not raw_df.empty:
        cleaned_df = clean_data(raw_df)
        print("Data Quality Report after cleaning:")
        print(check_data_quality(cleaned_df))
        
        subset_df = get_subset(cleaned_df)
        print(f"Subset shape: {subset_df.shape}")