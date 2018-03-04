from preprocess import *
import pickle
import os

def lm_train(data_dir, language, fn_LM):
    """
	This function reads data from data_dir, computes unigram and bigram counts,
	and writes the result to fn_LM
	
	INPUTS:
	
    data_dir	: (string) The top-level directory continaing the data from which
					to train or decode. e.g., '/u/cs401/A2_SMT/data/Toy/'
	language	: (string) either 'e' (English) or 'f' (French)
	fn_LM		: (string) the location to save the language model once trained
    
    OUTPUT
	
	LM			: (dictionary) a specialized language model
	
	The file fn_LM must contain the data structured called "LM", which is a dictionary
	having two fields: 'uni' and 'bi', each of which holds sub-structures which 
	incorporate unigram or bigram counts
	
	e.g., LM['uni']['word'] = 5 		# The word 'word' appears 5 times
		  LM['bi']['word']['bird'] = 2 	# The bigram 'word bird' appears 2 times.
    """
    # Dictionaries for storing uni-gram and bi-gram language models
    uni_dict = {}
    bi_dict = {}

    for subdir, dirs, files in os.walk(data_dir):
        for file in files:
            fullFile = os.path.join(subdir, file)
            gram_dict(bi_dict, uni_dict, fullFile, language)

    # Language model dictionary with sub dictionaries
    language_model = {"uni": uni_dict, "bi": bi_dict}

    # Create Pickle File
    with open(fn_LM+'.pickle', 'wb') as handle:
        pickle.dump(language_model, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return language_model


def gram_dict(bigram, unigram, fname, language):
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
    if fname[-1] == language:
        # If correct extension then proceed
        open_file = open(fname)
        for line in open_file.readlines():
            prev_word = "START"
            for word in preprocess(line, language).split():
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
        open_file.close()
