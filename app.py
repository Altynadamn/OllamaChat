import streamlit as st
from langchain_community.embeddings import OllamaEmbeddings
from llama_index.core.llms import ChatMessage
import logging
import time
from llama_index.llms.ollama import Ollama
import chromadb
from chromadb.config import Settings
import uuid
from sentence_transformers import SentenceTransformer
import tempfile
from langchain_community.document_loaders import PyPDFLoader
import os

logging.basicConfig(level=logging.INFO)

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
ollama_embedding = OllamaEmbeddings(model="all-minilm")
persist_directory = "./chroma_db"  
settings = Settings(persist_directory=persist_directory)
client = chromadb.Client(settings)
embeddings_collection = client.get_or_create_collection("embeddings")

if 'messages' not in st.session_state:
    st.session_state.messages = []

def generate_embeddings(texts):
    if isinstance(texts, str):
        texts = [texts]
    embeddings = embedding_model.encode(texts, convert_to_numpy=True).tolist()
    logging.info(f"Generated embeddings for {len(texts)} document(s). Sample embedding: {embeddings[0]}")
    return embeddings

def add_documents_to_collection(documents):
    ids = [str(uuid.uuid4()) for _ in documents]
    embeddings = generate_embeddings(documents)
    
    embeddings_collection.add(
        documents=documents,
        ids=ids,
        embeddings=embeddings,
        metadatas=[{"type": "document"} for _ in documents],
    )
    logging.info(f"Documents and embeddings added to ChromaDB. Total documents: {len(documents)}")

def query_documents(query):
    try:
        query_embedding = generate_embeddings(query)
        logging.info(f"Generated query embedding: {query_embedding[0]}")

        results = embeddings_collection.query(
            query_embeddings=query_embedding,
            n_results=3
        )
        
        documents = results.get("documents", [])
        logging.info(f"Query returned {len(documents)} documents.")
        return documents
    except Exception as e:
        logging.error(f"Error querying documents: {str(e)}")
        return []

def stream_chat(model, messages):
    try:
        llm = Ollama(model=model, request_timeout=120.0)
        resp = llm.stream_chat(messages)
        response = ""
        response_placeholder = st.empty()
        for r in resp:
            response += r.delta
            response_placeholder.write(response)
        logging.info(f"Model: {model}, Messages: {messages}, Response: {response}")
        return response
    except Exception as e:
        logging.error(f"Error during streaming: {str(e)}")
        raise e

def extract_text_from_file(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1].lower()
    if file_type == 'pdf':
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            loader = PyPDFLoader(temp_file.name)
            documents = loader.load()
        os.unlink(temp_file.name)  
        return [doc.page_content for doc in documents]
    elif file_type == 'txt':
        return [uploaded_file.read().decode('utf-8')]
    else:
        st.error("Unsupported file type. Please upload a PDF or TXT file.")
        return []

def main():
    st.title("Interactive RAG Chatbot")
    logging.info("App started")

    model = st.sidebar.selectbox("Choose a model", ["llama3.2"])
    logging.info(f"Model selected: {model}")

    st.sidebar.header("Upload Documents")
    uploaded_files = st.sidebar.file_uploader(
        "Upload .txt or .pdf files", type=["txt", "pdf"], accept_multiple_files=True
    )

    if uploaded_files:
        documents = []
        for uploaded_file in uploaded_files:
            try:
                logging.info(f"File uploaded: {uploaded_file.name}")
                content = extract_text_from_file(uploaded_file)
                if content:
                    documents.extend(content)
                    logging.info(f"Loaded document: {uploaded_file.name} with {len(content)} characters")
                else:
                    logging.warning(f"File {uploaded_file.name} is empty.")
            except Exception as e:
                logging.error(f"Error reading file {uploaded_file.name}: {str(e)}")

        if documents:
            add_documents_to_collection(documents)
            st.sidebar.success(f"Uploaded {len(uploaded_files)} file(s) and processed embeddings.")
        else:
            st.sidebar.warning("No valid content found in uploaded files.")

    if prompt := st.chat_input("Ask your question:"):
        relevant_docs = query_documents(prompt)
        flattened_docs = [doc for sublist in relevant_docs for doc in sublist] if relevant_docs else []
        logging.info(f"Relevant documents retrieved: {len(flattened_docs)}")

        context = "\n".join(flattened_docs) if flattened_docs else "No relevant documents found."
        prompt_with_context = f"Context: {context}\n\n{prompt}" if context else prompt

        st.session_state.messages.append({"role": "user", "content": prompt})
        logging.info(f"User input: {prompt}")

        with st.container():
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                logging.info("Generating response")

                with st.spinner("Assistant is typing..."):
                    try:
                        messages = [ChatMessage(role=msg["role"], content=msg["content"]) for msg in
                                    st.session_state.messages]
                        response_message = stream_chat(model, messages)

                        st.session_state.messages.append(
                            {"role": "assistant", "content": response_message})
                        st.write(response_message)
                    except Exception as e:
                        st.session_state.messages.append({"role": "assistant", "content": str(e)})
                        st.error("An error occurred while generating the response.")
                        logging.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
