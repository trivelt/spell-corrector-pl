#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from MockKnownWordsProvider import MockKnownWordsProvider
from SpellCorrector import SpellCorrector
import NGramsUtils


class SpellCorrectorEditsTest(unittest.TestCase):
    def setUp(self):
        self.words_provider = MockKnownWordsProvider()
        self.sut = SpellCorrector(self.words_provider)

    def assert_contains_list(self, container, member_list, print_container=True):
        container_members_str = '[' + ", ".join([str(elem) for elem in container]) + ']' if print_container else "container"
        for member in member_list:
            self.assertIn(member, container, str(member) + " not in " + container_members_str)

    def test_edit1(self):
        word = "hello"
        result = self.sut._edits1(word)

        deletes = ('ello', 'hllo', 'helo', 'hell')
        transposes = ('ehllo', 'hlelo', 'hello', 'helol')
        replaces = ('jello', 'hallo', 'helko', 'healo')
        inserts = ('heello', 'hhello', 'helllo', 'hellou')

        self.assert_contains_list(result, deletes)
        self.assert_contains_list(result, transposes)
        self.assert_contains_list(result, replaces)
        self.assert_contains_list(result, inserts)

    def test_edit2(self):
        word = "hello"
        result = self.sut._edits2(word)

        example_edits = ('hekko', 'tallo', 'hhhllo', 'belko')
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


class SpellCorrectorCorrectionTest(unittest.TestCase):
    def setUp(self):
        self.words_provider = MockKnownWordsProvider()
        self.sut = SpellCorrector(self.words_provider)

    def assert_equal_utf(self, first, second):
        self.assertEqual(first, second, str(first) + " != " + str(second))

    def test_should_correct_diacritics_at_first(self):
        self.words_provider.initialize({"że": 21,
                                        "za": 30})

        corrected = self.sut.correction("ze")
        self.assert_equal_utf("że", corrected)

    def test_should_choose_most_frequenc_word(self):
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


class NGramsUtilsTest(unittest.TestCase):
    def test_should_return_correct_freq(self):
        line = "123456 test"
        freq, _ = NGramsUtils.line_to_pair(line)
        self.assertEqual(123456, freq)

    def test_should_return_correct_word(self):
        line = "123456 test"
        _, word = NGramsUtils.line_to_pair(line)
        self.assertEqual("test", word)


if __name__ == '__main__':
    unittest.main()
