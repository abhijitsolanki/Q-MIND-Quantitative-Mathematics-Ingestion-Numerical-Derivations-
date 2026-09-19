# Q-MIND — Quantitative Mathematics Ingestion & Numerical Derivations

> A domain-focused Retrieval-Augmented Generation (RAG) system for Financial Mathematics, Quantitative Finance, Derivatives, Stochastic Calculus, Numerical Methods, Optimization, and Mathematical Finance.

Q-MIND builds a searchable mathematical knowledge base from a curated collection of financial-mathematics books. The system converts PDF textbooks into clean, overlapping text chunks, stores their vector representations in a persistent ChromaDB collection, retrieves the most relevant textbook passages for a user query, and then passes the retrieved evidence through a two-stage LLM reasoning pipeline to produce structured mathematical derivations, variable definitions, worked examples, applications, and source references.

---

## 🚀 What Q-MIND Does

Financial mathematics is notation-heavy, formula-heavy, and often requires context spread across multiple textbooks.

A normal keyword search can find the phrase "Black-Scholes", but it does not reliably connect:

- underlying stochastic assumptions,
- the relevant theorem,
- derivation steps,
- notation differences between books,
- financial interpretation, and
- practical applications.

Q-MIND addresses this with:

**PDF ingestion → mathematical chunking → embeddings → persistent vector database → semantic retrieval → context/notation synthesis → deep mathematical reasoning → generated report**

---

# 🧠 System Architecture

```text
                         ┌──────────────────────┐
                         │  Financial Math PDFs │
                         │   ~35+ processed     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    PDF Extraction    │
                         │        pypdf         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Text Cleaning       │
                         │  Formula Preservation│
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Recursive Math       │
                         │ Chunking             │
                         │ 1000 chars / 200 ov. │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Embedding Generation │
                         │ ChromaDB Embeddings │
                         └──────────┬───────────┘
                                    │
                                    ▼
                 ┌────────────────────────────────────┐
                 │ Persistent ChromaDB Vector Store   │
                 │ financial_mathematics_library      │
                 │ HNSW + Cosine Similarity           │
                 └────────────────┬───────────────────┘
                                  │
                            User Query
                                  │
                                  ▼
                 ┌────────────────────────────────────┐
                 │ Semantic Retrieval                 │
                 │ Top-K relevant textbook chunks    │
                 └────────────────┬───────────────────┘
                                  │
                                  ▼
                 ┌────────────────────────────────────┐
                 │ Stage 1 — Context / Notation LLM  │
                 │ Relevance filtering               │
                 │ Notation harmonization            │
                 │ Theorem ordering                  │
                 │ Source mapping                    │
                 └────────────────┬───────────────────┘
                                  │
                                  ▼
                 ┌────────────────────────────────────┐
                 │ Stage 2 — Mathematical Reasoner   │
                 │ Derivation + examples + finance   │
                 └────────────────┬───────────────────┘
                                  │
                                  ▼
                 ┌────────────────────────────────────┐
                 │ Markdown Financial Math Report    │
                 └────────────────────────────────────┘
```

---

# 📚 Knowledge Base

The vector database is built from a curated library of financial mathematics and quantitative finance references.

The repository's `processed_books.json` records the books processed by the ingestion pipeline.

## Included Book Sources

