import re


""" Global Variables """
abbrivaition_file_path1 = "/h/u1/cs401/Wordlists/abbrev.english"
abbrivaition_file_path2 = "/h/u1/cs401/Wordlists/abbrev.english~"
abbrivaition_file_path3 = "/h/u1/cs401/Wordlists/pn_abbrev.english"
abbrivaition_file_path4 = "/h/u1/cs401/Wordlists/pn_abbrev.english2"
abbrivaition_file1 = open(abbrivaition_file_path1, 'r')
abbrivaition_file2 = open(abbrivaition_file_path2, 'r')
abbrivaition_file3 = open(abbrivaition_file_path3, 'r')
abbrivaition_file4 = open(abbrivaition_file_path4, 'r')
abbrivaition_list = set(abbrivaition_file1.readlines()).union(
    set(abbrivaition_file2.readlines()).union(set(abbrivaition_file3.readlines()).union(
set(abbrivaition_file4.readlines())
    )))
abbrivaition_file1.close()
abbrivaition_file2.close()
abbrivaition_file3.close()
abbrivaition_file4.close()


def preprocess(in_sentence, language):
    """ 
    This function pre-processes the input text according to language-specific rules.
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
            out_sentence = english_clitics(out_sentence.lower())

        else:
            out_sentence = french_clitics(out_sentence.lower())

    return 'SENTSTART ' + out_sentence.strip() + ' SENTEND'

# =================== Helper Functions =========================

def punctuation_processor(in_sentence):
    """
    Returns a string with all its punctuation tokenized.
    @param String in_sentence: a String to tokenize punctuation from
    @rtype: String
    """ 
    abbr_list = abbrivaition_list
        # ['Capt', 'Col.', 'Dr.', 'Drs.', 'Fig.', 'Figs.', 'Gen.',
        #          'Mr.', 'Mrs.', 'Ref.', 'Rep.', 'Reps.', 'Sen.', 'fig.',
        #          'figs.', 'vs.', 'Lt.', 'e.g.', 'i.e.']

    lst_str = in_sentence.split()
    out_sentence = ""
    for item in lst_str:
        if not ((item + '\n' in abbr_list) or (item in abbr_list)):
            out_sentence += ' '.join(
                [re.sub(r"(([" + '!"#$%&\()*+,-./:;<=>?@[\\]^_`{|}~' + "])\\2*)", r" \1 ", item)]) + ' '
        else:
            out_sentence += item + ' '
    return out_sentence


def english_clitics(in_sentence):
    """
    Returns a string with clitics split from the comment.
    @param String in_sentence: a String to split clitics from
    @rtype: String
    """
    out_sentence = ' '.join([re.sub(r"((["+ "'" + "]))", r" \1", in_sentence)])
    out_sentence = ' '.join(out_sentence.split('  '))
    out_sentence = re.sub(r"(') ([A-Za-z] )", r"\1\2", out_sentence).strip()
    return out_sentence


def french_clitics(in_sentence):
    """
    Returns a string with clitics split from the comment.
    @param String in_sentence: a String to split clitics from
    @rtype: String
    """
    # 1 Separating singular definite article (le, la) -- separate l' from the words
    out_sentence = ' '.join([re.sub(r"l'([A-Za-z])", r"l' \1", in_sentence)])
    # remove the large L's as well
    out_sentence = ' '.join([re.sub(r"L'([A-Za-z])", r"L' \1", out_sentence)])
    # 2 Single constant words ending in 'e-muet'
    out_sentence = ' '.join([re.sub(r"([A-Za-z])'", r"\1' ", out_sentence)])
    # 3 Separate qu'
    out_sentence = ' '.join([re.sub(r"qu'([A-Za-z])", r"qu' \1", out_sentence)])
    # 4 Separate 'on and 'il
    out_sentence = ' '.join([re.sub(r"([A-Za-z ])qu' on", r"\1qu' on", out_sentence)])
    out_sentence = ' '.join([re.sub(r"([A-Za-z ])qu' il", r"\1qu' il", out_sentence)])
    # 5 Concatinate the words d'abord d'accord, d'ailleurs and d'habitude
    out_sentence = ' '.join([re.sub(r"d' (abord|accord|ailleurs|habitude)", r"d'\1", out_sentence)])

    out_sentence = ' '.join(out_sentence.split('  '))
    out_sentence = re.sub(r"(') ([A-Za-z] )", r"\1\2", out_sentence).strip()

    return out_sentence
