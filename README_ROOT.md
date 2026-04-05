# 📄 RAG Document Assistant

A **Retrieval Augmented Generation (RAG)** system that lets you upload documents and ask questions about them using AI.

## 📚 Documentation

All project documentation is organized in the [`docs/`](./docs/) folder:

- **[📖 Complete Guide](./docs/README.md)** - Full project documentation
- **[🚀 Quick Start](./docs/USAGE_GUIDE.md)** - Get started in 3 minutes
- **[🧠 How RAG Works](./docs/ARCHITECTURE.md)** - Visual explanations
- **[💻 Code Details](./docs/TECHNICAL_DETAILS.md)** - Line-by-line walkthrough
- **[📋 Reference](./docs/SUMMARY.md)** - Quick lookup guide

## 🎯 What It Does

Upload a document (PDF, Word, Excel) and ask questions about its content. The AI will provide accurate answers based only on your document.

## 🛠️ Quick Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Get free API key from https://groq.com
# Create .env file with your key

# Run the app
streamlit run app.py
```

## 📁 Project Structure

```
RAG/
├── app.py              # Main application
├── src/                # Modular source code
├── docs/               # 📚 Documentation
├── tests/              # Unit tests
├── deprecated/         # Old files (reference)
└── requirements.txt    # Dependencies
```

---

**📖 [Read the full documentation →](./docs/README.md)**</content>
<parameter name="filePath">d:\projects\RAG\README.md