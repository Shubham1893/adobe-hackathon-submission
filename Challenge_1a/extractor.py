
import fitz
import json
import os
import time
from collections import defaultdict
from rich.console import Console
from rich.table import Table

console = Console()

def extract_structure_single_pass(doc_path):
    """Extracts title and outline in a single, optimized pass."""
    doc = fitz.open(doc_path)
    
    potential_headings = []
    font_counts = defaultdict(int)

    # --- SINGLE PASS ---
    # In one loop, we collect potential headings and their font sizes.
    # A "potential heading" is a short, single-line text block.
    for page_num, page in enumerate(doc):
        for block in page.get_text("dict")["blocks"]:
            if "lines" in block and len(block["lines"]) == 1 and block["lines"][0]["spans"]:
                line = block["lines"][0]
                text = " ".join(s['text'].strip() for s in line['spans'])
                
                # Filter out empty or very long lines
                if text and len(text.split()) < 25:
                    size = round(line["spans"][0]['size'])
                    font_counts[size] += 1
                    potential_headings.append({
                        "text": text,
                        "size": size,
                        "page": page_num + 1,
                        "y": block["bbox"][1]
                    })
    
    if not potential_headings:
        return {"title": "No Title Found", "outline": []}, len(doc)

    # --- IN-MEMORY ANALYSIS (VERY FAST) ---
    # Determine heading levels from the collected font stats.
    sorted_fonts = sorted(font_counts.keys(), reverse=True)
    level_map = {}
    if len(sorted_fonts) > 0: level_map[sorted_fonts[0]] = "H1"
    if len(sorted_fonts) > 1: level_map[sorted_fonts[1]] = "H2"
    if len(sorted_fonts) > 2: level_map[sorted_fonts[2]] = "H3"
    
    # Process the in-memory list of potential headings.
    title_fontsize = sorted_fonts[0] if sorted_fonts else 0
    detected_title = "Untitled Document"
    title_found = False
    
    outline = []
    # Sort potential headings by page and position
    potential_headings.sort(key=lambda h: (h['page'], h['y']))

    for h in potential_headings:
        if not title_found and h['page'] == 1 and h['size'] == title_fontsize:
            detected_title = h['text']
            title_found = True
        
        if h['size'] in level_map:
            outline.append({"level": level_map[h['size']], "text": h['text'], "page": h['page']})
            
    # Fallback to find title if not found on page 1
    if not title_found and outline:
        detected_title = outline[0]['text']

    return {"title": detected_title, "outline": outline}, len(doc)

if __name__ == "__main__":
    input_dir, output_dir = "/app/input", "/app/output"
    os.makedirs(output_dir, exist_ok=True)
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    total_headings, start_time = 0, time.time()
    console.print("\n[bold green]--== Starting Round 1A: PDF Outline Extraction (Optimized) ==--[/bold green]")
    
    for pdf_file in pdf_files:
        try:
            input_path = os.path.join(input_dir, pdf_file)
            output_data, page_count = extract_structure_single_pass(input_path)
            headings_count = len(output_data['outline'])
            total_headings += headings_count
            
            file_name, _ = os.path.splitext(pdf_file)
            output_filename = f"{file_name}.json"
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, 'w', encoding='utf-8') as f: json.dump(output_data, f, indent=2)
            console.print(f"\n[bold cyan]Processed:[/bold cyan] {pdf_file} ({page_count} pages)")
            console.print(f"  [green]✓[/green] Headings Found: {headings_count}")
            console.print(f"  [green]✓[/green] Output saved to: {output_filename}")
        except Exception as e:
            console.print(f"  [bold red]Error processing {pdf_file}: {e}[/bold red]")

    processing_time = time.time() - start_time
    summary_table = Table(title="[bold]Round 1A: Final Summary[/bold]")
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="magenta")
    summary_table.add_row("Total PDFs Processed", str(len(pdf_files)))
    summary_table.add_row("Total Headings Found", str(total_headings))
    summary_table.add_row("Total Processing Time", f"{processing_time:.2f} seconds")
    console.print("\n"); console.print(summary_table)