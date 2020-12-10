#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);
int getCandidateIndex(string candidateName);
void print_2D_array(int array[MAX][MAX]);
void print_locked(bool array[MAX][MAX]);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
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
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // 1. validate the vote
    for (int index = 0; index < MAX; index ++)
    {
        int candidateIndex = getCandidateIndex(name);
        if (candidateIndex == -1)
        {
            return false;
        }
        if (candidates[index])
        {
            ranks[rank] = candidateIndex;
        }
    }
    return true;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // ["Alice", "Bob", "Charlie"]
    for (int index = 0; index < candidate_count; index ++)
    {
        // Get the most prefered candidate and its index
        int topCandidateIndex = ranks[index];
        // Loop through all other candidates
        for (int preferIndex = index + 1; preferIndex < candidate_count; preferIndex ++)
        {
            // Locate other candidates' index for preferences updates
            int preferCandidateIndex = ranks[preferIndex];
            preferences[topCandidateIndex][preferCandidateIndex] += 1;
        }
    }
    // print_2D_array(preferences);
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // Loop through all candidates to create pairs
    for (int candidate = 0; candidate < candidate_count; candidate ++)
    {
        for (int pairCandidate = candidate + 1; pairCandidate < candidate_count; pairCandidate ++)
        {
            // Dont add pairs when preferences are tied
            if (preferences[candidate][pairCandidate] != preferences[pairCandidate][candidate])
            {
                // Initialize a new pair, and incrementing the pair_count by 1
                pair newPair;
                pair_count += 1;
                // Compare preferences matrix to find out the winner among the two
                if (preferences[candidate][pairCandidate] > preferences[pairCandidate][candidate])
                {
                    newPair.winner = candidate;
                    newPair.loser = pairCandidate;
                }
                else if (preferences[candidate][pairCandidate] < preferences[pairCandidate][candidate])
                {
                    newPair.loser = candidate;
                    newPair.winner = pairCandidate;
                }
                // Find an empty storeage space for the new pair
                for (int pairIndex = 0; pairIndex < pair_count; pairIndex ++)
                {
                    if (pairs[pairIndex].winner == 0 && pairs[pairIndex].loser == 0)
                    {
                        pairs[pairIndex] = newPair;
                        // printf("Pairs %i index is now a newPair (%i -> %i)\n", pairIndex, newPair.winner, newPair.loser);
                        break;
                    }
                }
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    for (int pairIndex = 0; pairIndex < pair_count; pairIndex ++)
    {
        // Record current pair strength and index
        int strongestIndex = pairIndex;
        pair currentPair = pairs[pairIndex];
        int strongest = preferences[currentPair.winner][currentPair.loser];
        // Loop through the pairs array to check for a pair even stronger
        for (int nextPairIndex = pairIndex + 1; nextPairIndex < pair_count; nextPairIndex ++)
        {
            pair nextPair = pairs[nextPairIndex];
            if (preferences[nextPair.winner][nextPair.loser] > strongest)
            {
                strongest = preferences[nextPair.winner][nextPair.loser];
                strongestIndex = nextPairIndex;
            }
        }
        // Swap current pair with the strongest pair (if needed)
        if (strongestIndex != pairIndex)
        {
            pairs[pairIndex] = pairs[strongestIndex];
            pairs[strongestIndex] = currentPair;
            // printf("Pair %i(%i) swaped with pair %i(%i)\n", pairIndex, preferences[currentPair.winner][currentPair.loser], strongestIndex, strongest);
        }
    }
    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // Avoid true been displayed on all three columns
    int cycles[candidate_count];
    memset(cycles, 0, candidate_count * sizeof(int));

    for (int pair_index = 0; pair_index < pair_count; pair_index ++)
    {
        pair currentPair = pairs[pair_index];
        // check if there is a cycle, only lock the edge when no cycle will be created
        int count = 0;
        for (int index = 0; index < candidate_count; index++)
        {
            count += cycles[index];
        }
        // all candidate can win another candidate if this pair been added, which means a cycle will be created
        if ((count != candidate_count - 1) || (count == candidate_count - 1 && cycles[currentPair.loser] == 1))
        {
            locked[currentPair.winner][currentPair.loser] = true;
            cycles[currentPair.loser] = 1;
        }
    }
    // print_locked(locked);
    return;
}

// Print the winner of the election
void print_winner(void)
{
    int largest = 0;
    int largestIndex = 0;
    for (int index = 0; index < candidate_count; index ++)
    {
        int count = 0;
        for (int otherCandidate = 0; otherCandidate < candidate_count; otherCandidate++)
        {
            if (locked[index][otherCandidate] == true)
            {
                count += 1;
            }
        }
        // if a candidate wins all other candidates
        if (count == candidate_count - 1)
        {
            printf("%s\n", candidates[index]);
            return;
        }
        // if some candidates are tied, get the candidate with the largest wins
        else
        {
            if (count > largest)
            {
                largest = count;
                largestIndex = index;
            }
        }
    }
    printf("%s\n", candidates[largestIndex]);
    return;
}

int getCandidateIndex(string candidateName)
{
    for (int index = 0; index < candidate_count; index ++)
    {
        if (strcmp(candidates[index], candidateName) == 0)
        {
            return index;
        }
    }
    return -1;
}

void print_2D_array(int array[MAX][MAX])
{
    for (int i = 0; i < MAX; i ++)
    {
        if (array[i])
        {
            for(int j = 0; j < MAX; j++) {
                if (array[j])
                {
                    printf("%d ", array[i][j]);
                }
            }
            printf("\n");
        }
    }
}

void print_locked(bool array[MAX][MAX])
{
    for (int i = 0; i < MAX; i ++)
    {
        if (array[i])
        {
            for(int j = 0; j < MAX; j++) {
                if (array[j])
                {
                    printf("%s ", array[i][j] ? "true " : "false");
                }
            }
            printf("\n");
        }
    }
}