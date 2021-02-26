import re

# Get user input
change = -1.0
# Only take an input value between 1 and 8 (inclusive)
while not (0 <= change):
    user_input = input("Change owed: ")
    # Reject invalid inputs
    if (user_input.isnumeric() or "." in user_input):
        change = float(user_input)
change = int(change * 100)
# Greedy Algorithum (every coin is multiplited by 100 and turned into an integer)
coins = [25, 10, 5, 1]
count = 0
while change > 0:
    # print(f"Change before: {change}")
    if change >= coins[0]:
        change -= coins[0]
    elif coins[1] <= change < coins[0]:
        change -= coins[1]
    elif coins[2] <= change < coins[1]:
        change -= coins[2]
    else:
        change -= coins[3]
    count += 1
    # print(f"Change now: {change}")
print(f"{count}\n")