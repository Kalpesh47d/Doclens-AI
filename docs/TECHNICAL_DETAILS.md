# 💻 Code Walkthrough: Line by Line

Let's understand what each function does, step by step.

## 1. `extract_text()` - The File Reader

```python
def extract_text(uploaded_file):
    """Extract text from uploaded PDF, DOCX, or XLSX files."""
    text = ""

    if uploaded_file.name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text() or ""
```

**What happens:**
- Checks if file is PDF
- Opens PDF with PyPDF2 library
- Goes through each page one by one
- Extracts text from each page
- Adds all text together

**Why `or ""`?** Some PDF pages might be images only, so `extract_text()` returns `None`. We use empty string instead.

---

## 2. `split_text()` - The Text Cutter

```python
def split_text(text):
    """Split text into overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,      # Each piece is 500 characters
        chunk_overlap=100    # Pieces overlap by 100 characters
    )
    return splitter.split_text(text)
```

**What happens:**
- Creates a text splitter tool
- Sets chunk size to 500 characters
- Sets overlap to 100 characters
- Splits the text into pieces

**Why overlap?** Prevents important information from being cut in half.

---

## 3. `create_vector_store()` - The Number Converter

```python
def create_vector_store(chunks):
    model = get_embedding_model()  # Gets AI model (loads once)

    embeddings = model.encode(chunks)  # Convert text to numbers

    # Make all vectors the same "length" for fair comparison
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

    # Create search index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return index, embeddings, chunks
```

**What happens:**
1. Gets the AI model (cached, so fast after first time)
2. Converts each text chunk to a list of 384 numbers
3. Normalizes vectors (like making all arrows point same direction)
4. Creates FAISS search index
5. Adds all vectors to index for fast searching

---

## 4. `retrieve()` - The Smart Finder

```python
def retrieve(query, index, chunks, embeddings, k=3):
    """Find top-k most relevant chunks for the query."""
    model = get_embedding_model()

    # Convert question to same number format
    query_vec = model.encode([query])
    query_vec = query_vec / np.linalg.norm(query_vec, axis=1, keepdims=True)

    # Find 3 most similar chunks
    distances, indices = index.search(query_vec, k)

    results = []
    for i in indices[0]:
        results.append((chunks[i], i))  # (text, position)

    return results
```

**What happens:**
1. Convert question to vector (same as chunks)
2. Ask FAISS: "Find me the 3 closest vectors"
3. Get back distances and positions
4. Return the actual text chunks + their positions

---

## 5. `get_answer()` - The AI Writer

```python
def get_answer(context_chunks, query):
    """Use AI to generate answer from context."""
    context = "\n".join([str(c) for c in context_chunks])

    prompt = f"""You are an intelligent assistant.

Use ONLY the provided context to answer.
If answer is not found, say "Not found in document".

Context:
{context}

Question:
{query}

Answer:
"""

    # Send to Groq AI
    response = requests.post(LLM_API_ENDPOINT, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]
```

**What happens:**
1. Combine all relevant chunks into one text block
2. Create clear instructions for AI
3. Send question + context to Groq API
4. Get back AI-generated answer

---

## 6. Main App Flow (`app.py`)

```python
# When file uploaded:
if file:
    text = extract_text(file)              # Step 1: Read file
    chunks = split_text(text)              # Step 2: Cut text
    index, embeddings, chunk_list = create_vector_store(chunks)  # Step 3: Make searchable

# When question asked:
if query:
    results = retrieve(query, index, chunks, embeddings)  # Step 4: Find relevant parts
    contexts = [r[0] for r in results]                      # Step 5: Get text chunks
    answer = get_answer(contexts, query)                   # Step 6: Generate answer
```

**The complete journey:**
1. **File** → Text → Chunks → Vectors → Search Index
2. **Question** → Vector → Search → Relevant Chunks → AI → Answer

---

## 🔄 Data Transformations

### Text → Numbers
```
"Climate change affects weather patterns"
↓ (Sentence Transformer)
[0.23, -0.45, 0.12, 0.67, ...]  # 384 numbers
```

### Question Matching
```
Question: "How does climate affect weather?"
Vector:   [0.25, -0.42, 0.15, 0.69, ...]

Compares to all document chunk vectors
Finds closest matches using math
```

### AI Prompt
```
You are an intelligent assistant.
Use ONLY the provided context to answer.

Context:
Climate change affects weather patterns globally.
Rising temperatures cause more extreme weather events.

Question:
How does climate change affect weather?

Answer:
[AI generates response using only the context]
```

---

## 🎯 Key Concepts Made Simple

### Embeddings
- **What:** Converting words to numbers that capture meaning
- **Why:** Computers can compare numbers faster than text
- **How:** "Cat" and "feline" become similar numbers

### Vector Search
- **What:** Finding similar items in a collection
- **Why:** Traditional search finds exact words; vector search finds meaning
- **How:** Measures "distance" between number lists

### Normalization
- **What:** Making all vectors the same "length"
- **Why:** Fair comparison (like comparing directions, not speeds)
- **How:** Divide by vector length

### Overlapping Chunks
- **What:** Text pieces that share some content
- **Why:** Prevents cutting sentences in half
- **How:** Chunk 1 ends with "fox jumps", Chunk 2 starts with "jumps over"

---

## 🚀 Performance Secrets

- **Model Caching:** Load AI model once, reuse forever
- **FAISS Index:** Searches millions of vectors in milliseconds
- **Batch Processing:** Convert multiple chunks at once
- **API Efficiency:** Only call AI when needed

---

**Now you understand every line of code! 🎉**</content>
<parameter name="filePath">d:\projects\RAG\CODE_WALKTHROUGH.md