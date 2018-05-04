# -*- coding: utf-8 -*-

# alphabet = 'abcdefghijklmnopqrstuvwxyz'
alphabet = u"aąbcćdeęfghijklłmnńoópqrsśtuvwxyzżź"


def line_to_pair(line):
    splitted_line = line.split()
    frequency = int(splitted_line[0])
    word = " ".join(splitted_line[1:])
    return frequency, unicode(word, 'utf-8')


def line_to_bigram_pair(line):
    line = unicode(line, 'utf-8')
    line = line.replace(',', '')
    line = line.replace('.', '')
    line = line.replace('!', '')
    splitted_line = line.split()
    # print("Splitted line=" + str(splitted_line))
    if len(splitted_line) < 2:
        return 0, ('', '')
    frequency = int(splitted_line[0])
    first_word = splitted_line[1]
    if len(splitted_line) == 2:
        return frequency, (first_word, "")
    second_word = splitted_line[2]
    return frequency, (first_word, second_word)


def split_words_by_first_letter(words):
    splitted_words = dict()
    for word in words:
        first_letter = word[0]
        if first_letter in splitted_words:
            splitted_words[first_letter].append(word)
        else:
            splitted_words[first_letter] = [word]
    return splitted_words.values()


def get_filename_for_word(word):
    if not isinstance(word, unicode):
        word = unicode(word, 'utf-8')
    if len(word) == 1:
        return _get_filename_for_one_letter_word(word)
    elif len(word) == 2:
        return _get_filename_for_two_letters_word(word)
    else:
        return _get_filename_for_minimum_three_letters_word(word)


def _get_filename_for_one_letter_word(word):
    first_letter = word[0]
    if first_letter in alphabet:
        return first_letter
    else:
        return "other"


def _get_filename_for_two_letters_word(word):
    one_letter_filename = _get_filename_for_one_letter_word(word)
    if one_letter_filename != "other":
        second_letter = word[1]
        if second_letter in alphabet:
            return one_letter_filename + second_letter
    return one_letter_filename


def _get_filename_for_minimum_three_letters_word(word):
    two_letters_filename = _get_filename_for_two_letters_word(word)
    if len(two_letters_filename) == 2:
        third_letter = word[2]
        if third_letter in alphabet:
            return two_letters_filename + third_letter
    return two_letters_filename
