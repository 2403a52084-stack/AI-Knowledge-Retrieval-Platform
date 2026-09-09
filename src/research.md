# Milestone 1 – Research and Technical Understanding

## 1. Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation (RAG) is an approach that combines information retrieval with Large Language Model (LLM) based response generation.

The RAG pipeline used in this project follows:

User Query → Query Embedding → Vector Search → Relevant Documents → Context → Answer Generation

RAG helps the system generate answers using information stored in the project knowledge base instead of depending only on the knowledge contained in the language model.

## 2. Multi-Agent Query Resolution

A multi-agent architecture divides the query resolution process into specialized agents.

The proposed agents are:

- Query Understanding Agent – understands the user's question and identifies the intent.
- Retrieval Agent – searches the knowledge base for relevant information.
- Response Generation Agent – generates the final answer using retrieved context.
- Clarification Agent – asks for additional information when the query is ambiguous.
- Conversation Memory Agent – maintains relevant information from previous interactions.
- Multi-Agent Orchestrator – controls communication and execution between the agents.

## 3. Embeddings

Embeddings convert text into numerical vectors that represent the semantic meaning of the text.

This project uses the Sentence Transformer model:

`all-MiniLM-L6-v2`

The generated vectors are stored in a vector database and used for semantic search.

## 4. Semantic Similarity

Semantic similarity measures how closely two pieces of text are related in meaning.

When a user enters a query, the query is converted into an embedding and compared with document chunk embeddings stored in the vector database.

The most relevant chunks are retrieved based on vector similarity.

## 5. Text Chunking

Large documents are divided into smaller chunks before generating embeddings.

The project uses recursive text splitting with:

- Chunk size: 500 characters
- Chunk overlap: 50 characters

Chunking improves retrieval by allowing the system to retrieve smaller and more relevant sections of documents.

## 6. Vector Database

ChromaDB is used as the vector database.

It stores:

- Document chunks
- Embeddings
- Metadata

The metadata can include the source filename, domain and chunk index.

## 7. Web Speech API

The Web Speech API can provide speech-based interaction through:

- Speech-to-Text (STT)
- Text-to-Speech (TTS)

Speech-to-Text allows users to provide queries using their voice.

Text-to-Speech allows the generated answer to be read aloud.

The Web Speech API is considered for the voice interaction component of the platform.

## 8. Technology Selection

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | User interface |
| LangChain | RAG/application framework |
| Sentence Transformers | Text embeddings |
| ChromaDB | Vector database |
| PyMuPDF | PDF text extraction |
| python-docx | DOCX processing |
| Pandas | CSV processing |
| Web Speech API | Voice interaction |

## 9. Proposed Architecture

The proposed system contains the following major components:

1. User Interface
2. Knowledge Base Upload
3. Document Processing Pipeline
4. Text Cleaning
5. Chunking
6. Embedding Generation
7. ChromaDB Vector Store
8. Multi-Agent Query Resolution
9. Retrieval
10. Response Generation
11. Answer Display

## 10. Architecture Decision

The project uses a modular architecture so that document ingestion, retrieval, answer generation and agent-based query resolution can be developed independently.

The initial implementation focuses on RAG-based knowledge retrieval. Multi-agent orchestration and voice interaction can be extended in later development stages.

## 11. Expected Benefits

The proposed system aims to:

- Retrieve relevant information from uploaded documents.
- Answer user queries using knowledge-base content.
- Support multiple document formats.
- Improve query resolution using specialized agents.
- Provide a foundation for voice-based interaction.
- Maintain source information for retrieved knowledge.