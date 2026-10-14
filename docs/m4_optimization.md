# M4.3 Retrieval Optimization

## Objective

The objective of M4.3 is to optimize the retrieval component of the AI-Based Knowledge Retrieval Platform without reducing retrieval quality.

Two retrieval configurations were compared.

### Baseline Configuration

- Top-K: 3
- Confidence Threshold: 0.40

### Optimized Configuration

- Top-K: 2
- Confidence Threshold: 0.55

The same four queries from Education, Technology, and Finance domains were used for both configurations.

---

## Evaluation Queries

1. What is the minimum attendance percentage required?
2. What is cloud computing?
3. What is a savings account?
4. What is the difference between a savings account and a fixed deposit?

Each query was executed five times after a warm-up run.

---

## Baseline Results

| Metric | Baseline |
|---|---:|
| Top-K | 3 |
| Confidence Threshold | 0.40 |
| Domain Retrieval Accuracy | 100.0% |
| Average Top-1 Relevance | 0.6823 |
| Average Retrieved Chunks | 3.00 |
| Average Response Time | 17.59 ms |

---

## Optimized Results

| Metric | Optimized |
|---|---:|
| Top-K | 2 |
| Confidence Threshold | 0.55 |
| Domain Retrieval Accuracy | 100.0% |
| Average Top-1 Relevance | 0.6823 |
| Average Retrieved Chunks | 1.75 |
| Average Response Time | 14.04 ms |

---

## Optimization Impact

### Chunk Reduction

The optimized configuration reduced the average number of retrieved chunks from 3.00 to 1.75.

**Chunk Reduction = 41.67%**

### Response Time

The average response time decreased from 17.59 ms to 14.04 ms.

**Response Time Improvement = 20.15%**

### Top-1 Relevance

The average Top-1 relevance remained unchanged at 0.6823.

**Top-1 Relevance Change = 0.0%**

### Domain Retrieval Accuracy

Both configurations achieved 100% domain retrieval accuracy.

**Domain Accuracy Change = 0.0 percentage points**

---

## Comparison

| Metric | Baseline | Optimized | Improvement |
|---|---:|---:|---:|
| Domain Retrieval Accuracy | 100.0% | 100.0% | Maintained |
| Average Top-1 Relevance | 0.6823 | 0.6823 | 0.0% |
| Average Retrieved Chunks | 3.00 | 1.75 | 41.67% reduction |
| Average Response Time | 17.59 ms | 14.04 ms | 20.15% faster |

---

## Conclusion

The optimized retrieval configuration using Top-K = 2 and a confidence threshold of 0.55 improved system efficiency while maintaining the measured retrieval quality.

The system maintained 100% domain retrieval accuracy and the same average Top-1 relevance of 0.6823.

At the same time, the average number of retrieved chunks was reduced by 41.67% and the average response time improved by 20.15%.

Therefore, the optimized configuration was selected for the final system configuration.