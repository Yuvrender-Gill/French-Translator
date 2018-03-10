from preprocess import *
import preplexity
from decode import *
from log_prob import *
from BLEU_score import *
from lm_train import *
from align_ibm1 import *


def evalAlign():
    """

    :return: NONe

    """
    max_iteration = 10
    report = open('Temp', 'w')
    train_dir = '/u/cs401/A2_SMT/data/Hansard/Training'
    LM = lm_train(train_dir, "e", "englishLM")
    vocab_size = len(LM["uni"])
    report.write("Vocab size = " + str(vocab_size) +"\n")
    report.write("\n")
    corpus_size = [1000, 10000, 15000, 30000]
    n = [1, 2, 3]
    ref_file1 = open('/u/cs401/A2_SMT/data/Hansard/Testing/Task5.e', 'r')
    ref_file2 = open('/u/cs401/A2_SMT/data/Hansard/Testing/Task5.google.e', 'r')
    test_file = open('/u/cs401/A2_SMT/data/Hansard/Testing/Task5.f', 'r')
    ref_file1_ref = ref_file1.readlines()
    ref_file2_ref = ref_file2.readlines()
    test_lines = test_file.readlines()
    #train IBM
    for i in corpus_size:
        f = "".join(['am_hansard_', str(i)])
        AM = align_ibm1(train_dir, i, max_iteration, f);
        report.write("Model with " + str(i) + " sentences. \n")
        for line in test_lines:
            report.write("The sentence is: " + line + '\n')
            line = preprocess(line, "f")
            trans = decode(line, LM, AM)
            report.write('\n')
            bl1 = BLEU_score(trans, ref_file1_ref, 1)
            bl2 = BLEU_score(trans, ref_file1_ref, 2)
            bl3 = BLEU_score(trans, ref_file1_ref, 3)

            bl_google_1 = BLEU_score(trans, ref_file2_ref, 1)
            bl_google_2 = BLEU_score(trans, ref_file2_ref, 2)
            bl_google_3 = BLEU_score(trans, ref_file2_ref, 3)

            report.write("BLEU SCORE: \n")
            report.write("GOOGLE || SELF || i \n")
            report.write(str(bl_google_1)+" || " +str(bl1)+"|| 1 \n")
            report.write(str(bl_google_2)+" || "+str(bl2)+" || 2 \n")
            report.write(str(bl_google_3)+" || "+str(bl3)+" || 3 \n")

            report.write("====================================================================================\n")
            report.write("\n")
if __name__ == "__main__":
    evalAlign()
