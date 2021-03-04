import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # print(f"people is : {people}")

    # Keep track of gene and trait probabilities for each person (default probability)
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # print(f"probabilities is : {probabilities}")

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            # If the person's trait is undertermined, return True
            (people[person]["trait"] is not None and
            # If the evidence and the sampling is conflict to each other (sample a person to have trait where he/she actually does not)
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        # Skip this sampling since it violates the evidence we are provided
        if fails_evidence:
            continue

        # Start calculating the joint-probability when the sampling is possible
        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # Default joint probability
    joint_p = 1
    # Start with people with no genes
    no_genes = (set(people) - one_gene - two_genes)
    for person in no_genes:
        # If a person has no parents recorded:
        if people[person]["father"] is None and people[person]["mother"] is None:
            # Estimate the gene combination based on PROBS
            p_no_gene = PROBS["gene"][0]
        # A person has parents whose genes are recorded
        else:
            # We need to calculate the probability of this person with no genes
            p_no_gene = 1
            # A set of parents
            parents = [people[person]["father"], people[person]["mother"]]
            # Get the probability of having gene passed from parents
            for parent in parents:
                # check #gene the parent has
                if parent in no_genes:
                    p_no_gene *= 0.99
                elif parent in one_gene:
                    # 0.5 * (1 - 0.01) + 0.5 * 0.01
                    p_no_gene *= 0.5
                elif parent in two_genes:
                    p_no_gene *= 0.01
        
        # print(f"p_no_gene is: {p_no_gene}")
        
        # If he/she has trait
        if person in have_trait:
            p_no_gene_trait = PROBS["trait"][0][True]
        else:
            p_no_gene_trait = PROBS["trait"][0][False]

        # print(p_no_gene * p_no_gene_trait)
        # Adding the probability of he/she having no gene and (not)having a trait to the result
        joint_p *= p_no_gene * p_no_gene_trait

    # Loop through people with one genes
    for person in one_gene:
        # If a person has no parents recorded:
        if people[person]["father"] is None and people[person]["mother"] is None:
            # Estimate the gene combination based on PROBS
            p_one_gene = PROBS["gene"][1]
        # A person has parents whose genes are recorded
        else:
            # probability of having gene passed from father, and the probability of having it from mother
            p_one_gene_cases = {"father": 1, "mother": 1}
            # A set of parents
            parents = [people[person]["father"], people[person]["mother"]]
            
            # Go through both the mother, father cases
            for case in p_one_gene_cases:
                other_case = "mother" if case == "father" else "father"
                # Father/Mother give the gene
                gene_source = people[person][case]
                not_gene_source = people[person][other_case]
                # This parent donate the gene
                if gene_source in no_genes:
                    p_one_gene_cases[case] *= 0.01
                elif gene_source in one_gene:
                    p_one_gene_cases[case] *= 0.5
                elif gene_source in two_genes:
                    p_one_gene_cases[case] *= 0.99
                # The other parent should not donate a gene
                if not_gene_source in no_genes:
                    p_one_gene_cases[case] *= 0.99
                elif not_gene_source in one_gene:
                    p_one_gene_cases[case] *= 0.5
                elif not_gene_source in two_genes:
                    p_one_gene_cases[case] *= 0.01
            
            # print(p_one_gene_cases)
            p_one_gene = sum(p_one_gene_cases.values())
            # print(p_one_gene)

        # Probability of (not)having a trait
        p_one_gene_trait = (PROBS["trait"][1][True] if person in have_trait
                            else PROBS["trait"][1][False])
        # print(p_one_gene * p_one_gene_trait)
        # Upadating the joint probability result
        joint_p *= p_one_gene * p_one_gene_trait
    
    # Loop through people with two genes
    for person in two_genes:
        # If a person has no parents recorded:
        if people[person]["father"] is None and people[person]["mother"] is None:
            # Estimate the gene combination based on PROBS
            p_two_gene = PROBS["gene"][2]
        # A person has parents whose genes are recorded
        else:
            # We need to calculate the probability of this person with no genes
            p_two_gene = 1
            # A set of parents
            parents = [people[person]["father"], people[person]["mother"]]
            # Get the probability of having gene passed from parents
            for parent in parents:
                # check #gene the parent has
                if parent in no_genes:
                    p_two_gene *= 0.01
                elif parent in one_gene:
                    p_two_gene *= 0.5
                elif parent in two_genes:
                    p_two_gene *= 0.99
        # Probability of (not)having a trait
        p_two_gene_trait = (PROBS["trait"][2][True] if person in have_trait
                            else PROBS["trait"][2][False])
        # print(p_two_gene * p_two_gene_trait)
        # Upadating the joint probability result
        joint_p *= p_two_gene * p_two_gene_trait

    return joint_p


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # Set of people without a gene
    no_genes = (set(probabilities) - one_gene - two_genes)
    for person in no_genes:
        probabilities[person]['gene'][0] += p
        if person in have_trait:
            probabilities[person]['trait'][True] += p
        else:
            probabilities[person]['trait'][False] += p
    # One gene
    for person in one_gene:
        probabilities[person]['gene'][1] += p
        if person in have_trait:
            probabilities[person]['trait'][True] += p
        else:
            probabilities[person]['trait'][False] += p
    # Two gene
    for person in two_genes:
        probabilities[person]['gene'][2] += p
        if person in have_trait:
            probabilities[person]['trait'][True] += p
        else:
            probabilities[person]['trait'][False] += p        


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # There are two probability distributions
    # Normalize probabilities for each person
    for person in set(probabilities):
        # 1. trait: P(True) + P(False) == 1
        normalization_factor = 1 / sum(probabilities[person]['trait'].values())
        # Multiple each probability distribution with this factor
        for distribution in probabilities[person]['trait']:
            probabilities[person]['trait'][distribution] *= normalization_factor
        # 2. gene: P(0) + P(1) + P(2) == 1
        normalization_factor = 1 / sum(probabilities[person]['gene'].values())
        # Multiple each probability distribution with this factor
        for distribution in probabilities[person]['gene']:
            probabilities[person]['gene'][distribution] *= normalization_factor


if __name__ == "__main__":
    main()
