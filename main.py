from src.data import load_data, get_subset
from pathlib import Path

if Path('Data/supermarket_subset.csv').exists():
    print("Subset already exists. Loading from file.")
    subset =load_data('Data/supermarket_subset.csv')
else:
    df = load_data('Data/supermarket_large_dataset.csv')
    print("Original shape:", df.shape)
    subset = get_subset(df)
print("Subset shape:", subset.shape)