1. **An Introduction to the Financial Derivatives**
2. **An Introduction to the Mathematics of Financial Derivatives — Solution Manual (Neftci)**
3. **Applied Quantitative Finance**
4. **Arbitrage Theory in Continuous Time — Björk**
5. **Basics of Financial Mathematics**
6. **Bayesian Methods in Finance**
7. **Binomial Models in Finance**
8. **Computational Finance Numerical Methods**
9. **Copula Methods in Finance**
10. **Financial Calculus: An Introduction to Derivative Pricing — Baxter**
11. **Financial Econometrics: Modeling Derivatives — Pricing**
12. **Financial Engineering & Computation: Principles, Mathematics & Algorithms**
13. **Financial Mathematics**
14. **From Stochastic Calculus to Mathematical Finance — Kabanov**
15. **Inside Volatility Arbitrage — Javaheri**
16. **Introduction to Computational Finance Without Agonizing Pain**
17. **Introduction to Mathematical Finance — Ross**
18. **Introduction to Quantitative Finance**
19. **Martingale Methods in Financial Modelling — Musiela**
20. **Mathematical Economics and Finance — Harrison & Waldron**
21. **Mathematical Finance — Fries**
22. **Mathematics for Finance: An Introduction to Financial Engineering — Capinski**
23. **Mathematics of Financial Markets — Elliott**
24. **Methods of Mathematical Finance — Karatzas & Shreve**
25. **Modelling Financial Derivatives with Mathematica**
26. **Monte-Carlo Methods in Finance — Jackel**
27. **Neural Networks in Finance: Gaining Predictive Edge in the Market — McNelis**
28. **Nonlinear Optimization with Financial Applications**
29. **Numerical Methods in Finance and Economics: A MATLAB-Based Introduction — Brandimarte**
30. **Optimal Control Models in Finance: A New Computational Approach**
31. **Paul Wilmott on Quantitative Finance**
32. **Quantitative Finance for Physicists: An Introduction**
33. **Quantitative Trading**
34. **Structured Finance: The Object Oriented Approach**
35. **The Mathematics of Financial Derivatives**
36. **The Mathematics of Financial Modelling — Fabozzi**

> The exact files processed in the current run are tracked in `processed_books.json`.

---

# 🗄️ Vector Database

Q-MIND uses **ChromaDB** as its persistent vector database.

### Database configuration

| Property | Configuration |
|---|---|
| Database | ChromaDB |
| Persistence | Local persistent storage |
| Collection | `financial_mathematics_library` |
| Similarity metric | Cosine |
| Index | HNSW |
| Chunk size | 1000 characters |
| Chunk overlap | 200 characters |
| Embedding batch size | 64 |
| Embedding function in current database code | ChromaDB `DefaultEmbeddingFunction` |
| Persistence directory | `./vector_db` |

The configuration file also contains `BAAI/bge-base-en-v1.5` as an embedding-model setting. The current `database.py` implementation, however, initializes ChromaDB with `DefaultEmbeddingFunction()`; therefore this README documents the actual runtime implementation rather than claiming BGE embeddings are currently used.

---

# 🔢 What Is Stored in the Database?

Every processed PDF is converted into many smaller chunks.

A stored record contains:

### 1. ID

Generated using:

```text
{book_title}_p{page_number}_c{chunk_index}
```

Example:

```text
Financial Mathematics_p25_c3
```

### 2. Document

The extracted textbook passage.

### 3. Metadata

Each vector keeps source metadata:

```json
{
  "book_title": "Financial Mathematics",
  "page_number": 25,
  "total_pages": 420,
  "chunk_index": 3
}
```

This metadata allows the system to return mathematical content together with its original book and page location.

---

# 📥 Phase 1 — PDF Ingestion

The ingestion layer is implemented in `ingest.py`.

## Step 1 — Read PDF

Each PDF is opened using `pypdf.PdfReader`.

The system processes the document **page by page**, allowing the resulting chunks to retain page-level source information.

## Step 2 — Clean extracted text

The cleaning stage:

- normalizes repeated spaces and tabs,
- removes empty lines,
- trims whitespace,
- preserves extracted mathematical symbols and formulas as far as the PDF text layer allows.

Very short pages are skipped because they are commonly covers, blank pages, or pages with insufficient extractable text.

## Step 3 — Recursive mathematical chunking

Q-MIND does not simply cut text at a fixed character boundary.

The chunker prioritizes academic and mathematical boundaries:

```text
Paragraph
   ↓
Theorem
   ↓
Definition
   ↓
Lemma
   ↓
Proposition
   ↓
Proof
   ↓
Line
   ↓
Sentence
   ↓
Whitespace
```

This is useful for preserving coherent mathematical units.

### Default configuration

```python
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
```

The 200-character overlap helps preserve derivation context across adjacent chunks.

---

# 🧮 Phase 2 — Embedding & Vector Storage

After a PDF has been extracted and chunked, Q-MIND sends the chunks to ChromaDB in batches.

The logical flow is:

```text
Text Chunk
    ↓
Embedding
    ↓
Vector Representation
    ↓
ChromaDB
    ↓
HNSW Index
```

