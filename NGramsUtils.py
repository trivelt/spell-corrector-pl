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
