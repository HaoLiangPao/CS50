import unittest
from generate import *


class TestEnforceNodeConsistency(unittest.TestCase):
    def test_enforce_node_consistency(self):
        # Get data source
        structure = "data/structure0.txt"
        words = "data/words0.txt"
        # Generate crossword
        crossword = Crossword(structure, words)
        creator = CrosswordCreator(crossword)
        # Before enfoce_node_consistency:
        before = {Variable(1, 4, 'down', 4): {'EIGHT','FIVE','FOUR','NINE','ONE','SEVEN','SIX','TEN','THREE','TWO'}, 
                  Variable(4, 1, 'across', 4): {'EIGHT','FIVE','FOUR','NINE','ONE','SEVEN','SIX','TEN','THREE','TWO'},
                  Variable(0, 1, 'across', 3): {'EIGHT','FIVE','FOUR','NINE','ONE','SEVEN','SIX','TEN','THREE','TWO'},
                  Variable(0, 1, 'down', 5): {'EIGHT','FIVE','FOUR','NINE','ONE','SEVEN','SIX','TEN','THREE','TWO'}}
        self.assertDictEqual(before, creator.domains)
        after = {Variable(1, 4, 'down', 4): {'FIVE', 'FOUR', 'NINE'},
                 Variable(4, 1, 'across', 4): {'FIVE', 'FOUR', 'NINE'},
                 Variable(0, 1, 'across', 3): {'ONE', 'SIX', 'TEN', 'TWO'},
                 Variable(0, 1, 'down', 5): {'EIGHT', 'SEVEN', 'THREE'}}
        creator.enforce_node_consistency()
        self.assertDictEqual(after, creator.domains)


if __name__ == '__main__':
    unittest.main()
