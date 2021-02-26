// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
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
        // Create a new node to be added
        node *new_node = malloc(sizeof(node));
        // When no empty memory exists
        if (new_node == NULL)
        {
            printf("No memory, failed to load the dictionary.\n");
            unload();
            return false;
        }
        // Create a hash value
        hash_value = hash(word);
        strcpy(new_node->word, word);
        // Insert the node at the beginning of the linked-list
        new_node->next = table[hash_value];
        table[hash_value] = new_node;
        printf("%s\n", word);
    }

    return true;
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
    // Remove all nodes stored in the hashtable
    for (int index = 0; index < N; index++)
    {
        // Get access to the head of each bucket
        node *head = table[index];
        while (head->next != NULL)
        {
            // Keep the address of the current node
            node *temp = head->next;
            head = temp->next;
            // Free the node we just accessed
            free(temp);
        }
    }
    return true;
}
