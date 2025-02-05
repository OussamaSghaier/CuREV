import re
import json
from dataset import load_jsonl_file
from util import sort_dicts_by_key
from dataset import save_dicts_to_jsonl, jsonl_to_csv

def extract_judgments(text):
    text = "Reformulated review comment: " + text
    ttext = text.split('Reformulated review comment evaluation:')[1]

    reformulated_comment_pattern = r"Reformulated review comment:\s*(.*?)\s*Reformulated review comment evaluation:"
    type_pattern = r" Type:\s*(\[?[a-zA-Z, ]+\]?)"
    nature_pattern = r" Nature:\s*(\[?[a-zA-Z, ]+\]?)"
    civility_pattern = r" Civility:\s*(\w+)"
    conciseness_pattern = r" Conciseness:\s*(\d+)"
    clarity_pattern = r" Clarity:\s*(\d+)"
    rationale_pattern = r"\sRationale:\s*(.*)"

    reformulated_comment_match = re.search(reformulated_comment_pattern, text, re.DOTALL)
    type_match = re.search(type_pattern, ttext)
    nature_match = re.search(nature_pattern, ttext)
    civility_match = re.search(civility_pattern, ttext)
    conciseness_match = re.search(conciseness_pattern, ttext)
    clarity_match = re.search(clarity_pattern, ttext)
    rationale_match = re.search(rationale_pattern, ttext, re.DOTALL)

    reformulated_comment = reformulated_comment_match.group(1).strip()
    types = type_match.group(1).strip('[]').split(', ')
    types = [t.strip() for t in types]
    natures = nature_match.group(1).strip('[]').split(', ')
    civility = civility_match.group(1)
    conciseness = int(conciseness_match.group(1))
    clarity = int(clarity_match.group(1))
    rationale = rationale_match.group(1).strip()

    # handle special cases
    for i, t in enumerate(types):
        if t == "Bug fix":
            types[i] = "Bugfix"
        elif t in ["Clarification", 'Performance Optimization', "Performance", "Optimization", "Security", "Debugging", "Accessibility"]:
            types[i] = "Other"    

    extracted_info = {
        "Reformulated Review Comment": reformulated_comment,
        "Type": types,
        "Nature": natures,
        "Civility": civility,
        "Conciseness": conciseness,
        "Clarity": clarity,
        "Rationale": rationale
    }

    return extracted_info


def postprocess_inference_results(inference_results):
    postprocessed_results = []
    n = 0
    for i, result in enumerate(inference_results):
        judgments = None
        try:
            judgments = extract_judgments(result["completion"])
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
    assert "Rationale" in judgment
    for t in judgment["Type"]:
        try:
            assert t in ["Refactoring", "Bugfix", "Testing", "Logging", "Documentation", "Other"]
        except Exception as e:
            print(judgment)
            exit()
    for n in judgment["Nature"]:
        assert n in ["Descriptive", "Prescriptive", "Clarification", "Other"] 
    assert judgment["Civility"] in ["Civil", "Uncivil"]
    assert judgment["Conciseness"] in range(1, 11)
    assert judgment["Clarity"] in range(1, 11)


def postprocessing(results_file, output_file):
    results = load_jsonl_file(results_file)
    postprocessed_results = postprocess_inference_results(results)
    for result in postprocessed_results:
        assert_valid_judgment(result["judgments"])
    save_dicts_to_jsonl(postprocessed_results, output_file)


if __name__ == "__main__":
    results_file = "../data/reform_results/reform_results_final.jsonl"
    output_file = "../data/reform_results/reform_results_postprocessed.jsonl"
    postprocessing(results_file, output_file)


