# M4.2 End-to-End Testing

## Objective

The AI-Based Knowledge Retrieval Platform was tested across three distinct knowledge domains:

- Education
- Technology
- Finance

The objective was to verify retrieval, query resolution, ambiguity handling, and conversation memory.

## Test Cases

| Test | Query | Domain | Result |
|---|---|---|---|
| 1 | What is the minimum attendance percentage required? | Education | PASS |
| 2 | What is cloud computing? | Technology | PASS |
| 3 | What is a savings account? | Finance | PASS |
| 4 | What is the difference between a savings account and a fixed deposit? | Finance | PASS |
| 5 | Finance | Ambiguous Query | PASS |
| 6 | What are its services? | Conversation Memory | PASS |

## Result

All six automated end-to-end test cases completed successfully.

**Passed: 6/6**

**Test Pass Rate: 100%**

## Conclusion

The platform successfully handled queries from multiple knowledge domains and demonstrated successful retrieval, comparative queries, ambiguous-query handling, and conversation-memory processing.