CuREV: Curating Review Comments for Improved Code Review Automation
===============================
This is the replication package accompanying our paper, *Curating Review Comments for Improved Code Review Automation*.

The datasets of this paper are available on [Zenodo](https://zenodo.org/records/14058666).

Overview
---
We propose a methodology to curate a code reviews dataset to enhance its quality and improve the performance of language models on code review downstream tasks, namely comment generation and code refinement.

The main contributions of this work are threefold: 
(1) *A data-centric evaluation framework*, 
(2) *A curation pipeline to improve the quality of review comments*, and 
(3) *Evaluation of the curated dataset, compared to the original, on downstream tasks (i.e, comment generation and code refinement)*.

Project structure
---
The project is structured as follows.
    
    .
    ├── code_refinement/        # Code refinement package
    ├── comment_generation/     # Comment generation package
    ├── quality_assessment/        # empirical study package
    ├── data_curation/          # dataset curation package
    ├── util/                   # package for helpers and config
    ├── data/                   # Folder for dataset and results
    ├── models/                 # Folder for large language models
    ├── requirements.txt        # required python libraries



Environment setup
---
To facilitate usage and results replication, we include a file ```requirements.txt``` to install the required python libraries.
Here are the instructions to create a virtual environment, activate it, and install dependencies using the provided `requirements.txt` file:

1. **Create a Virtual Environment**  
   Run the following command to create a virtual environment named `venv`:
   ```bash
   python3 -m venv venv
   ```

2. **Activate the Virtual Environment**  
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```
   - On **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```

3. **Install Dependencies**  
   With the virtual environment activated, install the required Python libraries from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify the Installation**  
   To confirm that all dependencies are installed correctly, run:
   ```bash
   pip list
   ```

5. **Deactivating the Environment**  
   When you’re finished, you can deactivate the virtual environment with:
   ```bash
   deactivate
   ```

Data
---
The original code review dataset is available in [Zenodo](https://zenodo.org/records/14058666).
To run the experiments, you need to download ```Code_Refinement.zip``` and place the dataset under the ```data/``` folder.
You can use the utilities method *create_HFdataset* in ```util.dataset``` to merge the downloaded jsonl files into a HuggingFace dataset. 

Models
---
We run *Llama-3.1-70B* on our local machines using [ExLlamaV2](https://github.com/turboderp/exllamav2) to geneerate accurate judgments using our defined evaluation framework.
You can choose the [same model](https://huggingface.co/hugging-quants/Meta-Llama-3.1-70B-Instruct-GPTQ-INT4) or any other model.
Or, you can to download a quantized version of any other model that is compatible with *ExLlamaV2*.
The downloaded model should be placed under the folder ```models/```.


1- A data-centric evaluation framework
---

We propose an evaluation framework to categorize and assess the quality of code reviews. It consists of (1) a **categorization scheme** to classify the *type*, *nature*, and *civility* of code review comments, and (2) **scoring criteria** to assess the overall quality of code reviews based on their *relevance*, *clarity*, and *conciseness*. We apply our evaluation framework to the largest existing dataset of code reviews. Given the scale of the dataset, we utilize a large language model (LLM) as a judge to automatically annotate samples with thoroughly designed prompts to ensure reliable and consistent annotations.

The experiments conducted for this contribution are available under the folder ```quality_assessment/```.

To run the LLM judgments:
```bash
python quality_assessment/inference.py \
      --model_dir="models/Meta-Llama-3.1-70B-Instruct-GPTQ-INT4/" \
      --dataset_path="data/Code_Refinement/CRdataset" \
      --save_steps=5000
```
The full list of arguments is available in ```util/config.py```.


2- CuREV: a curated dataset for code review
---

The experiments conducted for this contribution are available under the folder ```data_curation/```.

To run the experiments for reformulating review comments:
```bash
python reformulate_reviews/inference.py \
      --model_dir="models/Meta-Llama-3.1-70B-Instruct-GPTQ-INT4/" \
      --dataset_path="data/Code_Refinement/CRdataset" \
      --output_path="data/eval_results/reform_results.jsonl" \
      --save_steps=5000
```
The full list of arguments is available in ```util/config.py```.


3-a. Comment generation
---

The experiments conducted for this contribution are available under the folder ```comment_generation/```.

- To train a language model on comment generation on the original dataset:
```bash
python comment_generation/sft_init.py \
      --model_name_or_path="deepseek-ai/deepseek-coder-6.7b-instruct" \
      --dataset_path="data/Code_Refinement/CRdataset" \
      --output_path="data/eval_results/reform_results.jsonl" \
      --save_steps=200 \
      --checkpoint_path="models/comment_generation/init_ckpts" \
      --output_path="models/comment_generation/final_model"
```

- To train a language model on comment generation on the original dataset:
```bash
python comment_generation/sft_cur.py \
      --model_name_or_path="deepseek-ai/deepseek-coder-6.7b-instruct" \
      --dataset_path="data/Code_Refinement/CRdataset_reform" \
      --output_path="data/eval_results/reform_results.jsonl" \
      --save_steps=200 \
      --checkpoint_path="models/comment_generation/init_ckpts" \
      --output_path="models/comment_generation/final_model"
```

- To run the inference on the initial or curated dataset:
```bash
python comment_generation/hf_inference-init.py
python comment_generation/hf_inference-cur.py
```

- To run the evaluation of both model:
```bash
python comment_generation/evaluation.py"
```


- The full list of arguments is available in ```util/config.py```.


3-b. Code refinement
---

The experiments conducted for this contribution are available under the folder ```code_refinement/```.

- To run the inference of a model for code on the initial dataset:
```bash
python comment_generation/hf_inference-init.py \
      --model_name_or_path="deepseek-ai/deepseek-coder-6.7b-instruct" \
      --dataset_path="data/Code_Refinement/CRdataset" \
      --output_path="data/eval_results/reform_results.jsonl" \
      --save_steps=1000 \
      --output_path="models/init_coderef_results.jsonl"
```

- To run the inference of a model for code on the curated dataset:
```bash
python comment_generation/hf_inference-cur.py \
      --model_name_or_path="deepseek-ai/deepseek-coder-6.7b-instruct" \
      --dataset_path="data/Code_Refinement/CRdataset_reform" \
      --output_path="data/eval_results/reform_results.jsonl" \
      --save_steps=1000 \
      --output_path="models/cur_coderef_results.jsonl"
```

- To run the evaluation of both model:
```bash
python comment_generation/evaluate.py"
```

- The full list of arguments is available in ```util/config.py```.
