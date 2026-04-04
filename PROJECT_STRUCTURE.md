# Project Structure Overview

## 📁 Root Directory (`/`)

**Active Application Files:**
- `app.py` - Main Streamlit application (uses src/ modules)
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (API keys, etc.)
- `.gitignore` - Git ignore rules
- `MODULAR_STRUCTURE.md` - Modular architecture documentation

**Directories:**
- `src/` - **Main application code (use this)**
- `tests/` - Unit test files
- `logs/` - Application logs
- `venv/` or `.venv/` - Python virtual environment
- `deprecated/` - Old module files (kept for reference)

---

## 🚀 Active Codebase (`src/`) - USE THIS

```
src/
├── config/
│   ├── __init__.py
│   └── constants.py          # Configuration constants and settings
│
├── core/                      # Core business logic modules
│   ├── __init__.py
│   ├── loader.py             # Extract text from PDF, DOCX, XLSX
│   ├── chunking.py           # Split text into chunks
│   ├── vector_store.py       # Create embeddings and FAISS index
│   ├── retriever.py          # Semantic search functionality
│   └── llm.py                # Groq LLM API integration
│
├── ui/                        # User interface modules
│   └── __init__.py
│
└── utils/                     # Utility modules
    └── __init__.py
```

### Module Responsibilities

| Module | Purpose | Key Function(s) |
|--------|---------|-----------------|
| `config/constants.py` | Centralized settings | Model names, chunk sizes, API endpoints |
| `core/loader.py` | Document loading | `extract_text()` - handles PDF, DOCX, XLSX |
| `core/chunking.py` | Text splitting | `split_text()` - chunks text with overlap |
| `core/vector_store.py` | Embeddings & indexing | `create_vector_store()` - creates FAISS index with cached model |
| `core/retriever.py` | Search & retrieval | `retrieve()` - k-NN semantic search |
| `core/llm.py` | LLM integration | `get_answer()` - queries Groq API |

---

## 📦 Deprecated Files (`deprecated/`) - DO NOT USE

Old files kept for reference only:
- `chunking.py` → moved to `src/core/chunking.py`
- `loader.py` → moved to `src/core/loader.py`
- `llm.py` → moved to `src/core/llm.py`
- `retriever.py` → moved to `src/core/retriever.py`
- `vector_store.py` → moved to `src/core/vector_store.py`
- `RAG_Project.py` → old configuration file

**These are archived for reference only. Use the `src/` modules instead.**

---

## 🎯 How to Run

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Run the application
streamlit run app.py
```

## 📝 Imports

All imports in `app.py` now use the modular structure:

```python
from src.core.loader import extract_text
from src.core.chunking import split_text
from src.core.vector_store import create_vector_store
from src.core.retriever import retrieve
from src.core.llm import get_answer
```

---

## ✅ Structure Benefits

- **Organized**: Clear separation of concerns
- **Maintainable**: Easy to locate and update specific functionality
- **Scalable**: Simple to add new modules
- **Testable**: Each module can be tested independently
- **Clean**: No duplicate/legacy files cluttering the root directory

---

## 📌 Next Steps

To further improve the codebase, consider:
1. Adding error handling and logging to modules
2. Creating unit tests in `tests/` folder
3. Adding type hints to functions
4. Creating `src/__init__.py` for package initialization
5. Extending `src/ui/` for future UI components
