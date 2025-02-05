import json
import re
from dataset import load_dataset
import random


def extract_code_block(text):
    # Regular expression to match code blocks with any language (eg: ```python ...code... ```))
    code_pattern = r"```[a-zA-Z]+\n(.*?)```"
    # Find all matches with multiline support
    code_blocks = re.findall(code_pattern, text, re.DOTALL)
    code = code_blocks[0]
    return code

data = None
with open('../data/refinement_results/results_0k20k_final.jsonl', "r") as f:
    data = [json.loads(l) for l in f]

print('Number of generated instances:', len(data))
n = 0

for i, d in enumerate(data):
    response = d['response']
    code = None
    try:
        code = extract_code_block(response)
    except:
        if '@@' in response:
            code = response.split('@@')[1]
        else:
            code = response
            n+=1
    d['generated_code'] = code

print(f'# Invalid instances: {n}/{len(data)}')


dataset = load_dataset("../data/Code_Refinement/CRdataset_reform")
print("Original dataset", dataset)

# select random k samples
seed = 3
k = 20000
random.seed(seed)
sample_indices = random.sample(range(len(dataset)), k)
dataset = dataset.select(sample_indices)
print("Selected dataset", dataset)

assert len(data) == len(dataset)

dataset = dataset.add_column('generated_code', [d['generated_code'] for d in data]).\
            add_column('response', [d['response'] for d in data]).\
            add_column('prompt', [d['prompt'] for d in data])

print(dataset)

dataset.save_to_disk('../data/refinement_results/final/init_refinement_20k')