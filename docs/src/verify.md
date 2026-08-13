<!-- BEGIN AA-PAGE-META
schema_version: 1
page_type: guide
audience: [auditor, security-engineer]
user_job: Take a published statement about this product to the evidence behind it
owner: L2:docs
canonical_source: self
describes_capability: false
disclosure_levels: [1, 3]
deeper: https://docs.agent-assembly.com/core/latest/adr/0033-canonical-governance-and-enforcement-architecture.html
END AA-PAGE-META -->

# Check a published claim

This section routes a published sentence to the evidence behind it, and routes a
vulnerability to the people who can act on it; it holds no evidence of its own, because
a copy of evidence is not evidence.

## Take a sentence to its evidence, in three steps

### 1. Find the claim term

A statement about what happened to an action is incomplete without its **timing** and
its **failure posture**. ADR 0033 §6 defines the canonical vocabulary for this, and
downstream material is required to pick one of its terms rather than an
undifferentiated verb.

The eleven terms are:

*Observed* · *Detected* · *Evaluated* · *Denied before execution* · *Redacted* ·
*Approval required* · *Degraded* · *Unmeasured* · *Experimental* · *Planned* ·
*Unsupported*

What each one means, and which mechanism can legitimately reach it today, are defined
in
[ADR 0033 §6](https://docs.agent-assembly.com/core/latest/adr/0033-canonical-governance-and-enforcement-architecture.html).
This page names the terms so you can find them; it does not define them, because a
second definition is how two definitions start disagreeing.

If a sentence uses none of these terms, that is the finding.

### 2. Ask for the evidence that term requires

Each term in §6 carries the evidence that substantiates it, and they are not
interchangeable: a durable event attributed to an action substantiates *Observed*, and
does not substantiate *Denied before execution*, which needs a refusal by a component
sitting before the effect.

Three signals look like coverage and are not, and ADR 0033 §7 names them so they cannot
be offered as substantiation: an environment variable that replaces a probe result, a
probe satisfied by a binary being present on `$PATH`, and a capability bit asserted
unconditionally.

### 3. Check the completeness claim separately

A statement usually carries two claims at once: what happened to an action, and how
much was covered. They have different owners and different evidence, so they are
checked separately and the more restrictive published outcome governs.

| To check | Read |
| --- | --- |
| What a scenario does and does not demonstrate | [Risk scenarios](risk-scenarios.md), and its [negative control](risk-scenarios.md#negative-control-for-the-flagship-ac-1) |
| Wording that has already been reviewed for reuse | [Risk scenarios: approved wording](risk-scenarios.md#approved-wording-for-reuse) |
| What may be said about the managed service | [SaaS claim publication checklist](saas-claim-publication-checklist.md) |
| Which areas are open source and which are not | [Open core boundary](open-core-boundary.md) |
| Who owns an area, and how mature its documentation is | [Status map](source-of-truth.md) |

## Report a vulnerability

**Do not report a security issue through a public GitHub issue.**

Vulnerability reports go to the repository that owns the affected code, through
GitHub's private vulnerability reporting on that repository, and each repository's
`SECURITY.md` carries its current reporting route and disclosure policy:

| Component | Security policy |
| --- | --- |
| Core | [`agent-assembly/SECURITY.md`](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/SECURITY.md) |
| Python SDK | [`python-sdk/SECURITY.md`](https://github.com/ai-agent-assembly/python-sdk/blob/HEAD/SECURITY.md) |
| Node SDK | [`node-sdk/SECURITY.md`](https://github.com/ai-agent-assembly/node-sdk/blob/HEAD/SECURITY.md) |
| Go SDK | no repository policy today; use the [organisation policy](https://github.com/ai-agent-assembly/.github/blob/HEAD/SECURITY.md) |
| Arena | no repository policy today; use the [organisation policy](https://github.com/ai-agent-assembly/.github/blob/HEAD/SECURITY.md) |
| This documentation hub | no repository policy today; use the [organisation policy](https://github.com/ai-agent-assembly/.github/blob/HEAD/SECURITY.md) |

The organisation-wide
[security policy](https://github.com/ai-agent-assembly/.github/blob/HEAD/SECURITY.md)
is the fallback for any repository that does not publish its own, and the rows above
were checked rather than assumed.

If you are unsure which repository owns the code, file against
[core](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/SECURITY.md) and
it will be routed.

The reporting address is deliberately not repeated on this page. Each `SECURITY.md`
above is the canonical source for its own route, and a copied address is one that keeps
working right up until it does not.

## What this page does not do

- **It does not hold evidence.** It routes to the artifact that does.
- **It does not define a claim term.** ADR 0033 §6 does.
- **It does not decide whether a statement may be published.** For managed-service
  wording that is the
  [SaaS claim publication checklist](saas-claim-publication-checklist.md).

## Going deeper

The claim vocabulary, the evidence each term requires, and the mechanisms mapped onto
them are in
[ADR 0033](https://docs.agent-assembly.com/core/latest/adr/0033-canonical-governance-and-enforcement-architecture.html).
