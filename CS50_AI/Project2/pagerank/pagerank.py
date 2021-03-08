import os
import random
import re
import sys
import math

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    # print(corpus)
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        # Only check html files
        if not filename.endswith(".html"):
            continue
        # Open and read html page
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            # Get all links 
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            # Remove the page itself if it links to itself
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # List of pages this page links to
    link_to = corpus[page]
    # Initialize a probability distribution for all pages
    model = {
        page: 0 for page in corpus
    }
    # Distributing damping factor evenly (links)
    # Treat page with no links to other pages as having links to all pages
    if len(corpus[page]) == 0:
        links_p = damping_factor / len(corpus)
    else:
        links_p = damping_factor / len(corpus[page])
    for link in link_to:
        model[link] += links_p
    # Distributing damping factor evenly (all pages)
    all_p = (1 - damping_factor) / len(corpus)
    for link in corpus:
        model[link] += all_p
    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Create a page rank calculator
    ranks = {
        page: 0 for page in corpus
    }
    # First start at a random page
    start = random.choice(list(corpus.keys()))
    # Keep samplping until we get expected #samples
    while n > 0:
        model = transition_model(corpus, start, damping_factor)
        # print(f"transition model is: {model}")
        for page in model:
            # 1. Updating the cumulative probability
            ranks[page] += model[page]
        # Choose the next start page
        # Make a probability & page pair set
        population, weights = zip(*model.items())
        start = random.choices(population, weights=weights, k=1)[0]
        # Decrease the #samples
        n -= 1
    # Normalize the probability when cumulative probability been calculated
    factor = 1 / sum(ranks.values())
    for page in ranks:
        ranks[page] = ranks[page] * factor
    # Return the pagerank calculated after normalization
    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Total number of pages in corpus
    N = len(corpus)
    # Create a page rank calculator (assuming everypage has an equal probability)
    ranks = {
        page: 1 / N for page in corpus
    }
    # Iterate through all pages, sum the probability up
    threshold = 0.001
    repeat = True
    temp_rank = {}
    # Stop when probability converges
    while repeat:
        # PR(p) = (1-d)/N + d*SUM(PR(i)/NumLinks(i))    
        for page_p in corpus:
            # First part, chose a page at random and ended up on page p
            p_1 = (1 - damping_factor) / N
            # Second part, the suffer followed a link from a page i to page p
            p_2 = 0
            # All links pointing to the current page
            for page_i in corpus:
                # Found a page i links to page p
                if page_p in corpus[page_i]:
                    p_2 += ranks[page_i] / len(corpus[page_i])
                # Treat pages with no links as pages having links to every page
                elif not corpus[page_i]:
                    p_2 += ranks[page_i] / len(corpus)
            # Pagerank probability
            probability = p_1 + p_2 * damping_factor
            # Temperarely storing a new probability
            temp_rank[page_p] = probability

        # Stop repeating when the probability of all pages been calculated
        repeat = False

        # Test if any page has a probability change more than the threshold
        for page in temp_rank:
            if not math.isclose(temp_rank[page], ranks[page], abs_tol=threshold):
                # Update the result ranks
                ranks[page] = temp_rank[page]
                repeat = True
    return ranks


if __name__ == "__main__":
    main()
