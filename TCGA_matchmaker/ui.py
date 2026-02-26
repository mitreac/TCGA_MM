import streamlit as st
import pandas as pd
import numpy as np
from match_computation import compute_match_scores

st.set_page_config(page_title="TCGA Matchmaker", layout="wide")

st.title("TCGA Matchmaker")
st.write("Upload a gene expression CSV file to compute match scores.")

st.markdown(
"""
**Expected format:**
- First column: Gene IDs
- Remaining columns: Sample expression values
"""
)

uploaded_file = st.file_uploader("Upload gene-expression CSV file", type=["csv"])

def validate_dataframe(df):
    """Validate uploaded expression dataframe"""
    
    if df.empty:
        return "Uploaded CSV file is empty."

    if df.shape[1] < 3:
        return "CSV must contain at least 1 gene column and 2 sample columns."

    # First column must be gene column
    gene_col = df.columns[0]

    if df[gene_col].isnull().any():
        return "Gene column contains missing values."

    if df[gene_col].duplicated().any():
        return "Duplicate gene IDs detected in gene column."

    # Check numeric values for samples
    sample_df = df.iloc[:, 1:]
    if not all(sample_df.dtypes.apply(lambda x: np.issubdtype(x, np.number))):
        return "Non-numeric expression values detected in sample columns."

    return None


if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

    except Exception:
        st.error("Unable to read CSV file. Please ensure it is a valid CSV.")
        st.stop()

    error_msg = validate_dataframe(df)

    if error_msg:
        st.error(error_msg)
        st.stop()

    # Set gene column as index
    gene_col = df.columns[0]
    df = df.set_index(gene_col)

    st.success("File successfully uploaded and validated.")

    sample_names = list(df.columns)

    reference_sample = st.selectbox(
        "Select reference sample",
        sample_names
    )

# Initialize session storage
if "results" not in st.session_state:
    st.session_state["results"] = None

if st.button("Run TCGA Matching"):

    try:
        profile = df[reference_sample]
        comparison_df = df.drop(columns=[reference_sample])

        match_scores = compute_match_scores(comparison_df, profile)

        # Sort in descending order
        results = (
            match_scores
            .sort_values(ascending=False)
            .reset_index()
        )

        results.columns = ["Sample", "Match Score"]

        # Create ranking column starting at 1
        results.index = results.index + 1
        results.index.name = "Rank"

        # Save to session state
        st.session_state["results"] = results

    except Exception as e:
        st.error("An unexpected error occurred during computation.")
        st.exception(e)


# Always display results if they exist
if st.session_state["results"] is not None:

    st.subheader("Ranked Match Results")

    st.dataframe(
        st.session_state["results"],
        use_container_width=True
    )

    # Prepare CSV
    csv_data = st.session_state["results"].reset_index().to_csv(index=False)

    st.download_button(
        label="Download Results as CSV",
        data=csv_data,
        file_name="tcga_match_results.csv",
        mime="text/csv"
    )
