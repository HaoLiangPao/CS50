#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int main(int argc, string argv[])
{
    string cipherKey = NULL;

    // Key validation
    // 1. No command line arguments || too much command line arguments
    if (!argv[1] || argv[2])
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    else
    {
        // 2. Too short
        cipherKey = argv[1];
        int index = 0;
        while (cipherKey[index] != '\0')
        {
            char charactor = cipherKey[index];
            // 3. Special character
            if (charactor < 65 || (charactor > 90 && charactor < 97) || charactor > 122)
            {
                printf("Key must only contain alphabetic characters.\n");
                return 1;
            }
            for (int search = 0; search < index; search ++)
            {
                // 4. Duplicate char
                if (cipherKey[search] == charactor)
                {
                    printf("Key must not contain repeated characters.\n");
                    return 1;
                }
            }
            index += 1;
        }
        if (index != 26)
        {
            printf("Key must contain 26 characters.\n");
            return 1;
        }

    }

    // 2.  Substitution
    string plainText = get_string("plaintext:  ");
    // printf("Length of string a = %i \n", (int) strlen(plainText));
    char cyperText[strlen(plainText)];
    int plainTextIndex = 0;
    while (plainText[plainTextIndex] != '\0')
    {
        char charactor = plainText[plainTextIndex];
        // Capital letters
        if (charactor >= 65 && charactor <= 90)
        {
            int newChar = (int) cipherKey[charactor - 65];
            if (newChar >= 97 && newChar <= 122)
            {
                newChar += -32;
            }
            cyperText[plainTextIndex] = (char) newChar;
        }
        // Small cases
        else if (charactor >= 97 && charactor <= 122)
        {
            int newChar = (int) cipherKey[charactor - 97];
            if (newChar >= 65 && newChar <= 90)
            {
                newChar += 32;
            }
            cyperText[plainTextIndex] = (char) newChar;
        }
        else // keep anything other than letters
        {
            cyperText[plainTextIndex] = plainText[plainTextIndex];
        }
        plainTextIndex += 1;
    }
    printf("ciphertext:  %s\n", cyperText);
}