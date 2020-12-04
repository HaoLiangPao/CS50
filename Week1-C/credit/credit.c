#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>

int main(void)
{
    long cardNumber = get_long("Number: ");
    int length = floor(1.0 + log10((double) llabs(cardNumber)));
    // printf("%i\n", length);


    int firstDigit;
    int secondDigit;
    int oddSum = 0;
    int evenSum = 0;

    // Length check
    if (length != 15 && length != 13 && length != 16)
    {
        printf("INVALID\n");
    }
    else
    {
        // Loop through all digits
        for (int index = 0; index < length; index++)
        {
            int digit = cardNumber % 10;
            // printf("%i\n", digit);
            // 1. add last digit to evenSum
            if (index % 2 == 0)
            {
                evenSum += digit;
            }
            else
            {
                // calculate by multiplying by 2
                int changeDigit = digit * 2;
                if (changeDigit >= 10)
                {
                    oddSum += changeDigit % 10 + 1;
                }
                else
                {
                    oddSum +=  changeDigit;
                }
            }

            // 2. record the first and the second digits
            if (index == length - 2)
            {
                secondDigit = digit;
            }
            if (index == length - 1)
            {
                firstDigit = digit;
            }
            cardNumber = (cardNumber - digit) / 10;
        }


        // Sumcheck
        // printf("oddSum is: %i\n", oddSum);
        // printf("evenSum is: %i\n", evenSum);
        // printf("firstDigit is: %i\n", firstDigit);
        // printf("secondDigit is: %i\n", secondDigit);
        int sumCheck = (oddSum + evenSum) % 10;

        if (sumCheck != 0)
        {
            printf("INVALID\n");
        }
        else
        {
            // 1. america express
            if (firstDigit == 3 && (secondDigit == 4 || secondDigit == 7))
            {
                printf("AMEX\n");
            }
            // 2. mastercard
            else if (firstDigit == 5 && (secondDigit < 6 && secondDigit > 0))
            {
                printf("MASTERCARD\n");
            }
            // 3. visa
            else if (firstDigit == 4)
            {
                // visa
                printf("VISA\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
    }
}