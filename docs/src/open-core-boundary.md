# Open core boundary

AI Agent Assembly follows an **open-core** model. The line is simple:

- **Enforcement is open source.** The interception layers, policy engine, SDK shims, and CLI are Apache-2.0. Anyone can read, audit, and contribute to them.
- **Enterprise operations are intended to be commercial.** Capabilities such as SSO, SCIM, advanced audit, and multi-region data residency are planned for a commercial tier. That tier is not available, its licence terms are not published, and there is no paid plan to buy.

> 🗺️ **The commercial side of this boundary is planned, not available.** You can
> self-host a limited-function stack from the Apache-2.0 crates today — using the
> published Docker Compose example — for local evaluation and development. The
> managed service that is intended to deliver the commercial capabilities is not
> running; see [Cloud deployment](cloud-deployment.md) and
> [Quick start (SaaS)](quickstart-saas.md) for what that means in practice, and
> [Source of truth & status](source-of-truth.md) for the canonical maturity label.

---

## Why open core?

### The enforcement path must be inspectable

The infrastructure that sits between AI agents and the outside world has to be trustworthy and independently auditable. Keeping the core open source is not a marketing choice — it follows directly from the security posture.

An enterprise cannot take our word for how the policy engine evaluates rules, how eBPF probes intercept system calls, or how the sidecar proxy terminates TLS. Open source means a third party can read, review, and verify the enforcement path without involving us.

### A single boundary rule

The split between open and commercial follows one principle: **enforcement is open; enterprise operations are commercial.**

- If a feature controls *what agents can do*, it belongs in the Apache-2.0 core.
- If a feature controls *how operators manage, scale, or audit the system at enterprise grade* — identity federation, directory-driven user lifecycle, longer-retention and higher-assurance audit storage, regional deployment control — it belongs in the commercial tier.

A motivated team can fork, read, or contribute to the security controls listed as Apache-2.0 below, regardless of subscription status.

### Open source strengthens the core

Open-sourcing the enforcement logic creates a community feedback loop. Security researchers who find a gap in the policy engine, proxy TLS handling, or an eBPF program can open an issue or send a pull request.

We chose Apache-2.0 specifically because it permits commercial integration without a copyleft obligation — SDK users can embed the shims in proprietary products without the license spreading to their own code.

### Limited-function self-host today; managed service planned

