# Milestone 2 Test Results

## M2.1 Query Understanding Agent

The Query Understanding Agent classifies user queries into:
- Factual
- Procedural
- Comparative
- Ambiguous

It returns:
- Query
- Query type
- Classification confidence
- Routing path

Example:
- "What is cloud computing?" → Factual
- "What is the difference between AI and machine learning?" → Comparative

## M2.2 Retrieval Agent

The Retrieval Agent performs semantic vector search using the existing RAG pipeline.

Features:
- Top-K retrieval
- Relevance scoring
- Ranking of retrieved chunks
- Configurable confidence threshold
- Low-confidence filtering
- Source metadata preservation
- Chunk identification
- Handling of unavailable information

Test result:
- Attendance information retrieved successfully.
- Cloud computing information retrieved successfully.
- AI and machine learning information retrieved successfully.
- Hostel fee query correctly returned a low-confidence response.

## M2.3 Response Generation Agent

The Response Generation Agent creates answers using retrieved knowledge-base content.

Features:
- Grounded responses
- Source attribution
- Confidence indicator
- Confidence score
- No-result handling

Example:

Question:
What is the minimum attendance requirement?

Answer:
Students are required to maintain a minimum attendance percentage of 75 percent.

Confidence:
Medium

Source:
data\education\attendance_policy.pdf

## M2.4 Multi-Agent Orchestration

The orchestration layer connects the agents sequentially:

Query Understanding
        ↓
Retrieval
        ↓
Response Generation

The orchestrator passes structured information between agents and handles classification, retrieval, and response errors.

## End-to-End Testing

The complete pipeline was tested using representative queries from the Education and Technology domains.

### Test Cases

1. What is the minimum attendance requirement?
   - Type: Factual
   - Status: Success
   - Confidence: Medium
   - Source: attendance_policy.pdf

2. What is cloud computing?
   - Type: Factual
   - Status: Success
   - Confidence: Medium
   - Source: cloud_computing.txt

3. What is the difference between AI and machine learning?
   - Type: Comparative
   - Status: Success
   - Confidence: Medium
   - Sources: artificial_intelligence.pdf and machine_learning_basics.docx

4. What is the hostel fee?
   - Type: Factual
   - Status: Low Confidence
   - Result: No sufficiently relevant information found.

## Conclusion

Milestone 2 successfully implements query classification, semantic retrieval, grounded response generation, source attribution, confidence indication, and sequential multi-agent orchestration.