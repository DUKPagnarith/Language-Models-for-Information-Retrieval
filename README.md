# Language Models for Information Retrieval

This is our Topic 2 group discussion project for Information Web Retrieval and Analytics. It connects Lecture 2's bag-of-words, TF-IDF, and query-likelihood ideas with BM25 from Lecture 5.

Our main question: if each document has its own language model, which document is most likely to generate a given query?

![Presentation preview](assets/presentation-preview.png)

## Beginner learning guide

The current guide is the editable Quarto source at [learning/learning-guide.qmd](learning/learning-guide.qmd). It explains preprocessing, word probabilities, query likelihood, smoothing, TF-IDF, BM25, and the two evaluation measures used in the presentation. It also includes worked examples, practice questions, answers, and a glossary.

Render the current PDF with `quarto render learning/learning-guide.qmd`. The checked-in [learning guide PDF](learning/learning-guide.pdf) is an earlier export and does not include the latest BM25 material.

## Team 4

| Member | Student ID |
|---|---|
| Duk Pagnarith | e20220184 |
| Leng Devid | e20220888 |
| Hoeurn Sreyka | e20220699 |
| Sou Pichchomrong | e20221074 |

## Files

- `presentation.qmd`: editable Quarto Reveal.js presentation, with speaker notes and 15 minutes of suggested timing.
- `presentation.css`: content layout, chapter header, and Team 4 footer.
- `presentation-frame.js`: per-slide labels and the four members with student IDs.
- `_extensions/clean/`: the bundled upstream theme and its license.
- `presentation.html`: rendered presentation. After editing `presentation.qmd`, refresh it with Quarto. Open it in a browser; press **S** for speaker notes and **F** for full screen.
- `presentation.pdf`: slide submission copy from an earlier render; refresh the Quarto source before submitting it.
- `language_models_ir.ipynb`: explanation, experiment, selected evaluation measures, results, and defense questions. It uses the shared implementation in `retrieval.py`.
- `data/collection.json`: 15 teaching documents, 5 queries, and declared binary relevance labels.
- `retrieval.py`: reusable implementation matching the notebook.
- `app.py`: interactive Streamlit demo for exploring the words in each document, entering queries, and comparing retrieval rankings, including BM25.
- `results/`: full rankings, per-query metrics, summary, and smoothing sensitivity.
- `speaker-guide.md`: timing, suggested division of speaking parts, and defense practice.

## Run the notebook

Use Python 3.10 or later. We checked the experiment with Python 3.12.

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter lab language_models_ir.ipynb
```

Run all notebook cells from top to bottom. No API key or data download is needed after installing the packages. The notebook creates the selected-metric results in the working directory.

## Run the interactive demo

Install the project packages as described above, then start the app from the project folder:

```sh
python -m streamlit run app.py
```

The notebook reports two evaluation measures: Precision@3 and MAP. The app displays each document and its word counts, lets you inspect collection-wide word frequencies, and ranks queries using TF-IDF, MLE, Jelinek–Mercer, Dirichlet, or BM25. Smoothing and BM25 parameters can be adjusted on screen.

## Presentation theme

The slides use Grant McDermott's [Quarto Reveal.js Clean theme](https://github.com/grantmcdermott/quarto-revealjs-clean), version 1.5.0. The extension is bundled in `_extensions/clean`, so cloning this repository includes the theme. Its MIT license and upstream commit are retained there.

The presentation selects `format: clean-revealjs`. The theme supplies Roboto typography, a white background, blue accents, and navigation styling. `presentation.css` adds content sizing and the top and bottom rules. Each slide shows its chapter above the top rule, with Team 4 and a page number below the bottom rule. `presentation-frame.js` adds these labels and the title-slide roster. The revised presentation explains query likelihood, TF-IDF, and BM25, then evaluates the three methods using Precision@3 and MAP.

## Render the presentation

Install [Quarto](https://quarto.org/docs/get-started/), then run:

```sh
quarto render presentation.qmd
```

Open `presentation.html`. Equations use KaTeX. To export an updated PDF, open the HTML presentation with `?print-pdf` added before any `#` fragment, then use the browser's **Print → Save as PDF**, with landscape orientation, background graphics enabled, and headers/footers disabled.

The slide result table is paired with `results/summary.csv`. If you change data or parameters, rerun the notebook and update the slide result table and discussion.

## What our experiment shows

On five handwritten queries, TF-IDF and BM25 each have MAP 0.900, while Dirichlet query likelihood has MAP 1.000. All three have mean Precision@3 of 0.600. The difference comes from one insurance query. A diagnostic query still retrieves parking instead of insurance, which shows that smoothing does not solve synonym matching.

These are teaching results, not benchmark evidence. We do not claim that query likelihood is generally better than TF-IDF or BM25. Labels are our own judgments, parameters are illustrative, and the same queries are used in the sensitivity analysis.

## References

The notebook and final slide contain the full references. Main readings are the supplied Lectures 2 and 5, Manning et al. (2008), Ponte and Croft (1998), Zhai and Lafferty (2001), and Robertson and Zaragoza (2009). The supplied course PDFs are not redistributed here.
