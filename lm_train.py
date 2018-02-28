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



    unigram_dict = {}
    bigram_dict = {}

    language_model = {"uni": unigram_dict, "bi": bigram_dict}

#Save Model
    with open(fn_LM+'.pickle', 'wb') as handle:
        pickle.dump(language_model, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return language_model

def unigram_dict(dictionary, fname):
    print("Processing " + fname)
    file = open(fname, "r")

    for line in file.readlines():
        for word in preprocess(line, "e").split():
            if (word in dictionary):
                dictionary[word] += 1
            else:
                dictionary[word] = 1
    file.close()
    return dictionary

if __name__ == "__main__":
    indir = "./data/"
    with Manager() as manager:
        dict = manager.dict()
    for subdir, dirs, files in os.walk(indir):
        for file in files:

            fullFile = os.path.join(subdir, file)
            p = Process(target=unigram_dict, args=(dict, fullFile))
            print(dict)
            p.start()
            p.join()







