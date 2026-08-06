# Product promise & message hierarchy

This page is for anyone writing public copy about AI Agent Assembly — the product
website, this hub, a README, a conference abstract, a sales deck. It exists because
the product's honest value is narrower than its architecture diagram suggests, and
narrower still than the words the category usually reaches for. A reader who
discovers an overstated claim *after* provisioning is a worse outcome than one who
reads an accurate limit up front.

It is also for evaluators. Levels 1 to 3 below are the fastest accurate account of
what the product does; if you only read this page, you will not be surprised later.

## What governs this page

This brief is downstream of two merged artifacts, and it does not add claims to
them:

| Source | What it supplies | Where |
|---|---|---|
| **ADR 0033 — Canonical Governance & Enforcement Architecture** | The architecture, the platform matrix, and §6's **claim vocabulary**. Every clause of the promise below is expressed in one of §6's terms. | [`docs/src/adr/0033-…`](https://docs.agent-assembly.com/core/adr/0033-canonical-governance-and-enforcement-architecture.html) in the `agent-assembly` repository |
| **AAASM-5528 — public claim inventory** | 69 audited rows of what may and may not be said, each tied to a re-verified evidence block (`E1`–`E7`). | `verification-reports/AAASM-5528-public-claim-inventory.md` in the `agent-assembly` repository |

Two further sources are chartered but not yet available, so nothing here depends on
them: the current-state capability matrix ([AAASM-5527](https://lightning-dust-mite.atlassian.net/browse/AAASM-5527),
in progress) and the machine-readable capability/evidence manifest
([AAASM-5531](https://lightning-dust-mite.atlassian.net/browse/AAASM-5531), not
started). Statements that would need either of those to be verified are collected
under [Provisional](#provisional) rather than asserted.

> **Precedence.** Where this hub still carries the superseded three-layer or
> "IronClaw five-layer" framing — [Security model](security-model.md) and
> [Glossary](glossary.md) both do, at the time of writing — **ADR 0033 wins**. Those
> pages are being migrated under
> [AAASM-5586](https://lightning-dust-mite.atlassian.net/browse/AAASM-5586) and
> [AAASM-5609](https://lightning-dust-mite.atlassian.net/browse/AAASM-5609); ADR 0033
> records the gap as a tracked, accepted window. Do not resolve a conflict in the
> superseded model's favour.

Maturity labels (🧪 Release candidate, 🗺️ Planned) belong to
[Source of truth & status](source-of-truth.md) and answer a *different* question —
how finished a feature is. ADR 0033 §6's terms answer *what the product did to an
action, when, and on what evidence*. The two are orthogonal: a 🧪 Release candidate
feature can be **Unsupported** on a platform, and a shipped feature can be
**Unmeasured** on a path. Cross-reference them; never let one redefine the other.

## The promise

There is exactly one. Everything else on this page is a rendering of it at a
different depth.

> **Agent Assembly decides whether an AI agent's action is allowed before that action
> runs — on the paths you route through it — and records what was decided, so a risky
> call can be refused or held for a person instead of discovered afterwards.**

### Headline and subheadline

For a hero or a first screen, the promise renders as:

**Headline**

> Decide what your AI agents may do — before they do it.

**Subheadline**

> Agent Assembly evaluates the actions you route through it against your policy,
> refuses or holds the ones your policy disallows, and records the decision. An
> action you have not routed through it is not inspected — and the record says so.

**These two are not severable.** The headline is bounded only by the subheadline;
published alone it reads as a claim over all agent behaviour, which is the exact
defect [AAASM-5528](https://lightning-dust-mite.atlassian.net/browse/AAASM-5528)
removed from 69 places. The rule for downstream pages is: *the boundary clause
appears on the same screen as the headline, above the fold, not in a footnote.*

### Clause map

Each clause is expressible in ADR 0033 §6's vocabulary. If a rewrite of the promise
cannot be mapped this way, it is not a rendering of the promise — it is a new claim,
and it needs its own evidence.

| Clause | ADR 0033 §6 term | Why the term fits |
|---|---|---|
| "decides whether an … action is allowed" | **Evaluated** | The control plane produces a decision for the action; a decision record exists. |
| "before that action runs" | **Denied before execution** | Reached where the refusing component sits before the effect — today the proxy, pre-dial, or an SDK shim that honours the answer. |
| "on the paths you route through it" | **Unmeasured** (by contrast) | Names the boundary. Anything off the path is Unmeasured; the clause exists so the promise does not quantify over agent behaviour. |
| "records what was decided" | **Observed** | A durable event attributed to the action, on a verifiable hash chain. |
| "refused" | **Denied before execution** | As above. |
| "held for a person" | **Approval required** | The action is held pending a human decision; a pending approval record exists. |
| "instead of discovered afterwards" | — | A contrast with after-the-fact observability, not a capability claim. Carries no evidence burden. |

---

*Last reviewed: 2026-08-06 — AI Agent Assembly Team*
