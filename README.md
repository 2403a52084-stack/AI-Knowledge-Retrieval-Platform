## Milestone 4 – Testing, Analytics and Optimization

Milestone 4 focused on system evaluation, query analytics, knowledge gap detection, multi-domain testing, and retrieval optimization.

### M4.1 Query Analytics and Knowledge Gap Detection

The platform now records:

- User queries
- Query type
- Domain/routing
- Confidence score
- Response time
- Retrieved sources
- Retrieved chunk count
- Clarification requirement

A knowledge gap detector identifies unresolved and low-confidence queries.

Analytics data is stored in `analytics.db` and can be viewed through the `/analytics` dashboard.

### M4.2 End-to-End Testing

The system was tested across three domains:

- Education
- Technology
- Finance

Six test cases were evaluated, covering factual queries, comparative queries, ambiguous queries, and conversation memory.

**Test Pass Rate: 100% (6/6)**

### M4.3 Retrieval Optimization

Two retrieval configurations were compared.

| Metric | Baseline | Optimized |
|---|---:|---:|
| Top-K | 3 | 2 |
| Confidence Threshold | 0.40 | 0.55 |
| Domain Retrieval Accuracy | 100.0% | 100.0% |
| Average Top-1 Relevance | 0.6823 | 0.6823 |
| Average Retrieved Chunks | 3.00 | 1.75 |
| Average Response Time | 17.59 ms | 14.04 ms |

The optimized configuration reduced retrieved chunks by **41.67%** and improved average response time by **20.15%**, while maintaining the measured domain retrieval accuracy and Top-1 relevance.

### M4 Documentation

Detailed documentation is available in:



- `docs/m4_analytics.md`
- `docs/m4_end_to_end_testing.md`
- `docs/m4_optimization.md`
- `docs/final_report.md`