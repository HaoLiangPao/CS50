#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    string input = get_string("Text: ");

    int letters = 0;
    int words = 1;
    int sentences = 0;

    int index = 0;
    while (input[index] != '\0')
    {
        char charactor = input[index];
        // find a letter
        if ((charactor >= 65 && charactor <= 90) || (charactor >= 97 && charactor <= 122))
        {
            letters += 1;
        }
        // find a word
        else if (charactor == 32)
        {
            words += 1;
        }
        else if (charactor == 33 || charactor == 46 || charactor == 63)
        {
            sentences += 1;
        }
        index += 1;
    }
    // Testing
    // printf("%i letters\n", letters);
    // printf("%i words\n", words);
    // printf("%i sentences\n", sentences);

    float hundred_words = (float) words / 100.00;
    float ave_letters_per_words = (float) letters / hundred_words;
    float ave_sentences_per_words = (float) sentences / hundred_words;
    int CL_index = (int) round(0.0588 * ave_letters_per_words - 0.296 * ave_sentences_per_words - 15.8);

    // Special case handling
    // Before Grade 1
    if (CL_index < 0)
    {
        printf("Before Grade 1\n");
    }
    else if (CL_index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", (int) round(CL_index));
    }
}