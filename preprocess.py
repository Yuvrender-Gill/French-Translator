import re


""" Global Variables """
# abbrivaition_file_path = "/h/u1/cs401/Wordlists/abbrev.english"
# abbrivaition_file = open(abbrivaition_file_path, 'r')
# abber_list = abbrivaition_file.readlines()
# abbrivaition_file.close()
def preprocess(in_sentence, language):
    """ 
    This function preprocesses the input text according to language-specific rules.
    Specifically, we separate contractions according to the source language, convert
    all tokens to lower-case, and separate end-of-sentence punctuation 
	
	INPUTS:
	in_sentence : (string) the original sentence to be processed
	language	: (string) either 'e' (English) or 'f' (French)
				   Language of in_sentence
	OUTPUT:
	out_sentence: (string) the modified sentence
    """
    # Remove the newline character if present in the in sentence

    out_sentence = punctuation_processor(in_sentence).replace("\n", "")
    if language == 'e' or language == 'f':
        if language == 'e':
            return out_sentence
        else:
            return out_sentence
    return out_sentence


def punctuation_processor(in_sentence):
    '''
    Returns a string with all its punctuation tokenized.
    @param String comment: a String to tokenize punctuation from
    @rtype: String
    '''
    abbr_list = ['Capt', 'Col.', 'Dr.', 'Drs.', 'Fig.', 'Figs.', 'Gen.',
                 'Mr.', 'Mrs.', 'Ref.', 'Rep.', 'Reps.', 'Sen.', 'fig.',
                 'figs.', 'vs.', 'Lt.', 'e.g.', 'i.e.']

    lst_str = in_sentence.split()
    out_sentence = ""
    for item in lst_str:
        if (not (item in abbr_list)):
            out_sentence += re.sub(r"(([" + '!"#$%&\()*+,-./:;<=>?@[\\]^_`{|}~' + "])\\2*)", r" \1  ", item) + ' '
        else:
            out_sentence += item + ' '
    out_sentence = ' '.join(out_sentence.split('   '))

    out_sentence = re.sub(r"(') ([A-Za-z] )", r"\1\2", out_sentence).strip()
    return out_sentence


#=================== Helper Functions =========================

if __name__ == "__main__":

    sentence = "Mr. Speaker, this prime minister seems to be spending 2x much on photo ops, vacations, and personal image than any prime minister ever has.\n"
    new = preprocess(sentence, "e")
    print(new)