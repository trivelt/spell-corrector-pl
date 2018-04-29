#!/usr/bin/python
# -*- coding: utf-8 -*-


class UnigramsFixer(object):
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.line_counter = 0

    def fix_and_save(self, output_file_path):
        input_file = open(self.input_file_path, 'r')
        output_file = open(output_file_path, 'w')
        self.line_counter = 0
        removed = 0

        for line in input_file:
            self._print_line_number()
            if self._all_chars_are_letters(self._word(line)):
                output_file.write(line)
            else:
                removed += 1

        input_file.close()
        output_file.close()
        print("Removed lines: " + str(removed))

    def _all_chars_are_letters(self, word):
        letters = 'aąbcćdeęfghijklłmnńoópqrsśtuvwxyzżź'
        return all(char in letters for char in word)

    def _print_line_number(self):
        self.line_counter += 1
        if self.line_counter % 100000 == 0:
            print("Line: " + str(self.line_counter))

    def _word(self, line):
        return " ".join(line.split()[1:])


if __name__ == "__main__":
    fixer = UnigramsFixer('1grams')
    fixer.fix_and_save('1grams_fixed')
