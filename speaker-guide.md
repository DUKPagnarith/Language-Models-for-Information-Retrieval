# Speaker guide

Hello everyone. Please use this guide to prepare together. Each member should understand the full experiment, even if we divide the speaking parts.

## Timing

| Slides | Section | Time |
|---|---|---:|
| 1–3 | Introduction and problem statement | 2 minutes |
| 4–5 | Background and Lecture 2 connection | 2 minutes |
| 6–10 | Methodology | 4 minutes |
| 11–15 | Experiment and results | 4 minutes |
| 16–17 | Limitations and system example | 2 minutes |
| 18 | Conclusion and future work | 1 minute |
| 19 | References, kept visible for questions | No separate speaking time |

The total planned speaking time is 15 minutes, followed by about 5 minutes of questions. Press **S** in the HTML presentation for the full notes. Each slide has its own suggested timing.

## Suggested speaking parts

For a team of four, one person can cover slides 1–5, one slides 6–10, one slides 11–15, and one slides 16–18. Adjust this to your actual team size. Every member should present a part, as requested in the assignment. Add actual member names to the Quarto author field before your final submission.

## What to understand before presenting

- Build the counts in the three-document example by hand. The collection has 14 tokens. The probability product for document C is about 0.018267 and its natural log is about −4.003.
- Explain why a missing term makes MLE zero and why logs alone do not fix it.
- Explain the difference between a document-level unseen word and a word absent from the whole collection.
- Read the top results for all five queries in the notebook.
- Explain MAP and Recall@3 using the declared relevance labels.
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

It is an illustrative value for documents averaging about 16 tokens. Our sensitivity table shows stable MAP and Recall@3 over the tested values. This tiny example does not establish the best parameter for other collections.

**How were the relevance labels chosen?**

We wrote binary judgments based on each query's intended information need before comparing methods. They are teaching judgments. Q1 includes general language modeling, query likelihood, bigrams and perplexity. Q3 includes both the crawler description and the web-page indexing description. A real study needs independent judged queries.

**Did query likelihood beat TF-IDF?**

It improved the first relevant rank for Q5 and tied on the other four queries. Both smoothed models and TF-IDF have mean Recall@3 of 0.95. We cannot generalize from five handwritten queries.

**Why is MLE recall only 0.50?**

Many documents tie at zero probability. We break ties by document ID, which can push relevant documents below rank 3. The metric illustrates an estimation failure and arbitrary ordering in the tied tail.

**Does smoothing solve vocabulary mismatch?**

No. In `car coverage`, D13 contains coverage, so partial evidence helps it rank first. In `car protection`, protection is unknown and dropped. The model then favors car parking. It has not learned the relation between car and automobile.

**What do unknown terms do?**

We report and ignore terms absent from the collection. A partly unknown query uses the remaining terms. If all terms are unknown, we return no ranking. Other applications may use a different declared policy.

**Does lower perplexity mean better retrieval?**

Not necessarily. Perplexity measures probability on held-out text. Retrieval needs relevance metrics such as MAP, MRR and Recall@3.

**Where is this used?**

Indri is a documented research retrieval system using language modeling with Dirichlet smoothing. Its documented default mu of 2500 is not automatically suitable for our small collection.

**What would we improve next?**

Use a larger judged benchmark, tune on development queries, evaluate on a separate test set, compare BM25, and try expansion or dense retrieval for vocabulary mismatch.

## Before submission

Replace the group author line with the team members. Rehearse once with a timer. Submit the PDF and executed notebook, and keep the Quarto source for editing. If you change the collection, rerun the notebook and update the affected slide tables and explanations.
