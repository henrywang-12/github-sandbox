# References and intellectual context

This paper proposes an architectural synthesis. It does not claim to invent APIs, capability security, adaptive interfaces, distributed workflows, or agent tooling.

## HTTP semantics and idempotence

Fielding, Nottingham, and Reschke, **RFC 9110: HTTP Semantics** (2022), especially [§9.2.2, Idempotent Methods](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2).

Supports the distinction between HTTP method semantics and stronger claims about business-level execution. The workflow and approval model in this repository is a proposal beyond the RFC.

## Agent integration architecture

**Model Context Protocol, Architecture**, [specification snapshot dated 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18/architecture).

Describes hosts, clients, servers, context isolation, and protocol capability negotiation. MCP capability negotiation concerns supported protocol features; it must not be confused with the per-operation authority grants proposed in this paper. This is a dated reference, not a claim about the latest specification.

## Ecosystem-native agents: dated primary sources

The [comparative chapter](docs/ecosystem-native-agents.md), added October 27, 2026, uses these product sources:

- Tencent, [Weixin Mini Programs](https://www.tencent.com/products/weixin-mini-programs/): service categories and host distribution.
- Tencent Yuanqi, [Publishing agent Mini Programs to Official Accounts/service accounts](https://yuanqi.tencent.com/guide/publish-agent-mini-program-wechat), updated January 23, 2026 (Chinese): documented agent distribution surfaces.
- Alibaba, [Qwen ecosystem integration](https://www.alibabagroup.com/en-US/document-1948497434959151104), January 15, 2026: public testing of connected task and payment flows in China.
- Alibaba, [Taobao integration expansion](https://www.alibabagroup.com/en-US/document-1991231293551017984), May 11, 2026: catalog and commerce capabilities reported by the company.
- OpenAI, [Apps in ChatGPT launch](https://openai.com/index/introducing-apps-in-chatgpt/), October 6, 2025: conversational third-party app interfaces.
- Google, [Connected Apps rollout](https://blog.google/innovation-and-ai/products/gemini-app/new-connected-apps-gemini/), September 23, 2026: additional partner integrations.

Company announcements document reported capabilities and rollout claims, not independently measured comparative effectiveness. The architectural mechanism and concentration argument are the author's analysis; no source establishes inevitable monopoly or validate Walify's implementation.

## Scope of the argument

The predictions about interface unbundling, intent routing, and software economics are hypotheses developed here. These references do not establish those predictions or validates Walify's implementation. The repository includes no original empirical findings.
