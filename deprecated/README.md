# Deprecated - Old Files

This folder contains the original module files that have been reorganized into the `src/` directory structure.

## What's Here

These are the original, unmodified files from before the refactoring:
- `chunking.py` - Text chunking (→ `src/core/chunking.py`)
- `loader.py` - Document loading (→ `src/core/loader.py`)
- `llm.py` - LLM integration (→ `src/core/llm.py`)
- `retriever.py` - Document retrieval (→ `src/core/retriever.py`)
- `vector_store.py` - Vector store creation (→ `src/core/vector_store.py`)
- `RAG_Project.py` - Old configuration file

## Why They're Here

These files are kept for reference only. They show the original code before refactoring into the modular structure.

## Do NOT Use These Files

❌ **Do not import from this folder**
❌ **Do not use any code from here**  
✅ **Use `src/` folder instead**

The application now imports from `src/core/` and `src/config/`, which contain the same logic but organized for better maintainability.

## Can I Delete Them?

Yes! Once you're confident the refactored code in `src/` is working correctly, this entire `deprecated/` folder can be safely deleted or archived.

## Git

If you want to keep git history, you can delete this folder. Git will maintain the history of these files in the commit where they were moved.

```bash
git rm -r deprecated/
git commit -m "Remove deprecated folder after successful refactoring"
```
