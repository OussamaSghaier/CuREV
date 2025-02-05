import logging
logging.getLogger().setLevel(logging.ERROR)
from code_bleu import compute_codebleu_avgscore
from crystal_bleu import compute_crystalBLEU_avgscore
from dataset import load_dataset

languages = ['.cs', 'cpp', 'py', 'js', 'php', 'go', 'rb', 'c', 'java']

def is_exactMatch(true_code, gen_code):
    true_code = true_code.strip().split('\n')
    true_code = [c.strip() for c in true_code if c.strip().startswith('+') or c.strip().startswith('-')]
    true_code = '\n'.join(true_code)
    true_code = ' '.join(true_code.split())
    
    gen_code = gen_code.strip().split('\n')
    gen_code = [c.strip() for c in gen_code if c.strip().startswith('+') or c.strip().startswith('-')]
    gen_code = '\n'.join(gen_code)
    gen_code = ' '.join(gen_code.split())


    return true_code == gen_code
    
def preprocess_code(code):
    code = code.strip().split('\n')
    code = [c.strip() for c in code if c.strip().startswith('+') or c.strip().startswith('-')]
    code = '\n'.join(code)
    code = ' '.join(code.split())
    return code

def preprocess_gen_code(code, hunk):
    code = code.strip().split('\n')
    code = [c.strip() for c in code]
    code = '\n'.join(code)
    code = ' '.join(code.split())
    return code

def preprocess_hunk(code):
    code = code.strip().split('\n')
    code = [c.strip() for c in code]
    code = '\n'.join(code)
    code = ' '.join(code.split())
    return code


def evaluate(data):
    samples = []
    for lang in languages:
        temp = []
        for d in data:
            if d['lang'] == lang:
                temp.append(d)
        samples.append(temp)

    codebleus = []
    exact_matches = []

    for i, sample in enumerate(samples):
        references = [[preprocess_code(example['hunk'])] for example in sample]
        candidates = [preprocess_code(example['generated_code']) for example in sample]
        temp = [compute_codebleu_avgscore([reference], [candidate], languages[i]) for reference, candidate in zip(references, candidates)]
        codebleu = sum(temp) / len(temp)
        # codebleu = compute_crystalBLEU_avgscore(references, candidates, lang=languages[i])
        codebleus.append(codebleu)

        # Calculate Exact Match
        exact_match = sum(1 for ref, cand in zip(references, candidates) if ref[0]==cand)
        exact_matches.append(exact_match)


    # Print CodeBLEU and Exact Match results
    print("CodeBLEU scores per language:", codebleus)
    print("Average CodeBLEU:", sum(codebleus) / len(codebleus))
    print("Exact Match scores per language (%):", exact_matches)
    print("Total Exact Match:", sum(exact_matches))




if __name__ == '__main__':
    print('### Initial dataset ###')
    data = load_dataset('../data/refinement_results/final/init_refinement_20k')
    evaluate(data)

    print('### Curated dataset ###')
    data = load_dataset('../data/refinement_results/final/cur_refinement_20k')
    evaluate(data)