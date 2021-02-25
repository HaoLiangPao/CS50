#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Numbering all possible images to be recovered
    int number = 0;
    uint8_t buffer[512];
    bool foundImage = false;
    // char *filename = malloc(8 * sizeof(char)); // 123.jpg
    char filename[8];
    FILE *output = NULL;

    // There are 512 bytes to be read
    while (fread(buffer, 512, 1, input) == 1)
    {
        // Check for signitures
        if (buffer[0] == 0xff &&
            buffer[1] == 0xd8 &&
            buffer[2] == 0xff &&
            // Make sure the first four bites are 1110
            (buffer[3] & 0xf0) == 0xe0)
        {
            // If found a new image
            if (foundImage == false)
            {
                // Switch found flag
                foundImage = true;
            }
            else
            {
                // Already found a new image
                fclose(output);
            }
            // free(filename);
            // Found a new picture, assign a new name
            sprintf(filename, "%.3i.jpg", number);
            // Increase the numbering system for images
            // printf("%s image is been created.\n", filename);
            number ++;
            output = fopen(filename, "w");
            // Write 512 bytes from the buffer into the new image file
            fwrite(buffer, 512, 1, output);

        }
        // Keep looking for more information of the current image
        if (foundImage && (buffer[0] != 0xff ||
                           buffer[1] != 0xd8 ||
                           buffer[2] != 0xff ||
                           (buffer[3] & 0xf0) != 0xe0))
        {
            fwrite(buffer, 512, 1, output);
        }
    }
}