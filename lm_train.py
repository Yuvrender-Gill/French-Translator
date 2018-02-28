from preprocess import *
from multiprocessing import Pool, Process, Manager
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

    uni_dict = {}
    bi_dict = {}
    for subdir, dirs, files in os.walk(data_dir):
        for file in files:
            fullFile = os.path.join(subdir, file)
            unigram_dict(uni_dict, fullFile, language)
            bigram_dict(bi_dict, fullFile, language)

    language_model = {"uni": uni_dict, "bi": bi_dict}
    with open(fn_LM+'.pickle', 'wb') as handle:
        pickle.dump(language_model, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return language_model


def unigram_dict(dictionary, fname, language):

    if fname[-1] == language:
        file = open(fname, "r")
        for line in file.readlines():
            for word in preprocess(line, language).split():
                if (word in dictionary):
                    dictionary[word] += 1
                else:
                    dictionary[word] = 1
        file.close()


def bigram_dict(Bigram, fname, language):

    if fname[-1] == language:
        file = open(fname)
        for line in file.readlines():
            prev_word = "STARTSENT"
            for word in preprocess(line, language).split():
                if prev_word in Bigram:
                    if word in Bigram[prev_word]:
                        Bigram[prev_word][word] += 1
                    else:
                        Bigram[prev_word][word] = 1
                else:
                    Bigram[prev_word] = {}
                    Bigram[prev_word][word] = 1
                prev_word = word
        file.close()




if __name__ == "__main__":
    indir = "./data/Hansard/Training"
    lm_train(indir, "e", "english")