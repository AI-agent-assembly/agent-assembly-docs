<!-- BEGIN AA-PAGE-META
schema_version: 1
page_type: architecture
audience: [evaluator, security-engineer, contributor]
user_job: Understand the intended managed control-plane design and why none of it is available yet
owner: L2:docs
canonical_source: self
describes_capability: true
area: cloud
limitations: "#what-this-page-does-not-publish-and-why"
platforms: []
last_verified:
  version: v0.0.1-rc.6
  ref: v0.0.1-rc.6
  date: 2026-09-07
  method: "No managed control plane is running; checked against source-of-truth.md's Cloud row and the claim publication checklist"
claims:
  - term: Planned
    evidence: "AAASM-5613"
disclosure_levels: [3, 4]
END AA-PAGE-META -->

# Managed control plane — design preview

> 🗺️ **Design preview — planned, not available.** The AI Agent Assembly managed
> control plane (Cloud) is not running. There is no workspace to provision, no
> console to log into, and no service, support, or compliance commitment
> attached to it. Nothing on this page is an offer or a contractual commitment.

This page is for enterprise platform, security, and procurement readers who need
to know what the managed control plane does **not** yet provide, so they can plan
against the open-source stack instead of against an unavailable service.

An earlier version of this page documented the managed platform as if it were
operating: a region list with data-residency guarantees, tenant provisioning
paths, per-tier quotas, SSO and SCIM configuration walkthroughs, a console budget
form, an availability-and-support SLA table, card and invoice billing setup, and
the handling of Data Processing Agreements and Business Associate Agreements.
None of those had a running service, an approved commercial policy, or a legal
review behind them, so they were removed rather than reworded into softer
promises.

Every removed claim is listed in the
[SaaS claim publication checklist](saas-claim-publication-checklist.md), together
with the owner who must approve restoring it and the evidence that approval
requires. [Source of truth & status](source-of-truth.md) carries the canonical
maturity label for Cloud and for every other area of this hub.

---

## What runs today instead

Governance enforcement is open source and does not depend on the managed control
plane. The gateway, the policy engine, the sidecar proxy, the eBPF sensor, the
SDK shims, and the `aasm` CLI are Apache-2.0 and can be run locally.

| Concern | Where it is documented today |
|---|---|
| Running the gateway, proxy, sensor, and CLI | [core docs](https://docs.agent-assembly.com/core/) |
| Bringing up a limited-function stack with Docker Compose | [Docker & containers](docker-containers.md#compose) |
| Health probes and Prometheus metrics for that stack | [Self-host observability](self-host-observability.md) |
| The policy rule schema the gateway evaluates against | [Policy reference](policy-reference.md) |
| Spend caps | [Policy reference → `budget`](policy-reference.md#budget) — per-agent and per-organisation USD limits declared in policy |
| Authentication that exists today | API keys, as described in [Open core boundary](open-core-boundary.md) |
| Which capabilities are open source and which are intended for the commercial tier | [Open core boundary](open-core-boundary.md) |

The console budget form this page previously described did not match the budget
schema the gateway actually validates against. [Policy reference](policy-reference.md#budget)
is the source of truth for budget behaviour.

---

## The control-plane design this is intended for

Everything in this section is design intent. It names no region, tenant format,
quota, plan, price, SLA, or date, because none of those exist — see
[what this page does not publish](#what-this-page-does-not-publish-and-why).

The managed control plane is intended to add the operator-management
capabilities that sit on the commercial side of the
[open core boundary](open-core-boundary.md#what-is-intended-for-the-commercial-tier):
identity federation, directory-driven user provisioning, longer-lived and
higher-assurance audit storage, audit export into external security tooling,
and regional deployment control. The reason managed delivery is the intent
rather than a self-managed distribution of the same code: multi-tenant
infrastructure and on-call operation are what a self-managed install does not
get for free.

The dependency that shapes the design: **enforcement does not wait on the
control plane.** The gateway, policy engine, proxy, and SDK shims a team runs
today are the same ones a managed workspace would run underneath — the control
plane is intended to add operator management around them, not to replace them.

---

## What this page does not publish, and why

Because the managed control plane is not running, this hub does not publish:

- Regions, region selection, or data-residency guarantees.
- Tenant or workspace provisioning steps, or a tenant-identifier format.
- Plan or tier names, prices, or per-tier quotas for agents, policies, or audit-log retention.
- SSO (SAML 2.0 / OIDC) or SCIM 2.0 configuration instructions, endpoints, or supported-operation matrices.
- A console role model, or group-to-role mapping instructions.
- Availability, uptime, or support-response commitments, or service credits.
- Billing, invoicing, payment-method, purchase-order, or payment-terms instructions.
- Compliance certifications, or the availability of a DPA or a BAA.

Publishing any of these before the corresponding service, owner approval, and
evidence exist would present an unavailable service as a defined one. The
[publication checklist](saas-claim-publication-checklist.md) names the evidence
required for each.

---

## What must be true before any of this is published

This hub does not decide when a planned area becomes available; the
[SaaS claim publication checklist](saas-claim-publication-checklist.md) does,
one claim class at a time. Each register row names the evidence required and
the approval owner who must sign the specific wording.

Two things gate the whole page rather than one row: the managed control plane
running and carrying real tenants, and the [status map](source-of-truth.md)
moving this area off 🗺️ Planned. Until both hold, no register row can be
satisfied, because every one of them requires evidence produced by a running
service.

---

## Evidence

- Maturity: [Source of truth & status](source-of-truth.md)'s **Cloud (SaaS
  control plane)** row — 🗺️ Planned.
- Claim record: this page's `AA-PAGE-META` carries a single ADR 0033 §6
  `Planned` claim, with `platforms: []` and no `availability` value — the
  metadata form for a capability present in no published artifact.
- Removed claims and their restoration conditions: the
  [publication checklist](saas-claim-publication-checklist.md) register.
- There is no implementation to link: the `cloud` repository is private and
  outside this hub's public content boundary. A design deep-dive here would
  describe a system no reader can verify.

---

## Related documentation

- [Source of truth & status](source-of-truth.md) — which areas ship today and which are planned
- [Managed SaaS onboarding — design preview](quickstart-saas.md) — managed onboarding, also planned
- [Open core boundary](open-core-boundary.md) — the open-source / commercial split
- [Security model](security-model.md) — the security posture of the open-source enforcement path
- [SaaS claim publication checklist](saas-claim-publication-checklist.md) — what must be evidenced before managed-service claims return

---

*Last reviewed: 2026-09-07 · AI Agent Assembly Team*
