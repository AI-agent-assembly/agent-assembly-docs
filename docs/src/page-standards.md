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

This page is downstream of three merged artifacts. It **adds no claim** to any of
them, and it does not restate their definitions.

| Source | What it supplies | Where |
|---|---|---|
| **ADR 0033 §6 — claim vocabulary** | The eleven enforcement/claim terms. Four of the badge names below are §6's words, reused verbatim. | [ADR 0033](https://docs.agent-assembly.com/core/latest/adr/0033-canonical-governance-and-enforcement-architecture.html) |
| **Content-layer ownership** | The L0–L6 layer model, the canonical-owner table, and the rule that neither governing vocabulary absorbs the other. | [`content-ownership.md`](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/docs/src/development/content-ownership.md) |
| **Product promise & message hierarchy** | The worked instance of the four levels, for one page. | [Product promise](product-promise.md) |

Ticket references are plain text, not links: the tracker is not publicly readable, so
a link would only reach a login wall — and a link checker scores that wall as
reachable, which makes the reference look verified when it is not.

### What this page does not decide

- **Precedence** between the two governing vocabularies when they appear to conflict,
  and **waivers**. `content-ownership.md` assigns both to AAASM-5621. Nothing below
  overrides a vocabulary owner; where a word is shared, this page scopes it and says
  who owns the definition.
