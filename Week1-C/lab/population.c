#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // pre-defined some variables
    int startSize, endSize, population;
    // year counter
    int years = 0;
    do
    {
        // Prompt for start size
        startSize = get_int("Start size: ");
    }
    while (startSize < 0);

    do
    {
        // Prompt for end size
        endSize = get_int("End size: ");
    }
    while (endSize < startSize);

    // Calculate number of years until we reach threshold
    population = startSize;
    do
    {
        population = population + population / 3 - population / 4;
        years ++;

    }
    while (population < endSize);

    // Print number of years
    printf("%i\n", years);
}