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
    

    def test_revise(self):
        # Get data source
        structure = "data/structure0.txt"
        words = "data/words0.txt"
        # Generate crossword
        crossword = Crossword(structure, words)
        creator = CrosswordCreator(crossword)
        # Enforce_node_consistency
        creator.enforce_node_consistency()
        # Create two variable
        v1 = Variable(1, 4, 'down', 4)
        v2 = Variable(4, 1, 'across', 4)
        v3 = Variable(0, 1, 'across', 3)
        v4 = Variable(0, 1, 'down', 5)
        # Revise v1, v2 will have no effect since they are not neighbors
        self.assertEqual(creator.revise(v1, v2), False)
        # Revise v3, v4 will have conflict and eliminate one from v3
        before = {Variable(1, 4, 'down', 4): {'FIVE', 'FOUR', 'NINE'},
                 Variable(4, 1, 'across', 4): {'FIVE', 'FOUR', 'NINE'},
                 Variable(0, 1, 'across', 3): {'ONE', 'SIX', 'TEN', 'TWO'},
                 Variable(0, 1, 'down', 5): {'EIGHT', 'SEVEN', 'THREE'}}
        self.assertDictEqual(before, creator.domains)
        self.assertEqual(creator.revise(v3, v4), True)
        after = {Variable(1, 4, 'down', 4): {'FIVE', 'FOUR', 'NINE'},
                 Variable(4, 1, 'across', 4): {'FIVE', 'FOUR', 'NINE'},
                 Variable(0, 1, 'across', 3): {'SIX', 'TEN', 'TWO'},
                 Variable(0, 1, 'down', 5): {'EIGHT', 'SEVEN', 'THREE'}}
        self.assertDictEqual(after, creator.domains)

    def test_ac3(self):
        # Get data source
        structure = "data/structure0.txt"
        words = "data/words0.txt"
        # Generate crossword
        crossword = Crossword(structure, words)
        creator = CrosswordCreator(crossword)
        # Enforce_node_consistency
        creator.enforce_node_consistency()
        # ac3 - make the whole board arc-consistent
        before = {Variable(1, 4, 'down', 4): {'FIVE', 'FOUR', 'NINE'},
                Variable(4, 1, 'across', 4): {'FIVE', 'FOUR', 'NINE'},
                Variable(0, 1, 'across', 3): {'ONE', 'SIX', 'TEN', 'TWO'},
                Variable(0, 1, 'down', 5): {'EIGHT', 'SEVEN', 'THREE'}}
        self.assertDictEqual(before, creator.domains)
        creator.ac3()
        after = {Variable(1, 4, 'down', 4): {'FIVE', 'NINE'},
                    Variable(4, 1, 'across', 4): {'NINE'},
                    Variable(0, 1, 'across', 3): {'SIX'},
                    Variable(0, 1, 'down', 5): {'SEVEN'}}
        self.assertDictEqual(after, creator.domains)
    
    def test_assignment_complete(self):
        # Get data source
        structure = "data/structure0.txt"
        words = "data/words0.txt"
        # Generate crossword
        crossword = Crossword(structure, words)
        creator = CrosswordCreator(crossword)
        assignment = {Variable(1, 4, 'down', 4): 'FIVE',
            Variable(4, 1, 'across', 4): 'NINE',
            Variable(0, 1, 'across', 3): 'SIX',
            Variable(0, 1, 'down', 5): 'SEVEN'}
        self.assertEqual(creator.assignment_complete(assignment), True)
        assignment = {Variable(1, 4, 'down', 4): '',
            Variable(4, 1, 'across', 4): 'NINE',
            Variable(0, 1, 'across', 3): 'SIX',
            Variable(0, 1, 'down', 5): 'SEVEN'}
        self.assertEqual(creator.assignment_complete(assignment), False)
    
    def test_consistent(self):
        # Get data source
        structure = "data/structure0.txt"
        words = "data/words0.txt"
        # Generate crossword
        crossword = Crossword(structure, words)
        creator = CrosswordCreator(crossword)
        assignment = {Variable(1, 4, 'down', 4): 'FIVE',
            Variable(4, 1, 'across', 4): 'NINE',
            Variable(0, 1, 'across', 3): 'SIX',
            Variable(0, 1, 'down', 5): 'SEVEN'}
        self.assertEqual(creator.consistent(assignment), True)
        assignment = {Variable(1, 4, 'down', 4): 'SIX',
            Variable(4, 1, 'across', 4): 'NINE',
            Variable(0, 1, 'across', 3): 'SIX',
            Variable(0, 1, 'down', 5): 'SEVEN'}
        self.assertEqual(creator.consistent(assignment), False)
    

if __name__ == '__main__':
    unittest.main()
