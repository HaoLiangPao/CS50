import itertools
import random

from pygame.image import save


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # Can only garentee mines when all cells in the set are mines
        if len(self.cells) == self.count:
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # Can only garentee safe cells when the count is 0
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # Check if a cell is been considering by this sentence
        if cell in self.cells:
            # Update the sentence based on this cell is been marked as a mine
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # Check if a cell is been considering by this sentence
        if cell in self.cells:
            # Update the sentence based on this cell is been tested to be safe
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Mark the cell as a move that has been made
        self.moves_made.add(cell)
        # 1. Mark the cell as safe
        # 2. Update existing knowledge the current cell is safe
        self.mark_safe(cell)
        # Add a new sentence to the AI's KB based on the value of `cell` and `count`\
        inference = set()
        c_row, c_column = cell
        # Add all nearby cells into the inference
        for row in range(c_row - 1, c_row + 2):
            # Not exceeding the game board limit
            if 0 <= row <= self.height - 1:
                for column in range(c_column - 1, c_column + 2):
                    # Not exceeding the game board limit
                    if 0 <= column <= self.width - 1:
                        neighbor = (row, column)
                        # Only add undetermined cells
                        if neighbor not in self.moves_made:
                            inference.add(neighbor)
        # Add the inference with the number of mines into a sentence
        new_knowledge = Sentence(inference, count)
        self.knowledge.append(new_knowledge)
        # Mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base

        # print(f"Moves made are: {self.moves_made}")
        # print(f"knowledge base is: {self.knowledge}")
        
        for knowledge_base in self.knowledge:
            # Check if there are any conclusions can be made already
            know_mines = knowledge_base.known_mines()
            know_safes = knowledge_base.known_safes()
            # print(f"Know safes are {know_safes}")
            # print(f"Know mines are {know_mines}")
            if know_mines:
                # Copy the set since the original return result may be changed by mark functions
                know_mines = know_mines.copy()
                for cell in know_mines:
                    print(f"Cell {cell} is a mine")
                    self.mark_mine(cell)
            if know_safes:
                # Copy the set since the original return result may be changed by mark functions
                know_safes = know_safes.copy()
                for cell in know_safes:
                    print(f"Cell {cell} is safe")
                    self.mark_safe(cell)
            # print(f"safe cells are: {self.safes}")
            # print(f"mines are: {self.mines}")
        current_knowledge = self.knowledge.copy()
        for knowledge_base in current_knowledge:
            # Add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge
            kb_cells, new_cells = knowledge_base.cells, new_knowledge.cells
            kb_count, new_count = knowledge_base.count, new_knowledge.count
            different_cells = set()
            # Check if one inference is a subset of the other
            if kb_cells.issubset(new_cells):
                # new_cells is bigger, what ever left in new_cells except the overlap can be drived into a new sentence
                different_cells = new_cells.difference(kb_cells)
                different_count = new_count - kb_count
            elif new_cells.issubset(kb_cells):
                # Similar idea, but this time knowledge_base is bigger
                different_cells = kb_cells.difference(new_cells)
                different_count = kb_count - new_count
            # If there are new knowledge to be added
            if different_cells:
                derived_knowledge = Sentence(different_cells, different_count)
                self.knowledge.append(derived_knowledge) # Changing the iterative while iterating it? could it be a flau?
        print(new_knowledge)
        print("\n")


    def generate_knowledge(self, new_knowledge):
        """
        Derived possible new knowledge based on knowledge base we captured so far
        """
        for knowledge_base in self.knowledge:
            # Check if one inference is a subset of the other
            if knowledge_base.issubset(new_knowledge):
                different_cells = new_knowledge.difference(knowledge_base)
                different_count = new_knowledge.count - knowledge_base.count
            elif new_knowledge.issubset(knowledge_base):
                different_cells = knowledge_base.difference(new_knowledge)
                different_count = knowledge_base.count - new_knowledge.count
            derived_knowledge = Sentence(different_cells, different_count)
            

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for row in range(self.height):
            for column in range(self.width):
                move = (row, column)
                if (move not in self.moves_made) and (move not in self.mines) and (move in self.safes):
                    print(f"Save move been took: {move}")
                    return move
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for row in range(self.height):
            for column in range(self.width):
                move = (row, column)
                if move not in self.moves_made and move not in self.mines:
                    print(f"Random move been took: {move}")
                    return move
        return None
