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
                "AGATC": row["AGATC"],
                "AATG": row["AATG"],
                "TATC": row["TATC"]
            }

def main():
    if len(sys.argv) > 3 or len(sys.argv) < 2:
        sys.exit("Usage: python dna.py [database.csv] [testing.txt]")
    database = sys.argv[1] if len(sys.argv) == 2 else "databases/small.csv"
    testing = sys.argv[2]

    # Load data from files into memory
    print("Loading data...")
    load_data(database)
    print("Data loaded.")

    print(people)


if __name__ == "__main__":
    main()
