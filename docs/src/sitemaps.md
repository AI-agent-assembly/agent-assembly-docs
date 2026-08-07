<!-- BEGIN AA-PAGE-META
schema_version: 1
page_type: reference
audience: [contributor]
user_job: Place a page in the product website or Docs Hub navigation, or take a non-overlapping slice of the implementation
owner: L2:docs
canonical_source: self
describes_capability: false
disclosure_levels: [3, 4]
END AA-PAGE-META -->

# Product website and Docs Hub sitemaps

This page is for anyone about to move a page, add a route, or pick up one of the
navigation tickets. It draws the two trees — `agent-assembly.com` and
`docs.agent-assembly.com` — and says, for every page that exists today and every page
the model implies, which section it belongs to, which reader it serves, which job that
reader is finishing, and which ticket may touch it.

It exists because navigation is where a correct set of pages still fails. Every page
below can be accurate, correctly owned and correctly bounded, and a reader can still
land on a repository directory and give up. The current hub sections are named
*Platform & Security*, *Getting Started*, *Operations*, *Reference*, *Support* and
*About* — five of those six describe a **kind of content**, not a thing a reader is
trying to finish, and the one that names a task opens on two pages that are both
`🗺️ Planned`.

**This page draws the trees; it does not build them.** Every implementation ticket is
named in [the partition](#partitioning-this-into-non-overlapping-tickets), and no page
body is edited by this ticket except the two files that carry this page itself.

## What governs this page

This page adds no product claim and coins no vocabulary. Everything it routes was
decided somewhere else.

| Source | What it supplies |
| --- | --- |
| [`audiences.md`](audiences.md) (AAASM-5591) | The six `audience` values, twenty jobs, forty information requirements, eight gaps, and the two checklists a proposed navigation is judged against |
| [`role-narratives.md`](role-narratives.md) (AAASM-5584) | The four role briefs the website's role surfaces are built from, and the shared claim register they cite |
| [`page-standards.md`](page-standards.md) (AAASM-5595) | The four disclosure levels, the `page_type` → required-levels table, the `owner` surface pairs, the `area` ids and the `availability` values |
| **Content-layer ownership** (AAASM-5592) | The L0–L6 roster, one canonical owner per content type, the narrowing rule and the four reuse patterns. [`content-ownership.md`](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/docs/src/development/content-ownership.md) |
| **Documentation inventory** (AAASM-5593) | The census, the disposition vocabulary, and the finding that every current hub page except `policy-reference.md` is `Keep`, that one being `Review`. [`documentation-inventory.md`](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/docs/src/development/documentation-inventory.md) |
| **ADR 0033 §6** | The eleven claim terms, and forbidden designs 1 and 2. [ADR 0033](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/docs/src/adr/0033-canonical-governance-and-enforcement-architecture.md) |
| **ADR 0034 §1** | The T1–T7 truth hierarchy, and hand-off 4 assigning the roadmap to L1. [ADR 0034](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/docs/src/adr/0034-one-product-truth-and-cross-repository-documentation-governance.md) |
| [`source-of-truth.md`](source-of-truth.md) | The status map, whose `Maturity` cell is the only place an area's maturity is set |

Ticket references are plain text, not links: the tracker is not publicly readable, so a
link would only reach a login wall — and a link checker scores that wall as reachable,
which makes the reference look verified when it is not.

### Why the product website's tree is drawn on this hub

`content-ownership.md` puts positioning at L1 and reference material off it, so the
obvious reading is that the website's sitemap belongs in the website's repository. It
does not, for the same reason [`role-narratives.md`](role-narratives.md) — briefs for
four **website** pages — is a hub page: ADR 0034 puts the Docs Hub above the product
website in the truth hierarchy, so the website derives from the hub and never the
reverse. A sitemap held in two repositories is two sitemaps within one release.

The website repository carries a pointer at
`design/content-briefs/AAASM-5594-sitemap.md`, which restates no route table of its
own.

### What this page does not decide

- **Any product claim.** Nothing here states what the product does. Where a route is
  named for a capability, the capability is the register entry's, not this page's.
- **The wording of any page.** [`role-narratives.md`](role-narratives.md) owns the role
  copy, [`product-promise.md`](product-promise.md) owns the promise.
- **`policy-reference.md`'s fate.** The hub and Core each publish an independent policy
  reference. That is the reference instance of prohibited duplication, and
  `documentation-inventory.md` marks the hub page `Review`, owned by AAASM-5586 and
  AAASM-5609. This page files it under *Reference* because that is where a reader looks
  for it today; it takes no position on whether it survives.
- **Page metadata.** [`page-standards.md`](page-standards.md) owns the block.
- **Slugs on the product website.** This page fixes the route *count* and the route
  *prefix*; AAASM-5587 picks the final slugs.

## Two axes, and why the six sections are only one of them

The six sections the parent scope names — Evaluate, Integrate, Operate, Verify,
Reference, Contribute — are a **task** axis. `audiences.md` routes on a **reader** axis
of six `audience` values. Neither substitutes for the other, and collapsing them is the
mistake available here.

Filing by reader gives six role sections, and a reader with two jobs has to pick a
personality before they can pick a task. Filing by task alone leaves
`audiences.md`'s first navigation check unmet — *"Six values, six routes. A value with
no entry means a reader with no way in"* — which is gap `GAP-1`.

So the tree carries both, in different places:

- **The sidebar is the task axis.** Six sections, each named for something a reader is
  trying to finish.
- **The index page is the reader axis.** [`README.md`](index.html) gains a six-row
  router — one row per `audience` value, naming that reader's entry, next step and
  escalation. `GAP-1` asks for exactly this and bounds it: the index already carries a
  role paragraph covering `operator` and `security-engineer` and routing `developer`
  and `contributor` off-site, so the router **extends** that paragraph rather than
  replacing it, and the residue is `evaluator` and `auditor`.

## The Docs Hub sitemap

### The six sections, and the task each one is

| Section | The task or decision a reader arrives with | `audience` values entering here | Jobs |
| --- | --- | --- | --- |
| **Evaluate** | Decide whether to adopt this, and learn what it leaves uncovered | `evaluator`, `security-engineer` | `EV1`, `EV2`, `EV3`, `SE1` |
| **Integrate** | Add a policy checkpoint to an agent I am building | `developer` | `DV1`, `DV2`, `DV3` |
| **Operate** | Run it on a host, and work out why a control did not fire | `operator` | `OP1`, `OP2`, `OP3`, `OP4` |
| **Verify** | Check a published statement against the evidence behind it | `auditor`, `security-engineer` | `AU1`, `AU2`, `AU3`, `SE2`, `SE3` |
| **Reference** | Look up one exact field, value or version | all six | supports every job; ends none |
| **Contribute** | Decide where a fact belongs, and write a page that conforms | `contributor` | `CO1`, `CO2`, `CO3`, `CO4` |

**Reference is the one section whose row is a lookup rather than a decision**, and that
is stated rather than dressed up. A reader in *Reference* is mid-task in one of the
other five. It earns a top-level slot because the alternative — filing the policy
reference under whichever task most often needs it — makes a lookup require knowing
whose job it is, which is the failure this whole exercise is about.

### Where every existing page goes

There are **24** pages under `docs/src/` today, and this is a re-filing rather than a
migration: `documentation-inventory.md`'s census dispositions them all as `Keep` **with
one exception** — `policy-reference.md` is `Review`, owned elsewhere. Two of the 24 are
not in that census at all, because `audiences.md` and `role-narratives.md` merged after
it was taken; the census counts 22 and both of those are `Keep` by the same reasoning as
their neighbours.

Each page appears in exactly one section. The counts below sum to 24, which is the check
that no page was filed twice or dropped — and it is a real count, not a reading of the
tables: no page is assigned twice, none in the tree is unassigned, and none is assigned
that is not in the tree.

#### Prefix chapters

Two, above the first separator, so they render above the six sections at every
viewport width.

| Page | Purpose | Canonical owner |
| --- | --- | --- |
| [`README.md`](index.html) | The index, and the six-row audience router | `L2:docs` |
| [`documentation.md`](documentation.md) | The component router — the standing route to `/core/`, `/python-sdk/`, `/node-sdk/`, `/go-sdk/` and `/arena/` | `L2:docs` |

#### Evaluate — 8 existing pages

| Page | Why it is here | Note |
| --- | --- | --- |
| [`product-promise.md`](product-promise.md) | Levels 1–3 of the promise, including the default-posture table | Closes `GAP-8` **on the evaluator route only** — one of the three routes that gap blocks. Opens the section until AAASM-5609 lands |
| [`risk-scenarios.md`](risk-scenarios.md) | The flagship story and three supporting threats — `IR-EV1-b` | Home section; *Verify* links to its negative-control section rather than re-filing it |
| [`security-model.md`](security-model.md) | The `security-engineer` entry — `SE1` | Carries a superseded model (`GAP-5`); the rewrite is another ticket's |
| [`comparison.md`](comparison.md) | Category placement — `EV1` | |
| [`open-core-boundary.md`](open-core-boundary.md) | The open-source / commercial split — `IR-EV3-c` | Canonical owner of that split per the ownership table |
| [`faq.md`](faq.md) | First-visit questions, before any detailed page | |
| [`quickstart-saas.md`](quickstart-saas.md) | Managed-service evaluation — `EV3` | `🗺️ Planned`; filed **last**, never in *Operate* |
| [`cloud-deployment.md`](cloud-deployment.md) | Managed-service evaluation — `EV3` | `🗺️ Planned`; filed **last**, never in *Operate* |

#### Integrate — 0 existing pages, 1 new

Every page a developer needs at depth is L3, in the SDK docs. The hub's job here is
the choice, not the content. See
[the language route](#the-language-route-and-what-mdbook-cannot-do).

#### Operate — 3 existing pages, 1 new

| Page | Why it is here |
| --- | --- |
| [`docker-containers.md`](docker-containers.md) | `OP2`, `OP4` — what ships as an image and how the topology is wired |
| [`self-host-observability.md`](self-host-observability.md) | `OP4` — what the running stack exposes |
| [`troubleshooting.md`](troubleshooting.md) | `OP3` — why a control did not fire |

#### Verify — 1 existing page, 1 new

| Page | Why it is here |
| --- | --- |
| [`saas-claim-publication-checklist.md`](saas-claim-publication-checklist.md) | `AU3` — the interim T3 register bounding managed-service claims |

#### Reference — 4 existing pages

| Page | Why it is here | Note |
| --- | --- | --- |
| [`policy-reference.md`](policy-reference.md) | Field-by-field lookup | **`Review`** — a second reference for content Core owns; AAASM-5586 / AAASM-5609 |
| [`glossary.md`](glossary.md) | Term lookup | Carries the same superseded framing as `security-model.md`; AAASM-5658 |
| [`compatibility.md`](compatibility.md) | Version pairing across components | Generated from `compatibility.toml` |
| [`source-of-truth.md`](source-of-truth.md) | The status map — the only place an area's maturity is set | Generated from `hub-components.toml` |

#### Contribute — 6 existing pages, plus this one

| Page | Why it is here |
| --- | --- |
| [`page-standards.md`](page-standards.md) | `CO2` — the metadata contract |
| [`audiences.md`](audiences.md) | `CO1` — who a page is for |
| [`role-narratives.md`](role-narratives.md) | The role copy contract |
| `sitemaps.md` (this page) | Where a page goes |
| [`docs-hub-aggregation.md`](docs-hub-aggregation.md) | How the hub is assembled |
| [`accessibility.md`](accessibility.md) | Site policy |
| [`localization.md`](localization.md) | Site policy and the translation workflow |

Count: 2 + 8 + 0 + 3 + 1 + 4 + 6 = **24**.

### The pages this model implies but does not write

Three new hub pages, and two surfaces that close a gap but already have an owner. None
of them is written by this ticket.

| New page | Section | What it is bounded to | Owner |
| --- | --- | --- | --- |
| `integrate.md` | Integrate | A language chooser and a pointer to the SDK mode decision. It may not restate an install step, an API surface or a mechanism | AAASM-5608 |
| `operate.md` | Operate | A router: route an agent → install for this platform → observe → diagnose. It may not restate a mechanism | AAASM-5608 |
| `verify.md` | Verify | How to take a published sentence to its evidence, plus the vulnerability-reporting route (`IR-SE3-a`, which no hub page carries today) | AAASM-5608 |
| *What Ships Today* | Evaluate | The current capability and status answer | **AAASM-5609** |
| *Choose Your Enforcement Path* | Evaluate | The path decision across runtime checkpoints, transport mediation and host adapters | **AAASM-5609** |

**There is deliberately no `evaluate.md`.** AAASM-5609 already publishes the two pages
an Evaluate landing page would have been, and a third router above them would be a
derivative reproducing its source. **Sequencing, so 5608 does not have to guess:**
until 5609 lands, *Evaluate* opens on [`product-promise.md`](product-promise.md); when
5609 lands, *What Ships Today* becomes the first chapter and `product-promise.md` moves
below it. Both states satisfy `audiences.md`'s third navigation check, that no route
opens on a `🗺️ Planned` page.

**`Choose Your Enforcement Path` is filed in Evaluate, not Integrate or Operate**, even
though `DV2` and `OP1` both need it — its own goal states it serves the evaluator
*before* integration begins. `integrate.md` and `operate.md` link to it. This is the
single decision that keeps those two new pages small enough to stay routers.

**There is no `reference.md` or `contribute.md`.** A section needs a landing page when
it is a route with a sequence; those two are indexes whose first entry is already the
entry point. This has a visible consequence — see the note on part titles in
[navigation constraints](#navigation-constraints-desktop-and-mobile).

### The language route, and what mdBook cannot do

`GAP-7` records that the SDK mounts *"appear nowhere in the sidebar"* and asks for
*"a sidebar route to the mounts"*. **That cannot be done in `SUMMARY.md`, and the
measurement is below rather than the assertion.**

An external URL in `SUMMARY.md` does not render as a sidebar link — mdBook resolves the
entry as a file path and the build aborts:

```text
$ mdbook build            # SUMMARY contains: - [Python SDK](https://docs.agent-assembly.com/python-sdk/)
ERROR Unable to create missing chapters
    Caused by: failed to write `src/https://docs.agent-assembly.com/python-sdk/`
exit 101
```

The same book with that one line removed builds at exit 0, so the failure is the
external entry's and not the fixture's. The draft-chapter form `- [Python SDK]()`
builds, but renders `<span>Python SDK</span>` with no anchor — a label, not a route.

**A second `SUMMARY.md` entry for a page that already has one is also rejected.** This
is recorded because it was this page's recommendation until review, and it fails the
same way the external link does:

```text
$ mdbook build   # SUMMARY has documentation.md as a prefix chapter AND under "# Integrate"
ERROR Summary parsing failed for file=".../src/SUMMARY.md"
    Caused by: Duplicate file in SUMMARY.md: "documentation.md"
exit 101
```

Control: the identical insertion with a **new unique** file builds at exit 0, so the
failure is the duplicate's rather than the insertion's. It would also have contradicted
this page's own [one page, one section](#one-page-one-section) rule, the 24-page
partition and the sidebar budget — a recommendation cannot be exempt from the rules the
page hands the same ticket.

So `SUMMARY.md` offers exactly **three** shapes for a mount route, and each was built:

| Shape | Build | Result |
| --- | --- | --- |
| External URL entry | **exit 101** | `failed to write src/https://…` |
| Duplicate entry for a page already listed | **exit 101** | `Duplicate file in SUMMARY.md` |
| Draft entry `- [Python SDK]()` | exit 0 | Renders a `<span>` with no anchor — a label, not a route |

That leaves two real options, and neither is free:

1. **Move `documentation.md` out of the prefix into Integrate.** Builds at exit 0,
   verified, and the page still renders. But it **costs the prefix slot**, and the
   [reachability guarantee](#component-documentation-stays-reachable) is stated over
   routes that do *not* pass through a task section — of which there are exactly two,
   both prefix chapters. Moving one leaves one, and the guarantee fails. Taking this
   option means restating that guarantee, not quietly weakening it.
2. **A theme-level navigation block**, outside `SUMMARY.md`. The hub already injects
   `theme/head.hbs` and four `additional-js` files, so the mechanism exists. This is
   the **only** way to put the literal mount names in the sidebar, and therefore the
   only way to close `GAP-7`'s sidebar half as `audiences.md` words it. **This is the
   recommendation**, on the grounds that it is the one option that closes the gap and
   the one that costs no existing route.

If neither is taken, the honest position is that the sidebar half stays open and the
mounts keep their one-hop prefix route. That is a smaller loss than it sounds — the
route exists today and is unaffected by anything in this design.

The checkpoint half of `GAP-7` stays open and stays L3 regardless, per that gap's own
ruling and this repository's project instructions: the hub orients toward component
docs and does not re-author their install steps or API surface.

### Component documentation stays reachable

The parent scope requires it, and repository-shaped routes are the thing this redesign
is removing, so the guarantee is stated as a count rather than a promise: **each of the
five mounts is reachable by exactly two routes that sit outside every task section, and
by a third inside one.**

| Route | Where it sits | Outside a task section? | Reaches |
| --- | --- | --- | --- |
| `documentation.md`, a prefix chapter | Above the six sections, every page, every viewport | **Yes** | All five mounts |
| [`README.md`](index.html)'s *SDKs & components* table | The index, also a prefix chapter | **Yes** | All five mounts, plus standalone per-version sites |
| [`source-of-truth.md`](source-of-truth.md)'s status map | Reference | No | All five, with owner, visibility and maturity |

The count is two, not three, and the third row is listed rather than counted — a reader
who has to enter *Reference* to find a component mount has been routed by task, which is
the thing this guarantee exists to rule out. **Two is also the floor**: taking option 1
in [the language route](#the-language-route-and-what-mdbook-cannot-do) moves
`documentation.md` inside *Integrate* and drops the count to one, which is why that
option is not the recommendation.

All three regions are generated from `hub-components.toml`, so a component added there
appears on all three without a navigation edit. That is the property that makes this a
guarantee rather than three lists to keep in step.

### Managed-service content, and the gate that moves it

The parent scope forbids promoting unavailable Cloud functions as operational
navigation. Three rules, each checkable:

1. **Placement.** `quickstart-saas.md` and `cloud-deployment.md` sit **last in
   Evaluate**. They are not in *Operate*, and they are not the first chapter of any
   section. Their reader today is `EV3` — deciding what to tell a stakeholder is not
   available yet — not an operator.
2. **Label.** A sidebar entry carries its area's maturity label in the link text **only
   when that maturity is `🗺️ Planned`**. mdBook sidebar entries are plain links and
   cannot carry a badge, so the label has to be in the text or it is nowhere; and
   applying it to shipping pages too would train the eye to skip it. The current
   SUMMARY already does this, as *"(Coming soon)"* — the change is to use the status
   map's own label instead of a second phrasing.
3. **The promotion gate.** A managed-service page moves from *Evaluate* into *Operate*
   when, and only when, its area's `Maturity` cell in `source-of-truth.md`'s
   `BEGIN GENERATED:hub-components:source-of-truth-table` region stops reading
   `🗺️ Planned`. That is a string comparison against a generated table, not a
   judgement, and it means no ticket can promote a Cloud page by deciding to.

## The product website sitemap

`content-ownership.md` gives L1 positioning, the evaluation narrative, trust,
early-access and conversion paths, and bars it from reference material, policy schemas,
threat models and API surfaces. Every route below is inside that boundary.

**A structural fact this tree has to be designed around** (`documentation-inventory.md`
finding D6): the website publishes two Markdown files, both blog posts, and sets
`docs: false`. Its copy is JSX inside `.tsx` components. So *there is no Markdown
migration here*, a page is a React route, and any check that enumerates `.md` files
passes over this layer without seeing it.

### Routes

| Route | The task or decision | Status | Owner |
| --- | --- | --- | --- |
| `/` | Decide in five seconds whether this is relevant to me | Exists — rewrite | AAASM-5585 |
| `/product` | Understand what it is before choosing a path | Exists — rewrite | AAASM-5586 |
| `/how-it-works` | Understand the flow without source-level knowledge | New | AAASM-5586 |
| `/use-cases` and four children | Recognise my own situation in a concrete story | New | Unassigned |
| Four role routes under one prefix | Decide relevance for my role in under three minutes | New | AAASM-5587 |
| `/trust` | Get from a published claim to the evidence behind it | New | Unassigned |
| `/maturity` | Learn what ships today, and what is decided but not built | New | Unassigned |
| `/blog`, `/blog/tags/*` | Read build notes | Exists — keep | — |
| `/early-access` | Register interest in the managed service | Exists — keep | — |
| `/arena` | See governance trials | Exists — keep | — |

Every existing route is preserved, which is AAASM-5585's own acceptance criterion.

### The four role routes

`role-narratives.md` supplies four briefs and `audiences.md`'s crosswalk maps each to an
`audience` value. This page fixes the **count** (four, one per brief) and the
**requirement that they share one route prefix** — 5596 has to write one canonical-URL
rule, and it cannot if the four routes are scattered. The slugs are AAASM-5587's.

| Brief | `audience` | Job it ends — *this page's derivation, not a cited mapping* |
| --- | --- | --- |
| Security / Risk | `security-engineer` | `SE1` |
| Platform / SRE | `operator` | `OP1`–`OP3` framing |
| Engineering | `developer` | `DV2` |
| Product / QA / Assurance | `auditor` | `AU3` |

**The third column is derived here and is labelled so.** The first two columns are
cited: `role-narratives.md` supplies the briefs and records each one's `audience` value.
Neither source assigns these job ids to these routes — `role-narratives.md` assigns no
job ids at all, and `audiences.md`'s crosswalk assigns them to two rows, neither of them
these four. The mapping is this page reading each brief's stated *Job* line against
`audiences.md`'s jobs table, which is a judgement a reviewer should be able to
disagree with rather than one they should take as sourced.

Each route carries the brief's seven fields in the brief's order. A fifth role route is
a change to `role-narratives.md` first, because a role surface with no brief is a page
authoring its own product truth.

### Which audiences get an L1 entry, and which do not

`audiences.md`'s `GAP-1` asks for a per-audience entry **on both L1 and L2**. L2 gets
all six. L1 gets five, and the sixth is a deliberate omission rather than a gap left
open, so it is accounted for here rather than in the gap table alone.

**One of the five is contingent, and the number is worthless to a planner who does not
know which.** `evaluator`'s L1 entry is `/` — and `audiences.md` says of the site as it
stands that it *"publishes four pages and a blog and routes by none of them"*. So `/`
is not an evaluator entry today; it becomes one when **AAASM-5585** rewrites it around
problem, governed decision, outcome and proof. Until that lands, L1 has **four**, not
five. AAASM-5585 and AAASM-5587 both consume this count, and neither should read it as
already true.

| `audience` | L1 entry | L2 entry |
| --- | --- | --- |
| `evaluator` | `/`, and `/maturity` for the forward-looking half | Evaluate |
| `security-engineer` | Security / Risk role route | Evaluate — `security-model.md` |
| `operator` | Platform / SRE role route | Operate |
| `developer` | Engineering role route | Integrate |
| `auditor` | Product / QA role route | Verify |
| `contributor` | **None, by design** | Contribute |

`contributor` has no L1 entry because `audiences.md`'s own `contributor` section puts
positioning copy and conversion paths under *belongs elsewhere* for that reader. An L1
contributor entry would route them to the layer that page says is wrong for their job.
This is the one place the design does not deliver `GAP-1`'s page-shape as literally
worded, and it is stated rather than absorbed.

### `/maturity` is where the roadmap goes, and it is not a hub page

`GAP-6` records that no roadmap surface exists anywhere. ADR 0034 hand-off 4 assigns
the roadmap to **L1**, on the reasoning that a roadmap is a forward-looking positioning
statement and positioning is already L1's. So the gap closes on the product website, not
on this hub, and a hub page named for a roadmap would be the wrong layer.

`content-ownership.md` bounds what may go on it: no dated commitment unless the date is
an already-released fix-version, and a forward-looking statement is admissible only in
one of **three** forms: ADR 0033 §6's `Planned` term — a ticket reference carrying **no
capability claim**; ADR 0033's `Research` label, which `content-ownership.md` marks
`→ move` because ADR 0033 uses the word once without defining it; or an area's
`🗺️ Planned` maturity label.

`/maturity` uses the **first and third** of those three, and therefore carries two
things and no others: the current release position, narrowed from
[`source-of-truth.md`](source-of-truth.md), and a `Planned` list whose rows are ticket
references. It does not use `Research`, because that label is marked `→ move` at its
source and a page built on a label in transit inherits the move.

### What the website may not carry

Restated here because a sitemap is where these get violated, each by adding one
reasonable-looking page.

- **No reference material, policy schema, threat model or API surface.** Those are L2
  and L3. `/trust` routes to the evidence; it does not reproduce it.
- **No company or portfolio positioning.** That is L0's, on `horonomy.dev`.
- **No architecture page built on a fixed pipeline of SDK, then proxy, then eBPF**, in
  prose or as a three-box diagram, and no depiction of eBPF as a cross-platform final
  layer. ADR 0033 forbidden designs 1 and 2. This binds `/how-it-works` most directly,
  which is why AAASM-5586 owns it rather than this page.
- **No claim without its bound on the same screen**, and no scenario sentence in a
  `<title>`, an `og:title` or a social card — those take
  [`product-promise.md`](product-promise.md)'s headline, which is written to survive
  being quoted alone.

## How current, limited, experimental and planned content stay separated

The parent scope asks for four states to be visibly separated. **Three of the four are
already values of one existing key and the fourth is a value of a different one**, so
this page coins nothing — coining a fifth vocabulary on the one axis a navigation routes
by is the defect these artifacts exist to prevent.

| The state | Axis that already carries it | Value | Set in | Rendered as |
| --- | --- | --- | --- | --- |
| Current | Page availability | `available-verified` | The page's own metadata block | A page badge |
| Limited | Page availability | `available-with-limits` | The page's own metadata block | A page badge |
| Experimental | Page availability | `preview` | The page's own metadata block | A page badge |
| Deprecated | Page availability | `deprecated` | The page's own metadata block | A page badge |
| Planned | **Documentation-area maturity** | `🗺️ Planned` | [`source-of-truth.md`](source-of-truth.md), reached through the page's `area` id | An area badge, **and** the sidebar link text |

Three consequences worth stating, because each is a way to get this wrong:

- **Planned is not a page-availability value, and that is not an oversight.** Maturity
  belongs to a documentation *area*, and [`page-standards.md`](page-standards.md)
  deliberately has no `maturity` key for exactly this reason. A page is `🗺️ Planned`
  because its area is.
- **`Experimental` and `Planned` are also ADR 0033 §6 claim terms, about an action.** A
  page badge and a claim term are different subjects, and ADR 0034 hand-off 7 rules that
  no axis may be applied to another's subject. A page is not `Planned` in §6's sense; an
  action is.
- **The sidebar can only render one of the five.** mdBook sidebar entries are plain
  links, so the four availability values are page badges and only `🗺️ Planned` reaches
  the sidebar, in the link text. That asymmetry is the reason rule 2 of
  [the managed-service gate](#managed-service-content-and-the-gate-that-moves-it) is
  worded the way it is.

Page badges depend on pages carrying metadata blocks. **Three of 24 hub pages do
today** — `audiences.md`, `page-standards.md` and `role-narratives.md`, plus this one,
making four on merge. Adoption is AAASM-5610's and the validator is AAASM-5601's. Until
then the separation is carried by the sidebar label and the status map, both of which
work now.

## Mapping the two existing plans in

### AAASM-5013 — Golden Paths

5013's target information architecture is three surfaces. Two of them are not hub
content, and saying so is the point of mapping rather than absorbing.

| 5013 surface | Layer that owns it | Where it lands | Why |
| --- | --- | --- | --- |
| Developer Quickstart — Python | L3 `python-sdk` | `/python-sdk/`, routed from Integrate | *Integration steps, per language* is that SDK's in the ownership table |
| Developer Quickstart — Node | L3 `node-sdk` | `/node-sdk/`, routed from Integrate | as above |
| Developer Quickstart — Go | L3 `go-sdk` | `/go-sdk/`, routed from Integrate | as above |
| Operator Quickstart | L3 Core | `/core/`, routed from Operate | *Integration steps, operator / CLI path* is Core's |
| End-to-end governance walkthrough | **L2, this hub** | Operate | It spans gateway, runtime and SDK, so no single component owns it, and cross-component routing is L2's job |

**One finding 5013 should have before it decomposes.** Its canonical scenario is
`ALLOW read_file` / `DENY delete_file` / `APPROVAL send_email`, held constant across all
three languages. The third leg is not runnable as documentation today:
`role-narratives.md`'s register entry `RC12` records `Approval required` as *no claim* —
no manifest row reaches the term, no shipped operator surface can answer a held action,
and inside the MCP tunnel a pending decision is downgraded to a refusal. A golden path
that documents an approval step would be documenting a path a reader cannot finish.
AAASM-5657 owns the underlying gap.

### AAASM-4237 — SaaS documentation IA

Most of 4237 is not this page's to decide, so this records only the parts a sitemap
settles and leaves the rest explicitly open.

**Settled here:**

- **Where SaaS docs live** — as L2 hub pages. Already decided by `content-ownership.md`,
  whose L2 row names *the managed-service pages* as part of L2's job, and by
  `page-standards.md`, which states that a hub page about the managed service is
  `L2:docs` while `L3:cloud` names the private component only. Recorded so 4237 does not
  re-open it.
- **Where in navigation** — last in *Evaluate*, under
  [the gate](#managed-service-content-and-the-gate-that-moves-it).
- **What they may say** — bounded by
  [`saas-claim-publication-checklist.md`](saas-claim-publication-checklist.md).

**On the two ticket references, because 5608 will otherwise stop and check.**
AAASM-5608's scope names *SaaS documentation from **AAASM-4224***; this page maps
**AAASM-4237**. That is not a contradiction and neither reference is wrong: 4224 is the
SaaS-documentation Epic and 4237 is the information-architecture Task beneath it. This
page consumes the Task, whose output is the IA; 5608's scope names the Epic, whose
output is the documentation set. Both stand at their own granularity.

**Still 4237's:** the SaaS-specific audience sub-model, the screenshots and diagrams
policy, documentation review ownership, and how SaaS docs reference the private `cloud`
and E2E repositories without crossing the public content boundary.

## Redirects

### The Docs Hub restructure needs none, and this is measured

An mdBook page's URL is derived from its **file path**, not from its position in
`SUMMARY.md`. So re-parting the sidebar moves no URL. That is the claim, and it was
tested rather than assumed:

| Step | Result |
| --- | --- |
| Build the hub unchanged, list every emitted `.html` | 27 files |
| Move `product-promise.md` and `risk-scenarios.md` into a new `# Evaluate` part; rebuild | exit 0 |
| `diff` the two file lists | **identical — 0 URL changes** |
| Control: does the sidebar actually change? `Evaluate` in the generated `toc-*.js` | **0 in base, 1 in mutant** |
| Control: is the probe capable of finding a part title at all? `Reference`, an existing part | 1 in base |
| Second control: prev/next chapter links | changed, `troubleshooting.html` → `faq.html` |

The mutation moves the token under test and the URL set does not move with it, so the
result is a property of mdBook rather than of a probe that saw nothing.

**Consequence for AAASM-5608:** the re-filing above creates **zero** redirect
obligations. Every external link into the hub keeps resolving — including the **five**
`docs.agent-assembly.com/*.html` deep links in the website's mega menu and a **sixth**
in `src/components/home/NextSteps.tsx`. Re-derived with
`git grep -nE '\$\{DOCS(_URL)?\}/[A-Za-z0-9_-]+\.html' origin/main -- src`, because counting
by eye had missed `quickstart-saas.html` twice over — the one page this design actually
relocates, and so the single most relevant row.
This is also why the three new pages are flat files at `docs/src/*.md` rather than a
directory per section: a directory would change nothing today but would set the
precedent that a section rename is a URL change.

**Keep it that way.** `docs/book.toml` has no `[output.html.redirect]` section, so a
page that is genuinely renamed later would 404 with nothing to catch it. Adding that
section is the prerequisite for any future rename, and it is not needed for this design.

### What this design does create

| Obligation | Where | Owner |
| --- | --- | --- |
| If `/how-it-works` takes the homepage's architecture section, `/` must **keep** an `#architecture` anchor | `official-website` | AAASM-5586 |

That one is worth spelling out because the usual remedy does not apply: a URL fragment
is never sent to the server, so no 301 can redirect `#architecture`. Either the anchor
stays on `/` or the link breaks silently. The same applies to `#security`.

Nothing else moves. Every other route on both sites is either unchanged or new.

### Redirects owned elsewhere, and not by this design

Recorded so a reader does not conclude from the section above that redirects are
handled. They are not, and three separate gaps are open:

- **Five legacy `ai-agent-assembly.github.io/<repo>/` URLs** have canonical targets on
  `docs.agent-assembly.com`, and **none of the five is implemented**. Owned by
  AAASM-3665. The five are enumerated below with their measured status, because an
  earlier draft gave the total without its parts and got the live-content count wrong —
  it said *one of them serves live content*, and four do.

  | Legacy URL | Measured 2026-08-08 | Serves content? |
  | --- | --- | --- |
  | `…github.io/agent-assembly/` | **200**, 2,896 bytes | Yes — landing page with a meta-refresh |
  | `…github.io/python-sdk/` | **200**, 1,423 bytes | Yes — meta-refresh |
  | `…github.io/node-sdk/` | **200**, 27,147 bytes | Yes — a full live page |
  | `…github.io/go-sdk/` | **200**, 3,329 bytes | Yes — meta-refresh |
  | The fifth row — the pre-rename docs host, spelled out in [`MIGRATION.md`](https://github.com/ai-agent-assembly/docs/blob/HEAD/MIGRATION.md) | **404** | No — that repository was renamed under AAASM-4341 |

  The fifth row's literal host is not written here on purpose: `check_repo_names.py`
  audits every tracked page for retired repo names and `MIGRATION.md` is its one
  content exemption, as the deliberate history record. Naming the URL here would either
  fail that gate or require widening its allowlist to cover a whole page, which is
  suppressing a scanner rather than satisfying it.

  So *"none is implemented"* holds — no row 301s to its canonical target — but **four of
  the five serve 200**, not one. The fifth carries a redirect obligation for a URL that
  no longer resolves at all, which makes that row of the plan moot rather than pending
  and AAASM-3665's remaining work four rows rather than five.
  `documentation-inventory.md` names only `agent-assembly/` as an *example* of live
  content; reading that as *the count* was this page's narrowing, not the inventory's
  claim. The stale fifth row is filed as **AAASM-5690** against the inventory and
  `MIGRATION.md`.

  Not in the five, and worth knowing before someone re-derives this list:
  `…github.io/docs/` **301s** to `docs.agent-assembly.com` already. It is not one of
  AAASM-3665's five rows, so it neither contradicts nor satisfies them.
- The host-level `www` redirect is proposed, not applied.
- Core's own book has no `[output.html.redirect]` either, which its migration slice
  needs before its three published `Move`/`Merge` pages land.

## One page, one section

The rule that keeps the trees free of duplicate architecture and reference pages:

> **A page appears in exactly one section. Every other section that needs it links to
> it.**

The 24-page assignment above satisfies this by construction — the section counts sum to
24, so no page has two homes. Four pages are wanted by more than one section, and each
resolves the same way:

| Page | Home | Also linked from |
| --- | --- | --- |
| [`risk-scenarios.md`](risk-scenarios.md) | Evaluate | Verify, to its negative-control section |
| [`source-of-truth.md`](source-of-truth.md) | Reference | Every section, for its area's maturity |
| [`compatibility.md`](compatibility.md) | Reference | Evaluate, Operate, Verify |
| [`open-core-boundary.md`](open-core-boundary.md) | Evaluate | Operate, for the self-host scope |

Two stronger constraints, because linking is not enough on its own:

- **This design creates no architecture page and no reference page for anything Core
  owns.** Architecture is Core's — ADR 0033 and `docs/src/architecture/` — and the hub's
  L2 row bars it from *"a reference of its own for anything Core owns"*. The three new
  hub pages are routers, and the bound in their table is what keeps them that way: a
  router that starts explaining a mechanism has become a fourth copy of it.
- **The existing duplicate is not made load-bearing.** The hub and Core each publish an
  independent policy reference, and [`README.md`](index.html) still frames the product
  with a three-layer model ADR 0033 supersedes. Neither is this ticket's to fix — they
  are AAASM-5586 / AAASM-5609 and AAASM-5611 respectively — but **AAASM-5608 must not
  build the Evaluate route on top of that `README.md` section**, because a navigation
  that routes readers into superseded framing makes the framing harder to remove.

## Navigation constraints, desktop and mobile

### Docs Hub — mdBook

| Constraint | Value | Why |
| --- | --- | --- |
| Sidebar entries, total | **36** after this design — 24 existing + this page + 3 new routers + 2 from AAASM-5609 = 30 page entries, plus 6 part titles | Below a viewport height at 1080px, the sidebar scrolls; on mobile the whole tree renders in one drawer |
| Nesting depth under a part | 2 levels | A third level is a drawer nobody scrolls to |
| Section headings | Not links | `part-title` renders as `<li class="part-title">Evaluate</li>` — plain text, no anchor. **A section that needs a landing page must have one as its first chapter**, which is why Evaluate, Integrate, Operate and Verify have one and Reference and Contribute do not |
| Sidebar entry decoration | Link text only | No badge mechanism exists, hence the label rule for `🗺️ Planned` |
| Breadcrumbs | **No mechanism** | mdBook renders no breadcrumb trail. AAASM-5608's scope asks for *contextual breadcrumbs*; in mdBook that is a theme change or it does not happen. Recorded so 5608 does not plan against it |
| Per-entry layer / component / maturity labels | **No channel beyond link text** | AAASM-5608's scope asks navigation labels to identify content layer, component and maturity. The sidebar has one string per entry and no data attributes, so three facts cannot ride on it. Either they go in the link text — which is how `🗺️ Planned` reaches the sidebar — or they belong on the page, not in the nav |
| External links in `SUMMARY.md` | Not supported | Build aborts at exit 101; see [the language route](#the-language-route-and-what-mdbook-cannot-do) |

### Product website — Docusaurus

| Constraint | Value | Why |
| --- | --- | --- |
| Navbar items | Unchanged at **3 left, 3 right** (six total) | AAASM-5587 requires cross-links *without* an oversized mega menu, and the drawer at narrow widths is a vertical list of the same items |
| New routes reach readers via | The `Product` navbar item becoming a three-entry dropdown, a role chooser block on `/`, and the footer | A dropdown of three is not a mega menu; the two existing mega menus stay as they are |
| Footer columns | 3, unchanged; `/trust` and `/maturity` join *Resources* | A fourth column wraps below 768px |
| Locale | Every new route exists in `en` and `zh-Hant` | The site declares both; a route that exists in one serves English content on a translated URL, which D6 already records as happening for the blog |

The role routes deliberately do **not** become navbar items. Four more top-level items
would put the drawer at ten, and a role page is something a reader is routed to from
a chooser, not something they navigate to by name.

## Partitioning this into non-overlapping tickets

Each row names the files it owns. **No file *region* appears in two rows** — the
distinction is load-bearing, and the earlier wording ("no file appears in two rows") was
simply false. Two overlaps exist: one is a genuinely shared file that predates this page,
the other is disjoint by region within a file. Both are named below rather than counted
as clean.

| Ticket | Repository and paths | Routes or sections | Must not touch |
| --- | --- | --- | --- |
| **AAASM-5608** | `docs`: `docs/src/SUMMARY.md`; new `docs/src/{integrate,operate,verify}.md` | The six sections | Any existing page body |
| **AAASM-5611** | `docs`: bodies of `README.md`, `security-model.md`, `comparison.md` | — | `SUMMARY.md` |
| **AAASM-5609** | `docs`: two new evaluator guides; `policy-reference.md` | First two chapters of Evaluate | `SUMMARY.md` ordering beyond its own two entries |
| **AAASM-5586** | `official-website`: `src/pages/product.tsx`, new `how-it-works` route; `docs`: `policy-reference.md` | `/product`, `/how-it-works` | `/`, the role routes |
| **AAASM-5585** | `official-website`: `src/pages/index.tsx`, `src/components/home/**` | `/` | Navbar, footer, `/product` |
| **AAASM-5587** | `official-website`: new role route files | Four role routes | `/`, `/product`, navbar |
| **AAASM-5596** | `official-website`: `docusaurus.config.ts`, `src/components/MegaMenu/menus.ts`, `_headers`; `docs`: `_headers`, `docs/book.toml` | Navbar, footer, canonical links, redirects | Any page body |
| **AAASM-5658** | `docs`: `glossary.md` | — | `SUMMARY.md` |
| **AAASM-5610** | `docs`: metadata blocks on existing pages | — | Page prose |
| Unassigned — use cases | `official-website`: new `/use-cases` routes | `/use-cases` and children | — |
| Unassigned — trust | `official-website`: new `/trust` route | `/trust` | — |
| Unassigned — maturity | `official-website`: new `/maturity` route | `/maturity` | — |
| Unassigned — walkthrough | `docs`: end-to-end governance walkthrough | Operate | — |

**The two overlaps, both named rather than left to be discovered.**

1. **`policy-reference.md` is named by both AAASM-5586 and AAASM-5609**, because
   `documentation-inventory.md` assigns it to both. That pairing predates this page and
   this page does not split it. This one is a genuine shared file, not a shared region.
2. **AAASM-5610 touches every page that any other row touches.** Its slice is *metadata
   blocks on existing pages* — all 24 — which intersects AAASM-5611 (`README.md`,
   `security-model.md`, `comparison.md`), AAASM-5658 (`glossary.md`) and AAASM-5609
   (`policy-reference.md`). The rows stay disjoint because 5610 owns the
   `AA-PAGE-META` block and the others own the prose below it, and the block is the
   first construct in the file with a fixed delimiter pair, so the two regions cannot
   be confused. **That is a disjointness by region, and the acceptance criterion is
   worded per page** — so it is recorded here rather than counted as clean. If 5610
   lands concurrently with any of the three, expect a same-file merge, not a conflict.

**Ordering.** AAASM-5608 can land before 5609, 5611 and the unassigned rows, because
`SUMMARY.md` and the three new routers do not depend on any of them. It should land
before AAASM-5596, so canonical links and navigation are written against the final tree.

## Which gaps this closes, and which it carries forward

`audiences.md` requires that every gap is *"either closed by a page in the proposal, or
carried forward as a named open item"*. All eight, and four of them are carried forward
rather than closed.

| Gap | Disposition |
| --- | --- |
| `GAP-1` — no surface routes all six audiences | **Closed at L2; five of six at L1.** `audiences.md` asks for a per-audience entry *on both L1 and L2*. L2 gets six: the index router plus the six sections. L1 gets five — four role routes, plus `/` for `evaluator`, and **that fifth is contingent on AAASM-5585 rewriting `/`**, since `audiences.md` records that the site routes by none of its current pages. Until 5585 lands the L1 count is four. **`contributor` gets none, deliberately**: `audiences.md`'s own `contributor` section puts positioning and conversion paths under *belongs elsewhere*, so an L1 contributor entry would route that reader to the wrong layer. Stated as five rather than six so 5608 and 5587 do not both assume the other built it |
| `GAP-2` — *Getting Started* holds only `🗺️ Planned` pages | **Closed.** The section is dissolved; `operate.md` is the operator entry and starts from what ships; the two Planned pages move to the end of Evaluate |
| `GAP-3` — no channel-and-platform position published | **Carried forward; no slot defined here, and that is the disposition.** An earlier draft said *a Reference slot is defined* — none is: *Reference* lists four existing pages and the implied-pages table has no Reference row. The content belongs to AAASM-5609's *What Ships Today*, which this design files in **Evaluate**, so **5609 owns it** and 5608 must not build a second matrix anywhere. Blocked on AAASM-5680 for the GHCR vocabulary |
| `GAP-4` — the evidence layer has no reader-facing surface | **Carried forward.** A Verify slot is defined and backed by `verify.md`. The manifest that feeds it is AAASM-5531, which is **Done**, so the live owner is **AAASM-5600** (To Do) — ADR 0034's T3 row names the pair, and pointing a carried-forward gap at a closed ticket is how it stops being tracked. ADR 0034's T3 registry still does not exist |
| `GAP-5` — the security entry carries a superseded model | **Carried forward.** `security-model.md` keeps the `security-engineer` entry slot in Evaluate; the rewrite is AAASM-5611's |
| `GAP-6` — no roadmap surface | **Carried forward, and relocated.** It closes at L1 as `/maturity`, not on this hub. Unassigned |
| `GAP-7` — SDK mounts absent from the sidebar | **Not closed by this design, and narrower than stated.** All three `SUMMARY.md` shapes were built and none delivers a sidebar route: external entry and duplicate entry both exit 101, the draft form renders no anchor. Only a theme-level block closes the sidebar half as worded, and that is a 5608 decision this page recommends rather than makes. The mounts keep their existing one-hop prefix route meanwhile. The checkpoint half stays L3 |
| `GAP-8` — the default-posture table is filed under *About* | **Closed on one route of three.** The page-shape is *a level-3 surface **on** those routes*, and only the evaluator route gets one: `product-promise.md` moves to Evaluate, satisfying `IR-EV1-a` and `IR-EV1-c`. **`IR-OP3-a` is not closed** — the table is one link from the operator route, and one link from is not on. **`IR-DV2-a` is not closed** either: `audiences.md` marks it *not on a developer route*, and this design bars `integrate.md` from restating a mechanism. Closing the other two is an L3 SDK ticket or an AAASM-5609 link, not a page 5608 can draw. An earlier draft counted the operator route as closed; it is not |

### The one navigation check this design does not pass

`audiences.md`'s fifth check is that *"no route requires a reader to reach L6 to finish
their job"*. **It is not met, and no sitemap can meet it alone.** The `auditor`'s `AU1` — find
the evidence behind a published claim — still terminates at `capability-manifest.yaml`
and `verification-reports/**`, both L6, and `content-ownership.md` states that nothing
in L6 is a reader-facing page. That is `GAP-4`, and the fix is a published surface, not
a route. This design defines the slot the surface will occupy and leaves the check
failing until something fills it.

The other four checks are met: every audience has an entry, every route reaches its
escalation in three steps, no route opens on a `🗺️ Planned` page, and every gap above is
closed or named.

### Entry, next and escalation under this tree

`audiences.md`'s second check, applied once.

| `audience` | Entry | Next | Escalation |
| --- | --- | --- | --- |
| `evaluator` | Evaluate — *What Ships Today*, or `product-promise.md` until it lands | `risk-scenarios.md`, `open-core-boundary.md` | ADR 0033 §5.3 and §6, in Core |
| `security-engineer` | Evaluate — `security-model.md` | `risk-scenarios.md`, then Verify | Core's threat model, the manifest, verification reports |
| `auditor` | Verify — `verify.md` | `saas-claim-publication-checklist.md`, `risk-scenarios.md`'s negative control | The manifest and verification reports (L6 — `GAP-4`) |
| `operator` | Operate — `operate.md` | `docker-containers.md`, `self-host-observability.md` | Core's quick start and CLI reference |
| `developer` | Integrate — `integrate.md` | The SDK mount for their language | Core's API reference, the examples repository |
| `contributor` | Contribute — `page-standards.md` | `audiences.md`, this page | ADR 0034, `content-ownership.md`, `claim-vocabulary.md` |

## How this page meets its acceptance criteria

| Criterion | How it is met |
| --- | --- |
| Each top-level item corresponds to a user task or decision | [The six sections](#the-six-sections-and-the-task-each-one-is) each name a task and the jobs it ends, and the product-site table gives a task per route. *Reference* is stated as a lookup rather than a decision rather than being described as one |
| The sitemaps avoid duplicate architecture and reference pages | [One page, one section](#one-page-one-section). The 24 assignments sum to 24, so no page has two homes; the four cross-wanted pages are resolved by link; and the design creates no architecture page and no reference page for content Core owns. The two duplicates that already exist are named with their owning tickets rather than absorbed |
| Current, limited, experimental and planned content are visibly separated | [The label crosswalk](#how-current-limited-experimental-and-planned-content-stay-separated). Three states are `availability` values, one is an area maturity label, and the asymmetry between them — only one reaches the sidebar — is stated with the mechanism that forces it |
| Mobile and desktop navigation constraints are considered | [Navigation constraints](#navigation-constraints-desktop-and-mobile), with a numeric budget per surface, each re-derived from the config or the build rather than recalled. Four constraints are measured rather than assumed: part titles are not links, `SUMMARY.md` rejects an external entry, it rejects a duplicate entry, and the navbar is six items. Two are recorded as absent mechanisms so 5608 does not plan against them: breadcrumbs and per-entry labels |
| The implementation can be divided into non-overlapping page or route tickets | [The partition](#partitioning-this-into-non-overlapping-tickets). Thirteen rows naming their own files, a landing order, and **two overlaps named rather than counted as clean** — `policy-reference.md` shared by AAASM-5586 and AAASM-5609, which predates this page, and AAASM-5610, which is disjoint from three other rows by *region within a file* rather than by file. The criterion is worded per page, so the second is a qualified pass and is labelled one |

## What this page hands off

| To | What |
| --- | --- |
| **AAASM-5608** | The tree, the 24-page assignment, the three new routers and their bounds, the sequencing against 5609, the zero-redirect measurement, and the two constraints mdBook imposes |
| **AAASM-5611** | That `README.md`'s three-layer section is on the Evaluate route and should be corrected before that route is built on it |
| **AAASM-5585 · AAASM-5586 · AAASM-5587** | The route table, the four-role count and the shared-prefix requirement, the `#architecture` anchor obligation, and the navbar budget |
| **AAASM-5596** | The final tree to write canonical links against, the fact that the hub restructure creates no redirect obligation, and the three redirect gaps that are open elsewhere |
| **AAASM-5609** | That `GAP-3` is routed to *What Ships Today* rather than to a second matrix, and that *Choose Your Enforcement Path* is filed in Evaluate and linked from Integrate and Operate |
| **AAASM-5013** | The layer split across its three surfaces, and that its canonical scenario's approval leg rests on a term no manifest row reaches |
| **AAASM-4237** | The three questions a sitemap settles, and the four that remain its own |
| **AAASM-5601 · AAASM-5610** | That the sidebar label and the status map carry the maturity separation until page badges exist |

---

*Last reviewed: 2026-08-08 — AI Agent Assembly Team*
