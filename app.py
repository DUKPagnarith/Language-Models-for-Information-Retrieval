"""Interactive, beginner-friendly information retrieval demo."""

import json
import math
from collections import Counter
from pathlib import Path

import pandas as pd
import streamlit as st

from retrieval import RetrievalExperiment, tokenize


PROJECT_FOLDER = Path(__file__).parent
COLLECTION_FILE = PROJECT_FOLDER / "data" / "collection.json"


@st.cache_data
def load_collection():
    """Load the small teaching corpus included with the project."""
    with COLLECTION_FILE.open(encoding="utf-8") as collection_file:
        return json.load(collection_file)


def make_word_count_table(word_counts):
    """Turn word counts into a table sorted from most common to least common."""
    rows = [
        {"Word": word, "Count": count}
        for word, count in word_counts.items()
    ]
    rows.sort(key=lambda row: (-row["Count"], row["Word"]))
    return pd.DataFrame(rows)


def make_result_details(experiment, document_id, query_words, method,
                        mu, background_weight):
    """Show how each known query word contributes for one document."""
    rows = []

    for word, query_count in Counter(query_words).items():
        document_count = experiment.counts[document_id][word]
        collection_count = experiment.collection_counts[word]
        collection_probability = (
            collection_count / experiment.collection_length
        )

        row = {
            "Query word": word,
            "Times in query": query_count,
            "Times in document": document_count,
            "Times in collection": collection_count,
            "Collection probability": round(collection_probability, 4),
        }

        if method != "tfidf":
            word_probability = experiment.term_probability(
                word,
                document_id,
                method=method,
                mu=mu,
                background_weight=background_weight,
            )
            row["Probability in document"] = round(word_probability, 4)
            if word_probability == 0:
                row["Log-score contribution"] = "-infinity"
            else:
                row["Log-score contribution"] = round(
                    query_count * math.log(word_probability), 4
                )

        rows.append(row)

    return pd.DataFrame(rows)


st.set_page_config(
    page_title="Search Ranking Learning Demo",
    page_icon="🔎",
    layout="wide",
)

st.title("Search Ranking: Learn by Trying")
st.write(
    "Explore the documents and their words, enter a query, and see how "
    "different retrieval methods rank the documents."
)

collection = load_collection()
documents = collection["documents"]
queries = collection.get("queries", [])
experiment = RetrievalExperiment(documents)

all_tokens = [
    word
    for text in documents.values()
    for word in tokenize(text)
]
collection_counts = Counter(all_tokens)

document_column, token_column, vocabulary_column = st.columns(3)
document_column.metric("Documents", len(documents))
token_column.metric("Word tokens", len(all_tokens))
vocabulary_column.metric("Different words", len(collection_counts))

st.header("1. Explore the collection")
st.caption(
    "Each row is one document. The word-count table shows how often each "
    "word appears in the selected document and in the whole collection."
)

document_rows = [
    {
        "Document": document_id,
        "Text": text,
        "Number of words": experiment.lengths[document_id],
    }
    for document_id, text in documents.items()
]
st.dataframe(
    pd.DataFrame(document_rows),
    hide_index=True,
    use_container_width=True,
)

left, right = st.columns([1, 1])
with left:
    selected_document = st.selectbox(
        "Choose a document to inspect",
        options=list(documents),
    )
    st.markdown(f"**{selected_document}:** {documents[selected_document]}")
    st.dataframe(
        make_word_count_table(experiment.counts[selected_document]),
        hide_index=True,
        use_container_width=True,
    )

with right:
    st.markdown("**Whole collection: word counts**")
    st.dataframe(
        make_word_count_table(collection_counts),
        hide_index=True,
        height=360,
        use_container_width=True,
    )

st.header("2. Search and compare ranking methods")

example_queries = [query["text"] for query in queries]
default_query = example_queries[0] if example_queries else "language model"
query_text = st.text_input(
    "Write a query",
    value=default_query,
    help="Try words such as: smoothing, crawler web pages, or car coverage.",
)

model_names = {
    "TF-IDF cosine similarity": "tfidf",
    "Maximum likelihood (MLE)": "mle",
    "Jelinek–Mercer smoothing": "jm",
    "Dirichlet smoothing": "dirichlet",
}
selected_model_name = st.selectbox(
    "Choose a ranking method",
    options=list(model_names),
)
selected_method = model_names[selected_model_name]

mu = 20
background_weight = 0.2
if selected_method == "dirichlet":
    mu = st.slider(
        "Dirichlet μ (mu): background support",
        min_value=1,
        max_value=100,
        value=20,
        help=(
            "A larger mu pulls each document's word probabilities closer "
            "to the whole collection's word probabilities."
        ),
    )
elif selected_method == "jm":
    background_weight = st.slider(
        "JM λ (lambda): collection weight",
        min_value=0.01,
        max_value=0.99,
        value=0.2,
        step=0.01,
        help=(
            "A larger lambda gives more influence to the whole collection; "
            "a smaller lambda gives more influence to the document."
        ),
    )

method_explanations = {
    "tfidf": (
        "TF-IDF gives more weight to useful, less common words. Cosine "
        "similarity compares the query and document word-weight vectors."
    ),
    "mle": (
        "MLE uses only the word frequencies inside each document. A missing "
        "query word gives that document a zero likelihood."
    ),
    "jm": (
        "Jelinek–Mercer mixes each document's word probabilities with the "
        "collection probabilities."
    ),
    "dirichlet": (
        "Dirichlet smoothing adds collection-based pseudo-count support to "
        "each document. The μ slider controls how much support is added."
    ),
}
st.info(method_explanations[selected_method])

known_words, unknown_words = experiment.prepare_query(query_text)
if not tokenize(query_text):
    st.info("Enter one or more words to search the collection.")
elif not known_words:
    st.warning(
        "None of the query words appear in this collection, so there is "
        "not enough evidence to rank the documents."
    )
else:
    ranking, _ = experiment.rank(
        query_text,
        method=selected_method,
        mu=mu,
        background_weight=background_weight,
    )

    st.write("**Words used from your query:** " + ", ".join(known_words))
    if unknown_words:
        st.caption(
            "Not found in the collection and left out of the score: "
            + ", ".join(unknown_words)
        )

    ranking_rows = [
        {
            "Rank": rank,
            "Document": document_id,
            "Score": score,
            "Text": documents[document_id],
        }
        for rank, (document_id, score) in enumerate(ranking, start=1)
    ]
    st.subheader("Ranked documents")
    st.caption(
        "For language models, a higher log score (closer to zero) is better. "
        "For TF-IDF, a higher cosine score is better."
    )
    st.dataframe(
        pd.DataFrame(ranking_rows),
        hide_index=True,
        use_container_width=True,
        column_config={
            "Score": st.column_config.NumberColumn(format="%.4f"),
        },
    )

    st.subheader("Why did each document get this score?")
    for rank, (document_id, score) in enumerate(ranking, start=1):
        with st.expander(f"Rank {rank}: {document_id} — score {score:.4f}"):
            st.write(documents[document_id])
            st.dataframe(
                make_result_details(
                    experiment,
                    document_id,
                    known_words,
                    selected_method,
                    mu,
                    background_weight,
                ),
                hide_index=True,
                use_container_width=True,
            )

st.caption(
    "This is a small teaching collection with 15 example documents. "
    "It is designed to explain ranking, not to represent a general-purpose "
    "search engine."
)
