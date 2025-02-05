from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction
import nltk
from dataset import load_jsonl_file


chencherry = SmoothingFunction()

def remove_stop_words(sentence):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    words = sentence.split()
    return ' '.join([word for word in words if word.lower() not in stop_words])

def calculate_blue_score(candidate_translation, reference_translations):
    # Tokenize candidate translation and reference translations
    candidate_tokens = nltk.word_tokenize(candidate_translation)
    reference_tokens = [nltk.word_tokenize(reference) for reference in reference_translations]
    blue_score = sentence_bleu(reference_tokens, candidate_tokens, smoothing_function=chencherry.method7, auto_reweigh=True)#, weights=(0.25, 0.25, 0.25, 0.25))
    return blue_score


def compute_bleu_score(data, column_name1, column_name2):
    bleu = 0
    for d in data:
        reference = d[column_name1].strip().lower()
        response = d[column_name2].strip().lower()
        
        reference = remove_stop_words(reference)
        response = remove_stop_words(response)

        score = calculate_blue_score(response, [reference])
        bleu += score

    return bleu/len(data)*100


file_path = '../../data/comment_results/inference/init/inference_results_final.jsonl'
data = load_jsonl_file(file_path)
bleu = compute_bleu_score(data, 'original_comment', 'genrated_comment') #genrated_comment : typo
print('### Initial dataset ###')
print(bleu)
print('='*50)
file_path = '../../data/comment_results/inference/cur/inference_results_final-v2.jsonl'
data = load_jsonl_file(file_path)
bleu = compute_bleu_score(data, 'reformulated_comment', 'genrated_comment')
print('### Curated dataset ###')
print(bleu)


