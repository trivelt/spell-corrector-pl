from NGramsUtils import line_to_pair


class KnownWordsProviderUsingRAM(object):
    def __init__(self):
        self.words = dict()
        self.N = 1

    def initialize(self, unigrams_file_path):
        self.words = dict()
        self.N = 0.0
        f = open(unigrams_file_path, 'r')
        for line in f:
            freq, word = line_to_pair(line)
            self.words[word] = freq
            self.N += freq
        f.close()

    def known(self, words):
        return set(w for w in words if w in self.words)

    def P(self, word):
        if word in self.words:
            p = self.words[word] / self.N
            # print("P(" + word + ")=" + str(p) + ", freq=" + str(self.words[word]))
            return p
        else:
            return 0
