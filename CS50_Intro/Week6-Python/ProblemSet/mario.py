# Get user input
height = 0
# Only take an input value between 1 and 8 (inclusive)
while not (0 < height < 9):
    user_input = input("Height: ")
    # Reject invalid inputs
    if (user_input.isnumeric()):
        height = int(user_input)
# Printing the pyramid
for i in range(height + 1):
    if i != 0:
        print(f"{' ' * (height - i)}{'#' * i}")