# Why AI Agent Assembly?

**AI Agent Assembly is a governance layer for AI agents** — a control that sits in the agent's action path and *enforces* policy, tracks cost, and intercepts unsafe actions (unsafe tool calls, network egress, and budget overruns) *before* they execute. Think of it as a security checkpoint in front of each *governed* agent action — the tool calls your SDK wraps and the outbound requests routed through its proxy — not a dashboard that reports on actions after they happen. Which actions reach that checkpoint depends on how the agent is wired up and launched; see [Known limitations](https://docs.agent-assembly.com/core/latest/devtools/limitations.html). That category distinction is what this comparison is about.

This page helps readers see where AI Agent Assembly fits next to other tools in the AI governance and observability space. All competitor data is taken from each vendor's public documentation as of 2026-05-05.

In short: most tools in this space **observe** what an agent did after the fact. AI Agent Assembly is built to **enforce** policy before an action runs. The sections below show where that difference matters, and where competitors are ahead.

---

## Feature matrix

Because AI Agent Assembly is an **enforcement** control rather than a pure observability or monitoring tool, the rows below span both categories: the observability rows show that it still gives you the visibility those tools provide, while the policy-enforcement, access-control, and budget-enforcement rows show the security-checkpoint capabilities that monitoring-only tools do not have. Read the matrix with that framing — equal coverage on observability, decisive coverage on enforcement.

Each row is a capability. The columns are AI Agent Assembly (AAASM), Langfuse, Helicone, Opik, and Pillar Security.

Legend: ✓ = full support · partial = limited or gated behind a paid tier · ✗ = not available · n/a = not applicable to the product category.

> 🚧 **Coming soon.** Rows marked ✓ 🚧 in the AAASM column describe the AAA-Commercial (Enterprise) tier and the paid SaaS platform that delivers it — both are planned and not yet generally available. See [Open core boundary](open-core-boundary.md) for what ships today versus what is intended design.

| Capability | AAASM | Langfuse | Helicone | Opik | Pillar Security |
|---|---|---|---|---|---|
| **Observability** | | | | | |
| LLM call tracing (latency, tokens, cost) | ✓ | ✓ | ✓ | ✓ | partial |
| Multi-turn conversation tracing | ✓ | ✓ | partial | ✓ | ✗ |
| Agent lineage / parent-child spans | ✓ | ✓ | ✗ | partial | ✗ |
| SIEM export (JSON / CEF) | ✓ 🚧 | ✗ | ✗ | ✗ | partial |
| **Policy enforcement** | | | | | |
| Pre-execution allow / deny (runtime block) | ✓ | ✗ | ✗ | ✗ | partial |
| Policy-as-code (YAML / JSON versioned rules) | ✓ | ✗ | ✗ | ✗ | ✗ |
| Network-level interception (no agent code change) [^proxy] | ✓ (aa-proxy) | ✗ | ✗ | ✗ | ✗ |
| Kernel-level bypass detection (eBPF) [^ebpf] | ✓ | ✗ | ✗ | ✗ | ✗ |
| PII / secret detection at gateway | ✓ (regex rules) | partial (post-hoc) | ✗ | partial (evaluators) | ✓ |
| **Vault-backed secrets management** | | | | | |
| Secrets vault integration | ✗ | ✗ | ✗ | ✗ | ✓ |
| Secret scanning in prompts / outputs | partial (regex policy) | ✗ | ✗ | ✗ | ✓ |
| **Multi-language SDK** | | | | | |
| Python SDK | ✓ | ✓ | ✓ | ✓ | ✓ |
| TypeScript SDK | ✓ | ✓ | ✓ | ✓ | partial |
| Go SDK | ✓ | ✗ | ✗ | ✗ | ✗ |
| **BYO-LLM (provider agnostic)** | | | | | |
| Works with any LLM provider | ✓ | ✓ | ✓ | ✓ | ✓ |
| Open-source SDK core (Apache-2.0) | ✓ | ✓ (MIT) | ✗ | ✓ (Apache-2.0) | ✗ |
| **Access control (RBAC)** | | | | | |
| Role-based access control | ✓ 🚧 (Owner/Admin/Developer/Viewer) | partial | partial | partial | ✓ |
| SAML 2.0 / OIDC SSO | ✓ 🚧 | partial (Enterprise) | partial (Enterprise) | partial (Enterprise) | ✓ |
| SCIM user provisioning | ✓ 🚧 | ✗ | ✗ | ✗ | partial |
| **Approval workflows** | | | | | |
| Human-in-the-loop approval gates | partial (policy deny; alerting 🚧) | ✗ | ✗ | ✗ | ✓ |
| Automated approval routing | ✗ | ✗ | ✗ | ✗ | ✓ |
| **Cost analytics** | | | | | |
| Per-team token / cost budgets (enforced) | ✓ | partial (tracking only) | ✓ (tracking + alerts) | partial (tracking only) | ✗ |
| Budget enforcement (hard deny on exceed) | ✓ | ✗ | ✗ | ✗ | ✗ |
| **Audit log integrity** | | | | | |
| Hash-chained, verifiable audit log [^audit] | partial (unkeyed SHA-256 chain over the JSONL sink) | ✗ | ✗ | ✗ | partial |
| Audit log retention > 30 days | ✓ 🚧 (up to 1 year, Enterprise) | partial (30 days free) | partial | partial | ✓ |
| **On-premises / self-hosted option** | | | | | |
| Self-hosted deployment | partial (limited-function OSS) | ✓ | ✗ (SaaS only) | ✓ | ✓ |

---

