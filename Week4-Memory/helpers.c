#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop through every row in the picture
    for (int row = 0; row < height; row ++)
    {
        // Loop through every column to get every pixel
        for (int column = 0; column < width; column ++)
        {
            int red = image[row][column].rgbtRed;
            int green = image[row][column].rgbtGreen;
            int blue = image[row][column].rgbtBlue;
            float average = round(((float) red + green + blue) / 3);
            image[row][column].rgbtBlue = (int) average;
            image[row][column].rgbtRed = (int) average;
            image[row][column].rgbtGreen = (int) average;
        }
    }
    return;

}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop through every row in the picture
    for (int row = 0; row < height; row ++)
    {
        // Loop through every column to get every pixel
        for (int column = 0; column < width / 2; column ++)
        {
            RGBTRIPLE left = image[row][column];
            image[row][column] = image[row][width - 1 - column];
            image[row][width - 1 - column] = left;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}
