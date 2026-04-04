# RAG Project - Modular Structure

## Project Organization

The project is now organized into modular components for better maintainability:

```
RAG/
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   └── constants.py          # All configuration constants in one place
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── loader.py             # Document extraction logic
│   │   ├── chunking.py           # Text splitting logic
│   │   ├── vector_store.py       # Embedding and indexing (with model caching)
│   │   ├── retriever.py          # Semantic search logic
│   │   └── llm.py                # LLM API integration
│   │
│   ├── ui/
│   │   └── __init__.py
│   │
│   └── utils/
│       └── __init__.py
│
├── app.py                         # Main Streamlit application (updated imports)
├── requirements.txt
└── ...(other original files remain unchanged)
```

## Key Improvements

### 1. **Centralized Configuration** (`src/config/constants.py`)
- All magic numbers and model names are in one place
- Easy to adjust parameters:
  ```python
  CHUNK_SIZE = 500
  CHUNK_OVERLAP = 100
  LLM_TEMPERATURE = 0.3
  ```

### 2. **Module Organization** (`src/core/`)
- **loader.py**: Handles PDF, DOCX, XLSX extraction
- **chunking.py**: Text splitting with configurable parameters
- **vector_store.py**: FAISS embeddings with model caching
- **retriever.py**: Semantic search implementation
- **llm.py**: Groq API integration

### 3. **Model Caching** 
- Embedding model is cached in memory to avoid reloading
- Improves performance on subsequent requests

### 4. **Better Maintainability**
- Each module has a single responsibility
- Configuration is separate from logic
- Easy to test individual components
- Clear import paths in app.py

## Running the Application

```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run the Streamlit app
streamlit run app.py
```

## Importing Modules

The app now uses cleaner imports:
```python
from src.core.loader import extract_text
from src.core.chunking import split_text
from src.core.vector_store import create_vector_store
from src.core.retriever import retrieve
from src.core.llm import get_answer
```

## Future Enhancements

The modular structure makes it easy to:
- Add error handling and logging per module
- Create unit tests for each module
- Add new document formats (just extend `src/core/loader.py`)
- Swap LLM providers (just update `src/core/llm.py`)
- Add caching layer
- Implement batch processing

## Original Code Preserved

All original functionality is preserved - only reorganized for better structure. The logic in each module remains unchanged, ensuring the application works exactly as before.
