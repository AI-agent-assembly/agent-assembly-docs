<!-- BEGIN AA-PAGE-META
schema_version: 1
page_type: reference
audience: [contributor]
user_job: Write a hub page that states its depth, its owner and its evidence
owner: L2:docs
canonical_source: self
describes_capability: false
disclosure_levels: [3, 4]
END AA-PAGE-META -->

# Page standards — progressive disclosure & mandatory metadata

This page is for anyone authoring or reviewing a page on this hub. It defines **how
deep a page goes**, **how it hands a reader deeper**, and **what metadata every page
must carry** so that a claim can be checked mechanically instead of by reading.

It exists because the same capability gets described at five different depths by five
different authors, and the shallow descriptions are the ones that drift into being
wrong. A reader who stops at the first paragraph should hold a *correct* picture, not
a *simplified* one — those are different properties, and only the first is achievable
by rule.

## What governs this page

This page is downstream of four artifacts. It **adds no claim** to any of them, and it
does not restate their definitions.

| Source | What it supplies | Where |
| --- | --- | --- |
| **ADR 0033 §6 — claim vocabulary** | The eleven enforcement/claim terms. Four of the badge names below are §6's words, reused verbatim. | [ADR 0033](https://docs.agent-assembly.com/core/latest/adr/0033-canonical-governance-and-enforcement-architecture.html) |
| **ADR 0034 — one product truth** | The three-axis ruling that decides which vocabulary may describe which subject, and the forbidden designs this page is checked against. | [ADR 0034](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/docs/src/adr/0034-one-product-truth-and-cross-repository-documentation-governance.md) |
| **Content-layer ownership** | The L0–L6 layer model and the canonical-owner table. | [`content-ownership.md`](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/docs/src/development/content-ownership.md) |
| **Product promise & message hierarchy** | The worked instance of the four levels, for one page. | [Product promise](product-promise.md) |

> **ADR 0034 is the governing document for the vocabulary question, and it is merged.**
> It shipped as AAASM-5621's deliverable, and this page is written against its
> hand-off 7 and forbidden-design list. This page was deliberately sequenced to land
> after it, so that its central ruling would never be published without a source; that
> ordering is now satisfied.
>
> It is linked above in the `blob/HEAD` source form rather than to the rendered docs
> site, because the published page — `docs.agent-assembly.com/core/latest/adr/0034-…` —
> still returns **404** while the site republishes after the merge, verified with ADR
> 0033's published URL returning 200 as a control in the same check. **When the
> rendered page resolves, swap that cell to the published URL**, which is the form
> `content-ownership.md` prefers for one rendered site linking another.

Ticket references are plain text, not links: the tracker is not publicly readable, so
a link would only reach a login wall — and a link checker scores that wall as
reachable, which makes the reference look verified when it is not.

### What this page does not decide

- **Precedence** between the three axes when they appear to conflict, and **waivers**.
  ADR 0034 owns both. This page applies its ruling; it does not extend it.
- **Cross-repository adoption records and conflict resolution.** Also ADR 0034
  (AAASM-5621).
