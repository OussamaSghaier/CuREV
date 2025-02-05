from typing import List
from codebleu import calc_codebleu
from transformers import AutoTokenizer

languages_map = {
    '.cs':'c_sharp', 
    'cpp': 'cpp', 
    'py': 'python', 
    'js': 'javascript', 
    'php': 'php', 
    'go': 'go', 
    'rb': 'ruby', 
    'c': 'c', 
    'java': 'java'
    }

model_name = "deepseek-ai/deepseek-coder-6.7b-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)

def compute_codebleu_avgscore(references: List[List[str]], candidates: List[str], lang: str) -> float:
    try:
        bleu = calc_codebleu(references, candidates, lang=languages_map[lang], weights=(0.25, 0.25, 0.25, 0.25), tokenizer=tokenizer)
        if bleu[ 'dataflow_match_score']==0:
            bleu = calc_codebleu(references, candidates, lang=languages_map[lang], weights=(1/3, 1/3, 1/3, 0), tokenizer=tokenizer)
        return bleu['codebleu']
    except Exception as e:
        print(e)
        return 0