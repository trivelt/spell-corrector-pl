#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Maciej Michalec
# Spelling corrector based on Peter Norvig's code
# (https://norvig.com/spell-correct.html)


class SpellCorrector(object):
    def __init__(self, words_provider, bigrams_provider=None):
        self.wp = words_provider
        self.bp = bigrams_provider

    def _candidates(self, word):
        diacritics_words = self.wp.known(self._add_diacritics(word))
        known_word = self.wp.known([word])

        if diacritics_words:
            return known_word.union(diacritics_words)
        else:
            return known_word or self.wp.known(self._edits1(word)) or self.wp.known(self._edits2(word)) or [word]

    def sentence_correction(self, sentence):
        words_to_correct = sentence.split()
        corrected_sentence = ""
        corrected_word = None
        for word in words_to_correct:
            corrected_word = self.correction(word, corrected_word)
            corrected_sentence += corrected_word + " "
        return corrected_sentence.rstrip()

    def correction(self, word, previous_word=None):
        if not isinstance(word, unicode):
            word = unicode(word, 'utf-8')

        candidates = self._candidates(word)
        sorted_candidates = list(sorted(candidates, key=self.wp.P, reverse=True))  # TODO: WHY REVERSE?

        if self.bp and previous_word:
            return self._correct_using_bigrams(sorted_candidates, previous_word)
        else:
            return sorted_candidates[0]

    def _correct_using_bigrams(self, sorted_candidates, previous_word):
        known_bigrams = self.bp.known(sorted_candidates, previous_word)
        if len(known_bigrams) > 0:
            sorted_bigrams = sorted(known_bigrams, key=lambda w: self.bp.P(" ".join([previous_word, w])), reverse=True)
            # print("Sorted bigrams: " + str(sorted_bigrams))
            return sorted_bigrams[0] # TODO if not P[0] > P[1], check length of words
        else:
            return sorted_candidates[0]

    def _add_diacritics(self, word):
        pl_edits1 = self._edit1_diacritics(word)
        pl_edits2 = list(e2 for e1 in pl_edits1 for e2 in self._edit1_diacritics(e1))
        return pl_edits1.union(pl_edits2)

    def _edit1_diacritics(self, word):
        pairs = {
            u'a': u'ą',
            u'c': u'ć',
            u'e': u'ę',
            u'l': u'ł',
            u'n': u'ń',
            u'o': u'ó',
            u's': u'ś',
            u'z': u'ż'#, 'ź']
        }

        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        e1 = list()
        for orig_letter, new_letter in pairs.items():
            for L, R in splits:
                if R and R[0] == orig_letter:
                    e1.append(L + new_letter + R[1:])
        return set(e1)

    def _edits1(self, word):
        letters    = u'aąbcćdeęfghijklłmnńoópqrsśtuvwxyzżź'
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        inserts    = [L + c + R               for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def _edits2(self, word):
        return list(e2 for e1 in self._edits1(word) for e2 in self._edits1(e1))
