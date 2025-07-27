# Challenge 1b: Persona-Driven Document Intelligence

## 🧠 Overview

This is the solution for **Challenge 1b**, an advanced PDF analysis system that processes multiple documents and extracts the most relevant content based on a specific user persona and their job-to-be-done.  
It operates entirely **offline and on-device**, leveraging a lightweight AI model for semantic understanding.

---

## 🚀 Key Features & Approach

The solution uses a modern semantic search pipeline to achieve high relevance scores:

- **Persona-based Content Analysis**  
  The user's persona and job description are combined into a rich semantic query.
  
- **Intelligent Sectioning**  
  Structured outlines from Challenge 1a are used to break down PDFs into meaningful, context-rich sections.
  
- **Importance Ranking**  
  A pre-trained Sentence-Transformer model (`all-MiniLM-L6-v2`) converts queries and sections into vector embeddings. Cosine similarity scores help rank the sections by relevance.
  
- **Structured JSON Output**  
  Outputs a ranked list of relevant sections, complete with metadata and short summaries.

📄 For a detailed methodology, refer to the [`approach_explanation.md`](./approach_explanation.md) file.

---

## 📊 Sample Output

### ✅ Analysis complete. Output saved to `ranked_sections.json`

#### 🔎 Top 5 Relevant Sections

| Rank | Document                         | Section Title             | Page |
|------|----------------------------------|----------------------------|------|
| 1    | `network interview bit.pdf`      | Networking Interview       | 1    |
| 2    | `cpp interview bit.pdf`          | C++ Interview Questions    | 1    |
| 3    | `network interview bit.pdf`      | Let's get Started          | 4    |
| 4    | `interview bit dbms question.pdf`| Let's get Started          | 4    |
| 5    | `interview bit dbms question.pdf`| DBMS Interview Questions   | 1    |

#### 📈 Final Summary

| Metric                    | Value        |
|---------------------------|--------------|
| Total PDFs Analyzed       | 4            |
| Total Sections Analyzed   | 35           |
| Average Relevance Score   | 0.276        |
| Total Processing Time     | 4.13 seconds |

---

## 🧪 How to Test

### 🔧 Build Command

Run this from the `Challenge_1b` directory:

```bash
docker build --platform linux/amd64 -t adobe-1b-solution .
