from NGramsUtils import line_to_pair


class KnownWordsProviderUsingRAM(object):
    def __init__(self):
        self.words = dict()
        self.N = 1.0

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


class KnownWordsProviderUsingBigFile(object):
    def __init__(self, num_of_cached_words=10000):
        self.words = dict()
        self.N = 1.0
        self.num_of_cached_words = num_of_cached_words
        self.most_frequent = list()
        self.unigrams_file_path = None

    def initialize(self, unigrams_file_path):
        self.unigrams_file_path = unigrams_file_path
        self.words = dict()
        self.N = 0.0
        f = open(unigrams_file_path, 'r')
        line_count = 0
        for line in f:
            line_count += 1
            freq, word = line_to_pair(line)
            self.N += freq
            if line_count <= self.num_of_cached_words:
                self.words[word] = freq
        f.close()

    def known(self, words):
        known_words = list()
        for word in words:
            if word in self.words:
                known_words.append(word)
            elif self._exists_in_file(word):
                known_words.append(word)

        return set(known_words)

    def _exists_in_file(self, searched_word):
        if not self.unigrams_file_path:
            return False
        f = open(self.unigrams_file_path, 'r')
        for line in f:
            freq, word = line_to_pair(line)
            if word == searched_word:
                self.words[word] = freq
                return True
        f.close()

    def P(self, word):
        if word in self.words:
            p = self.words[word] / self.N
            return p
        else:
            return 0
