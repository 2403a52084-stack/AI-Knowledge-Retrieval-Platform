# Multi-Agent Query Resolution Design

## 1. Overview

The system uses a multi-agent architecture in which different agents are responsible for different stages of query processing.

The Multi-Agent Orchestrator coordinates the agents and controls the overall query-resolution workflow.

---

## 2. Query Understanding Agent

### Responsibility
The Query Understanding Agent analyzes the user's question.

### Functions
- Identify the user's intent.
- Understand important keywords.
- Determine whether the query is clear or ambiguous.
- Prepare the query for retrieval.

### Input
User question.

### Output
Structured query containing:
- User intent
- Important keywords
- Query text
- Clarification requirement

---

## 3. Retrieval Agent

### Responsibility
The Retrieval Agent searches the knowledge base for relevant information.

### Functions
- Convert the query into an embedding.
- Perform semantic similarity search.
- Search the ChromaDB vector store.
- Retrieve the most relevant document chunks.
- Return retrieved context and metadata.

### Input
Processed user query.

### Output
Relevant document chunks with source information.

---

## 4. Response Generation Agent

### Responsibility
The Response Generation Agent generates the final answer using the retrieved context.

### Functions
- Read the retrieved context.
- Generate an answer relevant to the user's question.
- Avoid unsupported information.
- Present the answer clearly.

### Input
User query + retrieved context.

### Output
Final response.

---

## 5. Clarification Agent

### Responsibility
The Clarification Agent handles unclear or incomplete questions.

### Functions
- Detect ambiguous queries.
- Identify missing information.
- Ask the user a clarification question.
- Send the clarified query back for processing.

### Example

User:
"What is the attendance?"

Clarification Agent:
"Are you asking about the minimum attendance requirement?"

---

## 6. Conversation Memory Agent

### Responsibility
The Conversation Memory Agent maintains relevant information from the conversation.

### Functions
- Store previous queries and responses.
- Use previous context when required.
- Support follow-up questions.
- Maintain conversation continuity.

### Example

User:
"What is the minimum attendance?"

System:
"The minimum attendance requirement is ..."

User:
"What happens if I don't meet it?"

The memory agent helps the system understand that "it" refers to the attendance requirement.

---

## 7. Multi-Agent Orchestrator

### Responsibility

The Multi-Agent Orchestrator controls communication between the different agents.

### Workflow

User Query
↓
Query Understanding Agent
↓
Multi-Agent Orchestrator
↓
Check Query
↓
Clarification Agent (if required)
↓
Retrieval Agent
↓
Retrieved Context
↓
Response Generation Agent
↓
Final Answer
↓
Conversation Memory Agent

---

## 8. Agent Communication

| Agent | Input | Output |
|---|---|---|
| Query Understanding Agent | User Query | Processed Query |
| Retrieval Agent | Processed Query | Relevant Chunks |
| Response Generation Agent | Query + Context | Final Answer |
| Clarification Agent | Ambiguous Query | Clarification Question |
| Conversation Memory Agent | Conversation | Stored Context |
| Orchestrator | Agent Outputs | Next Agent / Final Result |

---

## 9. Query Resolution Flow

```text
User
  |
  v
Query Understanding Agent
  |
  v
Multi-Agent Orchestrator
  |
  +----> Query unclear?
  |          |
  |          v
  |    Clarification Agent
  |          |
  |          v
  |      User Input
  |
  v
Retrieval Agent
  |
  v
ChromaDB Vector Store
  |
  v
Relevant Context
  |
  v
Response Generation Agent
  |
  v
Final Answer
  |
  v
Conversation Memory Agent