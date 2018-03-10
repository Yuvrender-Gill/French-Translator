import math

def BLEU_score(candidate, references, n):
    """
	Compute the LOG probability of a sentence, given a language model and whether or not to
	apply add-delta smoothing
	
	INPUTS:
	sentence :	(string) Candidate sentence.  "SENTSTART i am hungry SENTEND"
	references:	(list) List containing reference sentences. ["SENTSTART je suis faim SENTEND", "SENTSTART nous sommes faime SENTEND"]
	n :			(int) one of 1,2,3. N-Gram level.

	
	OUTPUT:
	bleu_score :	(float) The BLEU score
	"""
    word_list = candidate.split()
    word_len = len(word_list)
    unigrams = 0
    bigrams = 0
    trigrams = 0
    unigram_dict = {}
    bigram_dict = {}
    trigram_dict = {}
    gram_dict(bigram_dict, unigram_dict, references)
    tri_dict(trigram_dict, references)
    dic = {"uni": unigram_dict, "bi": bigram_dict, "tri": trigram_dict}
    second = word_list[1]
    first = ""
    third = word_list[2]
    for word in word_list:
        if word in dic["uni"]:
            unigrams += 1

    for i in range(2, len(word_list)):
        first = second
        second = third
        third = word_list[i]
        if first in dic["bi"]:
            if second in dic["bi"][first]:
                bigrams += 1
        if first in dic["tri"]:
            if second in dic["tri"][first]:
                trigrams += 1

    unigram_precision = unigrams / float(word_len)
    bigram_precision = bigrams / (float(word_len) - 1)
    trigram_precision = trigrams / (float(word_len) - 2)
    penalty = penalty_counter(candidate, references)
    bleu_score = penalty *((unigram_precision * bigram_precision * trigram_precision) ** (1/n))
    return bleu_score

#================== HELPER FUNCTIONS =============================================================

def penalty_counter(candidate, references):
    """
    Returns the bleu penalty of a given candidate sentence given the list of reference sentences.
    :param candidate:
    :param references:
    :return:
    """
    sent_len = len(candidate.split())
    sig = 0
    smallest_delta  = float("inf")
    for i in range(len(references)):
        single_ref = len(references[i].split())
        if abs(single_ref - sent_len) < smallest_delta:
            sig = single_ref
            smallest_delta = abs(single_ref - sent_len)

    brevity = max(1, sig / sent_len)

    penalty = math.exp(1 - brevity)


    return penalty


def tri_dict(dict, references):
    """
    Returns a reference dictionary of tokens in the sentence in references. The dictionary has a count for the
    uni gram, bi gram and tri gram counts
    :param references:
    :return:
    """
    for line in references:
        word_list = line.split()
        first = ""
        second = word_list[1]
        third = word_list[2]
        for i in range(2, len(word_list)):
            if third in dict:
                if second in dict[third]:
                    if first in dict[third][second]:
                        dict[third][second][first] += 1
                    else:
                        dict[third][second][first] = 1
                else:
                    dict[third][second] = {}
                    dict[third][second][first] = 1
            else:
                dict[third] = {}
                dict[third][second] = {}
                dict[third][second][first] = 1
            first = second
            second = third
            third = word_list[i]
    return dict


def gram_dict(bigram, unigram,references):
    """
    Returns None. Given a file name fname, it opens the file and pre-processes all the sentences.
    Then it stores the count of the words in unigram dictionary and stores the bigram counts for
    pair of words in bigram structured dictionary. The language parameter can be set to 'e' or
    'f' for english and french language respectively, for the preprocess function.

    :param bigram: (Dict(str : Dict(str: int))) A dictionary with bigram pairs
    :param unigram: (Dict(str : int)) A dictionary with unigram pairs
    :param fname: (String) Name of the data file.
    :param language: (String) String 'e' or 'f' for language to be selected
    :return: None
    """

    # Check the file extension for correct language model
        # If correct extension then proceed

    for line in references:
        prev_word = ""
        for word in line.split():
            # Train uni-gram
            if word in unigram:
                unigram[word] += 1
            else:
                unigram[word] = 1
            # Train bi-gram
            if prev_word in bigram:
                if word in bigram[prev_word]:
                    bigram[prev_word][word] += 1
                else:
                    bigram[prev_word][word] = 1
            else:
                bigram[prev_word] = {}
                bigram[prev_word][word] = 1
            prev_word = word
