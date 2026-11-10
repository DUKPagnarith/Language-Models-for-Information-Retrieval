# Speaker guide

Hello everyone. Please use this guide to prepare together. Each member should understand the full experiment, even if we divide the speaking parts.

## Timing

| Slides | Section | Time |
|---|---|---:|
| 1–3 | Introduction and objective | 2 minutes |
| 4–6 | Lecture 2 and query likelihood | 3 minutes |
| 7–10 | TF-IDF, BM25, and worked example | 4 minutes |
| 11–14 | Experiment, evaluation, and results | 5 minutes |
| 15 | Conclusion and limitations | 1 minute |
| 16 | References, kept visible for questions | No separate speaking time |

The total planned speaking time is 15 minutes, followed by about 5 minutes of questions. Press **S** in the HTML presentation for the full notes. Each slide has its own suggested timing.

## Suggested speaking parts

For a team of four, one person can cover slides 1–4, one slides 5–8, one slides 9–12, and one slides 13–15. Keep slide 16 visible for questions. Every member should present a part, as requested in the assignment. The title slide lists the four Team 4 members and their student IDs.

## What to understand before presenting

- Build the counts in the three-document example by hand. The collection has 14 tokens. The probability product for document C is about 0.018267 and its natural log is about −4.003.
- Explain why a missing term makes MLE zero and why logs alone do not fix it.
- Explain the difference between a document-level unseen word and a word absent from the whole collection.
- Explain how BM25 combines rare words, saturated term frequency, and document-length normalization.
- Read the top results for the five queries in the notebook.
- Explain Precision@3 and MAP using the declared relevance labels.
- Run `car protection` and explain why the insurance example fails.

## Questions we may receive

**Why do we use unigrams?**

They need fewer counts and give a simple connection between bag-of-words and query probabilities. Bigrams retain local word order but are sparser. Unigrams are a choice for this experiment.

**Why do we use log probabilities?**

Logarithms preserve ranking and turn a product into a sum, which avoids numerical underflow. A zero probability still gives negative infinity, so we smooth first.

**How is Dirichlet different from JM?**

Dirichlet's effective background weight is mu divided by document length plus mu. Shorter documents get a larger background contribution at the same mu. JM uses a fixed background weight lambda. We define lambda as the background contribution throughout.

**Why not use the lecture's add-one smoothing?**

Add-one assigns the same pseudo-count to every vocabulary term. Collection smoothing uses the observed background distribution. We include add-one in the explanation to connect the methods, but do not report it as an experimental condition.

**Why mu 20?**

It is an illustrative value for documents averaging about 16 tokens. Our sensitivity table shows stable Precision@3 and MAP over the tested values. This tiny example does not establish the best parameter for other collections.

**How were the relevance labels chosen?**

We wrote binary judgments based on each query's intended information need before comparing methods. They are teaching judgments. Q1 includes general language modeling, query likelihood, bigrams and perplexity. Q3 includes both the crawler description and the web-page indexing description. A real study needs independent judged queries.

**Did query likelihood beat TF-IDF?**

Dirichlet has MAP 1.00, while TF-IDF and BM25 have MAP 0.90; all three have Precision@3 of 0.60. Dirichlet ranks the relevant insurance document first for Q5. We cannot generalize from five handwritten queries.

**Why is MLE recall only 0.50?**

Many documents tie at zero probability. We break ties by document ID, which can push relevant documents below rank 3. The metric illustrates an estimation failure and arbitrary ordering in the tied tail.

**Does smoothing solve vocabulary mismatch?**

No. In `car coverage`, D13 contains coverage, so partial evidence helps it rank first. In `car protection`, protection is unknown and dropped. The model then favors car parking. It has not learned the relation between car and automobile.

**What do unknown terms do?**

We report and ignore terms absent from the collection. A partly unknown query uses the remaining terms. If all terms are unknown, we return no ranking. Other applications may use a different declared policy.

**Does lower perplexity mean better retrieval?**

Not necessarily. Perplexity measures probability on held-out text. Retrieval needs relevance measures such as Precision@3 and MAP.

**Where is this used?**

Indri is a documented research retrieval system using language modeling with Dirichlet smoothing. Its documented default mu of 2500 is not automatically suitable for our small collection.

**What would we improve next?**

Use a larger set of independently judged queries, tune on development queries, evaluate on a separate test set, and try expansion or dense retrieval for vocabulary mismatch.

## Before submission

Verify the team names and student IDs on the title slide. Rehearse once with a timer. Submit the PDF and executed notebook, and keep the Quarto source for editing. If you change the collection, rerun the notebook and update the affected slide tables and explanations.
