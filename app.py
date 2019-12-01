import csv
import Levenshtein

""" Constants """
CUTOFF = 0.91

""" Reads CSV file and returns the content in a dictionary """
def readCsvFile():
    csvContents = {}

    with open('input.csv') as csvFile:
        fileReader = csv.reader(csvFile, delimiter=',', quotechar='"')

        # Ditch the first line (header)
        next(fileReader)

        for row in fileReader:
            csvContents[row[0]] = int(row[1])

    return csvContents

# Let's read the input dictionary from file
inputDict = readCsvFile()

# Let's grab the words as an array
wordArray = list(inputDict.keys())

with open('output.txt', 'w') as outputFile:
    for word in wordArray:
        for word2 in wordArray:
            if word == word2:
                continue

            # Calculate the distance according to Jaro Winkler
            # https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance
            calculatedDistance = Levenshtein.jaro_winkler(word, word2)

            if calculatedDistance > CUTOFF:
                # Combine the count
                if word in inputDict:
                    inputDict[word] += inputDict[word2]
                    outputFile.write(f'"{word}" count has been bumped to {inputDict[word]} due to merge with "{word2}" (distance: {calculatedDistance})\r\n')

                # Strip the word from the dictionary
                del inputDict[word2]
                wordArray.remove(word2)