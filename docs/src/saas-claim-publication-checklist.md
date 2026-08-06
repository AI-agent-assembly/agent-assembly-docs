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
and [Open core boundary](open-core-boundary.md).

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
| "Tamper-evident" or "immutable" audit log | A cryptographic-integrity claim, which requires a named mechanism and a verification procedure — the pages named neither | Head of Security **and** Head of Engineering | The integrity mechanism named and documented; a reader-runnable verification procedure; an independent review of the mechanism |
| Configurable audit-log retention, and retention periods per plan | Published retention durations that the service does not enforce per plan | Head of Engineering **and** Product Lead | The retention period enforced by the running service per plan, with a test asserting it |
| SIEM export in named formats (JSON, CEF) | Named specific interchange formats with no export path | Head of Engineering | The export produced by the running service; a sample accepted by at least one named SIEM |
| Console budget configuration presented as a managed-service capability | The described form did not exist, and the fields did not match the budget schema the gateway enforces — see [Policy reference](policy-reference.md#budget) | Head of Engineering **and** Product Lead | The managed configuration path working in production, and its fields reconciled against the enforced policy schema |

### Legal and compliance

| Claim removed | Why it was removed | Approval owner | Evidence required to restore |
|---|---|---|---|
| Compliance certifications and frameworks named in an onboarding context (SOC 2, HIPAA, GDPR, ISO 27001) | Named certifications in a way that implied the service holds them, or is ready to be assessed against them | Legal **and** Head of Security | The completed audit report or certificate from the assessing body, with its scope and date; the claim restated to match that scope exactly |
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

## Related documentation

- [Source of truth & status](source-of-truth.md) — the canonical maturity label for every area of this hub
- [Quick start (SaaS)](quickstart-saas.md) — managed onboarding, planned
- [Cloud deployment](cloud-deployment.md) — the managed control plane, planned
- [Open core boundary](open-core-boundary.md) — the open-source / commercial split

---

*Last reviewed: 2026-08-06 · AI Agent Assembly Team*
