import re
import json
from dataset import load_jsonl_file
from util import sort_dicts_by_key
from dataset import save_dicts_to_jsonl, jsonl_to_csv

def extract_judgments(text):
    type_pattern = r"Type:\s*(\[?[a-zA-Z, ]+\]?)"
    nature_pattern = r"Nature:\s*(\[?[a-zA-Z, ]+\]?)"
    civility_pattern = r"Civility:\s*(\w+)"
    conciseness_pattern = r"Conciseness:\s*(\d+)"
    clarity_pattern = r"Clarity:\s*(\d+)"
    relevance_pattern = r"Relevance:\s*(\d+)"
    rationale_pattern = r"Relevance:\s*\d+\s*(.*)" 


    type_match = re.search(type_pattern, text)
    nature_match = re.search(nature_pattern, text)
    civility_match = re.search(civility_pattern, text)
    conciseness_match = re.search(conciseness_pattern, text)
    clarity_match = re.search(clarity_pattern, text)
    relevance_match = re.search(relevance_pattern, text)
    rationale_match = re.search(rationale_pattern, text, re.DOTALL)

    types = type_match.group(1).strip('[]').split(', ')
    types = [t.strip() for t in types]
    natures = nature_match.group(1).strip('[]').split(', ')
    civility = civility_match.group(1)
    conciseness = int(conciseness_match.group(1))
    clarity = int(clarity_match.group(1))
    relevance = int(relevance_match.group(1))
    rationale = rationale_match.group(1).strip()

    # handle special cases
    for i, t in enumerate(types):
        if t == "Bug fix":
            types[i] = "Bugfix"
        elif t in ["Clarification", 'Performance Optimization', "Performance", "Optimization", "Security"]:
            types[i] = "Other"
    

    extracted_info = {
        "Type": types,
        "Nature": natures,
        "Civility": civility,
        "Conciseness": conciseness,
        "Clarity": clarity,
        "Relevance": relevance,
        "Rationale": rationale
    }

    return extracted_info


def postprocess_inference_results(inference_results):
    postprocessed_results = []
    for i, result in enumerate(inference_results):
        try:
            judgments = extract_judgments("Generated review comment:"+result["completion"])
        except Exception as e:
            print(e)
            exit()
        result["judgments"] = judgments
        postprocessed_results.append(result)
    return postprocessed_results

def assert_valid_judgment(judgment):
    assert "Type" in judgment
    assert "Nature" in judgment
    assert "Civility" in judgment
    assert "Conciseness" in judgment
    assert "Clarity" in judgment
    assert "Relevance" in judgment
    assert "Rationale" in judgment
    for t in judgment["Type"]:
        assert t in ["Refactoring", "Bugfix", "Testing", "Logging", "Documentation", "Other"]
    for n in judgment["Nature"]:
        assert n in ["Descriptive", "Prescriptive", "Clarification", "Other"] 
    assert judgment["Civility"] in ["Civil", "Uncivil"]
    assert judgment["Conciseness"] in range(1, 11)
    assert judgment["Clarity"] in range(1, 11)
    assert judgment["Relevance"] in range(1, 11)


def postprocessing(results_file, output_file):
    results = load_jsonl_file(results_file)
    postprocessed_results = postprocess_inference_results(results)
    save_dicts_to_jsonl(postprocessed_results, output_file)


if __name__ == "__main__":
    results_file = "../data/eval_results/eval_results_final.jsonl"
    output_file = "../data/eval_results/eval_results_postprocessed.jsonl"
    postprocessing(results_file, output_file)


