# SaaS claim publication checklist

This page is the control that keeps the managed-service claims off this hub until
they are true. It exists for two audiences: readers who want to know *why* the
SaaS pages are almost empty, and maintainers who are about to add a
managed-service claim back.

The rule it enforces is narrow and absolute in one direction only:

> **A managed-service operational or contractual claim may not be published on
> this hub until the service exists, a named owner has approved the claim, and
> the evidence listed below has been produced.**

"Removed rather than softened" is deliberate. Rewording *"99.9% uptime SLA"* into
*"high availability"* does not reduce the commitment a reader takes away from it;
it only makes the commitment harder to audit. Unevidenced claims are deleted.

## Scope

This checklist covers claims about the **managed AI Agent Assembly service**: its
availability, plans, quotas, regions, onboarding, billing, support, and legal or
compliance posture.

It does **not** cover the open-source stack. Apache-2.0 behaviour is documented
normally, in [core docs](https://docs.agent-assembly.com/core/), the
[policy reference](policy-reference.md), the [security model](security-model.md),
and [Docker & containers](docker-containers.md).

## How to use it

1. Find the claim class you want to publish in the register below.
2. Produce the evidence in the **Evidence required** column. Link it from the
   pull request.
3. Get written approval from the role in the **Approval owner** column. An
   approval covers a specific wording, not a topic.
4. Publish the claim with the wording that was approved, and add the label the
   claim's maturity warrants — see
   [Source of truth & status](source-of-truth.md) for the label vocabulary this
   hub uses.
5. Update the register row so the next maintainer can see what was approved and
   on what basis.

If a claim is not in the register, it does not get a fast path — add a row for
it first.

## Register of removed claims

Removed by AAASM-5612 on 2026-08-06 from
[Quick start (SaaS)](quickstart-saas.md), [Cloud deployment](cloud-deployment.md),
[Open core boundary](open-core-boundary.md), and
[Security model](security-model.md).

The security-model rows differ from the rest in one way worth noting: several of
those claims were not merely unevidenced, they were **contradicted by the
Apache-2.0 source**. Where that is the case the row says so, because the evidence
needed to restore such a claim is a code change, not an approval.

Approval owners are roles, not individuals, so the register does not go stale
when people change. "Evidence required" is the minimum; an owner may ask for
more.

### Availability and service commitments

| Claim removed | Why it was removed | Approval owner | Evidence required to restore |
|---|---|---|---|
| Named uptime or availability percentages (for example a 99.5% or 99.9% monthly figure), per tier | Asserted a measured, contractual availability level for a service that is not running, so no availability has ever been measured | Head of Engineering **and** Legal | A production service carrying real traffic; a published measurement window with the method stated; a public status page; and the availability commitment written into published terms |
| Service credits for missed availability | A financial remedy implies a contract; none is published | Legal **and** Finance | Published terms of service containing the credit schedule, countersigned |
| Support response times (for example 24-hour business-hours or 4-hour any-time response) | Asserted a staffed response commitment with no on-call rota, ticket system, or measurement behind it | Head of Support **and** Legal | A staffed support function with a ticketing system; a measured response-time distribution over a stated period; the commitment written into published terms |
| A named support channel presented as operating (support portal, community forum) | The referenced endpoints were not serving | Head of Support | The channel reachable at a published URL, with a named owner and a stated scope |
| A dedicated named engineering or SRE contact per customer | A staffing commitment with no staffing model behind it | Head of Engineering **and** Head of Support | A defined role with allocated headcount, and the commitment written into published terms |

### Plans, quotas, and pricing

| Claim removed | Why it was removed | Approval owner | Evidence required to restore |
|---|---|---|---|
| Plan and tier names presented as purchasable, and what each plan includes | Presented a commercial catalogue that cannot be bought | Product Lead **and** Finance | An approved and published pricing page; a working purchase path; the plan-to-entitlement mapping enforced by the running service |
| Prices, currencies, and billing periods | No published price list exists | Finance **and** Legal | An approved price list and published terms covering it |
| Numeric quotas — maximum agents, maximum policies, retention periods per plan | Published numbers that the service does not enforce | Product Lead **and** Head of Engineering | The limit enforced by the running service, and a test demonstrating the enforced value matches the documented one |
| "Unlimited" for any resource | An unqualified absolute; every real system has a limit | Product Lead **and** Head of Engineering | Either a stated numeric limit, or an explicit statement of what bounds the resource in practice |

### Regions and data residency

| Claim removed | Why it was removed | Approval owner | Evidence required to restore |
|---|---|---|---|
| A list of available regions, and per-region locations | Presented a deployment footprint that does not exist | Head of Infrastructure | The region running and serving traffic; the location published; the region selectable through a working path |
| Data-residency guarantees ("data at rest and in transit stays within the selected region") | A data-protection guarantee with no deployment, no control, and no audit behind it | Head of Infrastructure **and** Legal | A technical control enforcing the boundary; an audit demonstrating no cross-region egress of customer data; the guarantee written into published terms |
| Dedicated single-tenant regions | An isolation guarantee with no isolation implementation | Head of Infrastructure **and** Legal | The isolation model documented and independently reviewed; the guarantee written into published terms |
| Region migration on request | An operational procedure implying an operations team and a runbook | Head of Infrastructure | A tested migration runbook, and a named team accountable for running it |

### Onboarding and account operations

| Claim removed | Why it was removed | Approval owner | Evidence required to restore |
|---|---|---|---|
| Signup and contact-sales URLs presented as working | The referenced endpoints were not serving | Product Lead | The URL returning the described page in production |
| Step-by-step console instructions (navigation paths, screen and button names, credential-issuance screens) | Instructed readers to use screens that are not reachable, and the described paths did not match the intended product | Product Lead **and** Design | The console reachable in production, and the documented navigation path verified against the shipped UI on the day of publication |
| A tenant or workspace identifier format | Published a specific string format that the service does not produce | Head of Engineering | The format emitted by the running service, and a test asserting it |
| Onboarding-duration estimates ("about 10 minutes", "about 30 minutes") | An unmeasured performance claim | Product Lead | A measurement across real onboardings, with the sample size and method stated |
| Procurement timelines ("1–3 weeks", week-by-week activity tables) | Described a sales and legal process that is not running | Head of Sales **and** Legal | A defined procurement process with a named owner, and observed durations across completed deals |

### Billing

| Claim removed | Why it was removed | Approval owner | Evidence required to restore |
|---|---|---|---|
| A named payment processor and card-billing instructions | Named a specific processor that is not integrated, and instructed readers to enter card details on a page that does not exist | Finance **and** Head of Engineering | The processor integrated in production; a completed test transaction; the instructions verified against the shipped flow |
| Invoicing behaviour — issue cadence, recipients, delivery | Described an invoicing operation that does not run | Finance | Invoices issued in production, and a named owner for the billing operation |
| Payment terms (for example net-30), purchase orders, wire or ACH acceptance | Contractual payment terms with no published contract | Finance **and** Legal | Published terms containing the payment terms, countersigned |
| Payment-method management instructions | Described console screens that are not reachable | Finance **and** Product Lead | The flow reachable in production and verified on the day of publication |

### Identity, provisioning, and access control

| Claim removed | Why it was removed | Approval owner | Evidence required to restore |
|---|---|---|---|
| SSO configuration walkthroughs (SAML 2.0 and OIDC), including console paths, endpoints, and attribute mappings | Instructed readers through screens that are not reachable, for protocol support that must be confirmed protocol by protocol rather than asserted as a pair | Head of Engineering **and** Product Lead | The specific protocol working in production against at least one named identity provider; the walkthrough verified end to end against the shipped UI; each protocol documented only once it individually works |
| SCIM 2.0 provisioning instructions and a supported-operation matrix | Published a per-operation support matrix that was not verified operation by operation | Head of Engineering **and** Product Lead | Each listed operation exercised against the running service, with the test as evidence; unsupported operations shown as unsupported rather than omitted |
| A named role model and its per-role permission table | Published role names and permissions that did not match the intended product | Head of Engineering **and** Product Lead | The role set and permissions read from the running service, with authorization tests as evidence |
| Group-to-role mapping instructions | Described configuration screens that are not reachable | Head of Engineering | The mapping configurable in production and verified end to end |

### Audit and security posture

| Claim removed | Why it was removed | Approval owner | Evidence required to restore |
|---|---|---|---|
| "Tamper-evident" or "immutable" audit log, unqualified | A named mechanism does exist — an unkeyed SHA-256 hash chain over the per-session JSONL files, checkable with `aasm audit verify-chain`. But unqualified, the phrase claims more than it covers: the chain is unkeyed (an actor who can rewrite the file can re-chain it), it does not extend to the database mirror, and it says nothing about completeness | Head of Security **and** Head of Engineering | For the JSONL scope the mechanism may be named **with those three bounds stated in the same sentence**. Dropping the bounds requires a keyed construction, chain metadata persisted in the DB, and an independent review |
| Audit chain coverage stated without naming the sink | The chain covers the JSONL files only; the `audit_events` and `audit_logs` tables carry no `seq`, `previous_hash`, or `entry_hash` because the runtime-to-storage conversion drops them | Head of Engineering | Chain metadata persisted alongside the DB rows, plus a verifier that runs against the table |
| Audit entries "signed with HMAC-SHA256 using a log-signing key" | **Contradicted by the source** — the mechanism is a keyless SHA-256 hash chain; no HMAC over audit records and no log-signing key exist. A keyless chain does not resist an actor who can rewrite the store and recompute it | Head of Security **and** Head of Engineering | A keyed construction actually implemented, with the key's custody model documented — this needs a code change, not an approval |
| "Logs are append-only; no delete or update API exists" | **Contradicted by the source** — retention pruning issues `DELETE FROM audit_events` in both the SQLite and Postgres drivers, and no trigger, revoked grant, or WORM setting prevents deletion | Head of Engineering | An enforced constraint at the storage layer, plus a test demonstrating that a delete or update against audit rows is rejected |
| "Every agent action produces a log entry" | **Contradicted by the source** — emission is fire-and-forget onto a bounded channel: on backpressure the entry is dropped, counted, and the action proceeds. Separately, **budget debits emit no audit entry at all** — the budget event types are never constructed | Head of Engineering | A fail-closed emission path (the action is rejected when the audit write cannot be durably accepted), an emitter for every event type the claim covers, and tests for the backpressure and restart cases |
| Audit coverage listed by event category (for example "policy checks, events, and budget debits are audited") | A category list is a completeness claim per category. Budget debits are currently in the schema but never emitted, so listing them was wrong even though the other two categories were right | Head of Engineering | Each listed category exercised end to end, with a test asserting an entry is persisted for it |
| Configurable audit-log retention, and retention periods per plan | Published retention durations that the service does not enforce per plan | Head of Engineering **and** Product Lead | The retention period enforced by the running service per plan, with a test asserting it |
| **CEF** export, and "SIEM integration" as a managed capability | CEF does not exist anywhere in the codebase, and there is no integration — only a file a SIEM could ingest. **CSV, JSON and JSON Lines export do ship** via `aasm audit export`, and must not be swept up in this row | Head of Engineering | For CEF: the format actually emitted, plus a sample accepted by at least one named SIEM. For "integration": a delivery path the product operates, not an export a human runs |
| Console budget configuration presented as a managed-service capability | The described form did not exist, and the fields did not match the budget schema the gateway enforces — see [Policy reference](policy-reference.md#budget) | Head of Engineering **and** Product Lead | The managed configuration path working in production, and its fields reconciled against the enforced policy schema |

### Legal and compliance

| Claim removed | Why it was removed | Approval owner | Evidence required to restore |
|---|---|---|---|
| Compliance certifications and frameworks named in an onboarding context (SOC 2, HIPAA, GDPR, ISO 27001) | Named certifications in a way that implied the service holds them, or is ready to be assessed against them | Legal **and** Head of Security | The completed audit report or certificate from the assessing body, with its scope and date; the claim restated to match that scope exactly |
| A compliance status table with a target date ("SOC 2 Type II — In preparation, target Q3 2026"; "ISO 27001 — Roadmap") | A status table inside a compliance section reads as a programme with a trajectory, and the date makes it a commitment. No audit report, assessment scope, or engagement backed any row | Legal **and** Head of Security | A signed engagement with the assessing body defining scope and timing, before any date is published; the certificate itself before any status beyond "engaged" is published |
| An export flag or metadata header named after a framework (for example `--compliance soc2`) cited as compliance evidence | A formatting feature that prepends a header is not an attestation, and citing it as one inflates a build flag into a certification | Head of Security | Nothing to restore — the flag may be documented as a formatting option, but never as evidence of compliance |
| Availability of a Data Processing Agreement (DPA) | Asserted that a specific legal instrument exists and can be requested | Legal | The executed template, approved by counsel, and a named owner for the request process |
| Availability of a Business Associate Agreement (BAA) | Asserted a HIPAA-specific legal instrument, which additionally presupposes a compliance posture that has not been assessed | Legal **and** Head of Security | The executed template approved by counsel, **and** the underlying compliance evidence the agreement depends on |
| Countersignature and legal-review workflow descriptions | Described a legal operation that is not running | Legal | A defined process with a named owner |
| A named commercial licence for the non-open-source capabilities | Named a licence whose terms are not published anywhere | Legal | The licence text published, with a version and effective date |
| A "legal approver" attribution in a page footer | Attributed legal sign-off to a page whose content had since changed | Legal | Sign-off recorded against a specific page revision, re-obtained whenever that page's claims change |

## Language rules that apply to every row

These apply even after an owner approves a claim.

- **Do not use the present tense for a capability that is not running.** "Supports X" and "is available in X" are present-tense claims.
- **Label the maturity.** Use the label vocabulary in [Source of truth & status](source-of-truth.md). An unlabelled statement reads as shipped.
- **Do not use unqualified absolutes** — "all", "every", "complete", "comprehensive", "universal", "unlimited", "immutable", "cannot be bypassed". If one is genuinely correct, name the boundary it holds within and the evidence for it, in the same sentence.
- **Do not publish a number you have not measured.** Latencies, durations, retention periods, and quotas are measurements, not illustrations.
- **Do not soften instead of removing.** If the evidence is missing, the claim comes out.
- **Check the claim against the code, not against the neighbouring prose.** Several claims removed here were restated across three or four pages, and two contradicted the Apache-2.0 source outright. A claim that agrees with another doc is not thereby verified.
- **Understating is also inaccurate.** The goal is a claim that matches the system, not the smallest claim available. During this pass one control was initially written as weaker than it is — the audit chain was described as unverifiable when an operator command to verify it ships today. Removing an unevidenced claim and erasing a real one are different acts; only the first is the safe default.
- **Name the scope a control actually covers.** A mechanism that protects one sink, one protocol, or one code path should say which. "The audit log is hash-chained" and "the JSONL audit files are hash-chained, the database mirror is not" have very different operational consequences.

## Related documentation

- [Source of truth & status](source-of-truth.md) — the canonical maturity label for every area of this hub
- [Quick start (SaaS)](quickstart-saas.md) — managed onboarding, planned
- [Cloud deployment](cloud-deployment.md) — the managed control plane, planned
- [Open core boundary](open-core-boundary.md) — the open-source / commercial split
- [Security model](security-model.md) — the security posture of the open-source enforcement path, including the audit log's actual integrity properties

---

*Last reviewed: 2026-08-06 · AI Agent Assembly Team*
