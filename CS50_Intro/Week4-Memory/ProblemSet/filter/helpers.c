#include "helpers.h"
#include "math.h"

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

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop through every row in the picture
    for (int row = 0; row < height; row ++)
    {
        // Loop through every column to get every pixel
        for (int column = 0; column < width; column ++)
        {
            float sepiaRed = round(0.393 * image[row][column].rgbtRed + 0.769 * image[row][column].rgbtGreen + 0.189 * image[row][column].rgbtBlue);
            if (sepiaRed > 255) {
                sepiaRed = 255;
            }
            float sepiaGreen = round(0.349 * image[row][column].rgbtRed + 0.686 * image[row][column].rgbtGreen + 0.168 * image[row][column].rgbtBlue);
            if (sepiaGreen > 255) {
                sepiaGreen = 255;
            }
            float sepiaBlue = round(0.272 * image[row][column].rgbtRed + 0.534 * image[row][column].rgbtGreen + 0.131 * image[row][column].rgbtBlue);
            if (sepiaBlue > 255) {
                sepiaBlue = 255;
            }
            image[row][column].rgbtBlue = (int) sepiaBlue;
            image[row][column].rgbtRed = (int) sepiaRed;
            image[row][column].rgbtGreen = (int) sepiaGreen;
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
    RGBTRIPLE image_copy [height][width];
    for (int row = 0; row < height; row ++) {
        for (int column = 0; column < width; column ++) {
            image_copy[row][column].rgbtRed = image[row][column].rgbtRed;
            image_copy[row][column].rgbtBlue = image[row][column].rgbtBlue;
            image_copy[row][column].rgbtGreen = image[row][column].rgbtGreen;
        }
    }
    for (int row = 0; row < height; row ++) {
        for (int column = 0; column < width; column ++) {
            // Keep track of different color values
            float rgbRed = 0.0;
            float rgbGreen = 0.0;
            float rgbBlue = 0.0;
            // Perform a 3x3 box average
            int x_start = row - 1;
            int x_end = row + 2;
            int y_start = column - 1;
            int y_end = column + 2;
            float count = 0.0;
            // Calculating the sum of color values, keep the count as well
            for (int row_box = x_start; row_box < x_end; row_box ++) {
                for (int column_box = y_start; column_box < y_end; column_box ++) {
                    // Check image boundary and 3x3 box boundary
                    if ((row_box >= 0) & (row_box + 1 <= x_end & row_box + 1 <= height) & (column_box >= 0) & (column_box + 1 <= y_end & column_box + 1 <= width)) {
                        rgbRed += image_copy[row_box][column_box].rgbtRed;
                        rgbBlue += image_copy[row_box][column_box].rgbtBlue;
                        rgbGreen += image_copy[row_box][column_box].rgbtGreen;
                        count ++;
                    }
                }
            }
            // Update actual image with a rounded value
            image[row][column].rgbtRed = round (rgbRed / count);
            image[row][column].rgbtBlue = round (rgbBlue / count);
            image[row][column].rgbtGreen = round (rgbGreen / count);
        }
    }
    return;
}
