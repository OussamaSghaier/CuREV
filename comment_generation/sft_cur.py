import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, BitsAndBytesConfig, pipeline, HfArgumentParser
import random
from datasets import load_dataset
from trl import SFTTrainer
from peft import LoraConfig
import transformers
transformers.set_seed(27)
from config import ExLlamaArguments
from dataset import load_dataset
from prompt_templates import review_classification_system_prompt, review_classification_template

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
num_epochs = model_args.num_epochs


model_kwargs = {
        "low_cpu_mem_usage": True,
        "trust_remote_code": False, 
        "torch_dtype": torch.float16
}

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)
if tokenizer.pad_token_id is None:
    tokenizer.pad_token_id = tokenizer.eos_token_id


q_config = BitsAndBytesConfig(
   load_in_4bit=True,
   bnb_4bit_quant_type="nf4",
   bnb_4bit_use_double_quant=True,
   bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(model_name_or_path,
                                            **model_kwargs,
                                            attn_implementation="flash_attention_2",
                                            device_map="auto", 
                                            quantization_config=q_config)

data = load_dataset(dataset_path)
print("Dataset size", data.shape)

# select random k samples
seed = 3
k = 20000
random.seed(seed)
sample_indices = random.sample(range(len(data)), k)
# select 15000 samples for training
data = data.select(sample_indices[0:15000])
print("Selected dataset size", data.shape)
print("Dataset features", data.column_names)


system_prompt = review_classification_system_prompt
user_prompt = review_classification_template

def format_prompt(example):
    prompts = []
    for i in range(len(example['old_hunk'])):
        user_input = review_classification_template.format(
                code_diff=example["old_hunk"][i].strip()
            )
        messages = [
                    {'content': system_prompt, 'role': 'system'},
                    {'content': user_input, 'role': 'user'},
                    {'content': example["reformulated_comment"][i], 'role': 'assistant'}
        ]
        prompt = tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True
        )
        prompts.append(prompt)
    return prompts

# collator = DataCollatorForCompletionOnlyLM(response_template=answer_ids, tokenizer=tokenizer)

training_args = TrainingArguments(
    output_dir=checkpoint_path,
    gradient_accumulation_steps=4,
    num_train_epochs=num_epochs,
    save_steps=save_steps,
    logging_steps=10,
    per_device_train_batch_size=batch_size
)

peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)


trainer = SFTTrainer(
    model,
    train_dataset=data,
    tokenizer=tokenizer,
    args=training_args,
    peft_config=peft_config,
    max_seq_length=1024,
    # data_collator=collator,
    formatting_func=format_prompt,
    # packing=True
)

trainer.train()
trainer.save_state()
trainer.save_model(output_path)