- **Documentation-area maturity.** `source-of-truth.md` owns it, and this page reads
  it rather than restating it — see [`area` ids](#area-ids).
- **A capability identifier registry.** AAASM-5531 (Define a machine-readable
  capability and evidence manifest) has not started, so `capability_ids` is reserved
  and optional in schema version 1 — see [the field reference](#field-reference).
  Requiring identifiers before a registry exists would only make authors invent them.

## The four disclosure levels

The levels are a property of a *reader's need*, not of a page's length. Each level
adds precision; **none of them retracts what the level above said**. A reader must be
able to stop at any level and still be correct.

| Level | Name | Answers | Bound | Typical layer |
| --- | --- | --- | --- | --- |
| **1** | One-sentence outcome | *What do I get?* | Exactly one sentence. Must carry the boundary clause — everything shorter drops it. | L0, L1 |
| **2** | Three-step product flow | *How does it work, roughly?* | Exactly three steps, each one short paragraph. | L1, L2 |
| **3** | Evaluator detail | *What is on by default, and what does it not cover?* | No length bound. Must state defaults and non-coverage. | L2, L3 |
| **4** | Implementation deep dive | *How is it actually built, and on what evidence?* | **No bound of any kind.** | L3, L6 |

[Product promise](product-promise.md) is the reference instance **for the levels**: it
carries all four for one subject. Read it as the worked example; this page is the
general contract.

> **It is not yet a reference instance for the metadata.** `product-promise.md` carries
> no metadata block — it merged before this contract existed — so running a validator
> over it today produces a hard error for the missing block, and rule 13 additionally
> fires on `protects`, `enforces` and `catches`, which appear there in double quotes as
> examples of *banned* wording. Both results are correct behaviour, not validator bugs.
> Adding blocks to existing hub pages is AAASM-5610's work; the only page carrying one
> today is this one. The [rule 13 double-quote exemption](#rule-13--the-unbounded-claim-verbs)
> was added precisely because that page quotes the verbs it warns against.

### Level 4 is never abbreviated

> **Depth is not a defect.** No rule on this page — and no validator built from it —
> may be cited to remove technical detail from a component's documentation, an ADR, a
> threat model or a protocol reference. There is no maximum page length, no maximum
> section count, and no requirement that a deep page carry a shallow summary of
> itself.

Progressive disclosure is about **adding shallow entry points**, never about
**subtracting depth**. A page that was thinned to "fit a level" has been damaged, not
improved. If a summary would replace its source, link the source instead — that is
`content-ownership.md`'s prohibition on a derivative reproducing its source at the
same depth.

### Which levels a page must carry

Required levels are a function of `page_type`. A page may carry *more* levels than
required; it may never carry fewer. The one exception is level 4 on a `product` or
`guide` page, which is **forbidden** rather than optional — those types reach level 4
by handing off, because a page that both summarises and exhausts a subject is the
"derivative that reproduces its source at the same depth" `content-ownership.md`
prohibits. [Rule 15](#cross-field-rules) encodes this.

| `page_type` | Must carry | May also carry | Reaches level 4 by |
| --- | --- | --- | --- |
| `product` | 1, 2, 3 | — | a `deeper` link (4 is forbidden here) |
| `guide` | 1, 3 | 2 | a `deeper` link (4 is forbidden here) |
| `reference` | 3, 4 | 1, 2 | itself |
| `architecture` | 3, 4 | 1, 2 | itself |
| `adr` | 4 | 3 | itself |

### Handing a reader deeper

A level boundary is a **handoff**, and an unmarked handoff is how a reader ends up
treating a summary as the whole truth. Three rules:

1. **Every page that does not itself reach level 4 must name where level 4 is**, in
   the `deeper` metadata key and as a visible link in the prose. A page whose deepest
   level is 3 and which offers no route to 4 is a dead end, and the validator rejects
   it.
2. **The handoff link is the canonical source, not another summary.** Linking a
   sibling summary creates a chain of derivatives with no source at its end — the
   default drift failure. The link form is `content-ownership.md`'s: repo-relative
   within a repository; `blob/HEAD` across repositories in this org; the published
   `docs.agent-assembly.com` URL from one rendered site to another.
3. **A handoff may narrow, never widen.** The shallower text must be true of
   everything the deeper text describes. If the deeper page states a platform, a
   precondition or a default that the shallower one omits, the shallower one has
   widened the claim and must be corrected — not the deeper one.

## Badges and the ADR 0033 §6 reconciliation

This is the part most likely to be got wrong, so it is stated explicitly rather than
left implicit in a table.

**A claim vocabulary already exists and this page does not own it.** ADR 0033 §6
defines eleven terms — *Observed, Detected, Evaluated, Denied before execution,
Redacted, Approval required, Degraded, Unmeasured, Experimental, Planned,
Unsupported*. Four of the eight badge names below are §6 words. Publishing a second
definition for any of them would create exactly the two-vocabularies defect this
programme exists to eliminate.

So the eight badges are **not one enum**, and — the part that matters — **no §6 term
is redefined here, and none is carried on an axis it does not belong to**. Each badge
sits on the axis that owns its subject, and is carried only by the key for that axis.

Two of the keys below are defined by this page and still carry a §6 term:
`platforms[].status` carries `unsupported`. That is not a counter-example — §6 itself
names the platform matrix row as `Unsupported`'s evidence, so the term is on its own
subject there. What the page never does is give a §6 term a meaning of its own, or put
one on a key whose subject §6 does not range over.

| Badge | Subject it ranges over | Definition owned by | Carried by |
| --- | --- | --- | --- |
| `available-verified` | This capability in a published artifact | **This page** | `availability`, `platforms[].status` |
| `available-with-limits` | This capability in a published artifact | **This page** | `availability`, `platforms[].status` |
| `preview` | This capability in a published artifact | **This page** | `availability` |
| `deprecated` | This capability in a published artifact | **This page** | `availability` |
| `experimental` | One action, on evidence | **ADR 0033 §6**, verbatim | `claims[].term` **only** |
| `planned` | One action, on evidence | **ADR 0033 §6**, verbatim | `claims[].term` **only** |
| `unsupported` | This capability on one channel + platform | **ADR 0033 §6**, verbatim | `platforms[].status` **only** |
| `unmeasured` | One action, on evidence | **ADR 0033 §6**, verbatim | `claims[].term` **only** |

There is **no `maturity` key on this page**, and that absence is deliberate — see
[the axis ruling](#which-axis-owns-which-word--settled-by-adr-0034) below.

### The four that are ADR 0033 §6 terms reused verbatim

`experimental`, `planned`, `unsupported` and `unmeasured` are **§6's terms**. This
page does not define them, does not paraphrase them, and does not narrow them. It
specifies only where they are carried and how they are rendered. For their meaning
and their required evidence, ADR 0033 §6 is the source — go there.

Three scoping consequences follow from §6's own text and are recorded here because a
validator needs them:

- **`experimental` and `planned` are claim terms, so they live in `claims[]`.** They
  are not values of any key this page owns. A capability that is decided but not
  implemented is recorded as `claims: [{term: Planned, evidence: <ticket>}]` — with
  no `availability` value at all, because a planned capability is in no artifact.
- **`unsupported` is per (channel, platform), never page-level.** §6 names *"the
  platform matrix row"* as its required evidence, so the term belongs in a
  `platforms[]` row and is rejected everywhere else. Platform names follow ADR 0033
  §5.3's matrix rows — `linux-x86_64`, `linux-aarch64`, `macos`, `windows` — rather
  than a finer split §5.3 does not make.
- **`unmeasured` is per-action, never page-level.** §6 scopes it to an *action or
  payload*, and explicitly notes that a connection-level observation may still exist
  for the same traffic. Using it to mean "we did not check whether this ships" would
  be a redefinition, so it is rejected everywhere except `claims[].term`. A
  distribution fact that was never checked is not a badge at all — it is a **missing
  `platforms[]` row**, which is a validation error.

### The four that are this page's, on their own subject

`available-verified`, `available-with-limits`, `preview` and `deprecated` do not
appear anywhere in ADR 0033 — verified as zero occurrences against the ADR text, with
`Unmeasured`, `Unsupported`, `Experimental` and `Planned` as positive controls in the
same probe. Every one of them answers a single question — *what can a reader obtain
from a published artifact, and how much may they rely on it?* — and **none of them
says how finished anything is, or what it does to an action**.

| Badge | Means | Required evidence |
| --- | --- | --- |
| `available-verified` | Present in every published artifact named by a `platforms[]` row, at the named version, checked against a published tag | A `platforms[].evidence` string per shipping row, plus `last_verified` |
| `available-with-limits` | Present, but a stated limit changes what a reader may rely on | The above, **plus** a non-empty `limitations` |
| `preview` | Present, but **outside the compatibility commitment** — it may change without a deprecation cycle | The above |
| `deprecated` | Present, and scheduled for removal | The above, **plus** a `limitations` naming the replacement |

> **`available-verified` is an availability statement, not an enforcement claim.** It
> asserts that the capability *is present in a published artifact*. It asserts
> nothing about what the capability *does to an action* — that requires a §6 term in
> `claims[]`. Writing `available-verified` and expecting a reader to infer protection
> is the promotion error `content-ownership.md` lists among the moves that widen a
> claim, and ADR 0034 forbidden design 12 bans it by name.

### Which axis owns which word — settled by ADR 0034

An earlier draft of this page recorded this question as open and deferred it to
AAASM-5621. **It is no longer open.** ADR 0034 — the AAASM-5621 deliverable — settles
it, and this page is built against that ruling rather than around it.

Hand-off 7 of ADR 0034 rules that there are **three** axes, each ranging over a
different subject, and that **no axis may be applied to another's subject**:

| Axis | Vocabulary | Owner | Ranges over |
| --- | --- | --- | --- |
| Behaviour on evidence | ADR 0033 §6's eleven claim terms | ADR 0033 §6 (Core) | One **action** on one host, at one time |
| Documentation-area maturity | `🧪 Release candidate`, `🗺️ Planned` | Docs Hub [`source-of-truth.md`](source-of-truth.md) | One **area of Agent Assembly documentation** |
| Portfolio lifecycle | `available`, `beta`, `release_candidate`, `coming_soon` | The company site's pinned product registry | One **product in the Horonomy portfolio** |

Forbidden design 12 then bans *"applying a maturity label as a behaviour claim, a
claim term as a completeness claim, or a portfolio lifecycle value to either … and
coining a term **on the claim axis** — one naming a behaviour-on-evidence outcome —
that ADR 0033 §6 does not define."*

That second clause is **scoped to the claim axis, and to it alone**. §6 owns the first
axis only; `🧪 Release candidate` and `🗺️ Planned` are the Docs Hub's terms and the
portfolio lifecycle values are the company registry's, and §6 defines none of them.
**A new term on a non-claim axis is governed by that axis's owner, not by §6.**

Three consequences, all of which this page obeys:

1. **No `maturity` key.** A page does not restate its area's maturity. Documentation-
   area maturity ranges over an *area*, not a page, and `source-of-truth.md` owns it —
   so it is **read from the area row**, via this page's `area` key, and never copied
   into a page's metadata. Copying it would both duplicate a generated value and apply
   an area-scoped label to a page-scoped subject.
2. **No §6 term as a completeness value.** `experimental` and `planned` are claim
   terms; carrying them under a key named for completeness is forbidden design 12's
   second clause exactly. They are in `claims[]`.
3. **`availability` coins nothing on the claim axis, so its owner is this page.** Its
   subject — *a capability's presence in a published artifact* — is none of hand-off
   7's three: not an action, not a documentation area, not a portfolio product. It is
   the subject this ticket exists to make recordable, because distribution here is per
   channel and per platform and no existing vocabulary expresses it. Being a non-claim
   axis, it is governed by its own axis owner under forbidden design 12's scoping, and
   the four values below are that owner's to define. §6 supplies the **negative** value
   for the same subject (`Unsupported`, whose stated evidence is the platform matrix
   row) but has no positive counterpart, which is why the positives are defined here
   and the negative is reused verbatim.

Nothing on this page is a term on the claim axis. Every behaviour-on-evidence
statement a page makes is a §6 term in `claims[]`, spelled exactly as §6 spells it.

### Visual treatment

Badges render as inline spans, styled by the brand stylesheet. The **text is the
badge**; colour is redundant reinforcement, never the only carrier of meaning — the
hub's [accessibility](accessibility.md) baseline requires that.

```html
<span class="aa-badge aa-badge--available-verified">Available (verified)</span>
<span class="aa-badge aa-badge--unsupported">Unsupported</span>
```

| Badge | Class suffix | Tone |
| --- | --- | --- |
| `available-verified` | `--available-verified` | positive |
| `available-with-limits` | `--available-with-limits` | caution |
| `preview` | `--preview` | caution |
| `experimental` | `--experimental` | caution |
| `planned` | `--planned` | neutral |
| `deprecated` | `--deprecated` | caution |
| `unsupported` | `--unsupported` | negative |
| `unmeasured` | `--unmeasured` | neutral |

A badge whose term is owned by ADR 0033 §6 must link to §6 on first use on a page, so
a reader can reach the definition rather than infer it.

## The metadata block

### Where it lives, and why not front-matter

mdBook does not support YAML front-matter — it would render as literal text at the top
of the page. The block is therefore an **HTML comment**, which mdBook passes through
without rendering, placed as the **first construct in the file, before the `# H1`**.

A sidecar manifest keyed by page path was considered — it would match the repo's
existing `hub-components.toml` / `compatibility.toml` precedent — and rejected: page
metadata that lives away from its page drifts from it, and a new page acquires a row
only if someone remembers. In-page metadata is edited by the same person, in the same
commit, as the prose it describes.

The shape — this is an illustration of placement, **not** a template to copy; the
`...` stands for the remaining keys, and a real block never contains it. Copyable
blocks are in [Page templates](#page-templates):

```text
<!-- BEGIN AA-PAGE-META
schema_version: 1
page_type: product
...
END AA-PAGE-META -->
```

**Parsing contract for AAASM-5601:**

- **The delimiter match is anchored, not a substring search.** A line opens a block
  only if its content, after stripping leading and trailing whitespace, *begins with*
  the literal `<!-- BEGIN AA-PAGE-META`; a line closes it only if its stripped content
  *equals* `END AA-PAGE-META -->`. A mention of the literal in the middle of a
  sentence is not a delimiter.
- **Delimiters inside fenced code blocks or inline code spans do not open a block.**
  Strip fenced regions **and inline code spans** before scanning — the same exemption
  [rule 13](#rule-13--the-unbounded-claim-verbs) uses, and for the same reason.
- This page is the proof that both of the rules above are needed. The literal
  `<!-- BEGIN AA-PAGE-META` occurs on **nine** lines here: **one** real block, **six**
  inside fenced templates, and **two** inline — in the bullet above and in this
  sentence. A scanner that stripped fences but not inline code, or that matched
  anywhere in a line rather than at its start, would find three BEGIN delimiters and
  reject the page that defines the format.
- The **body** is the lines strictly between the two delimiter lines, parsed as a YAML
  1.2 mapping.
- The body **must not contain the two-character sequence `--`**, because that is not
  legal inside an HTML comment. The delimiter lines themselves are excluded from this
  check — they necessarily contain `<!--` and `-->`. Single hyphens in enum values are
  fine. A `--` in the body is a hard error.
- Exactly one block per file. Zero blocks, two blocks, or a block that is not the
  first construct is a hard error.
- Unknown keys are a hard error, not a warning — a typo'd key is otherwise a silently
  absent required field.

### Failure modes

Every rule below resolves to exactly one of these, so 5601 needs no judgement call:

| Outcome | Meaning | Effect |
| --- | --- | --- |
| **error** | The page is invalid | Build/CI fails |
| **warning** | The page is valid but stale or degrading | Reported, does not fail |

## Field reference

`R` = required, `O` = optional, `C` = conditional (see
[cross-field rules](#cross-field-rules)).

| Key | Type | Req | Allowed values | Missing / invalid |
| --- | --- | --- | --- | --- |
| `schema_version` | integer | R | `1` | error |
| `page_type` | string | R | `product` · `guide` · `reference` · `architecture` · `adr` | error |
| `audience` | list of string, non-empty | R | `evaluator` · `developer` · `operator` · `security-engineer` · `contributor` · `auditor` | error |
| `user_job` | string | R | 10–120 chars; one sentence — no interior period-then-space, no trailing period | error |
| `owner` | string | R | `L<n>:<surface>`, exactly as paired in the [surface table](#owner-surfaces) | error |
| `canonical_source` | string | R | `self`, **or** a link in the canonical-link form | error |
| `describes_capability` | boolean | R | `true` · `false` | error |
| `area` | string | C | one of the 12 [area ids](#area-ids) | error if required and absent |
| `availability` | string | C | `available-verified` · `available-with-limits` · `preview` · `deprecated` | error |
| `platforms` | list of object | C | see [`platforms[]`](#platforms) | error |
| `last_verified` | object | C | see [`last_verified`](#last_verified) | error |
| `claims` | list of object | C | see [`claims[]`](#claims) | error |
| `limitations` | string | C | non-empty; a link or an in-page anchor | error |
| `disclosure_levels` | list of integer, non-empty | R | subset of `[1,2,3,4]`, ascending, no duplicates | error |
| `deeper` | string | C | a link in the canonical-link form | error |
| `capability_ids` | list of string | O | **reserved** — pending AAASM-5531. Shape not validated in v1: the key is accepted and ignored | none |

There is deliberately **no `maturity` key** — see
[the axis ruling](#which-axis-owns-which-word--settled-by-adr-0034). A page's
documentation-area maturity is read from its [`area`](#area-ids) row, not restated
here.

### `owner` surfaces

`owner` names the layer that *owns the content*, not the repo the file sits in — a
Docs Hub page summarising a Core fact is owned by Core.

The value must be one of these eleven pairs, **exactly as written**. The pairing is
fixed here rather than by reference, so a validator needs no cross-repository lookup:

| `owner` | Layer | Surface |
| --- | --- | --- |
| `L0:horonomy.dev` | L0 Company site | `horonomy.dev` |
| `L1:official-website` | L1 Product website | `official-website` |
| `L2:docs` | L2 Docs Hub | `docs` |
| `L3:agent-assembly` | L3 Component docs | `agent-assembly` (Core) |
| `L3:python-sdk` | L3 Component docs | `python-sdk` |
| `L3:node-sdk` | L3 Component docs | `node-sdk` |
| `L3:go-sdk` | L3 Component docs | `go-sdk` |
| `L3:arena` | L3 Component docs | `arena` |
| `L3:cloud` | L3 Component docs (private) | `cloud` |
| `L3:agent-assembly-enterprise` | L3 Component docs (private) | `agent-assembly-enterprise` |
| `L4:examples` | L4 Examples | `examples` |

Any other value — including a right-hand surface paired with the wrong layer — is an
error.

Three notes on the boundaries of this table, because each one is a question a
validator author would otherwise have to guess at:

- **`cloud` and `agent-assembly-enterprise` are L3.** `content-ownership.md`'s layer
  table does not list them, but its prose is explicit that a private repository *"is
  an L3 component for its own contributors and is outside the public content
  boundary"*. Their **reader-facing** pages are published as L2 Docs Hub pages, so a
  hub page about the managed service is `L2:docs`; `L3:cloud` names the private
  component only, and what may be said about it is bounded by the
  [SaaS claim publication checklist](saas-claim-publication-checklist.md).
- **L5 and L6 cannot be owners.** L5 is a repository README and L6 is code, generated
  specs and evidence — `content-ownership.md` states that nothing in L6 is a
  reader-facing page. Neither owns a page's content, so no pair exists for them, and
  `owner` accepts no `L5:` or `L6:` value. That a level-4 section *cites* L6 evidence
  is a different relationship from L6 *owning* the page.
- **The layer is the content's, not the file's.** This page lives in the `docs` repo
  but a page here that summarises a Core fact carries `L3:agent-assembly` and a
  `canonical_source` link, per rule 9.
- **`canonical_source: self` is available only to `L2:docs` and the `L3:` surfaces.**
  Rule 9 turns on the `owner` surface naming the repository the page is in, and only
  those nine surfaces *are* repository names. `L0:horonomy.dev` is a domain — its
  repository is `horonomy-official-website`, in a different organisation — and
  `L1:official-website` and `L4:examples` name repositories this contract is not
  applied in. Pages under those owners always carry a link.

### `area` ids

`area` ties a page to one row of the status map in
[`source-of-truth.md`](source-of-truth.md). That row carries the page's
documentation-area maturity, which is therefore **read from the status map and
published beside the page's other metadata** rather than restated inside it.

No validation rule derives anything from the area's maturity label — see
[why there is no such rule](#there-is-no-rule-coupling-the-area-label-to-a-claim-term).
`area` identifies the row; the reader gets both the area label and the page's
`claims[]`, each checked against its own owner.

The row cannot be identified by name, because the area names exist in **three
incompatible forms**: the rendered table cell (`**Node / TypeScript SDK**`), the
`short_name` in `hub-components.toml` (`Node SDK`), and — for five of the twelve —
neither, because Specs, Releases, Cloud, Enterprise and Operations are literal
strings inside `generate_hub_components.py` rather than manifest rows. So `area`
takes a **stable id**, and this table is the mapping:

| `area` id | Row identified by this exact `Area` cell |
| --- | --- |
| `core` | `**Core** (gateway, policy engine, eBPF, proxy, FFI, WASM, CLI, API)` |
| `python-sdk` | `**Python SDK**` |
| `node-sdk` | `**Node / TypeScript SDK**` |
| `go-sdk` | `**Go SDK**` |
| `arena` | `**Arena** (cross-framework governance trials)` |
| `examples` | `**Runnable examples**` |
| `homebrew` | `**Homebrew / install channel**` |
| `specs` | `**Specs** (protocol & policy spec)` |
| `releases` | `**Releases** (versions & compatibility)` |
| `cloud` | `**Cloud** (SaaS control plane)` |
| `enterprise` | `**Enterprise** (SSO, SCIM, advanced audit)` |
| `operations` | `**Operations** (running & onboarding)` |

**Resolution procedure**, so no step is a judgement call: map the `area` id to its
`Area` cell using the table above; find the row in `source-of-truth.md`'s
`BEGIN GENERATED:hub-components:source-of-truth-table` region whose first cell matches
that string exactly; read its `Maturity` cell. A missing or ambiguous match is an
error — it means the status map changed and this table was not updated with it.

> **This mapping is hand-maintained, and that is a known weakness.** It duplicates
> identifiers that a generator should emit. The durable fix is a stable `id` per area
> in `hub-components.toml` **and** in the generator's five literal rows, with this
> table generated from it — recorded as a hand-off to AAASM-5601, which owns the
> tooling. It is not done here because `hub-components.toml` and the generator belong
> to the status-map pipeline, not to this page, and changing them is a separate
> concern from defining the metadata contract. Until then, an area rename requires
> editing this table in the same PR.

### `platforms[]`

Distribution in this product is **per channel and per platform**: a capability can
ship on one channel and not another. A single "released" boolean is therefore not
expressible, and is not offered. Each row is one (channel, platform) pair.

> **Relationship to ADR 0034 §6.1's `released_channels` / `released_platforms` /
> `released_matrix`.** Same shape, different surface, and deliberately not merged into
> one name. §6.1's fields belong to the **capability manifest** AAASM-5531 will publish
> — one record per capability, across the whole product. `platforms[]` here is **page**
> metadata: what this page's subject ships on, written by the page's author. When 5531
> lands, `platforms[]` becomes derivable from `released_matrix` and this page should
> say so rather than keeping a second hand-maintained copy — that is the same hand-off
> `capability_ids` already carries. Recording the correspondence now is what stops a
> third spelling appearing later.
>
> Note also that `availability` answers only §6.1's **Distributed?** question.
> *Buildable?* and *Activated?* are separate questions with separate fields
> (`default_state`, `reachability`), and no value on this page may be read as
> answering them — a capability can ship in an artifact and still be unreachable in it.

| Key | Type | Req | Allowed values |
| --- | --- | --- | --- |
| `channel` | string | R | `github-release` · `homebrew` · `ghcr` · `install-sh` · `crates-io` |
| `platform` | string | R | `linux-x86_64` · `linux-aarch64` · `macos` · `windows` |
| `status` | string | R | `available-verified` · `available-with-limits` · `unsupported` |
| `evidence` | string | C | non-empty; required when `status` is not `unsupported` |

- Duplicate (`channel`, `platform`) pairs are an error.
- A pair that is **absent** asserts nothing, and asserting nothing about a channel a
  page's capability plausibly ships on is the gap this field exists to close. A page
  with `describes_capability: true` must therefore enumerate a row for **every**
  channel in the enum, using `unsupported` where it does not ship. Partial
  enumeration is an error — **except where [rule 4](#cross-field-rules) applies**, in
  which case `platforms` is exactly `[]` and no row is written at all.
- `unsupported` requires no `evidence` string because ADR 0033 §5.3's matrix row is
  its evidence, per §6.
- **Enumeration is per channel, and platform coverage within a channel is deliberately
  partial.** The rule closes the gap that matters most — a channel a capability
  plausibly ships on being passed over in silence — and stops short of the full
  (channel × platform) cross product, which is twenty rows for a fact that is usually
  uniform across platforms within a channel. So a page naming `github-release` ×
  `linux-x86_64` asserts nothing about `github-release` × `windows`. Where the platform
  distinction is the point, write the extra rows: they are permitted, and only the
  per-channel minimum is enforced.

### `last_verified`

| Key | Type | Req | Allowed values |
| --- | --- | --- | --- |
| `version` | string | R | a release version, e.g. `v0.0.1-rc.6` |
| `ref` | string | R | a tag matching `^v\d+\.\d+\.\d+(-[A-Za-z0-9.]+)?$`, **or** a 40-character hex SHA |
| `date` | string | R | ISO 8601 `YYYY-MM-DD` |
| `method` | string | R | non-empty, ≤ 200 chars — how it was checked |

> **Evidence taken from a branch does not describe a published artifact.** A reader
> asking "does this ship?" is asking about a tag. The literal values `main`, `master`
> and `HEAD` are therefore **hard errors** in `ref`, as is any value that is neither a
> tag nor a full SHA. If the only evidence available is from a branch, the honest
> record is a `platforms[]` row you cannot yet fill — not a `ref` that overstates.

Freshness:

| Condition | Outcome |
| --- | --- |
| `date` more than 180 days old | **error** — evidence is stale |
| `date` more than 90 days old | **warning** |
| `version` differs from the current release | **warning** |
| `date` in the future | **error** |

"The current release" is the `core` value of the single `[[release]]` table in
`compatibility.toml` whose `status = "current"` — at time of writing `v0.0.1-rc.6`.
Naming the key matters: `compatibility.toml` holds one `[[release]]` per supported
version, so "the version in `compatibility.toml`" would otherwise match several.

**Parse the TOML; do not grep it.** A parser returns exactly one table with
`status = "current"`. A grep for the string returns **two** — the second occurrence
is inside a commented-out worked example further down the file, and an implementer who
takes the last match, or errors on finding two, gets the wrong answer from a file that
is actually unambiguous.

### `claims[]`

Zero or more. Each entry:

| Key | Type | Req | Allowed values |
| --- | --- | --- | --- |
| `term` | string | R | one of ADR 0033 §6's eleven terms, **verbatim** |
| `evidence` | string | R | non-empty — a link, or an `E`-block reference into the public claim inventory |

The permitted `term` values are §6's whole set, not a subset:
`Observed` · `Detected` · `Evaluated` · `Denied before execution` · `Redacted` ·
`Approval required` · `Degraded` · `Unmeasured` · `Experimental` · `Planned` ·
`Unsupported`. Restricting the list here would be a redefinition of someone else's
vocabulary; extending it would be worse. If §6 gains or loses a term, this enum
follows it — §6 is the source, and a mismatch is a bug in this page.

## Cross-field rules

These are the rules a prose field list cannot express, and they are where most of the
validation value is.

| # | Rule | Outcome if violated |
| --- | --- | --- |
| 1 | `describes_capability: true` ⇒ `area`, `platforms`, `last_verified` and `claims` all present | error |
| 2 | `describes_capability: false` ⇒ `area`, `availability`, `platforms`, `last_verified`, `claims`, `limitations` all **absent** | error |
| 3 | `availability: available-with-limits` **or** `deprecated` ⇒ `limitations` present and non-empty | error |
| 4 | `claims[]` contains `Planned` ⇒ `availability` **absent**, `platforms` exactly `[]`, and `claims` contains no other term | error |
| 5 | `availability: available-verified` ⇒ every `platforms[]` row has `status` ∈ {`available-verified`, `unsupported`} — no row may be `available-with-limits` | error |
| 6 | `availability` is present **iff** `describes_capability: true` **and** `claims[]` does not contain `Planned` | error |
| 7 | `platforms[].status` may never be `preview` or `deprecated`, and never a §6 term other than `unsupported` | error |
| 8 | `claims[].term` may never be a value outside §6's eleven | error |
| 9 | `canonical_source: self` ⇒ the `owner` surface names the repository the page is in; otherwise `canonical_source` must be a link | error |
| 10 | `canonical_source` other than `self` must match the canonical-link form: repo-relative, `https://github.com/<org>/<repo>/blob/HEAD/<path>`, or `https://docs.agent-assembly.com/<path>`. A branch-name blob URL is rejected | error |
| 11 | `max(disclosure_levels) < 4` ⇒ `deeper` present | error |
| 12 | `disclosure_levels` must be a subset of the page type's **must ∪ may** levels, and include all of its **must** levels — see [the table](#which-levels-a-page-must-carry) | error |
| 13 | An unbounded claim verb appears in the body ⇒ `describes_capability: true`, `claims` non-empty, and `limitations` present | error |
| 14 | `claims[]` contains any of `Observed`, `Detected`, `Evaluated`, `Denied before execution`, `Redacted`, `Approval required`, `Degraded` ⇒ `limitations` present and non-empty | error |
| 15 | `page_type` is `product` or `guide` ⇒ `4 ∉ disclosure_levels` (those types reach level 4 by a `deeper` link, never in the page) | error |

### There is no rule coupling the area label to a claim term

An earlier draft carried a rule 13 requiring a `🗺️ Planned` area's pages to claim
`Planned`, and forbidding the claim on `🧪 Release candidate` areas. **It is
withdrawn**, and no rule replaces it.

It was a forbidden design. The area label is on the documentation-area axis and
`claims[].term` is on the behaviour axis, and ADR 0034 hand-off 7 states that *no axis
may be applied to another's subject* — a documentation-area label says nothing about
an action's behaviour. Removing `maturity` took that collapse out of the **key** but
left it in the **rule**, which is the subtler half of the same defect.

It also produced wrong answers on ordinary pages, in both directions:

- An `operations` page documenting a capability that genuinely ships would have been
  forced to claim `Planned`, which [rule 4](#cross-field-rules) then forces to
  `platforms: []` — asserting the capability is in no published artifact, which is
  false, and which [this page](#platforms) elsewhere calls a validation error.
- A `core` page documenting a genuinely planned capability — the Windows host adapter,
  `Unsupported` in ADR 0033 §5.3 — could not have used §6's `Planned` at all, though
  that is the term §6 defines for exactly this case.

The correct treatment is a **publication** rule, not a metadata one. ADR 0034 hand-off
1 prescribes it: split the statement into a behaviour claim and a completeness claim,
check each against its own owner, publish both, and let the more restrictive published
outcome govern the surface. So a page carries its `area` label and its `claims[]` side
by side, each validated against its own owner, and neither constrains the other. The
internal consistency the withdrawn rule was reaching for is already carried by rules 4
and 6, which govern `claims[]` and `availability` — both on axes this page may bind
together, because `availability` is not §6's.

Rule numbering was closed up rather than leaving a gap; the rules formerly numbered
14, 15 and 16 are now 13, 14 and 15.

### Rule 4 and the enumeration carve-out

Rule 4 is the only place `platforms` may be empty, and it is the reason the
[full-enumeration requirement](#platforms) carries an explicit exception. A capability
that is `Planned` is in no artifact, so there is no channel row to write and no
availability to state — enumerating five `unsupported` rows for it would assert a
platform *result* where §6 requires a ticket reference and **no capability claim**.

The three `🗺️ Planned` areas today are `cloud`, `enterprise` and `operations`, so this
is the path AAASM-5610 will take on `quickstart-saas.md` and `cloud-deployment.md` —
the first hub pages it touches. Rules 4 and 6 are written to agree with each other
on exactly that case.

### Rule 14 — why the verb list is not enough

Rule 13 keys off English prose; rule 14 keys off a declared enum, and the second is
strictly the more reliable of the two. Without rule 14 a page can declare the
strongest term in §6's vocabulary — `Denied before execution` — with `availability:
available-verified` and an empty `limitations`, and pass every other rule: rule 3 does
not fire because the availability value is not `available-with-limits`, and rule 13
does not fire if the prose avoids the five listed verbs. Publishing the product's
strongest enforcement claim with no stated limitation is precisely what this page's
second acceptance criterion forbids, so the rule closes it from the metadata side.

The seven terms it covers are every §6 term that asserts a control **did something**
to an action or its payload. Only four are excluded, and each because it asserts the
opposite — that no control acted, or that none exists yet:

| Excluded term | Why |
| --- | --- |
| `Unmeasured` | §6: no control inspected the action; there is no capability to bound |
| `Unsupported` | §6: not available on this platform/configuration |
| `Planned` | Decided but not implemented, and §6 attaches **no capability claim**; rules 4 and 6 already force `platforms: []` and forbid `availability` |
| `Experimental` | Implemented but not validated for production — §6 requires the missing validation be named, which is itself the bound |

> **`Observed` and `Detected` are in the rule, not excluded from it.** An earlier draft
> excluded them as reporting "an absence of control", which is simply wrong: §6 defines
> `Observed` as *an event reached the evidence pipeline* and `Detected` as *a pattern of
> interest was found* — both are positive capability claims, and neither is bounded
> anywhere else in this page. Excluding them left the most historically dangerous claim
> in this product unbounded: ADR 0033 cites *"eBPF sensor catches kernel-level bypass attempts"*
> as a forbidden design, and §6 maps the eBPF syscall guard to `Detected`
> with an explicit *not Denied before execution* caveat. A page claiming `Detected`
> with no stated limitation is exactly that defect, so rule 14 now covers it.

### Rule 13 — the unbounded claim verbs

Rule 13 is the mechanical form of *"public pages cannot omit status and limitations
when the claim depends on them"*. [Product promise](product-promise.md) already
instructs authors to pick a §6 term for every verb; rule 13 restates that requirement
from the metadata side, so a page cannot satisfy it by wording alone.

The closed list, matched case-insensitively on word boundaries, **as these literal
forms only** — no inflection expansion:

`protects` · `enforces` · `catches` · `prevents` · `guarantees`

The first three are the three verbs ADR 0033 §6 names by name when it requires that
downstream material pick one of its terms rather than an undifferentiated verb like
`protects`, `enforces` or `catches`. Taking §6's own examples is the least inventive
possible choice of list.

**Exempt occurrences**, which a validator must strip before matching:

1. Fenced code blocks.
2. Inline code spans.
3. Text inside straight double quotes (`"…"`) or typographic double quotes (`"…"`).

Exemption 3 exists because a page *discussing* the rule quotes the banned verbs in
prose. It is mechanical — quote characters, not intent — and it is the difference
between this rule being usable and being wrong on the very pages that explain it.

Two properties of exemption 3 that a prose statement would leave to the implementer,
and which decide whether two conforming validators agree:

- **Quoted spans are matched across the whole document, not per line.** A quotation
  that wraps onto a second line is one span. This is the one place the page is *not*
  line-oriented, and it is called out because every other parsing rule here is —
  delimiters are matched per line, and an implementer who carried that habit into
  exemption 3 would get a different answer on a wrapped quotation.
- **An odd number of straight double quotes in a document is an error**, not a
  silently-shifted pairing. Quotes are paired left to right; an unmatched final quote
  means every subsequent pairing is offset, so the honest outcome is to reject the
  page rather than emit a result that depends on where the imbalance happened to fall.
  Typographic quotes pair by direction and are exempt from the count.

**Prefer inline code over quotation when naming a banned verb.** This page names all
five in backticks where it lists them; one further occurrence sits inside a quoted ADR
citation and does rely on exemption 3, which is the legitimate use — a page genuinely
quoting a source. Measured: deleting exemption 3 leaves exactly **one** hit on this
page, that citation. The earlier draft quoted three of the verbs in bare prose and was,
correctly, the first page to expose the ambiguity above; exemption 3 should not be the
mechanism a page relies on to *discuss* the rule, only to quote a source.

> **The list is deliberately high-precision, and it is a floor rather than a ceiling.**
> The obvious longer list — adding `blocks`, `stops`, `secures`, `ensures` and the bare
> infinitives — was tested against this page and rejected: `blocks` alone matches
> *"code blocks"*, *"fenced blocks"* and *"E-blocks"* several times here, none of them
> a product claim. A gate that fires on a common noun gets switched off, and a gate
> that is off finds nothing. Third-person singular is the form an actual capability
> claim takes (`Agent Assembly protects …`), so that is what is matched.
>
> False negatives are therefore expected and accepted. Rule 13 does not replace the
> editorial rule in [Product promise](product-promise.md) — *if the sentence works
> with an undifferentiated verb, it is not specific enough to publish* — it only makes
> the most common case unmissable. Rule 14, which keys off a declared enum rather than
> English, is the stronger of the two.

A page that uses one of these verbs in prose and declares `describes_capability:
false` has mis-declared its type, and that is an error rather than a warning: it is
the exact combination that lets an unevidenced claim through unchecked.

## Page templates

Five templates, one per `page_type`. They are the required *skeleton*; a page may add
sections freely. Copy the metadata block and the headings, then write.

Every template below carries a **complete, parseable** block — opening delimiter, YAML
body, `END AA-PAGE-META -->` terminator. None uses an elided `...` form, because a
template an author copies verbatim has to validate verbatim.

Templates are versioned by `template_version` below, which moves with
`schema_version`. A template change that adds a required section or changes a key is a
**major** change and needs a new `schema_version` plus a migration row in
[the changelog](#template-changelog).

**Current `template_version`: 1** (matches `schema_version: 1`).

### `product` — describes what the product does for a reader

```text
<!-- BEGIN AA-PAGE-META
schema_version: 1
page_type: product
audience: [evaluator]
user_job: Decide whether this capability meets my requirement
owner: L3:agent-assembly
canonical_source: https://docs.agent-assembly.com/core/latest/...
describes_capability: true
area: core
availability: available-with-limits
limitations: "#limits"
platforms:
  - {channel: github-release, platform: linux-x86_64, status: available-verified, evidence: "..."}
  - {channel: homebrew,       platform: macos,        status: available-verified, evidence: "..."}
  - {channel: ghcr,           platform: linux-x86_64, status: available-verified, evidence: "..."}
  - {channel: install-sh,     platform: linux-x86_64, status: available-verified, evidence: "..."}
  - {channel: crates-io,      platform: linux-x86_64, status: available-verified, evidence: "..."}
last_verified: {version: v0.0.1-rc.6, ref: v0.0.1-rc.6, date: 2026-08-06, method: "..."}
claims:
  - {term: Evaluated, evidence: "..."}
disclosure_levels: [1, 2, 3]
deeper: https://docs.agent-assembly.com/core/latest/...
END AA-PAGE-META -->

# <Capability>

<Level 1 — one sentence, including the boundary clause.>

## How it works

<Level 2 — exactly three steps.>

## For an evaluator

<Level 3 — defaults, and what is not covered.>

## Limits

<Every limit the maturity badge depends on.>

## Going deeper

<The level-4 handoff link.>
```

### `guide` — a task a reader performs

```text
<!-- BEGIN AA-PAGE-META
schema_version: 1
page_type: guide
audience: [operator]
user_job: Route an agent through the proxy on a single host
owner: L3:agent-assembly
canonical_source: https://docs.agent-assembly.com/core/latest/...
describes_capability: false
disclosure_levels: [1, 3]
deeper: https://docs.agent-assembly.com/core/latest/...
END AA-PAGE-META -->

# <Task>

<Level 1 — what you will have when you finish.>

## Before you start

<Preconditions. Every one of them — a dropped precondition is a widened claim.>

## Steps

<The task.>

## What this does not do

<Level 3 — the boundary of the outcome.>

## Going deeper

<The level-4 handoff link.>
```

### `reference` — the authoritative surface for something

```text
<!-- BEGIN AA-PAGE-META
schema_version: 1
page_type: reference
audience: [developer, operator]
user_job: Look up the exact behaviour of one policy field
owner: L3:agent-assembly
canonical_source: https://docs.agent-assembly.com/core/latest/...
describes_capability: false
disclosure_levels: [3, 4]
END AA-PAGE-META -->

# <Subject> reference

<Who this is for and what it covers.>

## Scope

<What is in this reference and what is deliberately not.>

## <Reference body>

<Level 3 and level 4. No length bound.>
```

### `architecture` — how something is built and why

```text
<!-- BEGIN AA-PAGE-META
schema_version: 1
page_type: architecture
audience: [security-engineer, contributor]
user_job: Understand how the proxy decides before it dials upstream
owner: L3:agent-assembly
canonical_source: https://docs.agent-assembly.com/core/latest/...
describes_capability: true
area: core
availability: available-with-limits
limitations: "#boundaries-and-non-goals"
platforms:
  - {channel: github-release, platform: linux-x86_64, status: available-verified, evidence: "..."}
  - {channel: homebrew,       platform: macos,        status: available-verified, evidence: "..."}
  - {channel: ghcr,           platform: linux-x86_64, status: available-verified, evidence: "..."}
  - {channel: install-sh,     platform: linux-x86_64, status: available-verified, evidence: "..."}
  - {channel: crates-io,      platform: linux-x86_64, status: available-verified, evidence: "..."}
last_verified: {version: v0.0.1-rc.6, ref: v0.0.1-rc.6, date: 2026-08-06, method: "..."}
claims:
  - {term: Denied before execution, evidence: "..."}
disclosure_levels: [3, 4]
END AA-PAGE-META -->

# <Component or subsystem>

## Context

<The problem, and the constraints that shape the design.>

## Design

<Level 4. Full depth. Diagrams, data flow, failure behaviour.>

## Boundaries and non-goals

<What it deliberately does not do.>

## Evidence

<Where each claim on this page is checked.>
```

### `adr` — a recorded decision

An ADR keeps the format of the ADR set it belongs to; this template adds the metadata
block and nothing else. ADRs live in the component repository that owns the decision —
per `content-ownership.md`, this hub does not author them.

Note the `canonical_source: self` paired with `owner: L3:agent-assembly`: an ADR *is*
the canonical source for its decision. That combination is valid under
[rule 9](#cross-field-rules) only when the validator runs in the `agent-assembly`
repository, which is where the page lives — the same block placed on a Docs Hub page
would be rejected, correctly, as a hub page cannot be canonical for a Core decision.

```text
<!-- BEGIN AA-PAGE-META
schema_version: 1
page_type: adr
audience: [contributor, auditor]
user_job: Understand why this decision was taken and what it binds
owner: L3:agent-assembly
canonical_source: self
describes_capability: false
disclosure_levels: [4]
END AA-PAGE-META -->

# ADR NNNN: <Title>

## Status

## Context

## Decision

## Consequences

## Alternatives Considered
```

### Template changelog

| `schema_version` | Date       | Change              | Migration |
| ---------------- | ---------- | ------------------- | --------- |
| 1                | 2026-08-06 | Initial definition. | —         |

## What this page hands off

| To | What |
| --- | --- |
| **AAASM-5601** | Implement the validator: the parsing contract, the field reference, the 15 cross-field rules and the freshness thresholds are intended to be sufficient with no further decisions. If a rule needs judgement to implement, that is a defect in this page — report it rather than choosing. **Also**: replace the hand-maintained [`area` id table](#area-ids) with a generated one, by adding a stable `id` to each row of `hub-components.toml` and to the five literal rows in `generate_hub_components.py`. |
| **AAASM-5610** | Apply metadata blocks to existing hub content. This page carries the only block today. Expect the three `🗺️ Planned` areas — `cloud`, `enterprise`, `operations` — to take the [rule 4](#cross-field-rules) path with `platforms: []`, and expect `product-promise.md` to need a block plus a rule 13 review. |
| **AAASM-5621 / ADR 0034** | Precedence between the three axes, waivers, and cross-repository adoption records. The scope of forbidden design 12's coining clause is **settled** — it is claim-axis only — and is applied here, not deferred. |
| **AAASM-5531** | The capability/evidence manifest. When it lands, `capability_ids` becomes validated and required, at `schema_version: 2`. |

---

*Last reviewed: 2026-08-06 — AI Agent Assembly Team*
