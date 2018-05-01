def line_to_pair(line):
    splitted_line = line.split()
    frequency = int(splitted_line[0])
    word = " ".join(splitted_line[1:])
    return frequency, word


def split_words_by_first_letter(words):
    splitted_words = dict()
    for word in words:
        first_letter = word[0]
        if first_letter in splitted_words:
            splitted_words[first_letter].append(word)
        else:
            splitted_words[first_letter] = [word]
    return splitted_words.values()
