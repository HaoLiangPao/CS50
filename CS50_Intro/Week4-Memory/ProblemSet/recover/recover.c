#include <stdio.h>
#include <stdlib.h>

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
    string filename;

    // There are 512 bytes to be read
    while (fread(buffer, 512, 1, input) != 1) {
        // Check for signitures
        if (buffer[0] == 0xff &&
            buffer[1] == 0xd8 &&
            buffer[2] == 0xff &&
            // Make sure the first four bites are 1110
            (buffer[3] & 0xf0 == 0xe0)) {
                // If found a new image
                if (foundImage == false) {
                    // Switch found flag
                    foundImage = true;
                    // Found a new picture, assign a new name
                    sprint(filename, "%3i.jpg", number);
                    // Increase the numbering system for images
                    number ++;
                    FILE *output = fopen(filename, "w");
                    // Write 512 bytes from the buffer into the new image file
                    fwrite(output, 512, 1, buffer);
                } else {
                    // Already found a new image
                    // Switch found flag

                    fclose(output);
                }

        }
        // Keep looking for more information of the current image
        if ( buffer[0] != 0xff ||
             buffer[1] != 0xd8 ||
             buffer[2] != 0xff ||
             (buffer[3] & 0xf0 != 0xe0)) {
                fwrite(output, 512, 1, buffer);
                fread(buffer, 512, 1, input);
        }
    }
}