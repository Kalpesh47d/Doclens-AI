import streamlit as st
from loader import extract_text
from chunking import split_text
from vector_store import create_vector_store
from retriever import retrieve
from llm import get_answer

st.title("📄 RAG Document Assistant")

file = st.file_uploader("Upload document")

if "messages" not in st.session_state:
    st.session_state.messages = []

if file:
    text = extract_text(file)
    chunks = split_text(text)

    index, embeddings, chunk_list = create_vector_store(chunks)

    st.session_state["index"] = index
    st.session_state["embeddings"] = embeddings
    st.session_state["chunks"] = chunk_list

    st.success("Document processed!")

if "index" in st.session_state:

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input
    query = st.chat_input("Ask something...")

    if query:
        # Store user message
        st.session_state.messages.append({"role": "user", "content": query})

        with st.chat_message("user"):
            st.write(query)

        # Retrieve context
        results = retrieve(
            query,
            st.session_state["index"],
            st.session_state["chunks"],
            st.session_state["embeddings"]
        )

        contexts = [r[0] for r in results]

        # Get answer
        answer = get_answer(contexts, query)

        # Store assistant response
        st.session_state.messages.append({"role": "assistant", "content": answer})

        # Display answer
        with st.chat_message("assistant"):
            st.write(answer)

        # Show sources (optional but powerful)
        with st.expander("Sources"):
            for chunk, idx in results:
                st.write(f"Chunk {idx}: {chunk[:200]}...")