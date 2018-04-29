#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Maciej Michalec
# Spelling corrector based on Peter Norvig's code
# (https://norvig.com/spell-correct.html)


class SpellCorrector(object):
    def __init__(self, words_provider):
        self.wp = words_provider

    def _candidates(self, word):
        diacritics_words = self.wp.known(self._add_diacritics(word))
        known_word = self.wp.known([word])

        if diacritics_words:
            return known_word.union(diacritics_words)
        else:
            return known_word or self.wp.known(self._edits1(word)) or self.wp.known(self._edits2(word)) or [word]

    def correction(self, word):
        cands = self._candidates(word)
        sort_cands = list(sorted(cands, key=self.wp.P, reverse=True))  # TODO: WHY REVERSE?
        return sort_cands[0]

    def _add_diacritics(self, word):
        pl_edits1 = self._edit1_diacritics(word)
        pl_edits2 = (e2 for e1 in pl_edits1 for e2 in self._edit1_diacritics(e1))
        return pl_edits1.union(pl_edits2)

    def _edit1_diacritics(self, word):
        pairs = {
            'a': 'ą',
            'c': 'ć',
            'e': 'ę',
            'l': 'ł',
            'n': 'ń',
            'o': 'ó',
            's': 'ś',
            'z': 'ż'#, 'ź']
        }

        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        e1 = list()
        for orig_letter, new_letter in pairs.items():
            for L, R in splits:
                if R and R[0] == orig_letter:
                    e1.append(L + new_letter + R[1:])
        return set(e1)

    def _edits1(self, word):
        letters    = 'abcdefghijklmnopqrstuvwxyz'
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        inserts    = [L + c + R               for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def _edits2(self, word):
        return (e2 for e1 in self._edits1(word) for e2 in self._edits1(e1))
