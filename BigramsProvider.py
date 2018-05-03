from NGramsUtils import *


class BigramsProvider(object):
    def __init__(self):
        self.bigrams = dict()
        self.bigrams_dir = ""

    def initialize(self, bigrams_directory):
        self.bigrams_dir = bigrams_directory

    def known(self, words, previous_word):
        known_words = list()
        print("HERE!")
        words_groups = split_words_by_first_letter(words)
        for group in words_groups:
            first_letter = group[0][0]
            if first_letter in 'abcdefghijklmnopqrstuvwxyz':
                file_name = self.bigrams_dir + "/2grams_" + first_letter
            else:
                file_name = self.bigrams_dir + "/2grams_other"

            f = open(file_name, 'r')
            for line in f:
                freq, bigram = line_to_bigram_pair(line)
                for w in group:
                    if w == bigram[1]:
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
