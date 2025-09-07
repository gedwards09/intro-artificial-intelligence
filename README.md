# Introduction to Artificial Intelligence - Class Projects

This repository contains my projects for the Introduction to Artificial Intelligence course. Each project explores different concepts and algorithms discussed in the class.

## Projects

This repository will be updated with new projects as they are completed throughout the semester.

### Project 1: Text Analysis with Markov Chains

This project, based on the `rush.txt` movie script, explores two different probabilistic models for text analysis:

1.  **Markov Chain (Bigram Model):** A character-level model is built to understand and simulate language patterns. This includes calculating unigram and bigram probabilities and generating new text based on the learned transitions.
2.  **Naive Bayes Classifier:** This part of the project (also in the notebook) likely involves training a classifier on the text data, although the specifics are contained within the notebook.

*   **Key Files & Components:**
    *   `A1-Markov_Chain_and_Naive_Bayes.ipynb`: A Jupyter Notebook that walks through the creation, training, and analysis of the models. It includes data loading, probability calculations, and visualizations like unigram bar charts and bigram heatmaps.
    *   `DocumentMarkovChainModel.py`: The core Python class that encapsulates the logic for the Markov Chain model.
    *   `TokenProbabilityArray.py`: A utility class for converting counting statistics into cumulative probability distributions, which is essential for sampling and generating new text from the model.
    *   `TokenAlphabet.py`: Defines the character set (the "alphabet") used by the models.
    *   `rush.txt`: The raw text data from the movie script "Rush," used to train the models.

---
*This README will be updated as more projects are added.*