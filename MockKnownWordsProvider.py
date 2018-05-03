class MockKnownWordsProvider(object):
    def __init__(self):
        self.words = dict()
        self.N = 1

    def initialize(self, words):
        self.words = {unicode(word, 'utf-8'): freq for word, freq in words.items()}
        self.N = float(sum(words.values()))

    def known(self, words):
        return set(w for w in words if w in self.words)

    def P(self, word):
        p = self.words[word] / self.N if word in self.words else 0
        return p
