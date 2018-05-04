from NGramsUtils import *
import os


class BigramsProvider(object):
    def __init__(self):
        self.bigrams = dict()
        self.bigrams_dir = ""

    def initialize(self, bigrams_directory):
        self.bigrams_dir = bigrams_directory

    def known(self, words, previous_word):
        known_words = list()
        filename_ending = get_filename_for_word(previous_word)
        if len(filename_ending) == 3:
            filename_ending = filename_ending[:2]
        file_name = os.path.join(self.bigrams_dir, "2grams_" + filename_ending)

        f = open(file_name, 'r')
        for line in f:
            freq, bigram = line_to_bigram_pair(line)
            for w in words:
                if bigram[0] == previous_word and w == bigram[1]:
                    raw_bigram = previous_word + " " + w
                    self._append_bigram(raw_bigram, freq)
                    known_words.append(w)
        f.close()
        return known_words

    def _append_bigram(self, bigram, freq):
        if bigram in self.bigrams and self.bigrams[bigram] > freq:
            return
        self.bigrams[bigram] = freq

    def P(self, bigram):
        if bigram in self.bigrams:
            p = self.bigrams[bigram]
            return p
        else:
            return 0
