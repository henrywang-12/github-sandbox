# References and intellectual context

This paper proposes an architectural synthesis. It does not claim to invent APIs, capability security, adaptive interfaces, distributed workflows, or agent tooling.

## HTTP semantics and idempotence

Fielding, Nottingham, and Reschke, **RFC 9110: HTTP Semantics** (2022), especially [§9.2.2, Idempotent Methods](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2).

Supports the distinction between HTTP method semantics and stronger claims about business-level execution. The workflow and approval model in this repository is a proposal beyond the RFC.

## Agent integration architecture

**Model Context Protocol, Architecture**, [specification snapshot dated 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18/architecture).

Describes hosts, clients, servers, context isolation, and protocol capability negotiation. MCP capability negotiation concerns supported protocol features; it must not be confused with the per-operation authority grants proposed in this paper. This is a dated reference, not a claim about the latest specification.

## Scope of the argument

The predictions about interface unbundling, intent routing, and software economics are hypotheses developed here. Neither reference establishes those predictions or validates Walify's implementation. The repository includes no original empirical findings.
