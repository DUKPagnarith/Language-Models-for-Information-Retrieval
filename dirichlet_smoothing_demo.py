"""Reproduce the Dirichlet smoothing calculation from the presentation slide.

Run with: python3 dirichlet_smoothing_demo.py

The slide gives aggregate collection counts for the query words, rather than
the full collection text, so those counts are entered directly below.
"""

import math
import re
from collections import Counter


def tokenize(text):
    """Lowercase the text and keep alphabetic words."""
    return re.findall(r"[a-z]+", text.lower())


# Collection-wide statistics shown on the slide.
collection_length = 14
collection_counts = {
    "search": 2,
    "documents": 3,
}

# The candidate document and query shown on the slide.
document_text = "language models rank documents"
query_text = "search documents"
mu = 5

document_tokens = tokenize(document_text)
query_tokens = tokenize(query_text)
document_counts = Counter(document_tokens)
document_length = len(document_tokens)

print("Dirichlet smoothing demo")
print(f"Document: {document_text!r} ({document_length} words)")
print(f"Query:    {query_text!r}")
print(f"mu:       {mu}")
print(f"Collection length: {collection_length} words\n")

query_probability = 1.0
log_query_score = 0.0

for word in query_tokens:
    count_in_document = document_counts[word]
    count_in_collection = collection_counts[word]
    probability_in_collection = count_in_collection / collection_length

    # Combine the document count with collection-based background support.
    probability_in_document = (
        count_in_document + mu * probability_in_collection
    ) / (document_length + mu)

    query_probability *= probability_in_document
    log_query_score += math.log(probability_in_document)

    print(f"Word: {word}")
    print(f"  Count in document:       {count_in_document}")
    print(f"  Probability in collection: {count_in_collection}/{collection_length}"
          f" = {probability_in_collection:.4f}")
    print(f"  Smoothed probability:    {probability_in_document:.4f}\n")

print(f"P(query | document) = {query_probability:.4f}")
print(f"Log query score     = {log_query_score:.3f}")
print("A higher log query score (closer to zero) means a better match.")
