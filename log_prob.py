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

    if "uni" in LM and "bi" in LM:
        uni_dict = LM["uni"]
        bi_dict = LM["bi"]

    else:
        print("Invalid Language Model")
        return 0

    # Implement the sentence probability
    if not smoothing: # check for case when smoothing is false and other values are not 0
        delta = 0
        vocabSize = 0

    word_list = sentence.split()
    log_prob1 = 0

    for i in range(1, len(word_list)):
        # Check if the bi-gram is legal
        if word_list[i - 1] in bi_dict and word_list[i] in bi_dict[word_list[i - 1]]:
            numerator = float((bi_dict[word_list[i - 1]][word_list[i]] + delta))
        else:  # otherwise its count is 0
            numerator = float(delta)
        if word_list[i - 1] in uni_dict:  # Check if uni-gram is legal
            denominator = float(uni_dict[word_list[i - 1]] + (delta * vocabSize))
        else:  # otherwise its count is 0
            denominator = float(delta * vocabSize)
        # if numerator or denominator are zero the log probability is negative infinity
        if denominator == 0 or numerator == 0:
            log_prob1 += float("-inf")
        else:
            log_prob1 += log(numerator/denominator, 2)

    return log_prob1

if __name__ == "__main__":
    indir = "./data/Hansard/Training"
    LM = lm_train(indir, "e", "test")
    sent = preprocess("WORLD SPRINT SPEED SKATING CHAMPIONSHIPS ", "e")
    print(log_prob(sent, LM))
    print(log_prob(sent, LM, True, 0.2, len(LM["uni"])))
    print(log_prob(sent, LM, True, 0.4, len(LM["uni"])))
    print(log_prob(sent, LM, True, 0.6, len(LM["uni"])))
    print(log_prob(sent, LM, True, 0.8, len(LM["uni"])))
    print(log_prob(sent, LM, True, 1.0, len(LM["uni"])))

