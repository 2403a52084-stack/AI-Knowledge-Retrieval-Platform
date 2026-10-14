# M4.1 Query Analytics and Knowledge Gap Detection

## Objective

The Query Analytics module records user interactions with the AI-Based Knowledge Retrieval Platform and helps identify potential knowledge gaps in the available dataset.

## Analytics Tracked

The system records:

- Query text
- Timestamp
- Query type
- Routing/domain
- Query status
- Confidence score
- Whether clarification was required
- Response time
- Retrieved sources
- Number of retrieved chunks

## Knowledge Gap Detection

The Knowledge Gap Detection module identifies queries that may require additional knowledge.

Potential knowledge gaps are detected using:

- Low retrieval confidence
- Unresolved queries
- Repeated low-confidence queries

These queries can be used to identify missing or insufficient knowledge sources.

## Analytics Database

Analytics information is stored in:

```text
analytics.db