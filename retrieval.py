"""Small, readable retrieval experiment. No network or downloaded models required."""
import math
import re
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer


def tokenize(text):
    """Use exactly the same lowercased word tokens for both retrieval methods."""
    return re.findall(r"[a-z]+", text.lower())


class RetrievalExperiment:
    def __init__(self, documents):
        if not documents or any(not tokenize(text) for text in documents.values()):
            raise ValueError("Provide a nonempty collection with nonempty documents.")
        self.documents = documents
        self.document_ids = sorted(documents)
        self.counts = {}
        self.lengths = {}
        self.collection_counts = Counter()
        for document_id in self.document_ids:
            counts = Counter(tokenize(documents[document_id]))
            self.counts[document_id] = counts
            self.lengths[document_id] = sum(counts.values())
            self.collection_counts.update(counts)
        self.collection_length = sum(self.lengths.values())
        self.average_document_length = (
            self.collection_length / len(self.document_ids)
        )
        self.vectorizer = TfidfVectorizer(
            tokenizer=tokenize, token_pattern=None, lowercase=False,
            norm="l2", smooth_idf=True, sublinear_tf=False,
        )
        texts = [documents[document_id] for document_id in self.document_ids]
        self.tfidf_matrix = self.vectorizer.fit_transform(texts)

    def prepare_query(self, query):
        tokens = tokenize(query)
        known = [term for term in tokens if term in self.collection_counts]
        unknown = sorted(set(tokens) - set(known))
        return known, unknown

    def term_probability(self, term, document_id, method="dirichlet", mu=20, background_weight=0.2):
        count = self.counts[document_id][term]
        length = self.lengths[document_id]
        collection_probability = self.collection_counts[term] / self.collection_length
        if method == "mle":
            return count / length
        if method == "dirichlet":
            if mu <= 0:
                raise ValueError("mu must be positive.")
            return (count + mu * collection_probability) / (length + mu)
        if method == "jm":
            if not 0 < background_weight < 1:
                raise ValueError("background_weight must be between 0 and 1.")
            return (1 - background_weight) * count / length + background_weight * collection_probability
        raise ValueError("Unknown language model method.")

    def bm25_term_score(self, term, document_id, k1=1.2, b=0.75):
        """Return one query term's BM25 contribution for a document."""
        if k1 < 0:
            raise ValueError("k1 must be zero or greater.")
        if not 0 <= b <= 1:
            raise ValueError("b must be between 0 and 1.")

        document_frequency = sum(
            1 for counts in self.counts.values() if counts[term] > 0
        )
        if document_frequency == 0:
            return 0.0

        document_count = self.counts[document_id][term]
        if document_count == 0:
            return 0.0

        document_length = self.lengths[document_id]
        length_factor = k1 * (
            1 - b + b * document_length / self.average_document_length
        )
        inverse_document_frequency = math.log(
            1 + (len(self.document_ids) - document_frequency + 0.5)
            / (document_frequency + 0.5)
        )
        saturated_term_frequency = (
            (k1 + 1) * document_count / (document_count + length_factor)
        )
        return inverse_document_frequency * saturated_term_frequency

    def rank(self, query, method="dirichlet", mu=20, background_weight=0.2,
             k1=1.2, b=0.75):
        known, unknown = self.prepare_query(query)
        # An all-OOV query has no evidence. Do not return an arbitrary ranking.
        if not known:
            return [], unknown
        if method == "tfidf":
            query_vector = self.vectorizer.transform([" ".join(known)])
            scores = (self.tfidf_matrix @ query_vector.T).toarray().ravel().tolist()
        elif method == "bm25":
            query_counts = Counter(known)
            scores = []
            for document_id in self.document_ids:
                score = 0.0
                for term, frequency in query_counts.items():
                    score += frequency * self.bm25_term_score(
                        term, document_id, k1=k1, b=b
                    )
                scores.append(score)
        else:
            query_counts = Counter(known)
            scores = []
            for document_id in self.document_ids:
                score = 0.0
                for term, frequency in query_counts.items():
                    probability = self.term_probability(term, document_id, method, mu, background_weight)
                    if probability == 0:
                        score = -math.inf
                        break
                    score += frequency * math.log(probability)
                scores.append(score)
        ranking = list(zip(self.document_ids, scores))
        ranking.sort(key=lambda item: (-item[1], item[0]))
        return ranking, unknown


def evaluate(ranking, relevant, k=3):
    relevant = set(relevant)
    if not relevant:
        raise ValueError("Evaluation requires at least one relevant document.")
    hits = 0
    average_precision = 0.0
    top_hits = 0
    for rank, (document_id, _) in enumerate(ranking, start=1):
        if document_id in relevant:
            hits += 1
            average_precision += hits / rank
            if rank <= k:
                top_hits += 1
    return {"P@3": top_hits / k, "AP": average_precision / len(relevant)}
