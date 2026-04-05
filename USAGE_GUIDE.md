# 🚀 Quick Start Guide

## In 3 Minutes: Upload Document → Ask Questions → Get Answers

### Step 1: Setup (2 minutes)
```bash
# Install Python dependencies
pip install -r requirements.txt

# Get free Groq API key at https://groq.com
# Create .env file:
echo "GROQ_API_KEY=your_api_key_here" > .env

# Run the app
streamlit run app.py
```

### Step 2: Use the App (1 minute)
1. **Open browser** (Streamlit shows the URL)
2. **Upload document** (PDF/Word/Excel)
3. **Wait for "Document processed!"** message
4. **Ask questions** like:
   - "What is the main topic?"
   - "Summarize the key points"
   - "What are the conclusions?"

### Step 3: Get Smart Answers
- AI reads your document
- Finds relevant sections
- Generates accurate answers
- Shows source chunks

---

## 📋 What You Need

| Requirement | Details |
|-------------|---------|
| **Python** | 3.10 or higher |
| **API Key** | Free from [groq.com](https://groq.com) |
| **Files** | PDF, DOCX, or XLSX documents |
| **Internet** | For LLM API calls |

---

## 🎯 Example Usage

**Document:** A research paper about climate change
**Questions you can ask:**
- "What are the main findings?"
- "What methodology was used?"
- "What are the limitations?"
- "Summarize the conclusions"

**Answers:** Based only on your document content!

---

## 🔧 Troubleshooting

### "API Key Error"
- Check `.env` file exists
- Verify key is correct
- No spaces around `=`

### "Document Not Processing"
- Ensure file is PDF/DOCX/XLSX
- Check file isn't corrupted
- Try smaller files first

### "No Answer Found"
- Try rephrasing your question
- Check if answer exists in document
- Use more specific terms

---

## 📊 Understanding the Results

### What You See:
- **Answer:** AI-generated response
- **Sources:** Document chunks used
- **Chat History:** Previous Q&A

### Behind the Scenes:
1. Your question → converted to numbers
2. Numbers compared to document chunks
3. Top 3 similar chunks selected
4. AI uses those chunks to answer

---

## 💡 Pro Tips

- **Be specific:** "What are the three main benefits?" vs "Tell me about benefits"
- **Use document terms:** Match vocabulary from your document
- **Try variations:** If one question doesn't work, rephrase it
- **Check sources:** Expand "Sources" to see what the AI read

---

**Ready to chat with your documents! 🎉**</content>
<parameter name="filePath">d:\projects\RAG\QUICK_START.md