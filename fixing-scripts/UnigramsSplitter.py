#!/usr/bin/python
# -*- coding: utf-8 -*-

import os


class UnigramsSplitter(object):
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.line_counter = 0
        self.letters = 'abcdefghijklmnopqrstuvwxyz'

    def split_to_dir(self, output_dir):
        f = open(self.input_file_path, 'r')
        if not os.path.exists(os.path.dirname(output_dir)):
            os.makedirs(output_dir)

        fds = dict()
        for letter in self.letters:
            fds[letter] = open(output_dir + os.sep + '1grams_' + letter, 'w')
        fds['other'] = open(output_dir + os.sep + '1grams_other', 'w')

        self.line_counter = 0
        for line in f:
            self._print_line_number()
            word = self._word(line)
            other = True
            for letter in self.letters:
                if word.startswith(letter):
                    fds[letter].write(line)
                    other = False
                    break

            if other:
                fds['other'].write(line)

        for elem in fds:
            fds[elem].close()

    def _print_line_number(self):
        self.line_counter += 1
        if self.line_counter % 100000 == 0:
            print("Line: " + str(self.line_counter))

    def _word(self, line):
        return " ".join(line.split()[1:])


if __name__ == "__main__":
    fixer = UnigramsSplitter('1grams_fixed')
    fixer.split_to_dir('1grams_splitted')
