class MockBigramsProvider(object):
    def __init__(self):
        self.bigrams = dict()
        self.N = 1

    def initialize(self, bigrams):
        self.bigrams = {unicode(word, 'utf-8'): freq for word, freq in bigrams.items()}
        self.N = float(sum(bigrams.values()))

    def known(self, words, previous_word):
        known_bigrams = list()
        for word in words:
            bigram = previous_word + " " + word
            if bigram in self.bigrams:
                known_bigrams.append(word)
        return known_bigrams

    def P(self, bigram):
        p = self.bigrams[bigram] / self.N if bigram in self.bigrams else 0
        return p
