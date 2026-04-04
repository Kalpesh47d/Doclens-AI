from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config.constants import CHUNK_SIZE, CHUNK_OVERLAP

def split_text(text):
    """Split text into overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    return splitter.split_text(text)
