import json
import time

from prompt_templates import (
    review_classification_system_prompt,
    review_classification_template,
    llama_template
)
from config import ExLlamaArguments
from transformers import HfArgumentParser
from dataset import load_dataset, save_data
import exllamav2
from exllamav2 import ExLlamaV2, ExLlamaV2Config, ExLlamaV2Cache, ExLlamaV2Tokenizer, Timer
from exllamav2.generator import ExLlamaV2DynamicGenerator, ExLlamaV2DynamicJob, ExLlamaV2Sampler


# parse arguments
parser = HfArgumentParser(ExLlamaArguments)
model_args = parser.parse_args_into_dataclasses()[0]

dataset_path = model_args.dataset_path
model_dir = model_args.model_dir
output_path = model_args.output_path
checkpoint_path = model_args.checkpoint_path
save_steps = model_args.save_steps
config = ExLlamaV2Config(model_dir)
config.arch_compat_overrides()
model = ExLlamaV2(config)
cache = ExLlamaV2Cache(model, max_seq_len = model_args.max_seq_len, lazy = True)
model.load_autosplit(cache, progress = True)

print("Loading tokenizer...")
tokenizer = ExLlamaV2Tokenizer(config)

generator = ExLlamaV2DynamicGenerator(
    model=model,
    cache=cache,
    tokenizer=tokenizer,
    max_batch_size=model_args.max_batch_size,
    max_q_size=model_args.max_q_size
)

gen_settings = ExLlamaV2Sampler.Settings(
    token_repetition_penalty = model_args.gen_settings[0],
    temperature = model_args.gen_settings[1],
)

data = load_dataset(dataset_path)
print("Dataset size", data.shape)
print("Dataset features", data.column_names)


with exllamav2.util.get_basic_progress() as progress:
    task = progress.add_task("[red]Creating jobs", total=len(data), name="Creating jobs")
    for idx, sample in enumerate(data):
        user_input = review_classification_template.format(
            review_comment=sample["comment"].strip(),
            code_diffs=sample["old_hunk"].strip()
        )
        input_prompt = llama_template.format(
            system_prompt=review_classification_system_prompt,
            user_prompt=user_input
        )
        input_ids = tokenizer.encode(input_prompt, encode_special_tokens=True, add_bos=False)

        job = ExLlamaV2DynamicJob(
            input_ids=input_ids,
            gen_settings=gen_settings,
            max_new_tokens=model_args.max_new_tokens,
            stop_conditions=[tokenizer.single_id("<|eot_id|>")],
            token_healing=True,
            identifier=idx,
        )

        generator.enqueue(job)
        progress.update(task, advance=1)

samples = []
num_completions = 0
num_tokens = 0
time_begin = time.time()

with exllamav2.util.get_basic_progress() as progress:
    task = progress.add_task("[red]Generating", total=generator.num_remaining_jobs(), name="Generating samples")

    while generator.num_remaining_jobs():
        results = generator.iterate()

        bsz = len(set([r["identifier"] for r in results]))
        num_tokens += bsz

        for result in results:
            if not result["eos"]: continue

            idx = result["identifier"]
            response = result["full_completion"]

            # Measure performance
            num_completions += 1
            elapsed_time = time.time() - time_begin
            rpm = num_completions / (elapsed_time / 60)
            tps = num_tokens / elapsed_time
            print()
            print("---------------------------------------------------------------------------")
            print(f"Current batch size: {bsz}")
            print(f"Avg. completions/minute: {rpm:.2f}")
            print(f"Avg. output tokens/second: {tps:.2f}")
            print("---------------------------------------------------------------------------")

            # Spam completions to the console
            print()
            print(f"Completion {idx} done.")
            print()

            samples.append(dict(task_id=idx, completion=response))
            progress.update(task, advance=1)

            if len(samples) % save_steps == 0:
                save_data(samples[len(samples)-save_steps:], checkpoint_path)

save_data(samples, output_path)
