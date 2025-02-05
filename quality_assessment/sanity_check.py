import json
import random
import pandas as pd
from util.dataset import load_dataset

dataset_path = "data/Code_Refinement/CRdataset"
output_file_path = "data/sanity_check/sample.xlsx"

dataset = load_dataset(dataset_path)
dataset = dataset.select(range(20000))

dataset_sample = dataset.shuffle(seed=0).select(range(100))

df = pd.DataFrame(dataset_sample)

df.to_excel(output_file_path, index=False, engine='openpyxl')

print(f"Random sample saved to {output_file_path}")