# Programming and Tools for Artificial Intelligence

**Author:** Jack Hickey  
**Institution:** University of Galway  
**Module:** CT5148 

## Overview
This repository contains my continuous assessment portfolio for the Programming and Tools for AI module. It includes weekly Jupyter notebook lecture notes, Python problem set solutions, test suite executions, and R language boot camp exercises.

The primary goal of this repository is to document my problem-solving process, demonstrate clean software engineering practices, and serve as a revision tool for the final written exam.

## Repository Structure
The workspace is divided by week and technology:

* `week_01/` to `week_04/`, `W06/` to `week_10/`: Python 3 lecture notes (`.ipynb`), exercises (`.py`), and test suites.
* `assignment_01/`: Mid-semester portfolio submission (Weeks 1–4 exercises, self-check suite, and submission archive).
* `r_bootcamp/`: Self-paced R language materials and exercises.
* `utils/`: Shared Python functions and helper scripts imported across multiple weeks.

## Environment & Setup
To run the code in this repository locally:
1. Ensure Python 3.9.6 is installed.
2. Activate the local virtual environment: `source venv/bin/activate` (macOS).
3. Install dependencies: `pip install -r requirements.txt`.

## AI Usage & Feedback Log
In accordance with module policy, AI tools (LLMs) are used strictly for **feedback and refactoring** after a genuine first attempt is made. 

When AI is utilized to debug or suggest neater implementations, the prompt and the reasoning for accepting/rejecting the AI's suggestion are documented in the respective weekly notebook under the `## AI Feedback & Refactoring` header.

---

## Semester Index & Exam Prep

| Week | Topic | Core Concepts (Exam Prep) | Status |
| :--- | :--- | :--- | :--- |
| **Week 1** | [Intro & Python Basics](./week_01/) | Loops, Functions, Types | 🟢 Complete |
| **Week 2** | [Dictionaries & N-Grams](./week_02/) | Dictionaries, Tallying, Grouping, N-Gram Language Models, File I/O | 🟢 Complete  |
| **Week 3** | [Trees, Recursion & JSON](./week_03/) | Tree Traversal, Recursive Functions, Bill of Materials (BOM), JSON I/O | 🟢 Complete  |
| **Week 4** | [Hash Tables & Dict Internals](./week_04/) | Hash Functions, Buckets, Collisions, Python Data Model, Computational Complexity | 🟢 Complete |
| **Week 5** | [Review & Catch-up / Assignment 1](./assignment_01/) | Mid-semester consolidation, portfolio review & [Assignment 1](./assignment_01/) submission | 🟢 Complete |
| **Week 6** | [Graph Search & State Spaces](./W06/) | State Space Representation, BFS, DFS, Dijkstra's Algorithm, Priority Queues, Shortest Path | 🟢 Complete |
| **Week 7** | [Dynamic Programming & Sequence Alignment](./W07/) | Memoization vs Tabulation, Levenshtein Distance, Traceback, Dynamic Time Warping (DTW) | 🟢 Complete |
| **Week 8** | [NumPy, Vectorisation & Broadcasting](./W08/) | Vectorisation, Broadcasting Rules, Boolean Masking, Axis Reductions, Fancy Indexing, Matrix Multiplication (@), Image Representation | 🟢 Complete |
| **Week 9** | [Topic Name](./week_09/) | Numerical Computing | ⚪ Pending |
| **Week 10** | [Topic Name](./week_10/) | Advanced Topics | ⚪ Pending |
| **Weeks 11-12** | [R Boot Camp](./r_bootcamp/) | R Syntax, Data Frames | ⚪ Pending |

---

## Assignments & Continuous Assessment

| Assessment | Scope | Submission Archive | Status |
| :--- | :--- | :--- | :--- |
| **Assignment 1** | Weeks 1–4 Portfolio (W01–W04 exercises & self-check) | [`assignment_01/`](./assignment_01/) ([submission_26257770.zip](./assignment_01/submission_26257770.zip)) | 🟢 Submitted |