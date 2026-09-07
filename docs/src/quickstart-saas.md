<!-- BEGIN AA-PAGE-META
schema_version: 1
page_type: architecture
audience: [evaluator, contributor]
user_job: Understand the intended managed onboarding flow and why none of it is available yet
owner: L2:docs
canonical_source: self
describes_capability: true
area: operations
limitations: "#what-this-page-does-not-publish-and-why"
platforms: []
last_verified:
  version: v0.0.1-rc.6
  ref: v0.0.1-rc.6
  date: 2026-09-07
  method: "No managed service is running; checked against source-of-truth.md's Operations row and the claim publication checklist"
claims:
  - term: Planned
    evidence: "AAASM-5613"
disclosure_levels: [3, 4]
END AA-PAGE-META -->

# Managed SaaS onboarding — design preview

> 🗺️ **Design preview — planned, not available.** The AI Agent Assembly managed
> SaaS platform has no public signup, no published plans or prices, and no
> service commitments. Nothing on this page is purchasable or usable today, and
> nothing here is an offer, a quote, or a contractual commitment.

This page is for readers evaluating whether to wait for a managed workspace or to
start on the open-source stack now. It deliberately does **not** contain
onboarding steps.

An earlier version of this page walked through managed-workspace onboarding:
tier selection, quotas, region selection, console screens, credential issuance,
support channels, procurement, and legal-agreement handling. Those instructions
described a service that is not running, so they were removed rather than
restated in vaguer language. The
[SaaS claim publication checklist](saas-claim-publication-checklist.md) records
each removed claim, the owner who must approve restoring it, and the evidence
that approval requires.

For the canonical maturity and visibility label of every area of this hub —
including Cloud — see [Source of truth & status](source-of-truth.md).

---

## What you can run today

The open-source stack is what ships. It is Apache-2.0, public, and versioned as
`v0.0.1-rc` (see the [compatibility matrix](compatibility.md) for the exact
component versions that work together).

| To do this | Go here |
|---|---|
| Run the gateway, policy engine, proxy, or CLI | [core docs](https://docs.agent-assembly.com/core/) |
| Instrument a Python agent | [Python SDK docs](https://docs.agent-assembly.com/python-sdk/) |
| Instrument a TypeScript agent | [Node SDK docs](https://docs.agent-assembly.com/node-sdk/) |
| Instrument a Go agent | [Go SDK docs](https://docs.agent-assembly.com/go-sdk/) |
| Run a limited-function stack locally with Docker Compose | [Docker & containers](docker-containers.md#compose) |
| Read the policy rule schema the gateway evaluates against | [Policy reference](policy-reference.md) |
| Step through a working governed agent end to end | [`examples` repo](https://github.com/ai-agent-assembly/examples) |

The self-hostable stack is **limited-function** and intended for local
evaluation and development. [Open core boundary](open-core-boundary.md)
describes which capabilities are in the open-source core and which are intended
for the commercial tier.

---

## The onboarding journey this is designed for

Everything in this section is design intent. It names no plan, price, quota,
region, retention period, console screen, tenant-identifier format,
availability commitment, or date, because none of those exist — see
[what this page does not publish](#what-this-page-does-not-publish-and-why).

The managed service is intended to deliver the operator-management capabilities
that sit on the commercial side of the
[open core boundary](open-core-boundary.md#what-is-intended-for-the-commercial-tier):
identity federation, directory-driven user provisioning, longer-lived and
higher-assurance audit storage, audit export into external security tooling,
and regional deployment control. The enforcement path itself is Apache-2.0 and
needs none of them.

The dependency that shapes the whole journey: **enforcement does not wait on
the control plane.** A team adopting the managed service later runs the same
gateway, policy engine, proxy and SDK shims it runs today; the managed service
is intended to add operator management around them, not to replace them. That
is why the available path above is not a stopgap.

---

## What this page does not publish, and why

The managed service is not running, so this hub does not publish:

- Plan or tier names, prices, or what any plan includes.
- Agent, policy, or retention quotas.
- Regions, region selection, or data-residency guarantees.
- Availability, uptime, or support-response commitments.
- Billing, invoicing, purchase-order, or procurement-timeline instructions.
- Onboarding steps that reference a console, signup form, or credential screen.
- Compliance certifications, or the availability of a DPA or BAA.

Each of these is tracked in the
[publication checklist](saas-claim-publication-checklist.md) with the evidence
needed to publish it. Publishing any of them before that evidence exists would
misrepresent the product.

---

## What must be true before any of this is published

This hub does not decide when a planned area becomes available; the
[SaaS claim publication checklist](saas-claim-publication-checklist.md) does,
one claim class at a time. Each register row names the evidence required and
the approval owner who must sign the specific wording.

Two things gate the whole page rather than one row: the managed service
running and carrying real traffic, and the [status map](source-of-truth.md)
moving this area off 🗺️ Planned. Until both hold, no register row can be
satisfied, because every one of them requires evidence produced by a running
service.

---

## Evidence

- Maturity: [Source of truth & status](source-of-truth.md)'s **Operations
  (running & onboarding)** row — 🗺️ Planned.
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
- [Open core boundary](open-core-boundary.md) — the open-source / commercial split
- [Managed control plane — design preview](cloud-deployment.md) — planned, not available
- [SaaS claim publication checklist](saas-claim-publication-checklist.md) — what must be evidenced before managed-service claims return

<div class="aa-cta-next">
  <span class="aa-cta-next__label">Next step</span>
  <a href="https://github.com/ai-agent-assembly/examples?utm_source=docs&amp;utm_medium=docs_link&amp;utm_campaign=oss_install&amp;utm_content=quickstart_next_step" data-cta-location="body" rel="noopener">Run a working example →</a>
  <p>Open the <code>examples</code> repo and step through a governed
     LangChain, LlamaIndex, or bare-OpenAI agent end-to-end.</p>
</div>

<div class="aa-cta-next">
  <span class="aa-cta-next__label">Interested in a managed workspace?</span>
  <a href="https://agent-assembly.com/early-access?utm_source=docs&amp;utm_medium=docs_link&amp;utm_campaign=early_access&amp;utm_content=quickstart_page" data-cta-location="body" rel="noopener">Register interest →</a>
  <p>Registering interest is not a purchase, a reservation, or a commitment by
     either side. The open-source stack above works today.</p>
</div>

---

*Last reviewed: 2026-09-07 · AI Agent Assembly Team*
