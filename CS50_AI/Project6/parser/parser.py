import nltk
from nltk.tree import Tree
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP | NP VP | S Conj S
AP -> Adj | Adv
NP -> N | Det NP | AP NP | NP PP | NP AP
PP -> P NP
VP -> V | V NP | V PP | AP VP | VP AP | VP Conj VP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
        # print(f"trees are: {trees}")
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    result = []
    # Tokenize
    tokens = nltk.word_tokenize(sentence)
    for token in tokens:
        # 2. Remove invalid words
        if token.isalpha():
            # 1. Convert to lower-case
            result.append(token.lower())
    return result


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    result = []
    stack = [tree]
    # Loop through all tree nodes
    while stack:
        tree_node = stack.pop()
        # Smallest unit of NP: contains no NP as children (NP -> N is okay but not NP -> NP)
        if Tree.label(tree_node) == 'NP':
            smaller_NP = False
            # Check children's label
            for child in tree_node:
                if Tree.label(child) == 'NP' and Tree.height(child) != 2:
                    smaller_NP = True
            # If no smaller NP node exists
            if not smaller_NP:
                result.append(tree_node)
                # No need to do further search
                continue
        # Could contains NP tree node with its subtrees
        if Tree.height(tree_node) > 2:
            for sub_tree in tree_node:
                stack.append(sub_tree)
    # I used a depth first search on the most right element, so reverse the order will match the normal reading order (left to right)
    result.reverse()
    return result

if __name__ == "__main__":
    main()
