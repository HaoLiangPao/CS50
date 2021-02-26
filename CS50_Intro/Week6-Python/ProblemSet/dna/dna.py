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
                "TTTTTTCT": int(row["TTTTTTCT"]),
                "TCTAG": int(row["TCTAG"]),
                "GATA": int(row["GATA"]),
                "GAAA": int(row["GAAA"]),
                "TCTG": int(row["TCTG"]),
                "TATC": int(row["TATC"]),
                "AATG": int(row["AATG"])
            }


def main():
    # Flag for compare result
    found = False

    if len(sys.argv) > 3 or len(sys.argv) < 2:
        sys.exit("Usage: python dna.py [database.csv] [testing.txt]")
    database = sys.argv[1]
    testing = sys.argv[2]

    # Load data from files into memory
    # print("Loading database...")
    load_data(database)
    # print("Database loaded.")

    # Load DNA sequence from testing file
    f = open(testing, "r")
    sequence = f.readline()
    # Searching for STRs
    counts = {
        "AGATC" : 0,
        "TTTTTTCT" : 0,
        "AATG" : 0,
        "TCTAG" : 0,
        "GATA" : 0,
        "TATC" : 0,
        "GAAA" : 0,
        "TCTG" : 0
    }
    for index in range(len(sequence)):
        four = sequence[index : index + 4]
        five = sequence[index : index + 5]
        eight = sequence[index : index + 8]
        if five in counts:
            counts[five] += 1
        if four in counts:
            counts[four] += 1
        if eight in counts:
            counts[eight] += 1
    # Comparing with the database records
    for person in people.keys():
        record = people[person]
        count = 0
        # Compare all counts statistics with records
        for STR in counts.keys():
            if counts[STR] == record[STR]:
                count += 1
                # Set a confidential threashold to 3
                if count >= 3:
                    found = True
                    print(person)

    print(people)
    print(counts)
    if not found:
        print("No match")


if __name__ == "__main__":
    main()
