# System Architecture

## AI-Based Knowledge Retrieval Platform with Query Resolution System

```mermaid
flowchart TD

    A[User] --> B[Streamlit User Interface]

    B --> C{User Action}

    C -->|Upload Document| D[Document Upload Module]

    D --> E[Document Loader]

    E --> F[Text Cleaning]

    F --> G[Text Chunking]

    G --> H[Embedding Generation]

    H --> I[(ChromaDB Vector Store)]

    C -->|Ask Question| J[Query Understanding Agent]

    J --> K[Multi-Agent Orchestrator]

    K --> L[Retrieval Agent]

    L --> M[Query Embedding]

    M --> I

    I --> N[Relevant Document Chunks]

    N --> L

    L --> O[Response Generation Agent]

    O --> P[LLM / Answer Generator]

    P --> Q[Final Answer]

    Q --> B

    J --> R[Clarification Agent]

    R --> B

    K --> S[Conversation Memory Agent]

    S --> K

    B --> T[Web Speech API]

    T -->|Speech-to-Text| J

    Q --> T

    T -->|Text-to-Speech| U[Voice Response]