from CS50_AI.Project1.knights.logic import And, Implication, Not, Or, Sentence, Symbol
from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Common Sense1: A person can only be either a knight or a knave
APerson = And(
    Or(AKnight, AKnave),
    Not(AKnight, AKnave)
)
BPerson = And(
    Or(BKnight, BKnave),
    Not(BKnight, BKnave)
)
CPerson = And(
    Or(CKnight, CKnave),
    Not(CKnight, CKnave)
)
# Common Sence2: A knight always says truth, A knave always says lies
Truth = Implication(AKnight, )

# Knight speaks true statement, 


# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(

    # Puzzle 0 (Translation)
    Implication(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
