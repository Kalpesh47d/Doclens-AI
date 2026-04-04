from PyPDF2 import PdfReader
import docx 
import pandas as pd

def extract_text(uploaded_file):
    text = ""

    if uploaded_file.name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        for i, page in enumerate(reader.pages):
            text += page.extract_text() or ""

    elif uploaded_file.name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"

    elif uploaded_file.name.endswith(".xlsx"):
        xls = pd.ExcelFile(uploaded_file)
        for sheet in xls.sheet_names:
            df = xls.parse(sheet)
            
            df = df.fillna("").astype(str)
            for _, row in df.iterrows():
                text += " ".join(row.values) + "\n"
        
    return text



