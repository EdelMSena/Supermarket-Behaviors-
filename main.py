from src.data import load_data

df = load_data('src/data/supermarket_large_dataset.csv')
print(df.head())
print(df.shape)