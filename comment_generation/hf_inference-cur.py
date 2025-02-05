import json
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, set_seed, HfArgumentParser
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    MofNCompleteColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    TaskProgressColumn,
    SpinnerColumn,
)
from rich.console import Console
console = Console()
import random
import torch
from prompt_templates import (
    review_classification_system_prompt,
    review_classification_template,
)
from config import ExLlamaArguments
from dataset import load_dataset, save_data
set_seed(27)

# parse arguments
parser = HfArgumentParser(ExLlamaArguments)
model_args = parser.parse_args_into_dataclasses()[0]

model_name_or_path = model_args.model_name_or_path
dataset_path = model_args.dataset_path
output_path = model_args.output_path
checkpoint_path = model_args.checkpoint_path
batch_size = model_args.batch_size
max_seq_length = model_args.max_seq_len
max_new_tokens = model_args.max_new_tokens
save_steps = model_args.save_steps

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name_or_path,
    device_map="auto",
    trust_remote_code=False,
    torch_dtype=torch.float16,
).eval()
generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

data = load_dataset(dataset_path)
print("Dataset size", data.shape)

# select random k samples
seed = 3
k = 20000
random.seed(seed)
sample_indices = random.sample(range(len(data)), k)
data = data.select(sample_indices[15000:])
print("Dataset features", data.column_names)
print("Selected dataset size", data.shape)

results = []

with Progress(
    SpinnerColumn(), 
    TextColumn(f"[bold blue]{model_name_or_path}"),
    BarColumn(bar_width=None), 
    TaskProgressColumn(),
    MofNCompleteColumn(),
    TextColumn("[bold green]•", justify="center"),
    TimeElapsedColumn(),
    TimeRemainingColumn(),
    console=console
) as p:

    for batch in p.track(data.iter(batch_size=batch_size), total=(len(data)+batch_size-1)//batch_size):
        prompts = []
        system_prompt = review_classification_system_prompt
        for i in range(len(batch['comment'])):
            user_input = review_classification_template.format(
                code_diff=batch["old_hunk"][i].strip(),
            )
            messages = [
                        {'content': system_prompt, 'role': 'system'},
                        {'content': user_input, 'role': 'user'}
            ]
            prompt = tokenizer.apply_chat_template(
                        messages,
                        tokenize=False,
                        add_generation_prompt=True
            )
            prompts.append(prompt)
        responses = generator(
                    prompts,
                    max_new_tokens=max_new_tokens,
                    # do_sample=True,
                    # top_p=0.95,
                    # num_return_sequences=1,
                    return_full_text=False
        )
        for i, res in enumerate(responses):
            results.append({
                'prompt': prompts[i],
                'genrated_comment': res[0]['generated_text'],
                'reformulated_comment': batch['reformulated_comment'][i],
            })
        if len(results) % save_steps == 0:
                save_data(results[len(results)-save_steps:], checkpoint_path)


# save results
print("Saving data to ", output_path)
print("Size: ", len(results))
save_data(results, output_path)

        
