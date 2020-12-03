#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (
        height > 8 || height < 1 // height can only be 1 to 8 (inclusive)
    );

    // printf("height: %i\n", height);

    for (int level = 0; level < height; level ++)
    {
        // Calculate space and block needed for each level
        int numberSpace = height - (level + 1);
        // printf("numberSpace: %i\n", numberSpace);
        int numberBlock = level + 1;
        // printf("numberBlock: %i\n", numberBlock);

        // 1. left side
        for (int i = 0; i < numberSpace; i++)
        {
            printf(" "); // space
        }
        for (int j = 0; j < numberBlock; j++)
        {
            printf("#");// block
        }
        // 2. middle gap
        printf("  ");
        // 3. right side
        for (int j = 0; j < numberBlock; j++)
        {
            printf("#");
        }
        // 4. line break
        printf("\n");
    }
}