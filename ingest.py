import re
import os
from typing import List, Dict, Any
from pypdf import PdfReader


def clean_math_text(text: str) -> str:
    """Cleans common extraction artifacts while preserving formulas and symbols."""
    # Replace multiple consecutive spaces and tabs while preserving single newlines
    text = re.sub(r'[ \t]+', ' ', text)
    # Remove repetitive page headers or trailing whitespace lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def recursive_math_chunker(
    text: str, 
    chunk_size: int = 1000, 
    chunk_overlap: int = 200
) -> List[str]:
    """
    Splits text recursively using delimiters prioritized for math/academic texts
    (sections, theorems, definitions, paragraphs, sentences).
    """
    delimiters = [
        "\n\n",
        "\nTheorem", "\nDefinition", "\nLemma", "\nProposition", "\nProof",
        "\n", ". ", " "
    ]
    
    def _split(txt: str, seps: List[str]) -> List[str]:
        if len(txt) <= chunk_size or not seps:
            return [txt] if txt else []
        
        sep = seps[0]
        splits = txt.split(sep)
        chunks = []
        current_chunk = ""
        
        for part in splits:
            candidate = f"{current_chunk}{sep}{part}" if current_chunk else part
            if len(candidate) <= chunk_size:
                current_chunk = candidate
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                # Recurse with finer separators if a single component exceeds chunk_size
                if len(part) > chunk_size and len(seps) > 1:
                    chunks.extend(_split(part, seps[1:]))
                else:
                    current_chunk = part
        
        if current_chunk:
            chunks.append(current_chunk)
            
        # Add overlap between adjacent chunks
        overlapped_chunks = []
        for i, chunk in enumerate(chunks):
            if i > 0 and chunk_overlap > 0:
                prev_overlap = chunks[i-1][-chunk_overlap:]
                chunk = f"... {prev_overlap} {chunk}"
            overlapped_chunks.append(chunk)
            
        return overlapped_chunks

    return _split(text, delimiters)


def process_single_pdf(pdf_path: str, chunk_size: int, chunk_overlap: int) -> List[Dict[str, Any]]:
    """
    Extracts and chunks a single PDF document page by page to retain accurate page metadata.
    """
    book_title = os.path.splitext(os.path.basename(pdf_path))[0]
    chunks_with_metadata = []
    
    try:
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        
        for page_idx, page in enumerate(reader.pages):
            raw_text = page.extract_text() or ""
            cleaned = clean_math_text(raw_text)
            
            # Skip empty or unparsable pages (e.g., blank cover pages)
            if len(cleaned.strip()) < 40:
                continue
                
            page_chunks = recursive_math_chunker(cleaned, chunk_size, chunk_overlap)
            
            for chunk_idx, chunk in enumerate(page_chunks):
                chunk_id = f"{book_title}_p{page_idx + 1}_c{chunk_idx}"
                chunks_with_metadata.append({
                    "id": chunk_id,
                    "text": chunk,
                    "metadata": {
                        "book_title": book_title,
                        "page_number": page_idx + 1,
                        "total_pages": total_pages,
                        "chunk_index": chunk_idx
                    }
                })
    except Exception as e:
        print(f"[Error] Failed to process {pdf_path}: {e}")
        
    return chunks_with_metadata