from NGramsUtils import *


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
            return p
        else:
            return 0


class KnownWordsProviderUsingBigFile(object):
    def __init__(self):
        self.words = dict()
        self.N = 1.0
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
        f.close()

    def known(self, words):
        known_words = set()
        words_to_check = set(words)
        if not self.unigrams_file_path:
            return False
        f = open(self.unigrams_file_path, 'r')
        for line in f:
            freq, word = line_to_pair(line)
            if word in words_to_check:
                self.words[word] = freq
                known_words.add(word)
                words_to_check.remove(word)
                if len(words_to_check) == 0:
                    break
        f.close()
        return known_words

    def P(self, word):
        if word in self.words:
            p = self.words[word] / self.N
            return p
        else:
            return 0


class KnownWordsProviderUsingMultipleFiles(object):
    def __init__(self, load_to_ram=True):
        self.words = dict()
        self.N = 194095426.0
        self.unigrams_dir = None
        self.load_to_ram = load_to_ram

    def initialize(self, unigrams_dir):
        self.unigrams_dir = unigrams_dir

    def known(self, words):
        if self.load_to_ram:
            return self.known_with_ram(words)
        else:
            return self.known_basic(words)

    def known_with_ram(self, words):
        known_words = list()
        words_groups = split_words_by_first_letter(words)
        for group in words_groups:
            known_words_letter = dict()
            first_letter = group[0][0]
            if first_letter in 'abcdefghijklmnopqrstuvwxyz':
                file_name = self.unigrams_dir + "/1grams_" + first_letter
            else:
                file_name = self.unigrams_dir + "/1grams_other"

            f = open(file_name, 'r')
            for line in f:
                freq, known_word = line_to_pair(line)
                known_words_letter[known_word] = freq
            f.close()

            known_words_in_group = [w for w in group if w in known_words_letter]
            known_words.extend(known_words_in_group)

            for w in known_words_in_group:
                self.words[w] = known_words_letter[w]

        return set(known_words)

    def known_basic(self, words):
        known_words = list()
        words_groups = split_words_by_first_letter(words)
        for group in words_groups:
            first_letter = group[0][0]
            if first_letter in 'abcdefghijklmnopqrstuvwxyz':
                file_name = self.unigrams_dir + "/1grams_" + first_letter
            else:
                file_name = self.unigrams_dir + "/1grams_other"

            f = open(file_name, 'r')
            for line in f:
                freq, known_word = line_to_pair(line)
                if known_word in group:
                    known_words.append(known_word)
                    self.words[known_word] = freq
            f.close()
        return set(known_words)

    def P(self, word):
        if word in self.words:
            p = self.words[word] / self.N
            return p
        else:
            return 0
