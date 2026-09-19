# app_web.py
import os
import re
from datetime import datetime
import streamlit as st
from rag_pipeline import run_financial_rag

# ---------------------------------------------------------------------------
# App Configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Financial Mathematics RAG",
    page_icon="📈",
    layout="wide"
)

# Folder where all outputs will be permanently archived
REPORTS_DIR = "./generated_reports"
os.makedirs(REPORTS_DIR, exist_ok=True)


def sanitize_filename(query: str, max_words: int = 5) -> str:
    """Creates a clean, filesystem-safe filename from the user prompt."""
    cleaned = re.sub(r'[^\w\s-]', '', query).strip()
    words = cleaned.split()[:max_words]
    slug = "_".join(words) if words else "report"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{timestamp}_{slug}.md"


# ---------------------------------------------------------------------------
# Sidebar: Past Generated Reports
# ---------------------------------------------------------------------------
st.sidebar.title("📁 Generated Reports Archive")
st.sidebar.caption(f"Saved in: `{REPORTS_DIR}`")

saved_files = sorted(
    [f for f in os.listdir(REPORTS_DIR) if f.endswith(".md")],
    reverse=True
)

if saved_files:
    selected_file = st.sidebar.selectbox("View a previous report:", ["-- Select a Report --"] + saved_files)
    if selected_file != "-- Select a Report --":
        with open(os.path.join(REPORTS_DIR, selected_file), "r", encoding="utf-8") as f:
            past_content = f.read()
        st.sidebar.markdown(f"**Loaded:** `{selected_file}`")
        st.sidebar.download_button(
            label="Download This Report",
            data=past_content,
            file_name=selected_file,
            mime="text/markdown"
        )
else:
    st.sidebar.info("No reports generated yet. Run your first query below!")


# ---------------------------------------------------------------------------
# Main Query Interface
# ---------------------------------------------------------------------------
st.title("📚 Financial Mathematics Research Assistant")
st.markdown(
    "Query across **50 Financial Mathematics textbooks** (~25,800 vectors). "
    "Generates in-depth mathematical derivations, formula mechanics, and practical quantitative finance examples."
)

with st.expander("💡 Prompt Examples (Click to expand)"):
    st.markdown("""
    - *Derive the Black-Scholes partial differential equation using Itô's Lemma and delta hedging.*
    - *Explain the Vasicek short-rate interest rate model and derive the zero-coupon bond pricing formula.*
    - *Explain the Heston stochastic volatility model and the mathematical role of the Feller condition.*
    - *Show the step-by-step derivation of the Cox-Ingersoll-Ross (CIR) interest rate model.*
    """)

# User Inputs
user_query = st.text_area(
    "Enter your mathematical/financial question:",
    height=120,
    placeholder="e.g., State Itô's Lemma, show its full derivation with Taylor expansion, and demonstrate with an option pricing example."
)

col1, col2 = st.columns([1, 4])
with col1:
    top_k = st.slider("Textbook Excerpts (Top-K):", min_value=3, max_value=10, value=5)

generate_btn = st.button("🚀 Generate In-Depth Analysis", type="primary")

# ---------------------------------------------------------------------------
# Execution and Display
# ---------------------------------------------------------------------------
if generate_btn:
    if not user_query.strip():
        st.warning("Please enter a question before generating.")
    else:
        # Create unique timestamped output file in the common folder
        output_filename = sanitize_filename(user_query)
        output_filepath = os.path.join(REPORTS_DIR, output_filename)

        try:
            with st.status("Executing Two-Stage Financial RAG...", expanded=True) as status:
                st.write("🔍 Searching ChromaDB across 25,871 vectors...")
                st.write("📝 Stage 1: Verifying relevance & harmonizing variable notation (Gemini 3.5 Flash-Lite)...")
                st.write("📐 Stage 2: Producing publication-grade mathematical derivation (~1,500 words)...")
                
                # Execute Pipeline
                result = run_financial_rag(
                    query=user_query,
                    top_k=top_k,
                    output_file=output_filepath
                )
                
                status.update(label="Analysis Completed Successfully!", state="complete", expanded=False)

            st.success(f"Report saved permanently to: `{output_filepath}`")

            # Download Button
            st.download_button(
                label="📥 Download Current Report (.md)",
                data=result,
                file_name=output_filename,
                mime="text/markdown"
            )

            # Render Formatted Output with Math
            st.markdown("---")
            st.markdown(result)

        except Exception as e:
            st.error(f"Error occurred during generation: {e}")

# If user selected a past report from the sidebar and didn't just generate a new one
elif saved_files and 'selected_file' in locals() and selected_file != "-- Select a Report --":
    st.markdown("---")
    st.subheader(f"Archived Report: {selected_file}")
    with open(os.path.join(REPORTS_DIR, selected_file), "r", encoding="utf-8") as f:
        st.markdown(f.read())