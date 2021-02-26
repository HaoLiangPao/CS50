# Get user input
text = input("Text: ")

letters, words, sentences = 0, 1, 0
for char in text:
    if char.isalpha():
        letters += 1
    elif char == " ":
        words += 1
    elif char in ".!?":
        sentences += 1
print(letters, words, sentences)
L = 100 / words * letters
S = 100 / words * sentences
CL_index = 0.0588 * L - 0.296 * S - 15.8
print(CL_index)

# Display a message about CL index
if CL_index < 0:
    print("Before Grade 1\n")
elif CL_index >= 16:
    print("Grade 16+\n")
else:
    print(f"Grade {round(CL_index)}")