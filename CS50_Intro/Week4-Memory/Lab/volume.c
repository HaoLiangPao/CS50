// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    // 1. Copy header from input file to output file
    uint8_t header[HEADER_SIZE];
    // Read header from input wav file
    fread(header, 1, 44, input);
    // Write header to output wav file
    fwrite(header, 1, 44, output);

    // 2. Read samples from input file and write updated data to output file
    int16_t *buffer = malloc(sizeof(int16_t));
    // Read each sample from input wav file
    int result = fread(buffer, 2, 1, input);
    while (result)
    {
        // printf("buffer is: %i\n", *buffer);
        *buffer = *buffer * factor;
        // printf("buffer is: %i\n", *buffer);
        // Write modified sample to output wav file
        fwrite(buffer, 2, 1, output);
        // Read next sample
        result = fread(buffer, 2, 1, input);
    }

    free(buffer);


    // Close files
    fclose(input);
    fclose(output);
}