- **Cross-repository adoption and conflict resolution.** Also AAASM-5621.
- **A capability identifier registry.** AAASM-5531 (Define a machine-readable
  capability and evidence manifest) has not started, so `capability_ids` is reserved
  and optional in schema version 1 — see [the field reference](#field-reference).
  Requiring identifiers before a registry exists would only make authors invent them.

## The four disclosure levels

The levels are a property of a *reader's need*, not of a page's length. Each level
adds precision; **none of them retracts what the level above said**. A reader must be
able to stop at any level and still be correct.

| Level | Name | Answers | Bound | Typical layer |
|---|---|---|---|---|
| **1** | One-sentence outcome | *What do I get?* | Exactly one sentence. Must carry the boundary clause — everything shorter drops it. | L0, L1 |
| **2** | Three-step product flow | *How does it work, roughly?* | Exactly three steps, each one short paragraph. | L1, L2 |
| **3** | Evaluator detail | *What is on by default, and what does it not cover?* | No length bound. Must state defaults and non-coverage. | L2, L3 |
| **4** | Implementation deep dive | *How is it actually built, and on what evidence?* | **No bound of any kind.** | L3, L6 |

[Product promise](product-promise.md) is the reference instance: it carries all four
levels for one subject. Read it as the worked example; this page is the general
contract.

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

Required levels are a function of `page_type`. A page may always carry *more* levels
than required; it may never carry fewer.

| `page_type` | Must carry | Must reach level 4 by |
|---|---|---|
| `product` | 1, 2, 3 | a `deeper` link |
| `guide` | 1, 3 | a `deeper` link |
| `reference` | 3, 4 | itself |
| `architecture` | 3, 4 | itself |
| `adr` | 4 | itself |

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

So the eight badges are **not one enum**. They sit on two axes, they are carried by
**different metadata keys**, and they have different owners.

| Badge | Axis | Definition owned by | Carried by |
|---|---|---|---|
| `available-verified` | Distribution availability | **This page** | `maturity`, `platforms[].status` |
| `available-with-limits` | Distribution availability | **This page** | `maturity`, `platforms[].status` |
| `preview` | Lifecycle maturity | **This page** | `maturity` |
| `deprecated` | Lifecycle maturity | **This page** | `maturity` |
| `experimental` | Capability state | **ADR 0033 §6**, verbatim | `maturity` |
| `planned` | Capability state | **ADR 0033 §6**, verbatim | `maturity` |
| `unsupported` | Capability state, per platform | **ADR 0033 §6**, verbatim | `platforms[].status` **only** |
| `unmeasured` | Enforcement claim, per action | **ADR 0033 §6**, verbatim | `claims[].term` **only** |

### The four that are ADR 0033 §6 terms reused verbatim

`experimental`, `planned`, `unsupported` and `unmeasured` are **§6's terms**. This
page does not define them, does not paraphrase them, and does not narrow them. It
specifies only where they are carried and how they are rendered. For their meaning
and their required evidence, ADR 0033 §6 is the source — go there.

Two scoping consequences follow from §6's own text and are recorded here because a
validator needs them:

- **`unsupported` is per-platform, never page-level.** §6 names *"the platform matrix
  row"* as its required evidence, so the term belongs in a `platforms[]` row and is
  rejected as a `maturity` value. Platform names follow ADR 0033 §5.3's matrix rows —
  `linux-x86_64`, `linux-aarch64`, `macos`, `windows` — rather than a finer split §5.3
  does not make.
- **`unmeasured` is per-action, never page-level.** §6 scopes it to an *action or
  payload*, and explicitly notes that a connection-level observation may still exist
  for the same traffic. Using it to mean "we did not check whether this ships" would
  be a redefinition, so it is rejected everywhere except `claims[].term`. A
  distribution fact that was never checked is not a badge at all — it is a **missing
  `platforms[]` row**, which is a validation error.

### The four that are this page's, on a different axis

`available-verified`, `available-with-limits`, `preview` and `deprecated` do not
appear anywhere in ADR 0033 — verified as zero occurrences against the ADR text, with
`Unmeasured`, `Unsupported`, `Experimental` and `Planned` as positive controls in the
same probe. They answer *how finished and how reachable is this?*, which
`content-ownership.md` assigns to the Docs Hub. They are defined here:

| Badge | Means | Required evidence |
|---|---|---|
| `available-verified` | Present and reachable on **every** `platforms[]` row that names it, at the named version, checked against a published tag | A `platforms[].evidence` string per row, plus `last_verified` |
| `available-with-limits` | Ships, but a stated limit changes what a reader may rely on | The above, **plus** a non-empty `limitations` |
| `preview` | Ships on at least one channel; the interface may change without a deprecation cycle | `platforms[]` naming the channels it ships on |
| `deprecated` | Still ships, but is scheduled for removal | `platforms[]`, plus `limitations` naming the replacement |

> **`available-verified` is an availability claim, not an enforcement claim.** It
> asserts that the capability *is reachable in a published artifact*. It asserts
> nothing about what the capability *does to an action* — that requires a §6 term in
> `claims[]`. Writing `available-verified` and expecting a reader to infer protection
> is the promotion error `content-ownership.md` lists among the moves that widen a
> claim.

### The one genuine collision, and who wins

`planned` is a three-way word overlap:

| Where | Granularity | Owner |
|---|---|---|
| ADR 0033 §6 `Planned` | A capability | Core |
| `source-of-truth.md` `🗺️ Planned` | An **area** of the hub (12 rows) | Docs Hub |
| `maturity: planned` here | A **page's** subject | uses §6's definition |

These are different granularities of the same word, and `content-ownership.md`
already records the two-vocabularies problem as a known non-conforming instance and
**defers the precedence ruling to AAASM-5621**. This page therefore does **not** rule
on precedence. It does two narrower things that are within its remit:

1. **Scopes the word.** Inside a metadata block, `maturity: planned` takes ADR 0033
   §6's definition — decided but not implemented, carrying a ticket reference and
   **no capability claim**. The `🗺️ Planned` label on the status map keeps its own
   area-level meaning and is neither overridden by, nor overrides, a page's
   `maturity`.
2. **Binds them so they cannot silently contradict.** The `area` key ties every
   capability-describing page to a row of the status map, and the validator rejects
   the combination that would be a visible lie — see
   [cross-field rules](#cross-field-rules). That turns two labels on one subject from
   a rivalry into an enforced refinement, without deciding which vocabulary is
   senior.

### Visual treatment

Badges render as inline spans, styled by the brand stylesheet. The **text is the
badge**; colour is redundant reinforcement, never the only carrier of meaning — the
hub's [accessibility](accessibility.md) baseline requires that.

```html
<span class="aa-badge aa-badge--available-verified">Available (verified)</span>
<span class="aa-badge aa-badge--unsupported">Unsupported</span>
```

| Badge | Class suffix | Tone |
|---|---|---|
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

```text
<!-- BEGIN AA-PAGE-META
schema_version: 1
page_type: product
...
END AA-PAGE-META -->
```

**Parsing contract for AAASM-5601:**

- The block is delimited by the exact literals `<!-- BEGIN AA-PAGE-META` and
  `END AA-PAGE-META -->`, each on its own line.
- **Delimiters inside fenced code blocks do not open a block.** Strip fenced regions
  before scanning. This page is the proof of why: it contains seven fenced examples of
  the delimiter and exactly one real block, and a scanner that skipped this step would
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
|---|---|---|
| **error** | The page is invalid | Build/CI fails |
| **warning** | The page is valid but stale or degrading | Reported, does not fail |

## Field reference

`R` = required, `O` = optional, `C` = conditional (see
[cross-field rules](#cross-field-rules)).

| Key | Type | Req | Allowed values | Missing / invalid |
|---|---|---|---|---|
| `schema_version` | integer | R | `1` | error |
| `page_type` | string | R | `product` · `guide` · `reference` · `architecture` · `adr` | error |
| `audience` | list of string, non-empty | R | `evaluator` · `developer` · `operator` · `security-engineer` · `contributor` · `auditor` | error |
| `user_job` | string | R | 10–120 chars; one sentence — no interior period-then-space, no trailing period | error |
| `owner` | string | R | `L<n>:<surface>`, `n` ∈ 0–6, surface ∈ the [surface list](#owner-surfaces) | error |
| `canonical_source` | string | R | `self`, **or** a link in the canonical-link form | error |
| `describes_capability` | boolean | R | `true` · `false` | error |
| `area` | string | C | one of the 12 area names in [`source-of-truth.md`](source-of-truth.md) | error if required and absent |
| `maturity` | string | C | `available-verified` · `available-with-limits` · `preview` · `experimental` · `planned` · `deprecated` | error |
| `platforms` | list of object | C | see [`platforms[]`](#platforms) | error |
| `last_verified` | object | C | see [`last_verified`](#last_verified) | error |
| `claims` | list of object | C | see [`claims[]`](#claims) | error |
| `limitations` | string | C | non-empty; a link or an in-page anchor | error |
| `disclosure_levels` | list of integer, non-empty | R | subset of `[1,2,3,4]`, ascending, no duplicates | error |
| `deeper` | string | C | a link in the canonical-link form | error |
| `capability_ids` | list of string | O | **reserved** — pending AAASM-5531. Any value permitted; not validated in v1 | none |

### `owner` surfaces

`owner` names the layer that *owns the content*, not the repo the file sits in — a
Docs Hub page summarising a Core fact is owned by Core. The surface must be one of:

`horonomy.dev` · `official-website` · `docs` · `agent-assembly` · `python-sdk` ·
`node-sdk` · `go-sdk` · `arena` · `examples` · `cloud` · `agent-assembly-enterprise`

The layer prefix must be the one `content-ownership.md`'s layer table assigns to that
surface — for example `L2:docs`, `L3:agent-assembly`, `L1:official-website`. A
mismatched pair is an error.

### `platforms[]`

Distribution in this product is **per channel and per platform**: a capability can
ship on one channel and not another. A single "released" boolean is therefore not
expressible, and is not offered. Each row is one (channel, platform) pair.

| Key | Type | Req | Allowed values |
|---|---|---|---|
| `channel` | string | R | `github-release` · `homebrew` · `ghcr` · `install-sh` · `crates-io` |
| `platform` | string | R | `linux-x86_64` · `linux-aarch64` · `macos` · `windows` |
| `status` | string | R | `available-verified` · `available-with-limits` · `unsupported` |
| `evidence` | string | C | non-empty; required when `status` is not `unsupported` |

- Duplicate (`channel`, `platform`) pairs are an error.
- A pair that is **absent** asserts nothing, and asserting nothing about a channel a
  page's capability plausibly ships on is the gap this field exists to close. A page
  with `describes_capability: true` must therefore enumerate a row for **every**
  channel in the enum, using `unsupported` where it does not ship. Partial
  enumeration is an error.
- `unsupported` requires no `evidence` string because ADR 0033 §5.3's matrix row is
  its evidence, per §6.

### `last_verified`

| Key | Type | Req | Allowed values |
|---|---|---|---|
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
|---|---|
| `date` more than 180 days old | **error** — evidence is stale |
| `date` more than 90 days old | **warning** |
| `version` is not the current release in `compatibility.toml` | **warning** |
| `date` in the future | **error** |

### `claims[]`

Zero or more. Each entry:

| Key | Type | Req | Allowed values |
|---|---|---|---|
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
|---|---|---|
| 1 | `describes_capability: true` ⇒ `area`, `maturity`, `platforms`, `last_verified` and `claims` all present | error |
| 2 | `describes_capability: false` ⇒ `area`, `maturity`, `platforms`, `last_verified`, `claims`, `limitations` all **absent** | error |
| 3 | `maturity: available-with-limits` **or** `deprecated` ⇒ `limitations` present and non-empty | error |
| 4 | `maturity: planned` ⇒ `platforms` is exactly `[]`, and `claims` contains no term other than `Planned` | error |
| 5 | `maturity: available-verified` ⇒ every `platforms[]` row has `status` ∈ {`available-verified`, `unsupported`} — no row may be `available-with-limits` | error |
| 6 | `maturity` may never be `unsupported` or `unmeasured` | error |
| 7 | `platforms[].status` may never be `preview`, `experimental`, `planned` or `deprecated` | error |
| 8 | `claims[].term` may never be a value outside §6's eleven | error |
| 9 | `owner` is not `L2:docs` ⇒ `canonical_source` must be a link, not `self` | error |
| 10 | `canonical_source` other than `self` must match the canonical-link form: repo-relative, `https://github.com/<org>/<repo>/blob/HEAD/<path>`, or `https://docs.agent-assembly.com/<path>`. A branch-name blob URL is rejected | error |
| 11 | `max(disclosure_levels) < 4` ⇒ `deeper` present | error |
| 12 | `disclosure_levels` must include every level [required for the page's `page_type`](#which-levels-a-page-must-carry) | error |
| 13 | The page's `area` is `🗺️ Planned` in the status map ⇒ `maturity` ∈ {`planned`, `preview`, `experimental`} | error |
| 14 | An unbounded claim verb appears in the body ⇒ `describes_capability: true`, `claims` non-empty, and `limitations` present | error |

### Rule 14 — the unbounded claim verbs

Rule 14 is the mechanical form of *"public pages cannot omit status and limitations
when the claim depends on them"*. [Product promise](product-promise.md) already
instructs authors to pick a §6 term for every verb; rule 14 restates that requirement
from the metadata side, so a page cannot satisfy it by wording alone.

The closed list, matched case-insensitively on word boundaries, **as these literal
forms only** — no inflection expansion:

`protects` · `enforces` · `prevents` · `guarantees`

Occurrences **inside fenced code blocks and inline code are exempt** — otherwise this
very page could not name the list.

> **The list is deliberately high-precision, and it is a floor rather than a ceiling.**
> The obvious longer list — adding `blocks`, `stops`, `catches`, `secures`, `ensures`
> and the bare infinitives — was tested against this page and rejected: `blocks` alone
> matches *"code blocks"*, *"fenced blocks"* and *"E-blocks"* four times here, none of
> them a product claim. A gate that fires on a common noun gets switched off, and a
> gate that is off catches nothing. Third-person singular is the form an actual
> capability claim takes (`Agent Assembly protects …`), so that is what is matched.
>
> False negatives are therefore expected and accepted. Rule 14 does not replace the
> editorial rule in [Product promise](product-promise.md) — *if the sentence works
> with an undifferentiated verb, it is not specific enough to publish* — it only makes
> the most common case unmissable.

A page that uses one of these verbs in prose and declares `describes_capability:
false` has mis-declared its type, and that is an error rather than a warning: it is
the exact combination that lets an unevidenced claim through unchecked.

## Page templates

Five templates, one per `page_type`. They are the required *skeleton*; a page may add
sections freely. Copy the metadata block and the headings, then write.

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
area: Core
maturity: available-with-limits
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
<!-- BEGIN AA-PAGE-META ... page_type: guide, disclosure_levels: [1, 3] ... -->

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
<!-- BEGIN AA-PAGE-META ... page_type: reference, disclosure_levels: [3, 4] ... -->

# <Subject> reference

<Who this is for and what it covers.>

## Scope

<What is in this reference and what is deliberately not.>

## <Reference body>

<Level 3 and level 4. No length bound.>
```

### `architecture` — how something is built and why

```text
<!-- BEGIN AA-PAGE-META ... page_type: architecture, disclosure_levels: [3, 4] ... -->

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

```text
<!-- BEGIN AA-PAGE-META ... page_type: adr, disclosure_levels: [4] ... -->

# ADR NNNN: <Title>

## Status

## Context

## Decision

## Consequences

## Alternatives Considered
```

### Template changelog

| `schema_version` | Date | Change | Migration |
|---|---|---|---|
| 1 | 2026-08-06 | Initial definition. | — |

## What this page hands off

| To | What |
|---|---|
| **AAASM-5601** | Implement the validator: the parsing contract, the field reference, the cross-field rules and the freshness thresholds are intended to be sufficient with no further decisions. If a rule needs judgement to implement, that is a defect in this page — report it rather than choosing. |
| **AAASM-5610** | Apply metadata blocks to existing hub content. This page carries its own block as the reference instance; the rest of the hub does not have one yet. |
| **AAASM-5621** | Precedence between the two governing vocabularies, waivers, and cross-repository adoption. The `planned` overlap is scoped here, not settled. |
| **AAASM-5531** | The capability/evidence manifest. When it lands, `capability_ids` becomes validated and required, at `schema_version: 2`. |

---

*Last reviewed: 2026-08-06 — AI Agent Assembly Team*
