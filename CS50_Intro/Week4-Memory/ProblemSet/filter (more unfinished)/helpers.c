#include "helpers.h"
#include <math.h>
#include <stdio.h>

RGBTRIPLE boxAverage(int x_start, int x_end, int y_start, int y_end, int width, RGBTRIPLE (*image)[width]);

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
    int x_start, x_end, y_start, y_end;
    // Loop through every row in the picture
    for (int row = 0; row < height; row ++)
    {
        // Loop through every column to get every pixel
        for (int column = 0; column < width; column ++)
        {
            // Create a possible box blur value
            // Top side
            if (row == 0)
            {
                x_start = 0;
                x_end = 2;
            }
            // Bottom side
            else if (row == height - 1)
            {
                x_start = row - 1;
                x_end = height;
            }
            // Middle row
            else
            {
                x_start = row - 1;
                x_end = row + 2;
            }
            // Left edge
            if (column == 0)
            {
                y_start = 0;
                y_end = 2;
            }
            // Right edge
            else if (column == width - 1)
            {
                y_start = column - 1;
                y_end = width;
            }
            // Middle column
            else
            {
                y_start = column - 1;
                y_end = column + 2;
            }
            image[row][column] = boxAverage(x_start, x_end, y_start, y_end, width, image);
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}

RGBTRIPLE boxAverage(int x_start, int x_end, int y_start, int y_end, int width, RGBTRIPLE (*image)[width])
{
    // RGBTRIPLE image = *imagePointer;
    float resultRed = 0.0;
    float resultBlue = 0.0;
    float resultGreen = 0.0;
    for (int row = x_start; row < x_end; row ++)
    {
        for (int column = y_start; column < y_end; column ++)
        {
            resultRed += image[row][column].rgbtRed;
            resultBlue += image[row][column].rgbtBlue;
            resultGreen += image[row][column].rgbtGreen;
        }
    }
    int area = (x_end - x_start) * (y_end - y_start);
    // If area is not 9, means the center of the blur box is in on the edge
    // if (area != 9)
    // {
    //     printf("Area on edge is: %i (height: %i, width: %i) \n", area, (x_end - x_start), (y_end - y_start));
    // }

    RGBTRIPLE result;
    result.rgbtRed = (int) resultRed / area;
    result.rgbtGreen = (int) resultGreen / area;
    result.rgbtBlue = (int) resultBlue / area;
    return result;
}