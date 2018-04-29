#!/usr/bin/python

from KnownWordsProvider import KnownWordsProviderUsingRAM, KnownWordsProviderUsingBigFile
from SpellCorrector import SpellCorrector
import sys

if __name__ == '__main__':
    words_provider = KnownWordsProviderUsingRAM()
    words_provider.initialize('1grams_fixed')
    corrector = SpellCorrector(words_provider)

    while True:
        text_to_correct = raw_input("> ")
        words_to_correct = text_to_correct.split()
        for word in words_to_correct:
            corrected_word = corrector.correction(word)
            sys.stdout.write(corrected_word + " ")
        print("")
