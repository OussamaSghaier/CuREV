from dataclasses import dataclass, field
from typing import Optional, Tuple


@dataclass
class ExLlamaArguments:
    # Used for inference with ExLlama-V2
    model_dir: Optional[str] = field(
        default="../models/Meta-Llama-3.1-70B-Instruct-GPTQ-INT4/",
        metadata={"help": "Path to the local model directory."}
    )

    # Used for training with Huggingface
    model_name_or_path: Optional[str] = field(
        default="deepseek-ai/deepseek-coder-6.7b-instruct",
        metadata={"help": "Name or path to the huggingface model."}
    )

    dataset_path: Optional[str] = field(
        default="./data/Code_Refinement/CRdataset",
        metadata={"help": "Path to the huggingface dataset."}
    )

    output_path: Optional[str] = field(
        default="./data/eval_results/results_final_special.jsonl",
        metadata={"help": "Path to the saved inference results after each save_steps steps."}
    )

    checkpoint_path: Optional[str] = field(
        default="./data/eval_results/results_ckpt_special.jsonl",
        metadata={"help": "Path to the final saved inference results."}
    )

    max_seq_len: Optional[int] = field(
        default=32768,
        metadata={"help": "Maximum sequence length for input tokens."}
    )

    max_batch_size: Optional[int] = field(
        default=256,
        metadata={"help": "Maximum batch size to be used during inference."}
    )

    max_q_size: Optional[int] = field(
        default=4,
        metadata={"help": "Maximum number of sequences to queue for processing at one time."}
    )

    gen_settings: Optional[Tuple[float, float]] = field(
        default=(1.0, 0),
        metadata={"help": "Pair of floats representing the token repetition penalty and sampling temperature settings for generation."}
    )

    max_new_tokens: Optional[int] = field(
        default=1024,
        metadata={"help": "Maximum number of new tokens to generate."}
    )

    save_steps: Optional[int] = field(
        default=200,
        metadata={"help": "The inference results will be saved at these steps."}
    )

    num_epochs: Optional[int] = field(
        default=5,
        metadata={"help": "The inference results will be saved at these steps."}
    )

    batch_size: Optional[int] = field(
        default=4,
        metadata={"help": "Batch size during inference."}
    )
    
