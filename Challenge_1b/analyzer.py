# Challenge_1b/analyzer.py
import fitz
import json
import os
import argparse
import time
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from rich.console import Console
from rich.table import Table

console = Console()
MODEL_PATH = '/app/model'

def load_sections_from_outline(json_path, pdf_path):
    """Loads text content for each section defined in the outline JSON."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            outline_data = json.load(f)
    except FileNotFoundError:
        return []

    doc = fitz.open(pdf_path)
    sections, page_texts = [], {i: page.get_text("text", sort=True) for i, page in enumerate(doc)}
    doc.close()

    for i, heading in enumerate(outline_data.get("outline", [])):
        start_page = heading["page"] - 1
        page_text = page_texts.get(start_page, "")
        start_index = page_text.find(heading["text"])
        section_text = ""

        if start_index != -1:
            end_index = -1
            if i + 1 < len(outline_data["outline"]):
                next_heading = outline_data["outline"][i+1]
                if next_heading["page"] - 1 == start_page:
                    end_index = page_text.find(next_heading["text"], start_index + len(heading["text"]))
            section_text = page_text[start_index:end_index].strip() if end_index != -1 else page_text[start_index:].strip()

        if section_text:
             sections.append({
                "doc": os.path.basename(pdf_path),
                "title": heading["text"],
                "page": heading["page"],
                "full_text": section_text
            })
    return sections

def refine_text(text, num_lines=3):
    """Provides a simple summary by taking the first few lines."""
    lines = text.strip().split('\n')
    return "\n".join(lines[:num_lines])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Persona-Driven Document Intelligence")
    parser.add_argument("--persona", required=True, help="User persona")
    parser.add_argument("--job", required=True, help="Job to be done")
    args = parser.parse_args()
    input_dir = "/app/input"
    output_dir = "/app/output"

    start_time = time.time()
    console.print("\n[bold green]--== Starting Round 1B: Document Intelligence Engine ==--[/bold green]")
    console.print(f"\n[bold]Persona:[/bold] {args.persona}")
    console.print(f"[bold]Job to be Done:[/bold] {args.job}\n")

    console.print("Loading AI model from local files...", style="yellow")
    model = SentenceTransformer(MODEL_PATH)

    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    console.print(f"Found {len(pdf_files)} PDFs to process...")

    all_sections = []
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file)
        base_name, _ = os.path.splitext(pdf_file)
        json_path = os.path.join(input_dir, f"{base_name}.json")
        
        if not os.path.exists(json_path):
            console.print(f"  [yellow]Warning:[/yellow] Outline not found for {pdf_file}. Skipping.")
            continue
        sections = load_sections_from_outline(json_path, pdf_path)
        all_sections.extend(sections)
    
    if not all_sections:
        console.print("[bold red]Error: No sections found. Ensure outlines are generated and copied to input directory.[/bold red]")
        exit()
    
    console.print(f"Total sections found across all documents: {len(all_sections)}")
    console.print("Performing semantic analysis...", style="yellow")
    
    query = f"{args.persona}. Task: {args.job}"
    query_embedding = model.encode(query)
    
    section_texts = [sec['full_text'] for sec in all_sections]
    section_embeddings = model.encode(section_texts)
    scores = cosine_similarity([query_embedding], section_embeddings)[0]

    for i, section in enumerate(all_sections):
        section['score'] = scores[i]
    
    ranked_sections = sorted(all_sections, key=lambda x: x['score'], reverse=True)
    
    for rank, section in enumerate(ranked_sections):
        section['importance_rank'] = rank + 1
        
    output_filename = "ranked_sections.json"
    output_path = os.path.join(output_dir, output_filename)
    final_output = {
        "metadata": {"persona": args.persona, "job_to_be_done": args.job, "processed_docs": pdf_files},
        "extracted_sections": [{"document": s["doc"], "section_title": s["title"], "importance_rank": s["importance_rank"], "page_number": s["page"]} for s in ranked_sections],
        "subsection_analysis": [{"document": s["doc"], "page_number": s["page"], "refined_text": refine_text(s["full_text"])} for s in ranked_sections[:5]]
    }
    
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(final_output, f, indent=2)

    processing_time = time.time() - start_time
    console.print(f"✅ [bold green]Analysis complete.[/bold green] Output saved to {output_filename}")

    results_table = Table(title="[bold]Round 1B: Top 5 Relevant Sections[/bold]")
    results_table.add_column("Rank", style="cyan")
    results_table.add_column("Document", style="yellow")
    results_table.add_column("Section Title", style="magenta")
    results_table.add_column("Page", style="green")
    for section in ranked_sections[:5]:
        results_table.add_row(str(section['importance_rank']), section['doc'], section['title'], str(section['page']))
    console.print("\n")
    console.print(results_table)

    avg_score = np.mean([s['score'] for s in ranked_sections]) if ranked_sections else 0
    summary_table = Table(title="[bold]Round 1B: Final Summary[/bold]")
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="magenta")
    summary_table.add_row("Total PDFs Analyzed", str(len(pdf_files)))
    summary_table.add_row("Total Sections Analyzed", str(len(all_sections)))
    summary_table.add_row("Average Relevance Score", f"{avg_score:.3f}")
    summary_table.add_row("Total Processing Time", f"{processing_time:.2f} seconds")

    console.print("\n")
    console.print(summary_table)