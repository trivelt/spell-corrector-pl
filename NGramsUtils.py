def line_to_pair(line):
    splitted_line = line.split()
    frequency = int(splitted_line[0])
    word = " ".join(splitted_line[1:])
    return frequency, word
