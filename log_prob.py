from preprocess import *
from lm_train import *
from math import log

def log_prob(sentence, LM, smoothing=False, delta=0, vocabSize=0):
    """
    Compute the LOG probability of a sentence, given a language model and whether or not to
    apply add-delta smoothing

    INPUTS:
    sentence :	(string) The PROCESSED sentence whose probability we wish to compute
    LM :		(dictionary) The LM structure (not the filename)
    smoothing : (boolean) True for add-delta smoothing, False for no smoothing
    delta : 	(float) smoothing parameter where 0<delta<=1
    vocabSize :	(int) the number of words in the vocabulary

    OUTPUT:
    log_prob :	(float) log probability of sentence
    """
    if not smoothing:
        process = preprocess(sentence, "e")
        if "uni" in LM and "bi" in LM:
            uni_dict = LM["uni"]
            bi_dict = LM["bi"]
        else:
            print("Invalid Language Model")
            return 0

        # Implement the sentence probablity

    return 1


if __name__ == "__main__":
    indir = "./data/Hansard/Training"
    dict = lm_train(indir, "f", "french")
    new = log_prob("hello", d)

    print(new)