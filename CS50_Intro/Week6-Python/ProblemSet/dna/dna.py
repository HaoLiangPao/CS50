import csv
import sys

# Maps person'name to a dictionary of: AGATC, AATG, TATC
people = {}


def load_data(database):
    """
    Load data from CSV files into memory.
    """
    # Load people with their DNA records
    with open(database, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["name"]] = {
                "AGATC": int(row["AGATC"]),
                "AATG": int(row["AATG"]),
                "TATC": int(row["TATC"])
            }

def main():
    # Flag for compare result
    found = False

    if len(sys.argv) > 3 or len(sys.argv) < 2:
        sys.exit("Usage: python dna.py [database.csv] [testing.txt]")
    database = sys.argv[1] if len(sys.argv) == 2 else "databases/small.csv"
    testing = sys.argv[2]

    # Load data from files into memory
    # print("Loading database...")
    load_data(database)
    # print("Database loaded.")

    # Load DNA sequence from testing file
    f = open(testing, "r")
    sequence = f.readline()
    # Searching for STRs
    STRs = ["AGATC", "AATG", "TATC"]
    counts = [0, 0, 0]
    for index in range(len(sequence)):
        if sequence[index : index + 5] == STRs[0]:
            counts[0] += 1
        elif sequence[index : index + 4] == STRs[1]:
            counts[1] += 1
        elif sequence[index : index + 4] == STRs[2]:
            counts[2] += 1
    # Comparing with the database records
    for person in people.keys():
        record = people[person]
        if ((record["AGATC"] == counts[0]) and
         (record["AATG"] == counts[1]) and
         (record["TATC"] == counts[2])):
           found = True
           print(person)
    if not found:
        print("No match")


if __name__ == "__main__":
    main()