Shipping the crates as open source lets teams read, audit, and contribute — and self-host a **limited-function** stack (via the published [Docker Compose example](docker-containers.md#compose)) for local evaluation and development.

The enterprise-operations capabilities are intended to be delivered as a managed
service rather than as self-managed software, because operating a multi-tenant
platform takes infrastructure and on-call capability that a self-managed install
does not get for free. That is a design intent, not a shipped service: the
managed platform is not running, and this hub publishes no availability, support,
or compliance commitment for it.

---

## What is in the Apache-2.0 core today

These ship in the public `agent-assembly` monorepo and the three SDK repos, under
Apache-2.0 (the `python-sdk` shim is MIT — see [crate licensing](#crate-licensing)).
They run without any managed service.

| Area | In the Apache-2.0 core |
|---|---|
| **Interception** | Language SDKs (Python, TypeScript, Go); sidecar proxy (`aa-proxy`); eBPF sensor (`aa-ebpf`, Linux) |
| **Gateway and policy** | Agent registry; policy engine (allow/deny/audit); policy-as-code (YAML/JSON); budget limits declared in policy and enforced by the gateway — see [Policy reference](policy-reference.md) |
| **Authentication** | API key authentication |
| **Audit** | Audit event emission and query — see [Security model](security-model.md) |
| **Operations** | `aasm` operator CLI; limited-function local stack via the published [Docker Compose example](docker-containers.md#compose); health probes and Prometheus metrics — see [Self-host observability](self-host-observability.md) |

The public issue trackers and pull-request queues on
[github.com/ai-agent-assembly](https://github.com/orgs/ai-agent-assembly/repositories)
are open to anyone. They are not a support channel with a response commitment.

## What is intended for the commercial tier

> 🗺️ **Planned — not available.** Everything in this section is design intent.
> The commercial tier is not for sale, its licence terms are not published, and
> the managed service that would deliver it is not running. This is not a
> roadmap commitment, a delivery date, or an offer.

Identity federation, directory-driven user provisioning, longer-lived and
higher-assurance audit storage, audit export into external security tooling, and
regional deployment control are the capability areas intended to sit on the
commercial side of the boundary — because they are operator-management concerns
rather than enforcement controls.

This hub deliberately does not publish, for any of them: a plan or tier they
belong to, a price, a quota, a retention period, a region list, a data-residency
guarantee, an availability or support commitment, or a compliance certification.
The [SaaS claim publication checklist](saas-claim-publication-checklist.md)
records what has to be evidenced, and by whom, before any of that can be
published.

---

## Crate licensing

All Cargo crates in the `agent-assembly` workspace are Apache-2.0:

| Crate | License | Notes |
|---|---|---|
| `aa-core` | Apache-2.0 | Core domain types — always OSS |
| `aa-proto` | Apache-2.0 | Protobuf definitions — always OSS |
| `aa-runtime` | Apache-2.0 | Async runtime utilities — always OSS |
| `aa-gateway` | Apache-2.0 | Gateway with policy engine — always OSS |
| `aa-api` | Apache-2.0 | REST API surface — OSS |
| `aa-proxy` | Apache-2.0 | Sidecar proxy — always OSS |
| `aa-ebpf` | Apache-2.0 | eBPF user-space loader — always OSS |
| `aa-ebpf-common` | Apache-2.0 | eBPF shared types — always OSS |
| `aa-wasm` | Apache-2.0 | WebAssembly build — always OSS |
| `aa-cli` | Apache-2.0 | `aasm` operator CLI — always OSS |
| `conformance` | Apache-2.0 | Conformance test suite — always OSS |

The three SDK native-binding shims are not members of the `agent-assembly` Cargo
workspace — each lives in its own SDK repo and carries that repo's own license:

| Crate | Repo | License | Notes |
|---|---|---|---|
| `aa-ffi-python` | `python-sdk` (`native/aa-ffi-python`) | MIT | Python SDK native shim — the `python-sdk` repo is intentionally MIT, not Apache-2.0 |
| `aa-ffi-node` | `node-sdk` (`native/aa-ffi-node`) | Apache-2.0 | TypeScript SDK native binding |
| `aa-ffi-go` | `go-sdk` (`native/aa-ffi-go`) | Apache-2.0 | Go SDK native shim |

### Apache 2.0 key terms

The Apache License 2.0 grants users the right to use, reproduce, prepare derivative works, distribute, and sublicense the software with or without modification. It does not grant trademark rights, and it requires preservation of copyright notices and attribution in distributed works. See the full license text at https://www.apache.org/licenses/LICENSE-2.0.

The commercial capabilities described above are intended to be delivered by the managed control plane rather than by separate closed-source crates, so the boundary is a deployment boundary rather than a second licence over the enforcement path. The interception and enforcement logic listed in [What is in the Apache-2.0 core today](#what-is-in-the-apache-20-core-today) is Apache-2.0.

---

## Contributing to the OSS core

The Apache-2.0 crates welcome community contributions. See `CONTRIBUTING.md` in the `agent-assembly` repository for:

- Branching and commit conventions
- How to run the test suite (`cargo nextest run --workspace`)
- The CLA requirement for non-trivial contributions
- How to file issues and feature requests

Requests for the capabilities intended for the commercial tier are tracked internally by the AI Agent Assembly team. Filing one is not a delivery commitment.

---

## Related documentation

- [Security model](security-model.md) — cryptographic primitives and audit log details
- [Cloud deployment](cloud-deployment.md) — the managed control plane, which is planned and not available
- [Source of truth & status](source-of-truth.md) — the canonical maturity label for every area of this hub
- [SaaS claim publication checklist](saas-claim-publication-checklist.md) — what must be evidenced before commercial-tier claims are published
- [Why AI Agent Assembly?](comparison.md) — open-source posture vs. competitors

---

*Last reviewed: 2026-08-06 · AI Agent Assembly Team*

> This page describes a licensing and deployment boundary. It is not legal advice
> and it is not a licence grant beyond the Apache-2.0 terms of the published
> crates. Commercial-tier licence terms are not published; nothing here creates
> one.
