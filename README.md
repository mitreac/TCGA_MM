# TCGA matchmaker

Matching a gene expression profile in TCGA cancer samples

- Input: gene expression profile for a sample, one column matrix with the sample on the column and genes on the rows and gene expression values for each of the genes as the data
  link to TCGA to download the sample profiles or a matrix with the sample profiles to check for a match
- Output: Ids and scores for highest matching TCGA samples.

To build the package use the following command in the top level folder of the cloned repo:
python -m build

### Dependencies

- python
- pandas
- numpy
- streamlit
