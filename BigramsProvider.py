from NGramsUtils import *


class BigramsProvider(object):
    def __init__(self):
        self.bigrams = dict()
        self.bigrams_dir = ""

    def initialize(self, bigrams_directory):
        self.bigrams_dir = bigrams_directory

    def known(self, words, previous_word):
        known_words = list()
        # print("HERE!")
        first_letter = previous_word[0]
        if first_letter in 'abcdefghijklmnopqrstuvwxyz':
            file_name = self.bigrams_dir + "/2grams_" + first_letter
        else:
            file_name = self.bigrams_dir + "/2grams_other"

        f = open(file_name, 'r')
        for line in f:
            freq, bigram = line_to_bigram_pair(line)
            for w in words:
                if bigram[0] == previous_word and w == bigram[1]:
                    print("Append word=" + w + ", bigram[0]=" + bigram[0])
                    self.bigrams[previous_word + " " + w] = freq
                    known_words.append(w)
        f.close()
        return known_words

    def P(self, bigram):
        if bigram in self.bigrams:
            p = self.bigrams[bigram]
            return p
        else:
            return 0
