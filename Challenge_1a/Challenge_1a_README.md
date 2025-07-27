# Challenge 1a: PDF Processing Solution

## Overview

This is the solution for Challenge 1a of the Adobe India Hackathon 2025. The challenge requires implementing a PDF processing solution that extracts structured data (Title, H1, H2, H3) from PDF documents and outputs them as JSON files. The solution is containerized using Docker and meets all specified performance and resource constraints.

## Official Challenge Guidelines

* **Execution Time:** ≤ 10 seconds for a 50-page PDF
* **Model Size:** ≤ 200MB (if using ML models)
* **Network:** No internet access allowed during runtime.
* **Architecture:** Must work on `linux/amd64`.

## Implemented Solution

Our solution (`extractor.py`) uses a rapid, rule-based heuristic model to determine the document structure efficiently, ensuring it meets the strict performance requirements.

1.  **Optimized Font Analysis:** The script performs a fast pass over the document's text blocks to build a frequency map of font sizes, assuming the most prominent sizes correlate to heading levels.
2.  **Hierarchy Mapping:** The largest font size found is mapped to `H1`, the second-largest to `H2`, and the third-largest to `H3`.
3.  **Title Detection:** The document's title is identified as the first text on the first page that uses the largest font size.
4.  **Batch Processing:** The script automatically processes every `.pdf` file found in the `/app/input` directory and generates a corresponding `.json` file for each.

## Sample Output

Here is a sample output from running the solution on a collection of test PDFs, demonstrating its performance and rich terminal logging.

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
│ Total Processing Time │ 14.12 seconds │
└───────────────────────┴───────────────┘
```

## How to Test

### 🏗️ Build Command (from the `Challenge_1a` directory)

```bash
docker build --platform linux/amd64 -t adobe-1a-solution .
```

### ▶️ Run Command (from the `Challenge_1a` directory)

```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none adobe-1a-solution
```