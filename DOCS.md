# 📄 RAG Document Assistant

A **Retrieval Augmented Generation (RAG)** system that lets you upload documents and ask questions about them using AI. Built with Streamlit, FAISS, and Groq's LLM API.

## 🎯 What This Project Does

Imagine you have a long PDF document, Word file, or Excel spreadsheet. Instead of manually searching through it, you can:

1. **Upload** your document
2. **Ask questions** in natural language
3. **Get accurate answers** based only on your document's content

The system finds relevant information from your document and uses AI to generate helpful answers.

---

## 🧠 How RAG Works (Simple Explanation)

RAG combines two powerful AI techniques:

### **Step 1: Document Processing** 📚
- Extract text from your uploaded file (PDF, Word, Excel)
- Break the text into smaller chunks (like paragraphs)
- Convert text chunks into numbers (embeddings) that computers can understand

### **Step 2: Smart Search** 🔍
- When you ask a question, convert your question into the same "number format"
- Find the most similar text chunks from your document
- Use only the relevant chunks as context

### **Step 3: AI Answer Generation** 🤖
- Send your question + relevant document chunks to an AI model
- The AI generates an answer using only the provided context
- You get an accurate, document-based response

---

## 🏗️ Project Architecture

```
RAG Document Assistant
├── 📁 src/config/constants.py    # Settings & configuration
├── 📁 src/core/
│   ├── loader.py                 # Extract text from files
│   ├── chunking.py              # Split text into chunks
│   ├── vector_store.py          # Create searchable embeddings
│   ├── retriever.py             # Find relevant chunks
│   └── llm.py                   # Generate AI answers
└── app.py                       # Streamlit web interface
```

### Data Flow
```
Document Upload → Text Extraction → Text Chunks → Embeddings → Vector Store
                                                                       ↓
User Question → Question Embedding → Similarity Search → Relevant Chunks
                                                                       ↓
Relevant Chunks + Question → LLM → Answer
```

---

## 📖 Code Explanation (Easy to Understand)

### 1. **Configuration** (`src/config/constants.py`)

This file contains all the "magic numbers" and settings:

```python
# Which AI model to use for text embeddings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# How to split text (500 characters per chunk, 100 overlap)
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# LLM settings (Groq API)
LLM_MODEL = "llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0.3  # How creative the answers should be

# How many document chunks to retrieve for each question
DEFAULT_K = 3
```

**Why?** Keeps all settings in one place for easy changes.

---

### 2. **Document Loader** (`src/core/loader.py`)

**What it does:** Extracts text from uploaded files (PDF, Word, Excel).

```python
def extract_text(uploaded_file):
    """Extract text from uploaded PDF, DOCX, or XLSX files."""
    text = ""

    if uploaded_file.name.endswith(".pdf"):
        # Use PyPDF2 to read PDF pages
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text() or ""

    elif uploaded_file.name.endswith(".docx"):
        # Use python-docx to read Word paragraphs
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"

    elif uploaded_file.name.endswith(".xlsx"):
        # Use pandas to read Excel sheets
        xls = pd.ExcelFile(uploaded_file)
        for sheet in xls.sheet_names:
            df = xls.parse(sheet)
            # Convert all cells to text and join them
            df = df.fillna("").astype(str)
            for _, row in df.iterrows():
                text += " ".join(row.values) + "\n"

    return text
```

**Simple explanation:** Different file types need different "readers". This function detects the file type and uses the right tool to extract text.

---

### 3. **Text Chunking** (`src/core/chunking.py`)

**What it does:** Breaks long text into smaller, manageable pieces.

```python
def split_text(text):
    """Split text into overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,      # Each chunk is 500 characters
        chunk_overlap=100    # Chunks overlap by 100 characters
    )
    return splitter.split_text(text)
```

**Why overlap?** Imagine text: "The quick brown fox jumps over the lazy dog."

Without overlap:
- Chunk 1: "The quick brown fox jumps"
- Chunk 2: "over the lazy dog"

With overlap:
- Chunk 1: "The quick brown fox jumps"
- Chunk 2: "fox jumps over the lazy dog"

This ensures important information isn't split awkwardly.

---

### 4. **Vector Store** (`src/core/vector_store.py`)

**What it does:** Converts text chunks into searchable "vectors" (numbers).

```python
# Cache the AI model so we don't load it multiple times
_model_cache = None

def get_embedding_model():
    global _model_cache
    if _model_cache is None:
        _model_cache = SentenceTransformer(EMBEDDING_MODEL)
    return _model_cache

def create_vector_store(chunks):
    model = get_embedding_model()

    # Convert text chunks to numbers (embeddings)
    embeddings = model.encode(chunks)

    # Normalize vectors (make them unit length for better search)
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

    # Create FAISS index for fast searching
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return index, embeddings, chunks
```

**Simple explanation:**
- **Embeddings:** Convert words into numbers that capture meaning
- **Normalization:** Makes vectors comparable (like making all arrows point the same direction)
- **FAISS Index:** A super-fast search engine for finding similar vectors

---

### 5. **Retriever** (`src/core/retriever.py`)

**What it does:** Finds the most relevant text chunks for your question.

```python
def retrieve(query, index, chunks, embeddings, k=3):
    """Retrieve top-k relevant chunks for a query."""
    model = get_embedding_model()

    # Convert question to embedding (same format as chunks)
    query_vec = model.encode([query])
    query_vec = query_vec / np.linalg.norm(query_vec, axis=1, keepdims=True)

    # Find k most similar chunks using FAISS
    distances, indices = index.search(query_vec, k)

    results = []
    for i in indices[0]:
        results.append((chunks[i], i))  # (chunk_text, chunk_index)

    return results
```

