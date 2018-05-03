class MockBigramsProvider(object):
    def __init__(self):
        self.bigrams = dict()
        self.N = 1

    def initialize(self, bigrams):
        self.bigrams = {unicode(word, 'utf-8'): freq for word, freq in bigrams.items()}
        self.N = float(sum(bigrams.values()))

    def known(self, word, previous_word):
        bigram = previous_word + " " + word
        return bigram in self.bigrams

    def P(self, word, previous_word):
        bigram = previous_word + " " + word
        p = self.bigrams[bigram] / self.N if bigram in self.bigrams else 0
        return p
