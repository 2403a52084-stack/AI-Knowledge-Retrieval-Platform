# Final Milestone 4 Report

# Development of AI-Based Knowledge Retrieval Platform with Query Resolution System

## 1. Introduction

Milestone 4 focuses on improving the AI-Based Knowledge Retrieval Platform through query analytics, knowledge gap detection, multi-domain end-to-end testing, and retrieval optimization.

The system was evaluated using Education, Technology, and Finance knowledge domains.

---

## 2. M4.1 Query Analytics and Knowledge Gap Detection

The system was extended with a Query Analytics module to record and analyze user interactions.

The following information is tracked:

- Query text
- Timestamp
- Query type
- Routing/domain
- Query status
- Confidence score
- Clarification requirement
- Response time
- Retrieved sources
- Number of retrieved chunks

The system also includes a Knowledge Gap Detection module that identifies potentially unresolved or low-confidence queries.

Analytics data is stored in:

```text
analytics.db