**How it works:**
1. Convert your question to an embedding vector
2. Ask FAISS: "Find me the 3 most similar vectors"
3. Return the corresponding text chunks

---

### 6. **LLM Integration** (`src/core/llm.py`)

**What it does:** Uses AI to generate answers based on retrieved context.

```python
def get_answer(context_chunks, query):
    """Generate answer from LLM using context chunks and query."""
    # Combine all relevant chunks into one context string
    context = "\n".join([str(c) for c in context_chunks])

    # Create a clear prompt for the AI
    prompt = f"""You are an intelligent assistant.

Use ONLY the provided context to answer.
If answer is not found, say "Not found in document".

Context:
{context}

Question:
{query}

Answer:
"""

    # Send to Groq API
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": LLM_TEMPERATURE
    }

    response = requests.post(LLM_API_ENDPOINT, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]
```

**Why this approach?**
- **Context-limited:** AI only uses your document, not its training data
- **Accurate:** Answers are based on your specific document
- **Safe:** No hallucinations or made-up information

---

### 7. **Main Application** (`app.py`)

**What it does:** The web interface that ties everything together.

```python
# 1. Show file uploader
file = st.file_uploader("Upload document")

# 2. When file is uploaded:
if file:
    text = extract_text(file)           # Extract text
    chunks = split_text(text)           # Split into chunks
    index, embeddings, chunk_list = create_vector_store(chunks)  # Create searchable index

    # Store in session (memory)
    st.session_state["index"] = index
    st.session_state["chunks"] = chunk_list

# 3. When user asks a question:
if query:
    results = retrieve(query, index, chunks, embeddings)  # Find relevant chunks
    contexts = [r[0] for r in results]                     # Get chunk texts
    answer = get_answer(contexts, query)                  # Generate answer
```

---

## 🚀 How to Use

### Prerequisites
- Python 3.10+
- Groq API key (free at [groq.com](https://groq.com))

### Setup
```bash
# 1. Clone/download the project
cd rag-project

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key
# Create .env file with: GROQ_API_KEY=your_key_here

# 5. Run the app
streamlit run app.py
```

### Using the App
1. **Upload Document:** Click "Browse files" and select PDF, DOCX, or XLSX
2. **Wait for Processing:** App extracts text and creates search index
3. **Ask Questions:** Type questions in natural language
4. **Get Answers:** AI responds based only on your document
5. **View Sources:** Expand "Sources" to see which parts of the document were used

---

## 🔧 Technical Details

### Dependencies
- **Streamlit:** Web interface
- **PyPDF2:** PDF text extraction
- **python-docx:** Word document reading
- **pandas/openpyxl:** Excel file processing
- **sentence-transformers:** Text to vector conversion
- **faiss-cpu:** Fast vector similarity search
- **langchain:** Text splitting utilities
- **requests:** API calls to Groq

### Performance
- **Model Loading:** Embedding model cached after first use
- **Search Speed:** FAISS enables sub-second similarity search
- **Memory Usage:** Embeddings stored in RAM during session
- **API Calls:** Only made when generating answers

### Supported Formats
- **PDF:** All text-based PDFs
- **DOCX:** Microsoft Word documents
- **XLSX:** Excel spreadsheets (converts all cells to text)

### Limitations
- Only works with text content (no images/tables in PDFs)
- Document size limited by available RAM
- Requires internet for LLM API calls
- Session-based (data lost on refresh)

---

## 🎯 Key Benefits

### For Users
- **Easy:** Upload and ask questions naturally
- **Accurate:** Answers based only on your document
- **Fast:** Quick responses with smart search
- **Private:** No data sent to external servers (except LLM API)

### For Developers
- **Modular:** Each component can be modified independently
- **Extensible:** Easy to add new file formats or LLM providers
- **Maintainable:** Clear separation of concerns
- **Testable:** Each module can be tested separately

---

## 🔮 Future Improvements

- Add support for more file formats (TXT, CSV, images)
- Implement document persistence (save/load processed docs)
- Add conversation memory across sessions
- Support multiple documents simultaneously
- Add answer confidence scoring
- Implement caching for repeated questions
- Add export functionality for answers

---

## 📚 Learn More

### RAG Concepts
- **Retrieval Augmented Generation:** [Paper](https://arxiv.org/abs/2005.11401)
- **Embeddings:** Converting text to vectors
- **Vector Databases:** Storing and searching embeddings
- **Semantic Search:** Finding meaning, not just keywords

### Technologies Used
- **FAISS:** [Facebook AI Similarity Search](https://github.com/facebookresearch/faiss)
- **Sentence Transformers:** [Hugging Face](https://huggingface.co/sentence-transformers)
- **Groq:** [Fast LLM Inference](https://groq.com)

---

## 🤝 Contributing

The code is organized into modules for easy contribution:
- Add new file formats in `src/core/loader.py`
- Modify chunking strategy in `src/core/chunking.py`
- Change LLM provider in `src/core/llm.py`
- Update settings in `src/config/constants.py`

---

## 📄 License

This project is open source. Feel free to use and modify!

---

**Happy chatting with your documents! 📄🤖**</content>
<parameter name="filePath">d:\projects\RAG\README.md