Vectors are stored with cosine similarity enabled:

```text
"hnsw:space": "cosine"
```

This enables semantic retrieval rather than exact keyword matching.

For example, a query such as:

> "derive the Black-Scholes PDE using Itô's lemma and delta hedging"

can retrieve passages about stochastic differential equations, Itô calculus, delta hedging, no-arbitrage, and derivative pricing even when the exact query wording is different.

---

# ♻️ Checkpoint / Resume System

Q-MIND includes a checkpoint mechanism in `database.py`.

The file:

```text
processed_books.json
```

stores filenames that have already completed ingestion.

Before processing a PDF:

```text
Is this book already processed?
        │
      YES ──► Skip
        │
       NO
        │
        ▼
Extract → Chunk → Embed → Store
        │
        ▼
Mark book as completed
```

This makes the ingestion pipeline **resumable**.

If ingestion is interrupted, rerunning `main.py` skips books already recorded in the checkpoint.

---

# 🔎 Retrieval Layer

The retrieval implementation is in `rag_pipeline.py`.

A user question is queried against the ChromaDB collection using semantic similarity.

Example:

```text
Query:
"Derive the Black-Scholes PDE using Itô's Lemma"
```

The retriever returns the top-(K) relevant chunks.

The default pipeline uses:

```text
Top-K = 5
```

Each retrieved source is formatted with:

```text
[Source 1]
Book: ...
Page: ...
Excerpt:
...
```

This source-aware context is then passed into the first LLM stage.

---

# 🤖 Two-Stage RAG Reasoning

A central design choice in Q-MIND is that retrieved context is **not passed directly to the final answer generator**.

The project uses two reasoning stages.

---

## Stage 1 — Context Verification & Notation Harmonization

Stage 1 acts as a mathematical context curator.

### Relevance filtering

Irrelevant or tangential textbook excerpts are discarded.

### Notation harmonization

Different books may define the same concept with different symbols.

For example:

```text
Book A → S_t
Book B → X_t
Book C → P_t
```

Stage 1 creates one consistent notation scheme for the final derivation.

### Logical ordering

Retrieved material is organized approximately as:

```text
Definitions
   ↓
Assumptions
   ↓
Theorems / Lemmas
   ↓
Mathematical derivation
   ↓
Financial interpretation
```

### Source attribution

Book names and page metadata are retained for later citation.

---

# 🧑‍🏫 Stage 2 — Mathematical & Financial Reasoner

The second stage receives the structured output from Stage 1.

Its role is to turn verified context into a self-contained mathematical explanation.

The prompt requires:

### Mathematical depth

Intermediate derivation steps should be shown rather than jumping directly to the final formula.

### LaTeX equations

Mathematical expressions are expected in LaTeX.

Example:

```latex
$$
\frac{\partial V}{\partial t}
+
\frac{1}{2}\sigma^2S^2
\frac{\partial^2V}{\partial S^2}
+
rS\frac{\partial V}{\partial S}
-rV=0
$$
```

### Variable dictionary

Important equations are accompanied by definitions of their symbols.

### Worked numerical example

The generated explanation is instructed to include an explicit numerical finance example.

### Real-world application

The output connects the mathematics to areas such as:

- derivatives pricing,
- delta hedging,
- risk management,
- market making,
- volatility analysis,
- quantitative finance.

---

# 🧪 Example End-to-End Query

A representative query used in the project is:

```text
Derive the Black-Scholes differential equation using
Itô's Lemma and delta hedging.
```

The pipeline is:

```text
User Question
      ↓
Retrieve Top-5 Textbook Chunks
      ↓
Filter Relevant Sources
      ↓
Harmonize Mathematical Notation
      ↓
Order Theorems / Assumptions
      ↓
Generate Structured Instructions
      ↓
Deep Mathematical Derivation
      ↓
Worked Example
      ↓
Financial Applications
      ↓
Markdown Report
```

An example generated report is included in:

```text
test_output.md
```

---

# 🌐 Web Application

Q-MIND also includes a Streamlit interface in:

```text
app_web.py
```

The interface allows a user to:

