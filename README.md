# Development of AI-Based Knowledge Retrieval Platform with Query Resolution System

## 1. Project Overview

This project develops an AI-based knowledge retrieval platform using Retrieval-Augmented Generation (RAG) and a multi-agent query resolution architecture.

The system allows users to retrieve information from a knowledge base containing documents from Education and Technology domains.

Supported document formats:

- PDF
- DOCX
- TXT
- CSV

## 2. Main Features

- Knowledge-base document ingestion
- Text extraction and cleaning
- Text chunking
- Sentence Transformer embeddings
- ChromaDB vector storage
- Semantic retrieval
- RAG-based answer generation
- Multi-agent query resolution
- Conversation memory
- Clarification handling
- Web Speech API prototype

## 3. System Architecture

### Knowledge Base Flow

```text
PDF / DOCX / TXT / CSV
        ↓
Document Loader
        ↓
Text Cleaning
        ↓
Chunking
        ↓
Embedding Generation
        ↓
ChromaDB Vector Store