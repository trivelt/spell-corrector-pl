#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
sys.path.insert(0, os.path.abspath(".."))
from NGramsUtils import get_filename_for_word

class BigramsSplitter(object):
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.line_counter = 0
        self.letters = u"aąbcćdeęfghijklłmnńoópqrsśtuvwxyzżź"

    def split_to_dir(self, output_dir):
        if not os.path.exists(os.path.dirname(output_dir)):
            os.makedirs(output_dir)

        self._split_to_one_letter_files(output_dir)
        self._split_to_two_letters_files(output_dir)


    def _split_to_one_letter_files(self, output_dir):
        fds = dict()
        for letter in self.letters:
            fds[letter] = open(os.path.join(output_dir, "2grams_" + letter + "_temp"), 'w')
        fds['other'] = open(os.path.join(output_dir, '2grams_other'), 'w')

        self.line_counter = 0
        f_in = open(self.input_file_path, 'r')
        self.line_counter = 0
        print("================== Split main file ==================")
        for line in f_in:
            self._print_line_number()
            word = self._word(line)
            filename_ending = get_filename_for_word(word)
            if len(filename_ending) == 2 or len(filename_ending) == 3:
                filename_ending = filename_ending[0]
            fds[filename_ending].write(line)
        f_in.close()

        for elem in fds:
            fds[elem].close()

    def _split_to_two_letters_files(self, output_dir):
        for letter in self.letters:
            print("================== Split 2grams_" + letter + "_temp ==================")
            f_in = open(os.path.join(output_dir, "2grams_" + letter + "_temp"), 'r')
            fds = dict()
            fds[letter] = open(os.path.join(output_dir, "2grams_" + letter), 'w')
            for second_letter in self.letters:
                fds[letter + second_letter] = open(os.path.join(output_dir, "2grams_" + letter + second_letter), 'w')

            self.line_counter = 0
            for line in f_in:
                self._print_line_number()
                word = self._word(line)
                filename_ending = get_filename_for_word(word)
                if len(filename_ending) == 2 or len(filename_ending) == 3:
                    filename_ending = filename_ending[:2]
                fds[filename_ending].write(line)
            f_in.close()

    def _print_line_number(self):
        self.line_counter += 1
        if self.line_counter % 100000 == 0:
            print("Line: " + str(self.line_counter))

    def _word(self, line):
        return unicode(line.split()[1], 'utf-8')


if __name__ == "__main__":
    fixer = BigramsSplitter('2grams')
    fixer.split_to_dir('2grams_splitted')
