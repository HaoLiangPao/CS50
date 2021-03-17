import nltk
import sys
import os
import re
import string
import math
from collections import Counter

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = {}
    # Get file path of each files in the given directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        # Only check valid txt files
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            # Open file and store data read into files dict
            with open(file_path, "r", encoding='utf8') as f:
                files[filename] = f.read()
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    result = []
    # Tokenize
    tokens = nltk.word_tokenize(document)
    for token in tokens:
        # 1. Not stopwords
        if token not in nltk.corpus.stopwords.words('english'):
            # 2. Remove punctuation symbols
            for symbol in string.punctuation:
                token = token.replace(symbol, '')
            # 3. Kept the lowercase version of each token
            if len(token) > 0:
                result.append(token.lower())
    return result



def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    total = len(documents)
    idf_map = {}
    # Grab words from each documents
    for document in documents:
        # Get each individual words
        for word in documents[document]:
            # Only create key-value pairs for each word once
            if word not in idf_map:
                count = 0
                # Check existence of a word in other documents
                for other_d in documents:
                    if word in documents[other_d]:
                        count += 1
                # Calculating a idf value for the word
                idf_map[word] = math.log(total / count)
    return idf_map


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idf = {
        document : 0 for document in files
    }
    for document in files:
        # Each word in the query contributes to the tf-idf
        for word in query:
            tf_idf[document] += files[document].count(word) * idfs[word]

    print([key for key, value in sorted(tf_idf.items(), key=lambda d: d[1], reverse=True)])
    # Sort the list by its tf_idf
    return [key for key, value in sorted(tf_idf.items(), key=lambda d: d[1], reverse=True)][:n]



def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sent_idfs = []
    for sentence in sentences:
        query_word_count, sum_idf = 0, 0
        for word in query:
            if word in sentences[sentence]:
                # Count the times a query word appears in the sentence
                query_word_count += 1
                # Count the total idf for a sentence
                sum_idf += idfs[word]
        query_term_density = query_word_count / len(sentences[sentence])
        sent_idfs.append([sentence, sum_idf, query_term_density])
    # Sort answers by sum_idf first, when draw, sort them on query term density
    return [sentence for sentence, sum_idf, qtd in sorted(sent_idfs, key=lambda item: (item[1], item[2]), reverse=True)][:n]


if __name__ == "__main__":
    main()
