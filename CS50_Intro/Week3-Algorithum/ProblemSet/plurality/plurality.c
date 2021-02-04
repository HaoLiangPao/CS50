#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    // 1. find candidate with the given name
    for (int index = 0; index < MAX; index ++)
    {
        // 2. return invalid message if name is not found in the candidates array
        if (candidates[index].name == NULL)
        {
            return false;
        }
        // 2. when candidate is found, increment the vote number by 1
        else if (strcmp(candidates[index].name, name) == 0)
        {
            candidates[index].votes += 1;
            return true;
        }
    }
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    int biggest = 0;
    string winners[MAX];
    // 1. loop through the whole candidate array, find the one with the biggest number of votes
    for (int index = 1; index < MAX; index ++)
    {
        if (candidates[index].votes > candidates[biggest].votes)
        {
            biggest = index;
        }
    }
    // 2. loop through the array again to find if there is a tie
    for (int index = 0; index < MAX; index ++)
    {
        if (candidates[index].votes == candidates[biggest].votes)
        {
            printf("%s\n", candidates[index].name);
        }
    }
}