1. Enter a financial mathematics question.
2. Choose the number of retrieved textbook excerpts.
3. Execute the two-stage RAG pipeline.
4. View the generated derivation.
5. Save generated reports.
6. Download the generated Markdown report.
7. Reopen previously generated reports.

---

# 📁 Project Structure

```text
Q-MIND/
│
├── app_web.py              # Streamlit web interface
├── config.py               # Pipeline configuration
├── database.py             # ChromaDB + checkpoint management
├── ingest.py               # PDF extraction + mathematical chunking
├── main.py                 # PDF ingestion pipeline entry point
├── rag_pipeline.py         # Retrieval + two-stage LLM pipeline
├── templates.py            # LLM prompts and output templates
│
├── processed_books.json    # Processed-book checkpoint
├── test_search.py          # Vector search test
├── test_system.py          # End-to-end system tests
├── test_output.md          # Example generated mathematical report
│
└── vector_db/              # Local ChromaDB persistence
    └── ...
```

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/abhijitsolanki/Q-MIND-Quantitative-Mathematics-Ingestion-Numerical-Derivations-.git
cd Q-MIND-Quantitative-Mathematics-Ingestion-Numerical-Derivations-
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install the repository dependencies:

```bash
pip install -r requirements.txt
```

The repository currently lists:

- `pypdf`
- `chromadb`
- `sentence-transformers`
- `tqdm`
- `pydantic`

The RAG application also imports the Google GenAI SDK and `python-dotenv`, so those packages must be available in the environment used to run the RAG/web application.

---

# 📂 Configure the PDF Library

Edit:

```text
config.py
```

and set:

```python
PDF_FOLDER_PATH = r"/path/to/your/financial/math/books"
```

Place the source PDFs in that directory.

The ingestion script automatically discovers:

```text
*.pdf
```

files.

---

# 🏗️ Build the Vector Database

Run:

```bash
python main.py
```

The ingestion pipeline performs:

```text
Find PDFs
   ↓
Skip completed books
   ↓
Read PDF pages
   ↓
Clean extracted text
   ↓
Create overlapping math-aware chunks
   ↓
Generate/store embeddings
   ↓
Upsert chunks into ChromaDB
   ↓
Update processed_books.json
```

At completion, the pipeline reports the total number of vectors in the collection.

---

# 🔐 Environment Variables

The RAG generation layer expects a Gemini API key.

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL_NAME=your_model_name
```

Do **not** commit your real API key to GitHub.

---

# 💬 Run the RAG Pipeline from Python

The main RAG entry point is:

```python
from rag_pipeline import run_financial_rag

result = run_financial_rag(
    query="Derive the Black-Scholes PDE using Itô's Lemma and delta hedging.",
    top_k=5,
    output_file="output.md"
)

print(result)
```

The generated answer is also written to the specified Markdown file.

---

# 🌐 Run the Web Interface

Launch Streamlit:

```bash
streamlit run app_web.py
```

Then open the local Streamlit URL printed by the terminal.

---

# 🧪 Testing

## Test vector retrieval

```bash
python test_search.py
```

This test prints:

- retrieval rank,
- cosine distance,
- source book,
- page number,
- retrieved excerpt.

## Test the complete system

```bash
python test_system.py
```

The system test checks:

1. ChromaDB collection availability.
2. Gemini connectivity.
3. End-to-end RAG generation.

---

# 📦 Vector Database Distribution

The generated ChromaDB directory is intentionally **not committed directly to GitHub**.

The local vector database is approximately **360 MB**, so the project distributes it separately as a **ZIP archive**.

This keeps the source repository lightweight while still allowing a pre-built knowledge base to be restored locally.

### Restoration workflow

```text
Download vector database ZIP
          ↓
Extract archive
          ↓
Place extracted folder at:
./vector_db
          ↓
Verify collection:
financial_mathematics_library
          ↓
