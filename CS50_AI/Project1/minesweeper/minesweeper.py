import itertools
import random


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
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # Can only garentee safe cells when the count is 0
        if self.count == 0:
            return self.cells
        else:
            return set()

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
        # 1) Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) Mark the cell as safe
        self.mark_safe(cell)

        # 3) Add a new sentence to the AI's KB based on the value of `cell` and `count`
        inference = set()
        c_row, c_column = cell
        # 1. Add all nearby cells into the inference
        for row in range(c_row - 1, c_row + 2):
            for column in range(c_column - 1, c_column + 2):
                # Not exceeding the game board limit
                if 0 <= column <= self.width - 1 and 0 <= row <= self.height - 1:
                    neighbor = (row, column)
                    if neighbor != cell:
                        inference.add(neighbor)
        # 2. Add the inference with the number of mines into a sentence
        new_knowledge = Sentence(inference, count)

        # print(new_knowledge)
        for mine in self.mines:
            new_knowledge.mark_mine(mine)
        for safe in self.safes:
            new_knowledge.mark_safe(safe)

        self.knowledge.append(new_knowledge)

        # 4) mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
        new_mines, new_safes = set(), set()
        # AI's knowledge base now have new inferences been added after the previous move is made, so we should check if now conclusions can be made
        for knowledge in self.knowledge:
            for mine in knowledge.known_mines():
                new_mines.add(mine)
            for safe in knowledge.known_safes():
                new_safes.add(safe)
        # Can not change the set at iteration runtime
        for mine in new_mines:
            self.mark_mine(mine)
        for safe in new_safes:
            self.mark_safe(safe)
        # Knowledge will only be removed when it is empty but not after it is been used. Where mark safe, make mine can do it

        # 5) add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge
        derived_knowledges = []
        # 1. Compare every two knowledge, check if they are subsites, find the part overlap and the part doesnt
        # new knowledge can be drawn not only between every old knowledge and the new knowledge, but also between any two old knowledges (since they could be changed by a new move been made)
        for knowledgeA, knowledgeB in itertools.combinations(self.knowledge, 2):
            A_cells, B_cells = knowledgeA.cells, knowledgeB.cells
            A_count, B_count = knowledgeA.count, knowledgeB.count
            # Only subset can drived a knowledge which is true for sure, if some overlaps with two different parts on each side will not able to give a certain knowledge
            if A_cells.issubset(B_cells):
                new_sentence = Sentence(B_cells - A_cells, B_count - A_count)
            elif B_cells.issubset(A_cells):
                new_sentence = Sentence(A_cells - B_cells, A_count - B_count)
            else:
                new_sentence = None
            # 2. Add the new knowledge to the base (only when the new knowledge is not duplicate or empty)
            if new_sentence is not None and new_sentence not in self.knowledge:
                derived_knowledges.append(new_sentence)
        # Can not change the knowledge on the for iteration runtime
        self.knowledge.extend(derived_knowledges)
        # 3. Clean empty sentences so the knowledge base will not be occupied with empty lists
        for knowledge in self.knowledge:
            if knowledge == Sentence(set(), 0):
                self.knowledge.remove(knowledge)
        # print("derived knowledge is: ")
        # for k in derived_knowledges:
        #     print(f"  {k.cells}")
        #     print(f"  {k.count}")
        # print("knowledge base is: ")
        # for k in self.knowledge:
        #     print(f"  {k.cells}")
        #     print(f"  {k.count}")

    def check_duplicate_knowledge(self, cells):
        for base in self.knowledge:
            if cells == base.cells:
                return True
        return False

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Not choosing from left top corner, choose from the known safes
        safe_moves = self.safes - self.moves_made
        # Randomly pick a safe cell if there exists, otherwise, return none
        if safe_moves:
            return random.choice(tuple(safe_moves))
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Original implementation is not completely random
        possible_moves = set(itertools.product(range(0, self.height), range(0, self.width)))
        moves_left = possible_moves - self.mines - self.moves_made - self.safes
        # Randomly pick a safe cell if there exists, otherwise, return none
        if moves_left:
            return random.choice(tuple(moves_left))
        else:
            return None