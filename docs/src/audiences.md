<!-- BEGIN AA-PAGE-META
schema_version: 1
page_type: reference
audience: [contributor]
user_job: Decide which audience and job a page serves before writing it or placing it in navigation
owner: L2:docs
canonical_source: self
describes_capability: false
disclosure_levels: [3, 4]
END AA-PAGE-META -->

# Audiences, jobs-to-be-done and information requirements

This page is for anyone deciding **what a page is for** — its author, its reviewer, or
whoever is designing the navigation it will sit in. It names the readers this product
writes for, the job each of them arrives to finish, and the information a page must
supply for that job to complete.

It exists because a surface can be accurate, well-owned and correctly bounded and
still fail: the reader who needed it could not tell it was theirs, or reached it and
found the one fact their decision turned on was somewhere else. Ownership answers
*who decides this fact*. This page answers the different question of *who needs it, to
finish what*.

It is an input to an information architecture, not a taxonomy for its own sake. Every
audience below has at least one job, every job ends in a named decision or action, and
every information requirement is traced to a surface that satisfies it today or
recorded as a gap. **The gaps are the operative output** — they are the page-shapes
that do not exist yet.

## What governs this page

This page is downstream of five merged artifacts. It **adds no claim** to any of them
and restates none of their definitions.

| Source | What it supplies | Where |
| --- | --- | --- |
| **Page standards** | The `audience` enum this page's audiences *are*, the four disclosure levels, and the metadata contract every page named below must satisfy | [`page-standards.md`](page-standards.md) |
| **Content-layer ownership** | The L0–L6 layer model, each layer's primary audience, and the rule that a derivative may narrow but never widen | [`content-ownership.md`](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/docs/src/development/content-ownership.md) |
| **ADR 0034 — one product truth** | The T1–T7 authority hierarchy, hand-off 7's three-axis ruling, and the reviewer classes that sign off a boundary | [ADR 0034](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/docs/src/adr/0034-one-product-truth-and-cross-repository-documentation-governance.md) |
| **Product promise & message hierarchy** | The one approved promise, the default-posture table, and the Provisional list | [`product-promise.md`](product-promise.md) |
| **Risk scenarios** | The flagship story and three supporting threats, with the Tier 1 / Tier 2 publication gate | [`risk-scenarios.md`](risk-scenarios.md) |

Ticket references are plain text, not links: the tracker is not publicly readable, so
a link would only reach a login wall — and a link checker scores that wall as
reachable, which makes the reference look verified when it is not.

### What this page does not decide

- **Which pages exist, and where they sit.** AAASM-5594 designs the product-site and
  Docs Hub sitemaps from this model. This page supplies the requirements and the gaps;
  it does not draw the tree.
- **Any product claim.** Where an audience's requirement names a product fact, the
  fact is cited to [`product-promise.md`](product-promise.md),
  [`risk-scenarios.md`](risk-scenarios.md) or a manifest row. Nothing here is a new
  capability statement, which is why this page carries `describes_capability: false`.
- **Page metadata rules.** [`page-standards.md`](page-standards.md) owns the block, the
  field reference and the fifteen cross-field rules. This page consumes its `audience`
  key; it does not extend it.
- **Ownership of any content type.** That is
  [`content-ownership.md`](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/docs/src/development/content-ownership.md)'s
  canonical-source table.

## The reader axis, and why this page coins nothing

This is the part most likely to go wrong, so it is stated before the model rather than
left implicit in it.

**A reader vocabulary already exists, and this page does not own it.**
[`page-standards.md`](page-standards.md)'s `audience` key takes one of six values —
`evaluator`, `developer`, `operator`, `security-engineer`, `contributor`, `auditor` —
and those six are the audiences below. Not analogues of them, not a refinement of them:
the same six words, used for the same subject. Publishing a second reader vocabulary
beside that key would create exactly the two-vocabularies defect this programme exists
to eliminate, and it would do it on the one key an information architecture routes by.

The six are also already in
[`content-ownership.md`](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/docs/src/development/content-ownership.md)'s
layer table, in its *Primary audience* column, which reads in full: *anyone assessing
the company* at L0; *evaluators, buyers, technical leaders* at L1; *teams, security
engineers, operators* at L2; *application developers, operators, contributors, security
researchers* at L3; *developers who want to see it run* at L4; *a visitor who landed on
the repo* at L5; *contributors, auditors* at L6. That column is the prose form of the
same axis, and this page reconciles to it rather than beside it — its *security
researchers* are `security-engineer`, and its *buyers* and *technical leaders* are
`evaluator`.

