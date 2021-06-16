import argparse
import pandas as pd

from style_trasnfer_accuracy import get_style_transfer_acc
from content_similarity import get_cosine_sim_corpus, calc_bleu, get_word_overlap_corpus
from language_quality import get_gpt2_ppl_corpus
from aggregation_metric import get_gm

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', "--inputs", help="path to test sentences", required=True)
    parser.add_argument('-p', "--preds", help="path to predictions of a model", required=True)
    
    args = parser.parse_args()
    
    with open(args.inputs, 'r') as input_file, open(args.preds, 'r') as preds_file:
        original_sentences = input_file.readlines()
        transferred_sentences = preds_file.readlines()
        
    file_name = args.preds.split('.')[0]
    df = pd.DataFrame({'comment': transferred_sentences, 'toxic': 0})
    df.to_csv(file_name+'.csv', index=False)
    
    results_file = open(file_name+'_results.txt', 'w')
    
    acc = get_style_transfer_acc(file_name+'.csv')
    results_file.write('Style transfer accuracy: ' + str(acc) + '\n')
    
    cs = get_cosine_sim_corpus(original_sentences, transferred_sentences)
    results_file.write('Cosine similarity: ' + str(cs) + '\n')
    
    wo = get_word_overlap_corpus(original_sentences, transferred_sentences)
    results_file.write('Word Overlap: ' + str(wo) + '\n')
    
    ppl = get_gpt2_ppl_corpus(transferred_sentences)
    results_file.write('Perplexity: ' + str(ppl) + '\n')
    
    gm = get_gm(acc, cs, ppl)
    results_file.write('Geometric mean: ' + str(gm) + '\n')
    
    bleu = calc_bleu(original_sentences, transferred_sentences)
    results_file.write('BLEU: ' + str(bleu) + '\n')
    
    results_file.close()