#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from MockKnownWordsProvider import MockKnownWordsProvider
from MockBigramsProvider import MockBigramsProvider
from SpellCorrector import SpellCorrector
import NGramsUtils


class SpellCorrectorEditsTest(unittest.TestCase):
    def setUp(self):
        self.words_provider = MockKnownWordsProvider()
        self.sut = SpellCorrector(self.words_provider)

    def assert_contains_list(self, container, member_list, print_container=True):
        container_members_str = '[' + ", ".join([elem.encode('utf-8') for elem in container]) + ']' if print_container else "container"
        for member in member_list:
            if not isinstance(member, unicode):
                member = unicode(member, 'utf-8')
            self.assertIn(member, container, member.encode('utf-8') + " not in " + container_members_str)

    def test_edit1(self):
        word = "hello"
        result = self.sut._edits1(word)

        deletes = ('ello', 'hllo', 'helo', 'hell')
        transposes = ('ehllo', 'hlelo', 'hello', 'helol')
        replaces = ('jello', 'hallo', 'helko', 'healo', 'hęllo')
        inserts = ('heello', 'hhello', 'helllo', 'hellou', 'helloż')

        self.assert_contains_list(result, deletes)
        self.assert_contains_list(result, transposes)
        self.assert_contains_list(result, replaces)
        self.assert_contains_list(result, inserts)

    def test_edit2(self):
        word = "hello"
        result = self.sut._edits2(word)

        example_edits = ('hekko', 'tallo', 'hhhllo', 'belko')
        self.assert_contains_list(result, example_edits, print_container=True)

        result = self.sut._edits2("komputeruf")
        example_edits = ('komputerów', 'omputeruf')
        self.assert_contains_list(result, example_edits, print_container=False)

    def test_diacritics_words(self):
        word = 'czesc'
        result = self.sut._add_diacritics(word)

        edit1_corrections = ('ćzesc',
                             'cżesc',  # 'cźesc',
                             'częsc',
                             'cześc',
                             'czesć')
        edit2_corrections = ('ćzesć', 'cześć', 'częśc')
        self.assert_contains_list(result, edit1_corrections)
        self.assert_contains_list(result, edit2_corrections)
        self.assertFalse(word in result)


class SpellCorrectorTestBase(unittest.TestCase):
    def assert_equal_utf(self, first, second):
        first = unicode(first, 'utf-8')
        self.assertEqual(first, second, first.encode('utf-8') + " != " + second.encode('utf-8'))


class SpellCorrectorCorrectionTest(SpellCorrectorTestBase):
    def setUp(self):
        self.words_provider = MockKnownWordsProvider()
        self.sut = SpellCorrector(self.words_provider)

    def test_should_correct_diacritics_at_first(self):
        self.words_provider.initialize({"że": 21,
                                        "za": 30})

        corrected = self.sut.correction("ze")
        self.assert_equal_utf("że", corrected)

    def test_should_choose_most_frequent_word(self):
        self.words_provider.initialize({"tata": 130,
                                        "taca": 44,
                                        "tara": 29})

        corrected = self.sut.correction("taya")
        self.assert_equal_utf("tata", corrected)

    def test_should_choose_edit2_if_no_edit1_available(self):
        self.words_provider.initialize({"lampka": 101,
                                        "choinka": 50})

        corrected = self.sut.correction("honika")
        self.assert_equal_utf("choinka", corrected)


    def test_should_choose_edit1_if_exist(self):
        self.words_provider.initialize({"lampka": 101,
                                        "choinka": 50,
                                        'konika': 5})

        corrected = self.sut.correction("honika")
        self.assert_equal_utf("konika", corrected)


class SpellCorrectorSentenceCorrectionBigramsTest(SpellCorrectorTestBase):
    def setUp(self):
        self.words_provider = MockKnownWordsProvider()
        self.bigrams_provider = MockBigramsProvider()
        self.sut = SpellCorrector(self.words_provider, self.bigrams_provider)

    def test_should_choose_word_existing_in_bigrams(self):
        self.words_provider.initialize({"panie": 50,
                                        "pranie": 19})
        self.bigrams_provider.initialize({"suszyć pranie": 15,
                                          "suszyć ubranie": 10})
        corrected = self.sut.sentence_correction("suszyć ptanie", print_words=False)
        self.assert_equal_utf("suszyć pranie", corrected)

    def test_should_choose_most_frequent_bigram(self):
        self.words_provider.initialize({"komputer": 99,
                                        "komputerów": 30,
                                        "programowanie": 20})
        self.bigrams_provider.initialize({"programowanie komputer": 1,
                                          "programowanie komputerów": 3})
        corrected = self.sut.sentence_correction("pogramowanie komputeruf", print_words=False)
        self.assert_equal_utf("programowanie komputerów", corrected)


class NGramsUtilsTest(unittest.TestCase):
    def test_should_return_correct_freq(self):
        line = "123456 test"
        freq, _ = NGramsUtils.line_to_pair(line)
        self.assertEqual(123456, freq)

    def test_should_return_correct_word(self):
        line = "123456 test"
        _, word = NGramsUtils.line_to_pair(line)
        self.assertEqual("test", word)

    def test_should_split_words_list_by_first_letter(self):
        words = ['cześć', 'czapka', 'cały', 'test', 'taras']
        splitted_list = NGramsUtils.split_words_by_first_letter(words)
        self.assertEqual(2, len(splitted_list))
        self.assertTrue(['cześć', 'czapka', 'cały'] in splitted_list)
        self.assertTrue(['test', 'taras'] in splitted_list)

    def test_should_return_empty_list_for_no_words(self):
        result = NGramsUtils.split_words_by_first_letter([])
        self.assertEqual(0, len(result))

    def test_should_return_filename_for_one_letter_word(self):
        filename = NGramsUtils.get_filename_for_word("a")
        self.assertEqual("a", filename)

        filename = NGramsUtils.get_filename_for_word(".")
        self.assertEqual("other", filename)

    def test_should_return_filename_for_two_letters_word(self):
        filename = NGramsUtils.get_filename_for_word(",a")
        self.assertEqual("other", filename)

        filename = NGramsUtils.get_filename_for_word("o!")
        self.assertEqual("o", filename)

        filename = NGramsUtils.get_filename_for_word("te")
        self.assertEqual("te", filename)

    def test_should_return_filename_for_minimum_three_letters_word(self):
        filename = NGramsUtils.get_filename_for_word("...ba")
        self.assertEqual("other", filename)

        filename = NGramsUtils.get_filename_for_word("a!!!!")
        self.assertEqual("a", filename)

        filename = NGramsUtils.get_filename_for_word("ma,")
        self.assertEqual("ma", filename)

        filename = NGramsUtils.get_filename_for_word("masło")
        self.assertEqual("mas", filename)


if __name__ == '__main__':
    unittest.main()