## Where we currently lag

These are capabilities competitors offer that AI Agent Assembly does not yet fully deliver.

1. **Vault-backed secrets management** — Pillar Security provides first-class secrets vault integration with automatic secret rotation and injection. AAASM currently supports secret-pattern detection via regex policies but does not integrate with HashiCorp Vault or AWS Secrets Manager.
2. **Automated human-in-the-loop approval workflows** — Pillar Security provides structured approval routing with escalation chains. AAASM can deny today (alert emission is planned, not yet shipped — see 🚧) and does not yet route decisions to a named approver queue.
3. **Full-function self-hosted deployment** — Langfuse, Opik, and Pillar Security offer a fully self-hostable product. AAASM self-hosting is limited-function today: a limited stack runs locally from the Apache-2.0 crates (Docker Compose) for evaluation and development, while the complete feature set is delivered via SaaS (see [Open Core Boundary](open-core-boundary.md)).
4. **Evaluation frameworks and LLM-as-judge scoring** — Langfuse and Opik provide built-in evaluation pipelines, dataset management, and automated LLM-as-judge scoring for output quality. AAASM's policy engine operates on patterns and metadata, not semantic quality.
5. **Prompt management and versioning** — Langfuse provides a managed prompt registry with version history and A/B comparison. AAASM does not include a prompt registry.

---

## Where we lead

These are capabilities where AI Agent Assembly is uniquely strong or differentiated.

1. **Pre-execution runtime enforcement** — AAASM is the only product in this comparison that makes binding allow/deny decisions *before* an agent action executes. All others are observability tools that record what happened after the fact.
2. **Kernel-level bypass detection via eBPF** — `aa-ebpf` reads TLS plaintext at the OpenSSL library level using Linux uprobes, surfacing bypass attempts that SDK-only solutions cannot see. It is a *detection* layer: the probes emit telemetry and return no verdict, so they report an action rather than preventing it, and they need Linux x86_64 with an OpenSSL-linked process. No competitor in this matrix offers kernel-level visibility at all.
3. **Network-layer interception without agent code changes** — `aa-proxy` performs MitM HTTPS interception using per-host certificates minted from a local root CA. Governance can be applied to agents that do not use the SDK, provided the agent process is launched so that it routes through the proxy and trusts that CA. No competitor supports sidecar-proxy-level enforcement.
4. **Policy-as-code with GitOps workflow** — AAASM policies are YAML/JSON documents that can be versioned, reviewed, and deployed via standard Git workflows. No competitor in this matrix offers a structured policy language; guardrails in other tools are typically configured through UI forms or proprietary DSLs.
5. **Hash-chained, verifiable audit log** — each entry in the per-session JSONL log carries a SHA-256 digest over its own fields plus the preceding entry's digest, and `aasm audit verify-chain` re-walks that chain. This ships in the **open-source** build, not behind an Enterprise flag. Read the guarantee precisely, because compliance work (PCI-DSS, SOC 2 Type II) depends on the difference: the chain is **unkeyed**, so it detects accidental or careless alteration but is not a signature — anyone who can rewrite the log can recompute the chain. It covers the **JSONL sink only**; the database mirror stores no chain metadata. The log is append-only *by convention*, not by constraint — retention pruning deletes rows — and emission is best-effort, so a dropped entry is indistinguishable from tampering. See [Audit log](security-model.md#audit-log) for the exact bounds. No competitor in this matrix offers a verifiable chain.

---

## Competitor documentation references

Last validated 2026-05-05 against each vendor's documentation as of that date.

| Competitor | Documentation URL |
|---|---|
| Langfuse | https://langfuse.com/docs |
| Helicone | https://docs.helicone.ai |
| Opik | https://www.comet.com/docs/opik |
| Pillar Security | https://docs.pillar.security |

---

## Related documentation

- [Security model](security-model.md) — STRIDE threat model, IronClaw defense
- [Open core boundary](open-core-boundary.md) — what is OSS vs. enterprise
- [Quick start (SaaS)](quickstart-saas.md) — get started in minutes

[^proxy]: No change to your *agent's* code, but the agent process must be
    launched so that it honours `HTTP_PROXY`/`HTTPS_PROXY` and trusts the
    proxy's local root CA (trust-store installation is implemented for macOS).
    Interception is HTTP/1.1 only — HTTP/2, gRPC, and WebSocket are out of
    scope — and by default only the built-in LLM provider hosts are decrypted;
    other hosts are tunnelled uninspected unless you list them.

[^audit]: Tamper-*evident*, not tamper-proof, and not immutable. Each entry in
    the per-session JSONL log carries a SHA-256 digest over its own fields plus
    the preceding entry's digest; `aasm audit verify-chain` re-walks it. The
    chain is **unkeyed** — there is no HMAC, no signature and no external
    anchoring — so it detects careless or accidental alteration but not an
    attacker who can rewrite the file and recompute the chain. It covers the
    JSONL sink only; the database mirror stores no chain metadata. The log is
    append-only by convention rather than by constraint (retention pruning
    deletes rows), and emission is best-effort, so a dropped entry is
    indistinguishable from tampering. Full bounds in
    [Audit log](security-model.md#audit-log).

[^ebpf]: Detection, not prevention: the probes emit telemetry and return no
    verdict, so an action they see is one that already happened. TLS visibility
    covers OpenSSL-linked processes only, and the layer requires Linux x86_64
    with a kernel that supports it — it degrades with a warning rather than
    failing closed if it cannot attach.

---

*Last reviewed: 2026-08-06 — AI Agent Assembly Team*
