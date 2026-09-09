# Retrieval Evaluation Report

## 1. Objective

The objective of this evaluation is to measure how effectively the RAG system retrieves relevant knowledge-base documents for user queries.

The evaluation covers two domains:

- Education
- Technology

The system retrieves the most relevant document chunks using semantic similarity search.

---

## 2. Evaluation Metrics

### Top-1 Accuracy

Measures whether the correct source is retrieved as the first result.

### Top-3 Accuracy

Measures whether the correct source appears within the first three results.

### Top-5 Accuracy

Measures whether the correct source appears within the first five results.

### Formula

Accuracy = (Number of Correctly Retrieved Queries / Total Queries) × 100

---

## 3. Education Domain Test Cases

| Test ID | Query | Expected Source | Top-1 | Top-3 | Top-5 |
|---|---|---|---|---|---|
| E1 | What is the minimum attendance requirement? | attendance_policy.pdf | PASS | PASS | PASS |
| E2 | What are the examination guidelines? | examination_guidelines.docx | - | - | - |
| E3 | How is grading calculated? | grading_system.csv | - | - | - |
| E4 | What are the academic rules? | academic_rules.txt | - | - | - |

---

## 4. Technology Domain Test Cases

| Test ID | Query | Expected Source | Top-1 | Top-3 | Top-5 |
|---|---|---|---|---|---|
| T1 | What is artificial intelligence? | artificial_intelligence.pdf | - | - | - |
| T2 | What is cloud computing? | cloud_computing.txt | - | - | - |
| T3 | What is cybersecurity? | cybersecurity_concepts.csv | - | - | - |
| T4 | What is machine learning? | machine_learning_basics.docx | - | - | - |

---

## 5. Current Observed Result

For the attendance query:

**Query:**

What is the minimum attendance requirement?

**Retrieved Result 1:**

`data\education\attendance_policy.pdf`

This confirms that the relevant attendance document is retrieved as the first result.

---

## 6. Evaluation Results

The retrieval evaluation was performed using 8 test queries across the Education and Technology domains.

| Metric | Accuracy |
|---|---|
| Top-1 Accuracy | 87.50% |
| Top-3 Accuracy | 100.00% |
| Top-5 Accuracy | 100.00% |
---

## 7. Low-Relevance Results

Some queries may return documents that are related to the query but are not the ideal source.

Possible reasons include:

- Similar wording between documents.
- Limited knowledge-base content.
- Semantic similarity between different topics.
- Small chunk size.
- Absence of query filtering by domain.

---

## 8. Limitations

The current system has the following limitations:

1. The retrieval system uses a fixed top-k value.
2. Query understanding is not yet fully agent-based.
3. Clarification handling is not implemented.
4. Conversation memory is not implemented.
5. Retrieval evaluation uses a limited number of test queries.
6. Voice-based interaction is not yet fully integrated.

---

## 9. Planned Improvements

Future improvements include:

- Multi-agent query orchestration.
- Query intent classification.
- Clarification agent.
- Conversation memory.
- Better retrieval ranking.
- Confidence scoring.
- Web Speech API integration.
- Larger and more diverse evaluation datasets.

---

## 10. Conclusion

The retrieval system successfully demonstrates semantic search over the project knowledge base.

The system can retrieve relevant information from multiple document formats and knowledge domains.

Further evaluation and multi-agent improvements will be carried out in subsequent development milestones.