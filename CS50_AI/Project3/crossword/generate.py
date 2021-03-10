import sys
import math

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        # Add all words to each domain of a variable
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        # Generate an empty 2D array
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        # Add items from a given assignment to the 2D array
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Enforce node consistency for each variable
        vars = self.crossword.variables
        for var in vars:
            # Compare values in the domain of each variable, remove it if length not suitable
            val_to_remove = []
            for val in self.domains[var]:
                # Remove a value from the domain if length is not equivalent
                if var.length != len(val):
                    val_to_remove.append(val)
            for val in val_to_remove:
                self.domains[var].remove(val)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # 1. Neighbors can't have different value at overlaping point
        # Flag for revised or not
        revised = False
        # Remove vals list
        x_remove = []
        overlap = self.crossword.overlaps[x, y]
        # Eliminating values from domains only if they are neighbors
        if overlap:
            # Check binary constraint for each possible values within a variable domain x
            for val_x in self.domains[x]:
                found = False
                for val_y in self.domains[y]:
                    # Test binary constraint
                    if val_x[overlap[0]] == val_y[overlap[1]]:
                        found = True
                        break
                # For given value x, no value y can meet the binary constraint
                if not found:
                    x_remove.append(val_x)
        # Remove elements from the x domain
        for val_x in x_remove:
            self.domains[x].remove(val_x)
            revised = True
        # 2. Same element can not appear more than once
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Get a quene of all arcs
        queue = [
            arc for arc in self.crossword.overlaps
            if self.crossword.overlaps[arc] is not None
        ]
        while queue:
            # Pop an arc pair
            arc = queue.pop(0)
            x, y = arc[0], arc[1]
            # When a change been made
            if self.revise(x, y):
                # Check if there are still values left in the x domain
                if len(self.domains[x]) == 0:
                    # Game over, no reasonable solution can be made
                    return False
                # Add possible arc to queue (which maintains an arc constraint to the value just changed)
                for z in self.crossword.neighbors(x):
                    # Y is already been arc consistent with x
                    if z != y:
                        # Less values in the domain now, will need to check if other neighbors are still consistent to x
                        queue.append((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Check the assignment has values for all variables
        if len(assignment) != len(self.crossword.variables):
            return False
        # Check every value in the assignment is meaningful
        for var in self.crossword.variables:
            if (var not in assignment) or (len(assignment[var]) == 0):
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Anser set, used for checing uniqueness
        answer = set()
        for var in assignment:
            if assignment[var] not in answer:
                answer.add(assignment[var])
            else:
                return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        return self.domains[var]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # 1. Get variables not in assignment yet
        unassigned_vars = []
        for var in self.crossword.variables:
            if var not in assignment:
                unassigned_vars.append(var)
        # 2. MRV (minimum remaining values) Heuristic
        min_mrv = math.inf
        vars_mrv = sorted(unassigned_vars, key=lambda var: len(self.domains[var]))
        # print(vars_mrv)
        vars_degree = []
        for var in vars_mrv:
            # If there is a unassigned variable with less possible choices
            # print(min_mrv, len(self.domains[var]))
            if var not in assignment and len(self.domains[var]) < min_mrv:
                vars_degree.append(var)
                min_mrv = len(self.domains[var])
        # If there is a tie, choose the one with highest degree
        # Degree Heuristic
        # Get the variable with the highest degree
        # print(sorted(vars_degree, key=lambda var: len(self.crossword.neighbors(var)), reverse=True))
        result = sorted(vars_degree, key=lambda var: len(self.crossword.neighbors(var)), reverse=True)[0]
        # Return the optimized variable selection
        return result


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Check if assignment is complete
        if self.assignment_complete(assignment):
            return assignment
        # Start backtracking by trying different variables
        var = self.select_unassigned_variable(assignment)
        # Trying different values within the variable domain
        for val in self.domains[var]:
            # Temperaraly add the value to the assignment
            assignment[var] = val
            # Current value could be add without violating constraints
            if self.consistent(assignment):
                # Try implement other variables
                result = self.backtrack(assignment)
                # If a complete assignment been returned instead of a none
                if result:
                    return result
            # Current value does not fit the other values within the assignment
            assignment[var] = None
        # If no assignment is possible
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
