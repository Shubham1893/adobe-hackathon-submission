# Adobe India Hackathon 2025: Connecting the Dots

## Welcome to the "Connecting the Dots" Challenge

This repository contains the solutions for **Round 1** of the Adobe India Hackathon 2025. The challenge is to **reimagine the PDF** as an intelligent, interactive experience that understands structure and surfaces insights.

---

## 🚀 The Journey Ahead

- **Round 1:** Kick things off by building the brains — extract structured outlines from raw PDFs with blazing speed and pinpoint accuracy. Then, power it up with on-device intelligence that understands sections and links related ideas together.
- **Round 2:** It’s showtime! Build a beautiful, intuitive reading webapp using Adobe’s PDF Embed API. You will be using your Round 1 work to design a futuristic webapp.

---

## 🧠 Challenge Solutions

### 🔹 Challenge 1a: PDF Processing Solution

A performance-optimized solution for extracting structured outlines (Title, H1, H2, H3) from PDF documents using Docker.

- **Location:** [`/Challenge_1a`](./Challenge_1a)

### 🔹 Challenge 1b: Multi-Collection PDF Analysis

An advanced, persona-based content analysis engine that ranks document sections by relevance across multiple collections.

- **Location:** [`/Challenge_1b`](./Challenge_1b)

> **Note:** Each challenge directory contains detailed documentation and implementation details. Please refer to the individual README files for comprehensive information about each solution.

---

# Challenge 1a: PDF Processing Solution

## 📄 Overview

This is the solution for Challenge 1a of the Adobe India Hackathon 2025. The challenge requires implementing a PDF processing solution that extracts structured data (Title, H1, H2, H3) from PDF documents and outputs JSON files. The solution is containerized using Docker and meets all specified performance and resource constraints.

## 📌 Official Challenge Guidelines

- **Execution Time:** ≤ 10 seconds for a 50-page PDF  
- **Model Size:** ≤ 200MB (if using ML models)  
- **Network:** No internet access allowed during runtime  
- **Architecture:** Must work on `linux/amd64`

## 🛠️ Implemented Solution

Our solution (`extractor.py`) uses a rapid, rule-based heuristic model to determine the document structure efficiently:

1. **Optimized Font Analysis**: Builds a frequency map of font sizes and maps the most common to heading levels.
2. **Hierarchy Mapping**: Largest font → `H1`, second-largest → `H2`, third-largest → `H3`.
3. **Title Detection**: First occurrence of the largest font size on the first page is treated as the title.
4. **Batch Processing**: Automatically processes all `.pdf` files in `/app/input` and generates corresponding `.json` files.

## 📦 Sample Output

```
--== Starting Round 1A: PDF Outline Extraction ==--

Processed: cpp interview bit.pdf (26 pages)
✓ Output saved to: cpp interview bit.json

Processed: interview bit dbms question.pdf (26 pages)
✓ Output saved to: interview bit dbms question.json

Processed: javascript-interview-qa-key-concepts-handwritten-notes-js-101.pdf (14 pages)
✓ Output saved to: javascript-interview-qa-key-concepts-handwritten-notes-js-101.json

Processed: network interview bit.pdf (34 pages)
✓ Output saved to: network interview bit.json

    Round 1A: Final Summary
┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Metric                ┃ Value         ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ Total PDFs Processed  │ 4             │
│ Total Headings Found  │ 38            │
│ Total Processing Time │ 9.12 seconds │
└───────────────────────┴───────────────┘
```

## 🧪 How to Test

### 🏗️ Build Command

```bash
docker build --platform linux/amd64 -t adobe-1a-solution .
```

### ▶️ Run Command

```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none adobe-1a-solution
```

---

# Challenge 1b: Multi-Collection PDF Analysis

## 📄 Overview

This is the solution for Challenge 1b, an advanced PDF analysis system that processes multiple documents and extracts the most relevant content based on a specific **user persona** and their **job-to-be-done**. It operates **entirely offline** and **on-device**, leveraging a lightweight AI model for semantic understanding.

## 🌟 Key Features

- **Persona-based Content Analysis**: Semantic queries are generated from persona + job.
- **Intelligent Sectioning**: Uses output from Challenge 1a to break PDFs into structured sections.
- **Relevance Ranking**: Uses `all-MiniLM-L6-v2` transformer model + cosine similarity for ranking.
- **Structured Output**: Outputs `ranked_sections.json` with metadata and summaries.

> For a more detailed explanation of the methodology, refer to [`approach_explanation.md`](./Challenge_1b/approach_explanation.md)

## 📦 Sample Output

```
--== Starting Round 1B: Document Intelligence Engine ==--

Persona: A software student  
Job to be Done: Prepare for a technical interview  

Loading AI model from local files...  
Found 4 PDFs to process...  
Total sections found across all documents: 35  
Performing semantic analysis...  
✅ Analysis complete. Output saved to ranked_sections.json  

  Round 1B: Top 5 Relevant Sections
┏━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┓
┃ Rank ┃ Document                      ┃ Section Title            ┃ Page ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━┩
│ 1    │ network interview bit.pdf       │ Networking Interview     │ 1    │
│ 2    │ cpp interview bit.pdf           │ C++ Interview Questions  │ 1    │
│ 3    │ network interview bit.pdf       │ Let's get Started        │ 4    │
│ 4    │ interview bit dbms question.pdf │ Let's get Started        │ 4    │
│ 5    │ interview bit dbms question.pdf │ DBMS Interview Questions │ 1    │
└──────┴───────────────────────────────┴──────────────────────────┴──────┘

  Round 1B: Final Summary
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Metric                    ┃ Value         ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ Total PDFs Analyzed       │ 4             │
│ Total Sections Analyzed   │ 35            │
│ Average Relevance Score   │ 0.276         │
│ Total Processing Time     │ 4.13 seconds  │
└───────────────────────────┴───────────────┘
```

## 🧪 How to Test

### 🏗️ Build Command

```bash
docker build --platform linux/amd64 -t adobe-1b-solution .
```

### ▶️ Run Command

```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output adobe-1b-solution python analyzer.py --persona "A software student" --job "Prepare for a technical interview"
```

---