Two of its entries name an **arrival** rather than a reader class, and neither maps to
an `audience` value on its own. L0's *anyone assessing the company* is
[outside what this product writes for](#roles-this-product-does-not-write-for)
entirely — it is the company site's reader. L5's *a visitor who landed on the repo* is
not out of scope but not yet resolved either: they become a `contributor`, a
`developer` or an `evaluator` as soon as they have a job, which is what a README's
"where its documentation is" line exists to decide. Neither is a seventh audience.

### The axis this sits on, and the one rule that binds it

[ADR 0034](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/docs/src/adr/0034-one-product-truth-and-cross-repository-documentation-governance.md)
hand-off 7 fixes three vocabularies, each ranging over a different subject — an
**action** takes an ADR 0033 §6 claim term, a **documentation area** takes a maturity
label, a **product in the portfolio** takes a lifecycle value — and rules that **no
axis may be applied to another's subject**.

The reader axis is a fourth, and it is none of those three. Its subject is *a person
arriving at a page*, which is not an action, not a documentation area and not a
portfolio product. Its vocabulary is the `audience` enum, its owner is
[`page-standards.md`](page-standards.md), and hand-off 7's rule applies to it in both
directions:

- **No term from another axis is written about a reader here.** No audience below
  carries an availability value, a §6 claim term, a maturity label or a lifecycle
  value. A reader is not `Unmeasured` and an audience is not `🧪 Release candidate`.
- **No term is coined on the claim axis.** Forbidden design 12's coining clause is
  scoped to the claim axis alone; this page adds nothing to any axis, so the question
  does not arise. Every product fact cited below is quoted or linked from a page that
  already owns it.

The one thing this page does add is the **job** and the **information requirement**,
and neither is a vocabulary. A job is a sentence about a reader's intent; a requirement
is a sentence about what a page must contain. Neither ranges over an action, an area,
a product or a reader class, so neither collides with anything.

### Crosswalk: seven role labels, six audience values

The parent scope names seven roles. They map onto six `audience` values, and the
collapse is deliberate rather than a rounding error.

| Role as named in the parent scope | `audience` value | Note |
| --- | --- | --- |
| Executive / Evaluator | `evaluator` | Job `EV1` |
| PM / Engineering Leader | `evaluator` | Job `EV3` — the same value, a different job |
| Security / Risk | `security-engineer` | Includes L3's *security researchers* |
| QA / Assurance | `auditor` | L6's audience in the layer table |
| Platform / SRE | `operator` | |
| Application / AI Developer | `developer` | |
| Maintainer / Contributor | `contributor` | |

**Two roles share `evaluator`, and the metadata key cannot tell them apart.** An
executive deciding whether to trial at all and an engineering leader deciding what to
sequence want different pages, and `audience: [evaluator]` routes both to the same
place. The distinction is real and it is carried by **`user_job`**, not by a seventh
enum value — a page states which of the two it serves in the one field
[`page-standards.md`](page-standards.md) reserves for exactly that. Coining a seventh
value would be an edit to someone else's enum, made from a page that does not own it,
to express something the existing schema already expresses.

That is a recorded limitation rather than a silent one: an automated router keyed on
`audience` alone cannot separate `EV1` from `EV3`. If a sitemap needs to, it reads
`user_job`. Whether the enum should gain a value at `schema_version: 2` is
[`page-standards.md`](page-standards.md)'s decision, and this page hands it the
evidence rather than pre-empting it.

## How to read an audience entry

Each of the six carries the same seven fields, and each field exists because a sitemap
needs it.

| Field | What it answers | Why an IA needs it |
| --- | --- | --- |
| **Who** | Which real roles this value covers | Stops two readers being served one page by accident |
| **Arrives knowing** | The context the reader already has | Fixes the disclosure level an entry page opens at |
| **Must be able to do** | The capability the reader leaves with | The test a candidate page is judged against |
| **Jobs** | Each job, and the decision or action it ends in | The unit a page is designed around |
| **Never hidden** | What must be reachable from their route, without exception | The content a navigation redesign may not bury |
| **Belongs elsewhere** | Content this reader is not the audience for | The anti-persona, stated as content rather than as a person |
| **Entry · next · escalation** | The three-step route | The spine of the sitemap branch |

**Belongs elsewhere is an anti-persona in its operative form.** Naming a person nobody
is writing for is unfalsifiable; naming the content that must *not* be on a reader's
entry page is checkable against a candidate sitemap in a single pass. Where a role is
genuinely out of scope for the whole product, it is recorded once at the end rather
than repeated six times.

### On the identifiers

Job ids are two letters and a digit (`EV1`, `SE1`, `AU1`, `OP1`, `DV1`, `CO1`); gaps are
`GAP-n`. Neither shape is arbitrary. The capability manifest's rows are a single letter
and a digit, and the letter is its **`domain`** — `S` sdk, `H` host_action, `N` network,
`M` mcp, `L` devtool_launch, `C` credentials, `I` identity, `G` degraded_mode, `P`
platform, eighty rows in nine series. This page cites some of them by id, so a job
called `S1` and a manifest row called `S1` would collide on exactly the identifier a
checking reader follows. [`risk-scenarios.md`](risk-scenarios.md) lettered its scenarios
`F` and `T1`–`T3` for the same reason. Where a single-letter id appears below, it is the
manifest's and is named as such.

**The letter is the domain, not the owning component**, and `G` is where that distinction
bites. Every `G` row is `domain: degraded_mode` — the series is about *what happens when
a control cannot run*, not about the gateway. Only four of the eleven are owned by
`aa-gateway`; the rest belong to `aa-runtime`, `aa-proxy` and the SDK. This matters for
reading the citations below rather than as a point of order: `G9` is this page's
recurring failure-posture exemplar precisely **because** it is a degraded-mode row, and a
reader who took `G` for "gateway" would look for degradation somewhere else and not find
it.

---

## `evaluator`

**Who.** Someone deciding whether this product should be adopted, and at what altitude
they need the answer. Two roles: an executive or evaluator deciding whether to trial at
all, and a PM or engineering leader deciding what to sequence and what to tell a
stakeholder is not yet available.

**Arrives knowing.** The category, and a concrete worry — an agent did something, or
plausibly could. Sometimes a competitor. Does not know the product's mechanisms, its
routing model, or its platform position, and should not need to.

**Must be able to do.** Reach an accurate account of what the product decides, on which
paths, what is on by default and what it leaves uncovered, without opening an ADR; and
separate what ships today from what is decided but not built.

**Jobs.**

| Job | Stated as a job | Ends in |
| --- | --- | --- |
| `EV1` | Decide whether this product is worth a trial | A trial started, or a recorded reason not to |
| `EV2` | Decide whether one stated capability meets one stated requirement | Met · met with a named limit · not met |
| `EV3` | Decide what to sequence, and what to tell a stakeholder is not available yet | A plan whose gaps are named rather than assumed |

**Never hidden.** The boundary clause, on the same screen as any headline that needs it
([`product-promise.md`](product-promise.md)). The default posture — a capability that
exists but is off is a different product from one that is on. The area's maturity
label. The channel and platform position. That an approval hold has no shipped
operator surface today, which
[`product-promise.md`](product-promise.md#provisional) carries as Provisional.

**Belongs elsewhere.** Protocol semantics, policy field validation rules, ADR rationale,
per-language API surfaces. An entry page that opens with an architecture diagram has
moved L3 content onto an L1 route; per
[`content-ownership.md`](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/docs/src/development/content-ownership.md),
that is content at the wrong layer, not a more thorough page.

**Entry · next · escalation.** Entry: the product website (T6/L1) or this hub's index.
Next: [`product-promise.md`](product-promise.md) level 3 and
[`source-of-truth.md`](source-of-truth.md). Escalation: ADR 0033 §5.3 for the platform
matrix and §6 for the vocabulary, in the core docs.

---

## `security-engineer`

**Who.** Security and risk reviewers, and the *security researchers*
[`content-ownership.md`](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/docs/src/development/content-ownership.md)
names as an L3 audience. One value, because they read the same pages for the same
reason: to find the edge of the boundary.

**Arrives knowing.** Threat modelling, and that vendor descriptions overstate. Arrives
sceptical, which is the correct posture and should be rewarded rather than managed.

**Must be able to do.** Determine the trust boundary and its enumerated bypasses; find
the failure posture of each control, including the ones that fail open; establish what
an absent or degraded control reports; and file a vulnerability report at the right
address.

**Jobs.**

| Job | Stated as a job | Ends in |
| --- | --- | --- |
| `SE1` | Decide whether this boundary is acceptable for a named class of agent traffic | An approval or a refusal for one deployment |
| `SE2` | Determine what a quiet result means | An uninspected action read as *Unmeasured* rather than as clean |
| `SE3` | Report a vulnerability | A report filed against the owning repository's `SECURITY.md` |

**Never hidden.** The bypass catalogue. The failure posture of every control cited,
including the silent fail-open on the budget store that
[`risk-scenarios.md`](risk-scenarios.md) records as row `G9`. That the audit chain is
tamper-evident rather than signed, and that emission is best-effort. The platform
matrix, in both directions — the understatement is a defect as much as the
overstatement.

**Belongs elsewhere.** Install ergonomics, SDK API surface, positioning. A security
reader does not need a getting-started path on their entry page and will read one as
evasion.

**Entry · next · escalation.** Entry: this hub's [`security-model.md`](security-model.md)
— **which carries a superseded model today**, recorded as gap `GAP-5` below. Next: the
core threat model and ADR 0033. Escalation: the capability manifest rows and the
verification reports in the core repository.

---

## `auditor`

**Who.** QA and assurance readers: anyone whose job is to check a published statement
against something, rather than to build or to buy.

**Arrives knowing.** How to evaluate evidence. Does not know the codebase and should
not have to read it to establish what backs a sentence.

**Must be able to do.** Take any published claim and reach the evidence it rests on, or
establish that there is none and record that; and interpret a verification result for
what it establishes rather than for what it suggests.

**Jobs.**

| Job | Stated as a job | Ends in |
| --- | --- | --- |
| `AU1` | Find the evidence behind one published claim | A cited row, or a recorded gap |
| `AU2` | Verify an audit record | A result read as integrity of the entries present, not completeness of the log |
| `AU3` | Decide whether a demonstration may be published as evidence | Tier 1 published, or Tier 2 withheld |

**Never hidden.** Which statements are Provisional, and why. The Tier 1 / Tier 2
publication gate in [`risk-scenarios.md`](risk-scenarios.md). That a passing chain
verification does not establish the log is whole. That absence of a finding is a fact
about the observer.

**Belongs elsewhere.** Positioning and conversion copy. An auditor arriving at a
marketing page has been misrouted, and no amount of accuracy in that page fixes it.

**Entry · next · escalation.** Entry: **none on this hub today** — gap `GAP-4`. Next: the
determinations in [`risk-scenarios.md`](risk-scenarios.md), which is the closest thing
to a claim-to-evidence route currently published. Escalation:
[`capability-manifest.yaml`](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/governance/capability-manifest.yaml)
and the verification reports — both L6, and
[`content-ownership.md`](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/docs/src/development/content-ownership.md)
states that nothing in L6 is a reader-facing page, which is the shape of the gap.

---

## `operator`

**Who.** Platform engineers and SREs: the people who put the product in front of an
agent and keep it there.

**Arrives knowing.** How to run a service. Does **not** know that routing is a thing
they do per agent and per launch, which is the single most consequential thing this
audience learns.

**Must be able to do.** Route an agent on one host; install the right artifact for
their platform from a channel that carries it; observe what the stack recorded; and
work out why a control did not fire.

**Jobs.**

| Job | Stated as a job | Ends in |
| --- | --- | --- |
| `OP1` | Route an agent through the product on one host | A governed launch |
| `OP2` | Decide what to install, on which platform, from which channel | An install performed |
| `OP3` | Work out why a control did not fire | A corrected configuration, or an accepted bound |
| `OP4` | Stand up a limited-function self-hosted stack for evaluation | A running stack |

**Never hidden.** That routing is per agent and per launch, so an agent nobody routed
is outside everything. The per-channel and per-platform position — the manifest's
`released_channels` and `released_platforms` are per row, and
[`risk-scenarios.md`](risk-scenarios.md) records that the proxy reaches macOS through
crates.io only. Which controls are off until configured. The failure postures, so a
silent fail-open is not discovered during an incident.

**Belongs elsewhere.** Production orchestration commitments. Helm, Terraform and
Kubernetes are a research question under current project policy, not committed work,
and [`open-core-boundary.md`](open-core-boundary.md) is where the self-host scope is
stated. A page that reads as a production deployment guide has made a commitment the
product has not.

**Entry · next · escalation.** Entry: this hub's *Getting Started* section — **whose
two pages are both `🗺️ Planned`**, gap `GAP-2`. Next:
[`docker-containers.md`](docker-containers.md) and
[`self-host-observability.md`](self-host-observability.md), which describe shipping
behaviour but are filed under *Operations* rather than on the entry route.
Escalation: the core quick-start and CLI reference.

---

## `developer`

**Who.** Application and AI developers integrating the product into an agent they are
building.

**Arrives knowing.** Their framework and their language. Wants working code, and will
judge the product on how quickly they get some.

**Must be able to do.** Add a policy checkpoint in their language; choose an SDK mode
knowing what each one does; and find a runnable integration for the framework they are
actually using.

**Jobs.**

| Job | Stated as a job | Ends in |
| --- | --- | --- |
| `DV1` | Add a policy checkpoint to an agent in my language | Code that runs and reaches a decision |
| `DV2` | Choose an SDK mode | An explicit choice between the advisory default and the check-capable mode |
| `DV3` | Find a runnable integration for my framework | An example running locally |

**Never hidden.** That the SDK is advisory, and that a policy refusal blocks a wrapped
tool only in the check-capable mode — [`product-promise.md`](product-promise.md)'s
default-posture table carries both. That an unadapted framework, or a call that does
not go through the framework's dispatch, is outside the wrapper: the manifest's `S1`
row lists both under `known_bypasses`, alongside *not calling `init_assembly()`* and
raw HTTP or subprocess use, and a quick-start that omits them has widened the claim by
dropping a precondition.

**Belongs elsewhere.** The threat model, the deployment matrix, positioning. A
developer needs the boundary, but as a precondition on their own code rather than as a
security chapter.

**Entry · next · escalation.** Entry: **no language route from this hub today** — gap
`GAP-7`. Next: the SDK documentation mounted at `/python-sdk/`, `/node-sdk/` and
`/go-sdk/` by the aggregation pipeline. Escalation: the core API reference and the
runnable examples at L4.

---

## `contributor`

**Who.** Maintainers and contributors, in any repository in the org, including the
coding agents working under
[the org's rules](https://github.com/ai-agent-assembly/.github/blob/HEAD/.claude/rules/03-coding-standards.md).

**Arrives knowing.** The repository they are in. Does **not** know the cross-repository
truth hierarchy, and will otherwise fix a defect in the place they noticed it.

**Must be able to do.** Classify a fact and find its canonical owner; choose a sanctioned
reuse pattern; write a page that satisfies the metadata contract; and route a correction
to the source before the derivative.

**Jobs.**

| Job | Stated as a job | Ends in |
| --- | --- | --- |
| `CO1` | Decide where a fact belongs before writing it | A layer and a canonical owner named in the ticket |
| `CO2` | Write a page that conforms | A page carrying a valid metadata block |
| `CO3` | Route a correction | A pull request against the canonical source first |
| `CO4` | Decide whether a change is a material truth change | The right reviewer class requested |

**Never hidden.** That depth is not a defect — no rule in this programme may be cited to
thin a component's documentation. That understating is a defect too, in the same way
overstating is. That an ownership dispute is a decision, not an edit, and stops rather
than resolves inside a content pull request.

**Belongs elsewhere.** Positioning copy and conversion paths. A contributor reading
those is reading the wrong layer for their job.

**Entry · next · escalation.** Entry: [`page-standards.md`](page-standards.md). Next:
[`content-ownership.md`](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/docs/src/development/content-ownership.md)
and
[`claim-vocabulary.md`](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/docs/src/development/claim-vocabulary.md).
Escalation:
[ADR 0034](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/docs/src/adr/0034-one-product-truth-and-cross-repository-documentation-governance.md)
for precedence, waivers and the reviewer classes.

---

## Roles this product does not write for

Recorded once rather than repeated as six anti-personas, because each is out of scope
for every surface rather than for one route.

| Not an audience | Why | Where such a reader goes |
| --- | --- | --- |
| Someone evaluating the **company** rather than the product | L0's job, and L0 must not carry a per-capability status or a platform claim | `horonomy.dev` |
| A reader looking for **agent-building** guidance | This product governs an agent; it does not help write one. A page that teaches agent construction has widened the product's subject | Framework documentation |
| A **procurement or compliance** reader wanting an SLA, a region or a certification | Planned, not available; asserting any of it is a managed-service claim bounded by the checklist | [`saas-claim-publication-checklist.md`](saas-claim-publication-checklist.md) and [`source-of-truth.md`](source-of-truth.md) |
| A reader of the **private** `cloud` or `agent-assembly-enterprise` internals | Outside the public content boundary; paraphrasing does not make it publishable | The public ticket |

## Information requirements

One row per (audience, job, requirement). **What a page must supply** is the contract:
if a candidate page does not carry it, the job does not complete on that page. **Where
it is satisfied today** is this model applied once to the surfaces that exist, which is
what makes it a review instrument rather than a wish list.

Status values: **✅ satisfied** — a published page carries it on that audience's route;
**◐ partial** — a published page carries it, but not on that route, or not in full;
**✗ gap** — nothing published carries it.

### Requirements for `evaluator`

| ID | Job | What a page must supply | Where it is satisfied today | Status |
| --- | --- | --- | --- | --- |
| `IR-EV1-a` | `EV1` | The one approved promise, with its boundary clause on the same screen | [`product-promise.md`](product-promise.md) | ◐ partial — filed under *About*, not on an evaluator route |
| `IR-EV1-b` | `EV1` | One concrete story of a decision the product made, with its determination | [`risk-scenarios.md`](risk-scenarios.md) | ✅ satisfied |
| `IR-EV1-c` | `EV1` | What is on by default, as a table rather than as prose | [`product-promise.md`](product-promise.md) level 3 | ◐ partial — one satisfier, and it is not on the route (`GAP-8`) |
| `IR-EV2-a` | `EV2` | Per capability: whether it ships, on which channel and which platform | manifest `released_channels` / `released_platforms` (L6) | ✗ gap `GAP-3`, `GAP-4` |
| `IR-EV2-b` | `EV2` | Per capability: whether anything reaches it by default | manifest `default_state` (L6); [`product-promise.md`](product-promise.md) for the headline set | ◐ partial |
| `IR-EV2-c` | `EV2` | The stated limit that changes what may be relied on | [`product-promise.md`](product-promise.md), [`risk-scenarios.md`](risk-scenarios.md) known-boundary blocks | ✅ satisfied |
| `IR-EV3-a` | `EV3` | The maturity of each documented area | [`source-of-truth.md`](source-of-truth.md) | ✅ satisfied |
| `IR-EV3-b` | `EV3` | What is decided but not built, with its ticket and no capability claim | scattered `Planned` statements; no roadmap surface | ✗ gap `GAP-6` |
| `IR-EV3-c` | `EV3` | The open-source / managed split, so a plan can be split along it | [`open-core-boundary.md`](open-core-boundary.md) | ✅ satisfied |

### Requirements for `security-engineer`

| ID | Job | What a page must supply | Where it is satisfied today | Status |
| --- | --- | --- | --- | --- |
| `IR-SE1-a` | `SE1` | The trust boundary, in the current architecture rather than a superseded one | core ADR 0033 and the core security section | ◐ partial — the hub entry page is superseded (`GAP-5`) |
| `IR-SE1-b` | `SE1` | The enumerated bypasses, published rather than implied | [`risk-scenarios.md`](risk-scenarios.md); manifest `known_bypasses` | ◐ partial — complete only at L6 |
| `IR-SE1-c` | `SE1` | The failure posture per control, including the fail-open ones | manifest `failure_posture`; `G9` in [`risk-scenarios.md`](risk-scenarios.md) | ◐ partial — one worked instance published, the rest at L6 (`GAP-4`) |
| `IR-SE1-d` | `SE1` | The platform matrix, stated in both directions | core ADR 0033 §5.3 | ◐ partial — no hub-level restatement |
| `IR-SE2-a` | `SE2` | That an uninspected action is reported as *Unmeasured*, never as clean | [`product-promise.md`](product-promise.md), [`risk-scenarios.md`](risk-scenarios.md) | ✅ satisfied |
| `IR-SE2-b` | `SE2` | What a passing chain verification does and does not establish | [`product-promise.md`](product-promise.md) | ✅ satisfied |
| `IR-SE3-a` | `SE3` | The vulnerability reporting address for the repository in question | each repo's `SECURITY.md`, falling back to the org default | ◐ partial — no hub route names it |

### Requirements for `auditor`

| ID | Job | What a page must supply | Where it is satisfied today | Status |
| --- | --- | --- | --- | --- |
| `IR-AU1-a` | `AU1` | A published route from a claim to the row or record that backs it | nothing published; the manifest is L6 | ✗ gap `GAP-4` |
| `IR-AU1-b` | `AU1` | Which claims are Provisional, and the ticket that would close each | [`product-promise.md`](product-promise.md#provisional) | ✅ satisfied |
| `IR-AU2-a` | `AU2` | What the verification command establishes, and its two negative results | [`product-promise.md`](product-promise.md) | ✅ satisfied |
| `IR-AU3-a` | `AU3` | The Tier 1 / Tier 2 gate, and which tickets lift it | [`risk-scenarios.md`](risk-scenarios.md) | ✅ satisfied |
| `IR-AU3-b` | `AU3` | For a managed-service claim, the register that bounds it | [`saas-claim-publication-checklist.md`](saas-claim-publication-checklist.md) | ◐ partial — interim, and managed-service only |

### Requirements for `operator`

| ID | Job | What a page must supply | Where it is satisfied today | Status |
| --- | --- | --- | --- | --- |
| `IR-OP1-a` | `OP1` | That routing is performed per agent and per launch | [`product-promise.md`](product-promise.md) level 2 step 1 | ◐ partial — not on the operator route |
| `IR-OP1-b` | `OP1` | The launch preconditions in full, none dropped | core quick-start; [`risk-scenarios.md`](risk-scenarios.md) governed-path fields | ◐ partial |
| `IR-OP2-a` | `OP2` | Which artifact reaches which platform, from which channel | manifest (L6); [`compatibility.md`](compatibility.md) carries versions only | ✗ gap `GAP-3` |
| `IR-OP2-b` | `OP2` | An install route that does not begin with an unavailable page | [`docker-containers.md`](docker-containers.md) | ✗ gap `GAP-2` on the entry route |
| `IR-OP3-a` | `OP3` | Which controls are off until configured | [`product-promise.md`](product-promise.md) level 3 | ◐ partial |
| `IR-OP3-b` | `OP3` | The failure postures, including the ones that produce no decision-path signal | [`risk-scenarios.md`](risk-scenarios.md) for `G9`; manifest for the rest | ◐ partial (`GAP-4`) |
| `IR-OP4-a` | `OP4` | The scope of a limited-function self-host, and what it excludes | [`open-core-boundary.md`](open-core-boundary.md), [`docker-containers.md`](docker-containers.md) | ✅ satisfied |
| `IR-OP4-b` | `OP4` | What the stack records, and how to read it | [`self-host-observability.md`](self-host-observability.md) | ◐ partial — filed off the entry route |

### Requirements for `developer`

| ID | Job | What a page must supply | Where it is satisfied today | Status |
| --- | --- | --- | --- | --- |
| `IR-DV1-a` | `DV1` | A language-specific first checkpoint, reachable from this hub | SDK docs, mounted but unlisted | ✗ gap `GAP-7` |
| `IR-DV1-b` | `DV1` | The initialisation preconditions the wrapper depends on | SDK docs; manifest `S1` `preconditions` (`AA_AGENT_ID` set) | ◐ partial |
| `IR-DV2-a` | `DV2` | That the SDK is advisory, and what the check-capable mode changes | [`product-promise.md`](product-promise.md) level 3 | ◐ partial — not on a developer route |
| `IR-DV2-b` | `DV2` | What sits outside the wrapper, stated as preconditions on their code | manifest `S1` `known_bypasses`, and rows `S10`–`S12` (L6) | ✗ gap `GAP-4` |
| `IR-DV3-a` | `DV3` | A runnable integration per framework, and a way to choose between them | the `examples` repository (L4) | ◐ partial — no hub route |

### Requirements for `contributor`

| ID | Job | What a page must supply | Where it is satisfied today | Status |
| --- | --- | --- | --- | --- |
| `IR-CO1-a` | `CO1` | The canonical owner per content type | [`content-ownership.md`](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/docs/src/development/content-ownership.md) | ✅ satisfied |
| `IR-CO1-b` | `CO1` | The four sanctioned reuse patterns, and when each applies | same | ✅ satisfied |
| `IR-CO2-a` | `CO2` | The metadata contract and a copyable template per page type | [`page-standards.md`](page-standards.md) | ✅ satisfied |
| `IR-CO2-b` | `CO2` | Which audience and job a page is being written for | **this page** | ✅ satisfied |
| `IR-CO3-a` | `CO3` | Where a correction goes first, as an ordered procedure | [`content-ownership.md`](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/docs/src/development/content-ownership.md) | ✅ satisfied |
| `IR-CO4-a` | `CO4` | The reviewer classes, and what counts as a material truth change | [ADR 0034](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/docs/src/adr/0034-one-product-truth-and-cross-repository-documentation-governance.md) Decision 9 | ✅ satisfied |

## The gaps

This is the list AAASM-5594 turns into pages. Each row names the requirement it closes
and the page-shape it implies; none of them is a request to move an existing page
without a job to justify it.

| # | Gap | Requirements it blocks | Page-shape implied |
| --- | --- | --- | --- |
| `GAP-1` | **No surface addresses a reader by role.** This hub's contents are grouped by topic; the product website publishes four pages and a blog. Nothing on either routes by audience | every route below | An audience-addressed entry, on both L1 and L2 |
| `GAP-2` | **The hub's *Getting Started* section contains only `🗺️ Planned` pages.** Both entries are labelled *Coming soon*, and [`source-of-truth.md`](source-of-truth.md) marks the Operations area `🗺️ Planned` with a managed-service page as its *Where to read* cell — while two pages describing shipping behaviour sit under *Operations* and are not named by that row | `IR-OP2-b`, `IR-OP4-b` | An operator entry that starts from what ships |
| `GAP-3` | **No per-channel, per-platform install position is published on this hub.** [`compatibility.md`](compatibility.md) pairs versions across the four repos and names the two SDK registries, npm and PyPI — but no Homebrew, crates.io, GitHub release or install-script position for the core binary, and **no platform at any point**: a sweep for `linux`, `macos`, `windows`, `x86_64` and `aarch64` returns zero hits in that file. The facts exist per row in the manifest, as `released_channels` and `released_platforms` | `IR-EV2-a`, `IR-OP2-a` | A channel-and-platform matrix at L2, generated from the manifest rather than hand-written |
| `GAP-4` | **The evidence layer has no reader-facing surface.** `capability-manifest.yaml` exists with a schema, a validator and a CI gate, and `verification-reports/**` holds the records — but [`content-ownership.md`](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/docs/src/development/content-ownership.md) states nothing in L6 is a reader-facing page, and ADR 0034's T3 approved-claims registry does not exist yet | `IR-AU1-a`, `IR-DV2-b`, and the L6-only half of `IR-EV2-a`, `IR-SE1-b`, `IR-SE1-c`, `IR-OP3-b` | A generated claim-to-evidence surface at L2 |
| `GAP-5` | **The hub's security entry page carries a superseded model.** [`product-promise.md`](product-promise.md) records that where this hub still carries the older framing, ADR 0033 wins, and names the migration tickets — but a reader arriving at that page first never sees the note | `IR-SE1-a` | A security entry rewritten against ADR 0033, not a note added to the old one |
| `GAP-6` | **No roadmap surface exists.** No file named for one is present in this repository, the product website or the core repository, checked with a positive control in the same sweep; ADR 0034 hand-off 4 assigns the owner, so the owner currently owns an empty surface | `IR-EV3-b` | A bounded forward-looking page at L1, in the admissible forms only |
| `GAP-7` | **No language route from this hub to the SDKs.** The SDK documentation is mounted under `/python-sdk/`, `/node-sdk/` and `/go-sdk/` by the aggregation pipeline, and this hub's contents list none of them | `IR-DV1-a`, `IR-DV3-a` | A developer entry that branches by language |
| `GAP-8` | **The default-posture table has exactly one satisfier, and it is filed under *About*.** No page of type `product` exists on this hub yet, and that is the page type [`page-standards.md`](page-standards.md) requires to state defaults at level 3 | `IR-EV1-a`, `IR-EV1-c`, `IR-OP3-a`, `IR-DV2-a` | One or more `product` pages carrying levels 1 to 3 |

### Two hand-offs, not gaps

Recorded here because they were found while deriving the gaps and would otherwise be
lost, but neither is this page's to fix and neither blocks a requirement.

- **`page-standards.md`'s note that the capability manifest has not started is now
  stale.** `capability-manifest.yaml` is present in the core repository under
  AAASM-5531 with a schema, a semantic validator and a CI gate. That affects the
  reserved status of `capability_ids` and the `platforms[]` hand-off, both of which
  that page marks as pending AAASM-5531. It is
  [`page-standards.md`](page-standards.md)'s edit to make, at whatever schema version
  it decides.
- **The `evaluator` value cannot separate `EV1` from `EV3`.** Recorded above; the
  evidence is handed to [`page-standards.md`](page-standards.md) rather than resolved
  by coining a value here.

## Using this model

### To evaluate an existing page

Answer four questions in order. The first two are the ones that catch a misplaced page.

1. **Which audience value, and which job?** Name one of the six and one job id. A page
   that serves no job on this list either has an unnamed audience — in which case name
   it — or does not need to exist. This is the same question
   [`page-standards.md`](page-standards.md)'s `audience` and `user_job` keys ask, so a
   conforming page has already answered it.
2. **Does it carry every requirement for that job?** Walk the rows for that job id. A
   missing requirement is either a defect in the page or a link the page must add.
3. **Does it carry anything from *belongs elsewhere*?** Content for another audience on
   this reader's route is the commonest cause of a page that is accurate and still
   unusable.
4. **Is anything from *never hidden* absent?** That list has no exceptions, and its
   items are the ones a redesign removes first because they are the least attractive.

### To evaluate a proposed navigation

1. **Every audience has an entry.** Six values, six routes. A value with no entry means
   a reader with no way in.
2. **Every route reaches its escalation in three steps.** Entry, next, escalation. A
   fourth step is a route nobody finishes.
3. **No route opens on a `🗺️ Planned` page.** Gap `GAP-2` is what that looks like when it
   happens.
4. **Every gap above is either closed by a page in the proposal, or is carried forward
   as a named open item.** A sitemap that silently drops one has not resolved it.
5. **No route requires a reader to reach L6 to finish their job.** Where it does today,
   that is gap `GAP-4` and the fix is a surface, not a deep link.

## How this page meets its acceptance criteria

| Criterion | How it is met |
| --- | --- |
| Every audience has an explicit job-to-be-done and information contract | Six audience sections, each with a *Jobs* table whose every row ends in a decision or an action, and an [information requirements](#information-requirements) block keyed by job id. Twenty jobs, forty requirements, each with a named satisfier or a gap |
| The model distinguishes non-developer technical readers from application developers and maintainers | `security-engineer`, `operator` and `auditor` are the non-developer technical readers and each carries its own jobs, its own *never hidden* list and its own *belongs elsewhere* boundary; `developer` and `contributor` are separate values with separate routes. The [crosswalk](#crosswalk-seven-role-labels-six-audience-values) states which of the parent scope's seven roles lands on which value, including the two that share `evaluator` and the reason they are separated by `user_job` rather than by a coined enum value |
| The model is usable to evaluate current pages and proposed navigation | [Using this model](#using-this-model) gives both checklists, and the *Where it is satisfied today* column is that evaluation already applied once to every published surface — which is what produced [the gaps](#the-gaps) |
| Website, Docs Hub, SaaS docs and project docs owners approve the boundaries | Not something a page can assert about itself. The boundaries are stated in the owning classes' own terms — L1/T6 for positioning and the roadmap, L2/T5 for routing and maturity, L3/T4 for architecture and semantics, and the SaaS claim publication checklist for managed-service claims — so approval is the pull request's, under ADR 0034 Decision 9, from `truth-owner-website`, `truth-owner-docs-hub` and `truth-owner-core` |

## What this page hands off

| To | What |
| --- | --- |
| **AAASM-5594** | The eight gaps and the forty information requirements, as the input to the product-site and Docs Hub sitemaps. The two navigation checklists are intended to be sufficient to review a proposed tree without further decisions from this page |
| **AAASM-5585 · AAASM-5587** | The `evaluator` entry and its requirements, including the default-posture table gap `GAP-8` |
| **AAASM-5596 · AAASM-5608 · AAASM-5611** | The per-audience *never hidden* lists, which bound what a rewritten page may drop |
| **`page-standards.md`** | Two records: that the `evaluator` value cannot separate `EV1` from `EV3`, and that its AAASM-5531 pending note is now stale |

---

*Last reviewed: 2026-08-07 — AI Agent Assembly Team*
