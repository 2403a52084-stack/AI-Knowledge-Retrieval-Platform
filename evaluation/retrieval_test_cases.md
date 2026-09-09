# Retrieval Test Cases

## Education Domain

| Test ID | Query | Expected Source | Expected Result |
|---|---|---|---|
| E1 | What is the minimum attendance requirement? | attendance_policy.pdf | Attendance requirement should be retrieved |
| E2 | What are the examination guidelines? | examination_guidelines.docx | Examination information should be retrieved |
| E3 | How is grading calculated? | grading_system.csv | Grading information should be retrieved |
| E4 | What are the academic rules? | academic_rules.txt | Academic rules should be retrieved |
| E5 | What happens when attendance is below the required percentage? | attendance_policy.pdf | Attendance shortage information should be retrieved |

---

## Technology Domain

| Test ID | Query | Expected Source | Expected Result |
|---|---|---|---|
| T1 | What is artificial intelligence? | artificial_intelligence.pdf | AI information should be retrieved |
| T2 | What is cloud computing? | cloud_computing.txt | Cloud computing information should be retrieved |
| T3 | What is cybersecurity? | cybersecurity_concepts.csv | Cybersecurity information should be retrieved |
| T4 | What is machine learning? | machine_learning_basics.docx | Machine learning information should be retrieved |
| T5 | What are the applications of artificial intelligence? | artificial_intelligence.pdf | AI application information should be retrieved |

---

## Procedural Query Tests

| Test ID | Query | Expected Source | Expected Result |
|---|---|---|---|
| P1 | What steps should a student follow for examination preparation? | examination_guidelines.docx | Relevant examination procedure should be retrieved |
| P2 | How is attendance monitored? | attendance_policy.pdf | Attendance procedure should be retrieved |
| P3 | How is a machine learning model trained? | machine_learning_basics.docx | Relevant machine learning procedure should be retrieved |

---

## Comparative Query Tests

| Test ID | Query | Expected Source | Expected Result |
|---|---|---|---|
| C1 | What is the difference between artificial intelligence and machine learning? | artificial_intelligence.pdf | Relevant comparison information should be retrieved |
| C2 | What is the difference between cloud computing and traditional computing? | cloud_computing.txt | Relevant comparison information should be retrieved |
| C3 | What is the difference between cybersecurity and artificial intelligence? | cybersecurity_concepts.csv | Relevant comparison information should be retrieved |

---

## Unavailable Query Tests

| Test ID | Query | Expected Result |
|---|---|---|
| U1 | What is the population of India? | System should indicate that information is unavailable |
| U2 | Who is the current Prime Minister of Canada? | System should not invent an answer |
| U3 | What is the price of Bitcoin today? | System should indicate that information is unavailable |

---

# Retrieval Evaluation

For each query, record:

- Top-1 retrieved source
- Top-3 retrieved sources
- Top-5 retrieved sources
- Whether the expected source was retrieved
- Relevance of retrieved chunks

## Evaluation Formula

### Top-K Accuracy

```text
Accuracy = (Correctly Retrieved Queries / Total Queries) × 100