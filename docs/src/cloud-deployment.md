# Cloud deployment

> 🗺️ **Planned — not available.** The AI Agent Assembly managed control plane
> (Cloud) is not running. There is no workspace to provision, no console to log
> into, and no service, support, or compliance commitment attached to it.
> Nothing on this page is an offer or a contractual commitment.

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
| The policy rule schema the gateway enforces | [Policy reference](policy-reference.md) |
| Spend caps | [Policy reference → `budget`](policy-reference.md#budget) — per-agent and per-organisation USD limits declared in policy, enforced by the gateway |
| Authentication that exists today | API keys, as described in [Open core boundary](open-core-boundary.md) |
| Which capabilities are open source and which are intended for the commercial tier | [Open core boundary](open-core-boundary.md) |

The console budget form this page previously described did not match the budget
schema the gateway actually enforces. [Policy reference](policy-reference.md#budget)
is the source of truth for budget behaviour.

---

## What is not documented here, and why

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

## Related documentation

- [Source of truth & status](source-of-truth.md) — which areas ship today and which are planned
- [Quick start (SaaS)](quickstart-saas.md) — managed onboarding, also planned
- [Open core boundary](open-core-boundary.md) — the open-source / commercial split
- [Security model](security-model.md) — the security posture of the open-source enforcement path
- [SaaS claim publication checklist](saas-claim-publication-checklist.md) — what must be evidenced before managed-service claims return

---

*Last reviewed: 2026-08-06 · AI Agent Assembly Team*
