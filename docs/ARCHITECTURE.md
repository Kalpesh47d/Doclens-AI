# 🧠 RAG Flow Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   USER UPLOADS  │    │  TEXT EXTRACTED │    │   TEXT CHUNKED  │
│     DOCUMENT    │───▶│   FROM FILE     │───▶│  INTO PIECES    │
│   (PDF/DOCX)    │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                         │
┌─────────────────┐    ┌─────────────────┐               │
│  USER ASKS      │    │ QUESTION        │               ▼
│   QUESTION      │───▶│ CONVERTED TO    │    ┌─────────────────┐
│                 │    │   NUMBERS       │    │   CHUNKS MADE    │
└─────────────────┘    └─────────────────┘    │  SEARCHABLE      │
                                                         │
┌─────────────────┐    ┌─────────────────┐    │   (EMBEDDINGS)   │
│   AI FINDS      │    │  MOST SIMILAR   │◀───│                 │
│  RELEVANT       │◀───│   CHUNKS        │    └─────────────────┘
│   CHUNKS        │    │   FOUND         │
└─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ QUESTION +      │    │   SENT TO AI    │    │   AI GENERATES   │
│ RELEVANT CHUNKS │───▶│   (GROQ API)    │───▶│   ACCURATE       │
│                 │    │                 │    │   ANSWER         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐
│   USER SEES     │
│   ANSWER +      │
│   SOURCES       │
└─────────────────┘
```

## Step-by-Step Explanation

### Phase 1: Document Preparation
1. **Upload:** User uploads PDF, Word, or Excel file
2. **Extract:** Text is pulled from the file using specialized libraries
3. **Chunk:** Long text is broken into smaller pieces (500 chars each)

### Phase 2: Making Searchable
4. **Embed:** Each chunk is converted to "numbers" (vectors) that capture meaning
5. **Index:** Vectors stored in FAISS for super-fast searching

### Phase 3: Question Processing
6. **Question:** User types a question
7. **Convert:** Question also becomes a vector (same format as chunks)
8. **Search:** Find 3 most similar chunk vectors

### Phase 4: Answer Generation
9. **Context:** Top chunks + question sent to AI
10. **Generate:** AI creates answer using only provided context
11. **Display:** User sees answer + source chunks

---

## Key Technologies

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Text Extraction** | PyPDF2, python-docx, pandas | Read different file formats |
| **Text Chunking** | LangChain | Split text intelligently |
| **Embeddings** | Sentence Transformers | Convert text to vectors |
| **Vector Search** | FAISS | Find similar vectors quickly |
| **AI Generation** | Groq API | Generate natural language answers |

---

## Why This Works

- **Semantic Search:** Finds meaning, not just keywords
- **Context-Aware:** AI uses your document, not general knowledge
- **Efficient:** FAISS can search millions of chunks in milliseconds
- **Accurate:** Only answers based on your specific document

---

## Performance Numbers

- **Document Processing:** ~5-30 seconds (depends on size)
- **Question Answering:** ~2-5 seconds
- **Search Speed:** < 1 millisecond for similarity search
- **Memory Usage:** ~100MB per 1000 text chunks</content>
<parameter name="filePath">d:\projects\RAG\RAG_EXPLANATION.md