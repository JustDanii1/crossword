# Crossword

This project is part of Harvard's CS50's Introduction to Artificial Intelligence with Python. It focuses on using artificial intelligence to generate crossword puzzles from a given grid structure and a list of words.

## Overview

The program solves crossword puzzles by assigning words to horizontal and vertical slots while satisfying the constraints of the puzzle.

It uses a Constraint Satisfaction Problem (CSP) model to find a valid solution.

## How It Works

The project uses several algorithms to solve the crossword:

- **Node Consistency:** Ensures that each word matches the length of its slot.
- **Arc Consistency (AC-3):** Removes words that conflict with words in overlapping slots.
- **Backtracking Search:** Tries different word assignments until it finds a valid solution.
- **Minimum Remaining Values (MRV):** Selects the variable with the fewest possible values.
- **Degree Heuristic:** Helps choose variables that constrain the largest number of other variables.
- **Least Constraining Value (LCV):** Prioritizes words that eliminate the fewest options for neighboring variables.

## Files

- `crossword.py` — Defines the crossword structure, variables, and overlapping positions.
- `generate.py` — Implements the algorithms used to generate and solve crossword puzzles.
- `data/` — Contains example crossword structures and word lists.

## Requirements

- Python 3
- Pillow (optional, for saving crossword puzzles as images)

Install Pillow with:

```bash
pip install Pillow
```

## How to Run

Run the program with a crossword structure and a word list:

```bash
python generate.py data/structure1.txt data/words1.txt
```

To save the generated crossword as an image:

```bash
python generate.py data/structure1.txt data/words1.txt output.png
```

You can use different structure and word files from the `data/` directory.

## About

This project demonstrates how constraint satisfaction, search algorithms, and heuristics can be used to solve problems with multiple constraints.

Course: CS50's Introduction to Artificial Intelligence with Python  
Project: Crossword
