from src.data import load_data, get_subset, check_data_quality
from pathlib import Path

data_dir = Path(__file__).resolve().parent / "Data"
subset_path = data_dir / "supermarket_subset.csv"
dataset_path = data_dir / "supermarket_large_dataset.csv"

if subset_path.exists():
    print("Subset already exists. Loading from file.")
    subset = load_data(subset_path)
else:
    df = load_data(dataset_path)
    print("Original shape:", df.shape)
    subset = get_subset(df)

print("Subset shape:", subset.shape)
print("Checking data quality...")
quality_report = check_data_quality(subset)
print("Shape:", quality_report["shape"])
print("Missing values:", quality_report["missing_values"].sum())
print("Duplicated values:", quality_report["duplicated_values"])