Run retrieval / RAG pipeline
```

> Extract the archive so that the ChromaDB persistence path configured in `config.py` points to the restored `vector_db` directory.

The source PDFs are also kept separate from the Git repository because of their size and distribution constraints.

---

# 📊 Current Database Information

The existing RAG pipeline reports a working collection containing:

```text
25,871 vectors
```

The project reports this count directly from the ChromaDB collection during retrieval/testing.

Because the vector database is distributed as a ZIP rather than committed into Git, the Git repository contains the **source code, configuration, tests, and processing metadata**, while the full precomputed vector store is distributed separately.

---

# 🔍 Why Page-Level Metadata Matters

Financial mathematics is highly dependent on derivation context.

Suppose a retrieved chunk contains:

```text
dV = ...
```

Without source information, the chunk is difficult to audit.

Q-MIND retains:

```text
Book
Page
Chunk
```

so a retrieved result can be traced back to its original textbook location.

This is useful for:

- checking derivations,
- comparing competing notation,
- validating assumptions,
- studying a topic across multiple books,
- building research notes,
- auditing generated answers.

---

# 🎯 Design Goals

### 1. Mathematical Retrieval

Retrieve equations, definitions, derivations, and theoretical context rather than relying purely on keywords.

### 2. Cross-Book Knowledge Integration

Combine information from multiple quantitative-finance references.

### 3. Notation Consistency

Different textbooks often use different symbols for the same quantities. Stage 1 explicitly harmonizes these differences before final reasoning.

### 4. Explainable Financial Mathematics

The intended output combines:

```text
Theory
   +
Assumptions
   +
Derivation
   +
Variables
   +
Numerical Example
   +
Financial Application
   +
Source References
```

---

# 🛠️ Future Extensions

Possible extensions include:

- dedicated mathematical embedding models,
- hybrid lexical + semantic retrieval,
- retrieval reranking,
- equation-aware parsing,
- OCR for scanned books,
- chapter/section hierarchy in metadata,
- citation verification against original pages,
- text + equation multi-vector representations,
- theorem/definition knowledge graphs,
- retrieval evaluation benchmarks,
- support for additional LLM providers,
- cached query results and report versioning.

---

# ⚠️ Important Notes

### Source PDFs

The books used to construct the knowledge base are third-party materials. Users should ensure that their storage and redistribution of those files complies with applicable copyright and licensing requirements.

### Generated Mathematics

LLM-generated mathematical explanations should be independently checked against the underlying references before being used for academic, research, trading, or production decisions.

### Vector Database

The `vector_db` directory is external to the normal GitHub source tree because of its size. A ZIP archive can be used to restore the precomputed database instead of recomputing embeddings.

---

# 📄 Example Output

A generated report follows this structure:

```text
# 1. Executive Summary & Theoretical Intuition
# 2. Mathematical Framework & Underlying Assumptions
# 3. Step-by-Step Derivation & Formula Mechanics
# 4. Comprehensive Variable Dictionary
# 5. Worked Numerical Financial Example
# 6. Real-World Applications in Quantitative Finance & Risk Management
# 7. Source Textbook Citations
```

An example is available in:

```text
test_output.md
```

---

# 👨‍💻 Author

**Abhijit Solanki**

GitHub:  
https://github.com/abhijitsolanki

Project:  
https://github.com/abhijitsolanki/Q-MIND-Quantitative-Mathematics-Ingestion-Numerical-Derivations-

---

# ⭐ Project Summary

Q-MIND is a **Financial Mathematics Knowledge Engine**:

```text
Books
  ↓
PDF Parser
  ↓
Math-Aware Chunking
  ↓
Embeddings
  ↓
ChromaDB
  ↓
Semantic Retrieval
  ↓
Context + Notation Harmonization
  ↓
Mathematical Reasoning
  ↓
Derivation + Example + Application
```

The key idea is not simply to build a chatbot over PDFs.

It is to build a **retrieval and reasoning layer specialized for quantitative finance**, where the system can locate mathematical evidence, reconcile notation across references, and transform that evidence into a structured derivation.

---

## 📌 Quick Start

```bash
git clone https://github.com/abhijitsolanki/Q-MIND-Quantitative-Mathematics-Ingestion-Numerical-Derivations-.git
cd Q-MIND-Quantitative-Mathematics-Ingestion-Numerical-Derivations-
pip install -r requirements.txt

# 1. Put source PDFs in the configured PDF folder
# 2. Build or restore ./vector_db
# 3. Set GEMINI_API_KEY in .env

python main.py
python test_search.py
python test_system.py

# Optional web UI
streamlit run app_web.py
```
