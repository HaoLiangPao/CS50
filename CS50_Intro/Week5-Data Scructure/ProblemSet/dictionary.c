// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];
FILE *dict;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO
    return 0;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    //open the dictionary
    dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        printf("Dictionary can not be opened.");
        return false;
    }

    // Load each word into the dictionary
    char word[LENGTH + 1];
    unsigned int hash_value = 0;

    // Not reaching the end of the dictionary
    while (fscanf(dict, "%s", word) != EOF)
    {
        printf("%s\n", word);
    }


    return false;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    return false;
}
