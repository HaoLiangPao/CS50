#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(void)
{
    int height;
    do{
        height = get_int("Height: ");
    } while (
        height > 8 || height < 1 // height can only be 1 to 8 (inclusive)
    );

    printf("height is: %i\n", height);

    char result[] = "";
    if (height >= 1 && height <= 8) {
        for (int level=0; level < height; level++) {
        int repeatTimes = level + 1;
        printf("height is: %i\n", height);
        printf("level is: %i\n", level);
        printf("repeatedTimes is: %i\n", repeatTimes);
        char levelResult[] = "";
        // Left side pyramid
        for (int leftRepeat = 0; leftRepeat < repeatTimes; leftRepeat++) {
            // printf("%i\n", leftRepeat);
            strcat(levelResult, "#");   
        }

        printf("%s\n", levelResult);

        // Middle gap
        strcat(levelResult, "  ");

        printf("after middle gap %s\n", levelResult);


        // Right side pyramid
        for (int rightRepeat = 0; rightRepeat < level+1; rightRepeat++) {
            // printf("right repeat is: %i\n", rightRepeat);
            // printf("level + 1 is: %i\n", level + 1);
            // strcat(levelResult, "#");
        }
        // Change to the next line
        strcat(levelResult, "\n");


        printf("%s\n", levelResult);

        strcat(result, levelResult);
    }
    }


    printf("%s\n", result);
}