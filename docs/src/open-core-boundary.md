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

## Feature matrix

> 🚧 **Coming soon.** The AAA-Commercial (Enterprise) tier described below — and the paid SaaS platform that delivers it — is planned and not yet generally available. The Apache-2.0 (OSS) column reflects what ships today; the commercial column reflects the intended design.

| Feature | Apache-2.0 (OSS) | AAA-Commercial (Enterprise) |
|---|---|---|
| **Core interception layers** | | |
| Language SDK (Python, TypeScript, Go) | ✅ | ✅ |
| Sidecar proxy (`aa-proxy`) | ✅ | ✅ |
| eBPF sensor (`aa-ebpf`) | ✅ | ✅ |
| **Gateway and policy** | | |
| Agent registry | ✅ | ✅ |
| Policy engine (allow/deny/audit) | ✅ | ✅ |
| Per-team budget enforcement | ✅ | ✅ |
| Policy-as-code (YAML/JSON) | ✅ | ✅ |
| **Authentication and access** | | |
| API key authentication | ✅ | ✅ |
| SAML 2.0 / OIDC SSO | ❌ | ✅ |
| SCIM user provisioning | ❌ | ✅ |
| Role-based access control (RBAC) | Basic | Full (Owner/Admin/Developer/Viewer) |
| **Audit and compliance** | | |
| Basic audit log | ✅ | ✅ |
| Tamper-evident signed audit log | ❌ | ✅ |
| Audit log retention > 30 days | ❌ | ✅ (configurable, up to 1 year) |
| SIEM export (JSON / CEF) | ❌ | ✅ |
| **Deployment and SLA** | | |
| Limited-function self-host (Docker Compose) | ✅ (local eval/dev) | — |
| SaaS — shared region | ✅ (Free/Team tier) | ✅ |
| SaaS — dedicated region | ❌ | ✅ (Enterprise tier) |
| Multi-region data residency | ❌ | ✅ |
| 99.9% uptime SLA | ❌ | ✅ (Enterprise tier) |
| Dedicated SRE contact | ❌ | ✅ (Enterprise tier) |
| **Support** | | |
| Community forum | ✅ | ✅ |
| Business-hours support | ❌ | ✅ (Team tier) |
| 24/7 support | ❌ | ✅ (Enterprise tier) |

---

## Crate licensing

All Cargo crates in the `agent-assembly` workspace are Apache-2.0:

| Crate | License | Notes |
|---|---|---|
| `aa-core` | Apache-2.0 | Core domain types — always OSS |
| `aa-proto` | Apache-2.0 | Protobuf definitions — always OSS |
| `aa-runtime` | Apache-2.0 | Async runtime utilities — always OSS |
| `aa-gateway` | Apache-2.0 | Gateway with policy engine — OSS core; enterprise features gated behind SaaS config |
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

Enterprise features (SSO, SCIM, tamper-evident audit, dedicated regions) are delivered via SaaS-side configuration — not via separate closed-source crates. The OSS codebase contains all interception and enforcement logic.

---

## Contributing to the OSS core

The Apache-2.0 crates welcome community contributions. See `CONTRIBUTING.md` in the `agent-assembly` repository for:

- Branching and commit conventions
- How to run the test suite (`cargo nextest run --workspace`)
- The CLA requirement for non-trivial contributions
- How to file issues and feature requests

Enterprise feature requests (SSO, SCIM, audit extensions) are tracked as AAASM JIRA tickets in the Enterprise component and delivered by the AI Agent Assembly team.

---

## Related documentation

- [Security model](security-model.md) — cryptographic primitives and audit log details
- [Cloud deployment](cloud-deployment.md) — SSO, SCIM, SLA tier comparison
- [Why AI Agent Assembly?](comparison.md) — open-source posture vs. competitors

---

*Last reviewed: 2026-06-11 · Legal approver: @legal-team*
