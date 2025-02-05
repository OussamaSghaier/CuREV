import datasets
import json
import csv
import pandas as pd
from util import sort_dicts_by_key


def load_dataset(dataset_path, split=None):
    print("Loading dataset from {}".format(dataset_path))
    dataset = datasets.load_from_disk(dataset_path)

    if split is not None and split in ["train", "valid", "test"]:
        return dataset[split]
    return dataset

def load_jsonl_file(file_path):
    print("Loading dataset from {}".format(file_path))
    data = None
    with open(file_path) as lines:
        data = [json.loads(line) for line in lines]
    for d in data:
        if 'ids' in d:
            d['ids'] = list(map(str, d['ids']))
    print("Dataset size = {}".format(len(data)))
    return data

def load_CRdatasets(train_file, valid_file, test_file):
    train_data = load_jsonl_file(train_file)
    valid_data = load_jsonl_file(valid_file)
    test_data = load_jsonl_file(test_file)
    data = train_data + valid_data + test_data
    return data

def create_HFdataset(train_file, valid_file, test_file, output_dir, seed=0):
    data = load_CRdatasets(train_file, valid_file, test_file)
    dataset = datasets.Dataset.from_list(data)
    print("Dataset features = {}".format(dataset.column_names))
    print("Total datasets size = {}".format(len(dataset)))
    dataset = dataset.shuffle(seed=seed)
    dataset.save_to_disk(output_dir)


def save_jsonl_file(data, file_path):
    with open(file_path, 'w') as f:
        for d in data:
            f.write(json.dumps(d) + '\n')


def save_dicts_to_jsonl(data, file_path):
    with open(file_path, 'w') as jsonl_file:
        for item in data:
            jsonl_file.write(json.dumps(item) + '\n')

def jsonl_to_csv(jsonl_file_path, excel_file_path, key=None):
    with open(jsonl_file_path, 'r') as jsonl_file:
        data = [json.loads(line) for line in jsonl_file]
    
    if key:
        data = [d[key] for d in data]

    df = pd.DataFrame(data)    
    df.to_excel(excel_file_path, index=False, engine='openpyxl')

def assert_task_ids(data):
    for i in range(len(data)):
        assert i==data[i]['task_id'], f"task_id {i} not found in data"

def merge_jsonl_files(jsonl_files, output_file, task_bases):
    data = []
    for i, file in enumerate(jsonl_files):
        with open(file, 'r') as f:
            tmp = [json.loads(line) for line in f]
            for t in tmp:
                t['task_id'] += task_bases[i]
            data += tmp 
    data = sort_dicts_by_key(data, "task_id")
    assert_task_ids(data)
    save_jsonl_file(data, output_file)

def save_data(data, data_file):
    print("Saving data to", data_file)
    with open(data_file, "a") as f:
        for d in data:
            f.write(json.dumps(d) + "\n")

