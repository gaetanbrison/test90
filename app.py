import streamlit as st
import pandas as pd
import fitz  # PyMuPDF for handling PDFs

# Load the dataset
uploaded_file = "merged.xlsx"  # Replace with the file path if hosted locally

@st.cache
def load_data(file_path):
    # Load the dataset
    df = pd.read_excel(file_path)
    return df

def extract_text_from_pdf(pdf_file):
    # Extract text from PDF file using PyMuPDF
    pdf_document = fitz.open(pdf_file)
    text = ""
    for page in pdf_document:
        text += page.get_text()
    pdf_document.close()
    return text

# Streamlit app layout
st.title("Dataset Viewer and PDF Upload")
st.sidebar.header("Options")

# File Upload
uploaded_pdfs = st.sidebar.file_uploader(
    "Upload PDF Documents", type="pdf", accept_multiple_files=True
)

if uploaded_pdfs:
    st.sidebar.subheader("Extracted Text from PDFs")
    for pdf in uploaded_pdfs:
        st.sidebar.write(f"**{pdf.name}**")
        pdf_text = extract_text_from_pdf(pdf)
        st.sidebar.text_area(f"Text from {pdf.name}", pdf_text, height=150)

# Load and display the dataset
df = load_data(uploaded_file)
st.subheader("Dataset")

# Search functionality in Abstract column
search_query = st.text_input("Search Abstracts")
if search_query:
    filtered_df = df[df["Abstract"].str.contains(search_query, case=False, na=False)]
else:
    filtered_df = df

# Display the dataframe
st.dataframe(filtered_df)

# Download the filtered dataset
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv",
)
