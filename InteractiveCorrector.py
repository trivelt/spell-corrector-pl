#!/usr/bin/python

from KnownWordsProvider import KnownWordsProviderUsingRAM, KnownWordsProviderUsingBigFile
from BigramsProvider import BigramsProvider
from SpellCorrector import SpellCorrector
import sys

if __name__ == '__main__':
    words_provider = KnownWordsProviderUsingRAM()
    words_provider.initialize('1grams_fixed')
    bigrams_provider = BigramsProvider()
    bigrams_provider.initialize("2gramy")
    corrector = SpellCorrector(words_provider, bigrams_provider)

    while True:
        text_to_correct = raw_input("> ")
        print(corrector.sentence_correction(text_to_correct))
        # words_to_correct = text_to_correct.split()
        # for word in words_to_correct:
        #     corrected_word = corrector.correction(word)
        #     sys.stdout.write(corrected_word + " ")
        # print("")
