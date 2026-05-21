# NOTES

## Design Decisions

I kept the client intentionally small and focused on testability rather than building a full SDK.

The code is separated into:
- `client.py` for public API operations,
- `transport.py` for HTTP concerns,
- `models.py` for typed request/response models,
- `exceptions.py` for domain-specific errors.

I used Pydantic models to avoid passing raw dictionaries through the client and to provide typed request/response contracts.

The transport layer handles:
- authentication headers,
- timeout handling,
- retry behavior for temporary server-side failures,
- HTTP error mapping to client-specific exceptions.

Integration tests create and clean up their own data to ensure repeatable execution and independence from test order.

## Tradeoffs

I intentionally avoided:
- async support,
- pagination support,
- advanced logging,
- generic abstractions,
- SDK-style architecture.

The goal was to keep the solution readable and pragmatic for the scope of the task.

## What I Would Add With More Time

With additional time I would add:
- pagination support,
- structured logging,
- richer validation error parsing,
- reusable long-lived HTTP client/session handling,
- CI pipeline example,
- contract/schema validation tests.

## LLM Usage

LLM assistance was mainly used for reviewing ideas, discussing tradeoffs, and helping refine parts of the README and NOTES documentation.

The implementation, debugging, API validation, and test behavior verification were done manually against the real API.