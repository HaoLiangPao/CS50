import csv
import sys
import calendar

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Read data in from file
    with open(filename) as f:
        reader = csv.reader(f)
        # Record the column titles, plug it into a one line reader function
        columns = next(reader)
        # print(columns)
        evidence = []
        lable = []
        for row in reader:
            evidence.append(read_one_row(row, columns))
            lable.append(0 if row[17] == "FALSE" else 1)
        data = (evidence, lable)
    # Return evidence, lable sets read from the file
    return data

def read_one_row(row, columns):
    """
    Read one row of data from shopping.csv, turn a long string into desireable datatype
    """
    result = []
    # ["Administrative", "Informational", "ProductRelated", "Month", "OperatingSystems", "Browser", "Region", "TrafficType", "VisitorType", "Weekend"]
    int_index = [0, 2, 4, 10, 11, 12, 13, 14, 15, 16]
    # Three special values: Month, VisitorType, Weekend
    special = [10, 15, 16]
    # ["Administrative_Duration", "Informational_Duration", "ProductRelated_Duration", "BounceRates", "ExitRates", "PageValues", "SpecialDay"]
    float_index = [1, 3, 5, 6, 7, 8, 9]
    for index in range(len(row)):
        if index in int_index:
            # Numerical input, just convert into integers
            if index not in special:
                result.append(int(row[index]))
            # Variables which need special treatment
            else:
                # Month
                if index == 10:
                    if row[index] != "June":
                        result.append(list(calendar.month_abbr).index(row[index]))
                    else:
                        result.append(6)
                # VisitorType
                elif index == 15:
                    visitor = 1 if row[index] == "Returning_Visitor" else 0
                    result.append(visitor)
                # Weekend
                elif index == 16:
                    weekend = 0 if row[index] == "FALSE" else 1
                    result.append(weekend)
        elif index in float_index:
            result.append(float(row[index]))
    return result

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Initialize a k-neighbors model
    model = KNeighborsClassifier(n_neighbors=1)
    # Train model on training set
    model.fit(evidence, labels)
    return model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # Compute how well we performed
    # Sensitivity
    sen_correct = 0
    sen_incorrect = 0
    sen_total = 0
    # Spectivity
    spe_correct = 0
    spe_incorrect = 0
    spe_total = 0
    for actual, predicted in zip(labels, predictions):
        # Sensitivity
        if actual == 1:
            sen_total += 1
            if actual == predicted:
                sen_correct += 1
            else:
                sen_incorrect += 1
        # Specificity
        else:
            spe_total += 1
            if actual == predicted:
                spe_correct += 1
            else:
                spe_incorrect += 1
    return (float(sen_correct / sen_total), float(spe_correct / spe_total))


if __name__ == "__main__":
    main()
