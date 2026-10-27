# Ecosystem-native agents and the race for the web's execution layer

**Added October 27, 2026.** This chapter separates company-reported product capabilities, architectural inference, and the author's market hypothesis. It is not a comparative benchmark.

## 1. The US–China contrast is about the execution environment

A model's reasoning ability and an agent's practical usefulness are different quantities. Completing an everyday task also requires service discovery, authenticated access, meaningful action contracts, payment authorization, and reliable observation of the result.

China's super-app ecosystems provide an instructive setting: many services are already distributed through a familiar host or connected commercial network. An agent can potentially operate over an existing service substrate instead of reconstructing it from unrelated websites.

The contrast is not “China has ecosystems, the US has none.” US platforms also integrate services, and Chinese services retain separate permissions and business boundaries. The useful comparison is **ecosystem-native execution versus coordination across independently governed services**. Both patterns exist in both markets.

## 2. Tencent: service distribution before universal agency

Tencent describes [Weixin Mini Programs](https://www.tencent.com/products/weixin-mini-programs/) as services running inside Weixin, discoverable through search or QR codes, across shopping, dining, travel, and public-service use cases. Its [Yuanqi documentation](https://yuanqi.tencent.com/guide/publish-agent-mini-program-wechat), updated January 23, 2026, documents distributing agent Mini Programs through Official Accounts and service accounts, including article embeds and menus.

These establish a service-distribution substrate and documented agent entry points. They do **not** establish that one Tencent agent can autonomously invoke every Mini Program or complete arbitrary multi-service transactions.

The architectural inference is that embedding agents into an established host can reduce the cost of reaching users and locating services. Existing merchant relationships and familiar interaction surfaces can support adoption. Integration with identity or payment infrastructure still requires explicit authorization; co-location inside a super-app does not dissolve security boundaries.

## 3. Alibaba: connecting intention to commercial execution

Alibaba's [January 15, 2026 announcement](https://www.alibabagroup.com/en-US/document-1948497434959151104) described public testing in China of Qwen integrations spanning Taobao, instant commerce, Alipay, Fliggy, and Amap. Reported functions included food ordering, travel workflows, and user-confirmed in-chat payment for supported commerce flows.

Its [May 11, 2026 announcement](https://www.alibabagroup.com/en-US/document-1991231293551017984) described extending Qwen shopping to the Taobao/Tmall catalog and adding a Qwen shopping assistant within Taobao, with order, logistics, and after-sales capabilities.

The significant pattern is a conversational entry point connected to transaction infrastructure. Discovery, ordering, payment, and subsequent service can be coordinated through a connected commercial environment. “Ecosystem” here describes product integration and partnerships, not an assertion that every participating service has the same owner or authorization system.

These are Alibaba's product reports. They do not independently establish task-success rates, universal availability, or comparative agent performance.

## 4. The US: assembling ecosystems across service boundaries

OpenAI's [October 6, 2025 Apps launch](https://openai.com/index/introducing-apps-in-chatgpt/) introduced third-party apps with conversational and interactive interfaces inside ChatGPT. Google's [September 23, 2026 Connected Apps announcement](https://blog.google/innovation-and-ai/products/gemini-app/new-connected-apps-gemini/) described further partner integrations across productivity, creativity, and lifestyle services.

These examples challenge a simplistic opposition between Chinese super-apps and US standalone chatbots. US companies are also bringing service interaction into AI entry points. The commercial starting conditions differ: extending an established transaction ecosystem is different from negotiating access across independent providers.

| Dimension | Ecosystem-native route | Cross-provider route |
|---|---|---|
| Discovery | Host distribution and existing service catalogs | Partner integration, catalogs, protocols, or web discovery |
| Identity | Host identity can help, subject to service scope | Account linking and delegated access across providers |
| Execution | Native integrations can expose domain actions | APIs and partner tools; UI automation where necessary |
| Verification | Order and service records may be directly available | Evidence must be reconciled across providers |
| Reach | Deep coverage inside participating services | Potentially broader reach with uneven integration depth |
| Governance | Host can coordinate standards and restrict access | More negotiation and more independent failure domains |

These are architectural tendencies, not country-wide measurements or claims that all integrations behave alike.

## 5. Why the environment can outperform a model upgrade

Consider a workflow with several required steps. By the probability chain rule:

$$
P(\text{success}) = \prod_{i=1}^{n} P(S_i \mid S_1,\ldots,S_{i-1})
$$

Here each conditional probability concerns a step succeeding given prior steps succeeded. No independence assumption is required.

For illustration, ten required steps each with conditional success probability 0.95 yield roughly 0.60 end-to-end success; ten at 0.99 yield roughly 0.90. These are hypothetical values, not measurements of Tencent, Alibaba, or any US product. Real workflows have retries, branching, and shared failure causes.

The implication is that improving service access, state visibility, and transaction semantics can materially improve practical reliability even with the same model. Reducing unnecessary handoffs can also simplify the workflow. A structured integration may outperform a stronger model forced to infer state from changing screens.

This is the sense in which agents *can* be substantially more effective inside a well-integrated ecosystem. Demonstrating how much more effective requires matched tasks, comparable models, independent outcome verification, and explicit accounting for approval and recovery effort.

## 6. The opportunity: bring ecosystem coherence to the web

My thesis is that the next important software platform could reproduce the coordination advantages of a super-app across independently operated web services.

The scarce layer would combine:

- discovery of executable capabilities;
- scoped identity and delegation;
- consistent review and approval surfaces;
- transaction and recovery semantics;
- durable evidence of completed effects;
- distribution that makes joining worthwhile for service providers.

This is harder than adding a chat interface or publishing a tool schema. Providers must expose dependable actions and have an incentive to participate. Users must be able to inspect and revoke authority. Cross-provider errors still require reconciliation.

For Walify, this is a public strategic direction to investigate, not a claim of an existing universal execution layer. The potential advantage is the combination of a usable human environment and services agents can act on through explicit contracts.

## 7. The monopoly hypothesis: control the intent gateway

The strongest version of my market thesis is that an early platform achieving sufficient coverage, trusted execution, and habitual usage could become the default gateway between user intention and digital services.

A possible feedback loop is:

**More useful services → more completed tasks → more habitual users → stronger provider incentive to integrate → more useful services.**

This is a cross-side network-effect hypothesis. Outcomes could also inform reliability improvements where data access, consent, and engineering permit; more usage does not automatically improve the model or the product.

If users route most tasks through one gateway, that gateway can influence which providers are discovered, ranked, and invoked. Distribution, saved preferences, delegated relationships, and workflow history could make switching costly. A company might capture substantial platform power without owning all underlying services.

I therefore expect strong concentration pressure if this format succeeds. But “the first company to launch becomes a monopoly” is too strong. Timing alone does not create defensibility. Incumbent distribution, provider resistance, multi-homing, portable identity, open standards, specialized alternatives, and competition policy could constrain concentration. An open protocol may spread the format while preventing one operator from owning it.

The defensible prediction is **winner-takes-most potential under specific conditions**, rather than inevitable monopoly. Here monopoly describes the hypothesized extreme of platform concentration, not a legal finding about any company.

## 8. What would test this extension?

Compare the same model on matched tasks through native integrations and browser-driven workflows. Report verified success, time, user interventions, duplicate effects, and unresolved outcomes. Count integration development and maintenance costs.

Then test the economics separately: do additional services increase user retention and task completion, and does increased demand attract more providers? Can users and providers use several gateways without substantial switching costs?

The ecosystem advantage and the monopoly hypothesis are distinct claims. Evidence for easier execution does not establish market tipping. The architectural opportunity is credible enough to investigate; the market outcome remains contingent.
