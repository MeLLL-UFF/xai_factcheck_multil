import pandas as pd

dev_path = 'data/raw/dev-00000-of-00001.csv'
ood_path = 'data/raw/ood-00000-of-00001.csv'
test_path = 'data/raw/test-00000-of-00001.csv'
train_path = 'data/raw/train-00000-of-00001.csv'

dev = pd.read_csv(dev_path)
ood = pd.read_csv(ood_path)
test = pd.read_csv(test_path)
train = pd.read_csv(train_path)

print("Original dataset shapes:")
print(f" - dev: {dev.shape}")
print(f" - ood: {ood.shape}")
print(f" - test: {test.shape}")
print(f" - train: {train.shape}")

dev['source'] = 'dev'
ood['source'] = 'ood'
test['source'] = 'test'
train['source'] = 'train'

all_data = pd.concat([dev, ood, test, train], ignore_index=True)
print(f"\nShape combinado (antes da deduplicação): {all_data.shape}")

columns_for_dedup = [col for col in all_data.columns if col != 'source']
duplicates = all_data.duplicated(subset=columns_for_dedup, keep='first')
print(f"Número de linhas duplicadas: {duplicates.sum()}")

unified_data = all_data.drop_duplicates(subset=columns_for_dedup, keep='first')
print(f"Shape após remover duplicatas: {unified_data.shape}")

print("\nOrigem das instâncias mantidas:")
print(unified_data['source'].value_counts())

output_path = 'data/processed/unified_dataset.csv'
unified_data.to_csv(output_path, index=False)
print(f"\nArquivo salvo em: {output_path}")

print("\nOverlap entre os conjuntos:")
datasets = {'dev': dev, 'ood': ood, 'test': test, 'train': train}
for name1, ds1 in datasets.items():
    for name2, ds2 in datasets.items():
        if name1 >= name2:
            continue
        ds1_set = set(map(tuple, ds1[columns_for_dedup].values))
        ds2_set = set(map(tuple, ds2[columns_for_dedup].values))
        common = ds1_set.intersection(ds2_set)
