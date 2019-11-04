#####################################################
# Author: Samuel Le
# Date: November 3, 2019
# Course: Statistical Natural Language Processing
# Purpose: Build a language model based off of Shakespeare
#############################################################
import collections
import json
import math
import random
import string
import sys


# Given an input word, it will return a random bigram from the top 15 bigrams with the input word as the first word
# (does not contain a start or end tag)
def getRandomBigramFromInput(inputWord):
    count = 0
    bigrams = []

    for bigram in sortedNormalizedBigramFrequencies.keys():
        currentBigram = bigram.split()
        
        if '<start>' not in currentBigram and '</start>' not in currentBigram:
            if currentWord == bigram.split()[0]:
                bigrams.append(bigram)
                count += 1
            if count == 15:
                break

    try:
        return random.choice(bigrams)
    except IndexError:
        return getRandomBigramFromCorpus()

# Return a random bigram from the top 15 most likely bigrams (does not contain a start or end tag)
def getRandomBigramFromCorpus():
    count = 0
    bigrams = []

    for bigram in sortedNormalizedBigramFrequencies.keys():
        currentBigram = bigram.split()

        if '<start>' not in currentBigram and '</start>' not in currentBigram:
            bigrams.append(bigram)
            count += 1
        
            if count == 15:
                break

    return random.choice(bigrams)
    

file = open('Shakespeare.txt', 'r')

# Will hold a list of all of the tokens in the text file
modifiedTokens = []

# Preprocess the text
# Remove punctuation, digits, and convert to lowercase
# Append a <start> to the beginning of each line and a <start/> to the end of each line
# Convert the text file to a list of Strings
for line in file:
    preprocessedLine = '<start>' + line.translate(str.maketrans('', '', string.punctuation)).translate(str.maketrans('', '', string.digits)).lower() + ' </start>'
    modifiedTokens += preprocessedLine.split()

# Count the bigram frequencies
bigramFrequencies = {}
# Count the unigram frequencies
unigramFrequencies = {}
for i in range(len(modifiedTokens)):
    if i < len(modifiedTokens) - 1:
        bigram = modifiedTokens[i] + " " + modifiedTokens[i + 1]

        try:
            bigramFrequencies[bigram] += 1
        except KeyError:
            bigramFrequencies[bigram] = 1

    try:
        unigramFrequencies[modifiedTokens[i]] += 1
    except KeyError:
        unigramFrequencies[modifiedTokens[i]] = 1

# Normalize the bigrams using the unigram frequencies
normalizedBigramFrequencies = {}
for bigram, frequency in bigramFrequencies.items():
    firstWord = bigram.split()[0]

    normalizedBigramFrequencies[bigram] = frequency / unigramFrequencies[firstWord]
# Pre-process the sentence
sentence = input('Enter a sentence to get the probability: ')
sentence = sentence.translate(str.maketrans('', '', string.punctuation)).translate(str.maketrans('', '', string.digits)).lower()
sentence = '<start> ' + sentence + ' </start>'
sentence = sentence.split()

# This will be the log probability of the sentence
logProbability = 0

# Calculate the log probabilities of the bigrams
for i in range(len(sentence) - 1):
    bigram = sentence[i] + " " + sentence[i + 1]

    try:
        logProbability += math.log10(normalizedBigramFrequencies[bigram])
    except KeyError:
        logProbability += math.log10(sys.float_info.epsilon)

print('The log probability: ', logProbability)
print('The probability: ', 10**logProbability)

# Sort the bigrams based on frequency and convert to a dictionary
sortedNormalizedBigramFrequencies = sorted(normalizedBigramFrequencies.items(), key=lambda kv: kv[1], reverse=True)
sortedNormalizedBigramFrequencies = collections.OrderedDict(sortedNormalizedBigramFrequencies)

# Get user input for the random bigram
builtSentence = input('Enter a random bigram: ')
builtSentence = builtSentence.translate(str.maketrans('', '', string.punctuation)).translate(str.maketrans('', '', string.digits)).lower()

# The current word will always be the last word in the sentence
currentWord = builtSentence.split()[1]

for i in range(8):
    likelyBigram = getRandomBigramFromInput(currentWord)

    try:
        currentWord = likelyBigram.split()[1]
        builtSentence += " " + currentWord
    except IndexError:
        currentWord = currentWord

print(builtSentence)
