from typing import List
from typing import List
from collections import Counter
from nltk.util import ngrams
from crystalbleu import corpus_bleu
import pickle
import os
from dataset import load_dataset

trivial_ngrams_path = 'trivial_ngrams.pkl'
dataset_path = '../data/Code_Refinement/CRdataset_reform'

def compute_trivial_ngrams(dataset_path, trivial_ngrams_path, column, k, n):
    dataset = load_dataset(dataset_path)
    tokenized_corpus = []
    for d in dataset:
        tokenized_corpus.extend(d[column].split())

    all_ngrams = []
    for n in range(1, n+1):
        all_ngrams.extend(list(ngrams(tokenized_corpus, n)))

    frequencies = Counter(all_ngrams)
    trivially_shared_ngrams = dict(frequencies.most_common(k))

    with open(trivial_ngrams_path, 'wb') as f:
        pickle.dump(trivially_shared_ngrams, f)

    return trivially_shared_ngrams

def get_trivial_ngrams(column='oldf', k=500, n=4):
    if os.path.exists(trivial_ngrams_path):
        with open(trivial_ngrams_path, 'rb') as f:
            trivial_ngrams = pickle.load(f)
    else:
        trivial_ngrams = compute_trivial_ngrams(dataset_path, trivial_ngrams_path, column, k, n)
    return trivial_ngrams

def compute_crystalBLEU_avgscore(references: List[List[str]], candidates: List[str], lang):
    trivial_ngrams = get_trivial_ngrams()
    crystalBLEU_score = corpus_bleu(
        references, candidates, ignoring=trivial_ngrams)
    return crystalBLEU_score