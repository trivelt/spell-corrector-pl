#!/usr/bin/python

from KnownWordsProvider import KnownWordsProviderUsingRAM, KnownWordsProviderUsingBigFile, KnownWordsProviderUsingMultipleFiles
from BigramsProvider import BigramsProvider
from SpellCorrector import SpellCorrector
import argparse

UNIGRAMS_FILEPATH = '../n-grams/1grams_fixed'
UNIGRAMS_FILES_DIR = '../n-grams/1grams_splitted/'
BIGRAMS_FILEPATH = "../n-grams/2grams_splitted"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bigrams", help="turn on using 2-grams to spell correction", action="store_true")
    parser.add_argument("-w", "--word", help="non-interactive mode, correct specified word(s)")
    parser.add_argument("-t", "--type", help="type of unigrams provider - RAM/BigFile/MultipleFiles\nRAM is used by default")
    args = parser.parse_args()

    unigrams_path = UNIGRAMS_FILEPATH
    if args.type == "BigFile":
        words_provider = KnownWordsProviderUsingBigFile()
    elif args.type == "MultipleFiles":
        unigrams_path = UNIGRAMS_FILES_DIR
        words_provider = KnownWordsProviderUsingMultipleFiles()
    else:
        words_provider = KnownWordsProviderUsingRAM()
    words_provider.initialize(unigrams_path)

    bigrams_provider = None
    if args.bigrams:
        bigrams_provider = BigramsProvider()
        bigrams_provider.initialize(BIGRAMS_FILEPATH)

    corrector = SpellCorrector(words_provider, bigrams_provider)

    if args.word:
        corrector.sentence_correction(args.word)
        print("")
        exit(0)

    while True:
        text_to_correct = raw_input("> ")
        corrector.sentence_correction(text_to_correct)
        print("")
