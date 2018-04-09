#!/usr/bin/python3
import sys

wordfreq={}

# Returns a dictionary whose keys are the words from the given list of words
# and values are the corresponding frequencies.
def word_frequencies_create(filename):
    try:
       file = open(filename, 'r')
    except:
       print('Cannot open', filename)
    else:
       for line in open(filename):
            line = line.lower()
            for word in line.split():
                if word not in wordfreq:
                    wordfreq[word] = 1
                else:
                    wordfreq[word] += 1

    return wordfreq

# st to standard output, one per line, and with a ' -> ' between a key and
# the corresponding value.
def word_frequencies_print(st):
    for i in st:
        print(i, " -> ", wordfreq[i])

word_freq = word_frequencies_create('xxxx')
word_freq = word_frequencies_create('gettysburg.txt')
word_frequencies_print(word_freq)
