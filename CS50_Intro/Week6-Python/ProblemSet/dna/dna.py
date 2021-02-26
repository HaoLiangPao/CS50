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
            if database == "databases/small.csv":
                people[row["name"]] = {
                    "AGATC": int(row["AGATC"]),
                    "TATC": int(row["TATC"]),
                    "AATG": int(row["AATG"])
                }
            else:
                people[row["name"]] = {
                    "AGATC": int(row["AGATC"]),
                    "TATC": int(row["TATC"]),
                    "AATG": int(row["AATG"]),
                    "TTTTTTCT": int(row["TTTTTTCT"]),
                    "TCTAG": int(row["TCTAG"]),
                    "GATA": int(row["GATA"]),
                    "GAAA": int(row["GAAA"]),
                    "TCTG": int(row["TCTG"]),
                }


def findConsecutivePattern(source, target):
    count, longest = 0, -1
    left, right, consecutive = 0, len(target), False
    while left < len(source) and right < len(source):
        # When a pattern found
        if source[left: right] == target:
            if consecutive == False:
                consecutive = True
            count += 1
            left, right = right, right + len(target)
        else:
            consecutive = False
            # A longer consecutinve sequence is found
            if count > longest:
                # Update the max and reset the count
                longest, count = count, 0
            # Check next index
            left, right = left + 1, right + 1
    return longest

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
    if database == "databases/small.csv":
        counts = {
            "AGATC" : 0,
            "AATG" : 0,
            "TATC" : 0,
        }
    else:
        counts = {
            "AGATC" : 0,
            "AATG" : 0,
            "TATC" : 0,
            "TTTTTTCT" : 0,
            "TCTAG" : 0,
            "GATA" : 0,
            "GAAA" : 0,
            "TCTG" : 0
        }

    # Count the longest consecutive STR patterns
    for STR in counts:
        counts[STR] = findConsecutivePattern(sequence, STR)

    # Comparing with the database records
    for person in people.keys():
        record = people[person]
        count = 0
        # Compare all counts statistics with records
        for STR in counts.keys():
            if counts[STR] == record[STR]:
                count += 1
                # Set a confidential threashold to 2
                if count >= 3:
                    found = True
                    print(person)
                    break
    # print(counts)
    # print(people["Charlie"])
    # print(people["Ron"])
    # print(people["Ginny"])
    if not found:
        print("No match")


if __name__ == "__main__":
    main()
