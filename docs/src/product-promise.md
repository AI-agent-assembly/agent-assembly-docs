# Product promise & message hierarchy

This page is for anyone writing public copy about AI Agent Assembly — the product
website, this hub, a README, a conference abstract, a sales deck. It exists because
the product's honest value is narrower than its architecture diagram suggests, and
narrower still than the words the category usually reaches for. A reader who
discovers an overstated claim *after* provisioning is a worse outcome than one who
reads an accurate limit up front.

It is also for evaluators. Levels 1 to 3 below are the fastest accurate account of
what the product does, what is on by default, and what it leaves uncovered.

## What governs this page

This brief is downstream of two merged artifacts, and it does not add claims to
them:

| Source | What it supplies | Where |
|---|---|---|
| **ADR 0033 — Canonical Governance & Enforcement Architecture** | The architecture, the platform matrix, and §6's **claim vocabulary**. Every clause of the promise below is expressed in one of §6's terms. | [ADR 0033](https://docs.agent-assembly.com/core/latest/adr/0033-canonical-governance-and-enforcement-architecture.html) in the core docs |
| **AAASM-5528 — public claim inventory** | 69 audited rows of what may and may not be said, each tied to a re-verified evidence block (`E1`–`E7`). | [`verification-reports/AAASM-5528-public-claim-inventory.md`](https://github.com/ai-agent-assembly/agent-assembly/blob/main/verification-reports/AAASM-5528-public-claim-inventory.md) |

Ticket references on this page are plain text, not links: the tracker is not publicly
readable, so a link would only take a reader to a login wall — and a link checker
scores that wall as reachable, which makes the reference look verified when it is not.

Two further sources are chartered but not yet available, so nothing here depends on
them: the current-state capability matrix (AAASM-5527, in progress) and the
machine-readable capability/evidence manifest (AAASM-5531, not started). Statements
that would need either of those to be verified are collected under
[Provisional](#provisional) rather than asserted.

> **Precedence.** Where this hub still carries the superseded three-layer or
> "IronClaw five-layer" framing — [Security model](security-model.md) and
> [Glossary](glossary.md) both do, at the time of writing — **ADR 0033 wins**. Those
> pages are being migrated under AAASM-5586 and AAASM-5609, and ADR 0033 records the
> gap as a tracked, accepted window. Do not resolve a conflict in the superseded
> model's favour. Note the rule is one-directional as written — a reader who arrives
> at those pages first never sees it — so the migration tickets, not this note, are
> the actual fix.

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
> call can be refused, or blocked pending a decision, instead of discovered
> afterwards.**

### Headline and subheadline

For a hero or a first screen, the promise renders as:

**Headline**

> Decide what an AI agent may do — before it does it.

**Subheadline**

> Agent Assembly evaluates the actions you route through it against your policy,
> refuses or blocks the ones your policy disallows, and records the decision. An
> action you have not routed through it is not inspected — and the record says so.

**These two are not severable.** The headline is bounded only by the subheadline;
published alone it reads as a claim over all agent behaviour. That is the `absolute`
claim class, which accounts for 37 of the 69 audited rows in the AAASM-5528
inventory — by some distance the most common defect in this product's published copy.
The rule for downstream pages is: *the boundary clause appears on the same screen as
the headline, above the fold, not in a footnote.*

Note what the headline deliberately does **not** say: *"your AI agents"*. The
possessive quantifies over agents you never routed, which is the wording the table
below bans, and it is the same correction AAASM-5528 applied to "three boundaries for
every agent" → "for a **governed** agent". The indefinite article costs nothing and
survives the places non-severability cannot reach — a `<title>`, an `og:title`, a
search snippet, a chat unfurl, a slide. **Metadata surfaces must carry the bounded
form**, because there is no room beside them for a subheadline.

### Clause map

Each clause is expressible in ADR 0033 §6's vocabulary. If a rewrite of the promise
cannot be mapped this way, it is not a rendering of the promise — it is a new claim,
and it needs its own evidence.

| Clause | ADR 0033 §6 term | Why the term fits |
|---|---|---|
| "decides whether an … action is allowed" | **Evaluated** | The control plane produces a decision for the action; a decision record exists. |
| "before that action runs" | **Denied before execution** | Reached where the refusing component sits before the effect — today the proxy, pre-dial, or an SDK shim that honours the answer. |
| "on the paths you route through it" | **Unmeasured** (by contrast) | Names the boundary. Anything off the path is Unmeasured; the clause exists so the promise does not quantify over agent behaviour. |
| "records what was decided" | **Observed** | An event attributed to the action. §6 requires this to be *durable*; emission is best-effort under backpressure, so the clause is bounded by the note at Level 2 step 3 and by its own Provisional row — do not publish it unqualified. |
| "refused" | **Denied before execution** | As above. |
| "blocked pending a decision" | **Approval required** | The action is held and a pending approval record exists. **§6's term does not assert that a person can act on it** — see the [Provisional](#provisional) row. An earlier draft of this promise said "held for a person"; the plain-language rendering silently added a human who, today, has no shipped surface to answer on. |
| "instead of discovered afterwards" | — | A contrast with after-the-fact observability, not a capability claim. Carries no evidence burden. |

## Progressive disclosure — four levels

A reader should be able to stop at any level and hold a correct picture. Each level
adds precision; none of them retracts what the level above said.

### Level 1 — one sentence

The promise, verbatim. Nothing shorter is approved, because everything shorter drops
the boundary clause.

### Level 2 — three steps

**1. Route it.** An agent is on a *governed path* when you have put it there:
launched through `aasm run`, or started by a developer-tool integration that writes
the proxy settings into the tool's own configuration, or calling a policy checkpoint
from an SDK. Routing is a thing you do, per agent and per launch. An agent you did
not route is not on the path.

Not every tool has a managed launch to offer. One shipped adapter returns a launch
failure rather than a governed command, and another is hard-capped at observation —
for those, no proxy environment is injected and there is no data-path mediation to
route into. "Supported tool" and "governable tool" are different lists; check the
per-adapter boundaries before implying the second.

**2. Decide it.** Before the action takes effect, something on the path decides
whether it may proceed — and *which* thing depends on the path. The control plane
answers policy, budget and approval questions: allow, refuse, or block pending an
approval. Budget exhaustion, a suspended agent and an anomaly detection each resolve
to a refusal through that same path.

But the control plane is not always the decider, and copy that says it is will be
wrong more often than right. The proxy refuses on its **own local configuration** for
CONNECT-time egress and for LLM-provider hosts — those code paths contain no gateway
call at all. A gateway `Deny` stops bytes in exactly one place: an MCP tool-call
envelope on a non-LLM intercepted host with a gateway endpoint configured — and since
`llm_only` defaults to on, those hosts are not intercepted unless an operator says so.
Attribute the refusal to whichever component actually made it.

Redaction is a separate stage, not a fourth branch of the same answer: it is the
proxy's outbound credential scan, applied *after* the connection decision, and it
defaults to redact-and-forward. Do not present allow/refuse/hold/redact as one
four-way per-action verdict — the API's five-way `RuntimeVerdict` is a frozen
vocabulary whose derivation is unimplemented and which is surfaced as `null`, and
presenting it as a live outcome is a forbidden design.

**3. Show it.** Decisions are written to a hash-chained audit log that you can verify
yourself with `aasm audit verify-chain` — that command ships in the open-source build.
Where nothing inspected an action, the rule is that the record reports it as
**Unmeasured** rather than as clean, because an uninspected action must never be
reported as allowed.

> **Emission is best-effort — say so in the same sentence.** The gateway advances the
> chain head *before* attempting the send, and on a full channel it logs a warning,
> increments a drop counter and returns the RPC anyway; several sibling emit sites
> discard the error with no counter at all. So a decision can be made and its record
> lost, and a dropped entry is indistinguishable from a deleted one. Three bounds
> belong together wherever this is claimed: **which** actions are decided (the
> governed path), **whether the record survives** (best-effort), and **what
> verification proves** (chain integrity, not completeness). The boundary clause in
> the promise covers only the first. This is the same rule-plus-open-defect shape as
> the note above, and the hub's own security model already states that absence of an
> entry is not proof of absence.

> **State this as a rule, not as finished behaviour.** ADR 0033 §4 mandates it, and
> the transparent-tunnel path implements it — it persists "forwarded, and nothing
> looked at it". But §2 records a live defect on the same path: the CONNECT-level
> decision event still emits an *allow* for a connection the proxy is about to tunnel
> uninspected. Until that is fixed, do not write copy that promises the property
> holds everywhere today.

> **Why "route it" is step one.** The control plane holds no traffic, so a decision
> only stops something when a component in front of the action blocks on it. That set
> has exactly two members today — the proxy's MCP path, and an SDK shim that honours
> the answer — not "the proxy" generally. Routing is what puts an action in front of
> one of them.

### Level 3 — for an evaluator

Agent Assembly is a decision point you place in front of an AI agent's actions,
plus the evidence trail that shows what it decided.

**What it decides.** Which tools an agent may call, which network destinations it may
reach, how much it may spend, and which actions are blocked pending an approval.
Policy is versioned YAML/JSON you review through normal Git workflows.

**Where the decision is applied.** In several places, with genuinely different
authority. Resist the urge to number them: they are not an ordered chain, one does
not cover for another, and an absent one is a reportable state rather than a silent
hand-off to the next. That inference — "the SDK did not see it, so the kernel did" —
is the specific error the current architecture exists to stop.

- The **sidecar proxy** is the strongest one. It refuses at CONNECT time, re-checks
  the host inside the tunnel, blocks or redacts recognised credentials, and
  adjudicates MCP tool calls — each of those returns before it dials upstream. This
  is genuine pre-execution refusal, out of the agent's process.
- The **SDK** wraps your framework's tool seam and raises before the wrapped tool body
  runs. It is deliberately **advisory**: it is a defence-in-depth posture, not the
  authoritative gate, and an agent that does not call it is simply not asking.
- **Operating-system-level controls** are platform-specific and, where they exist
  today, they mostly *observe*. On Linux, eBPF probes report TLS plaintext, process
  execution and file I/O; they do not participate in any allow/deny decision. There is
  one opt-in syscall guard that terminates a confined process, and it does so
  asynchronously — the offending syscall runs once before the process dies, so it is
  **Detected**, not *Denied before execution*. **macOS has no equivalent adapter, and
  is simultaneously the only platform where the host-enforcement rung is reachable** —
  through an opt-in, authorized managed-settings write. Both halves are required;
  writing only the first is the understatement this page bans two sections down.
  Windows has neither.

**What is on by default, and what is not.** This is the question that most changes an
evaluation:

| | Default posture |
|---|---|
| Approval holds | **Off until a policy asks for one, and unresolvable when it does.** A hold is produced only by an explicit `requires_approval_if` expression; three of the eight shipped policy examples declare one, and `low-risk.yaml` says "No approval gates." When a hold does fire the gateway blocks awaiting the decision and a timeout resolves to a refusal — genuinely fail-closed — but **no shipped operator surface can answer it**, so in practice it blocks and then auto-refuses. See the [Provisional](#provisional) row before writing anything about human review. |
| Proxy inspection | **Narrow.** `llm_only` defaults to on, which TLS-intercepts three built-in LLM hosts. Any other host is tunnelled without payload inspection: the *connection* is Observed, the *payload* is Unmeasured. |
| Egress allow/deny lists | **Empty.** You configure them. The one always-on egress control is the SSRF guard, and it is stronger than a literal check: it refuses IP-literal CONNECT targets **and re-checks every resolved address before dialling**, so a hostname that resolves into private space is refused too — that is DNS-rebinding cover. Its blocked set spans loopback, private, link-local, broadcast, CGNAT, `0.0.0.0/8`, and on IPv6 loopback, ULA, link-local, NAT64, 6to4 and IPv4-compatible. **No environment variable can relax it** — the config field is hardcoded false with the comment that production binaries can never turn it off. |
| Credential handling | **Redact and forward.** Blocking on a detected credential is opt-in. Model *responses* are not scanned. |
| SDK enforcement | **Off in the default mode.** A policy refusal blocks a wrapped tool only in the check-capable mode; asking for enforcement without it is refused loudly at init rather than silently allowed. |
| eBPF | **Off unless deployed.** Linux only, needs a privileged loader daemon, and its syscall guard needs an explicit opt-in on top of that. |
| Launching an ungoverned session | **Refused.** `aasm run` will not start a tool when no effective policy resolves, and it will not start one whose policy parses but declares no rule — *"an absent policy is not permission"*, *"an empty policy is unconfigured, not allow-all"*. Both refuse before anything launches. This is the strongest default-on behaviour in the product and the easiest to leave out of a comparison. |
| The policy engine's fallthrough | **Allow.** Once a policy is in force, an action matching no network, tool, capability or approval rule is allowed. Default-open *within* a policy, default-refuse on *having* one — state both or the pair is misleading. |
| Budget caps | **None unless declared.** Limit resolution returns nothing when neither a per-agent nor a global limit is configured, so an undeclared budget means uncapped spend. Most shipped policy examples *do* declare daily and monthly caps, so an evaluator who starts from one gets a cap — but a hand-written policy that omits the block has none. |
| Audit | **On, best-effort.** Hash-chained JSONL, verifiable. Writing is not guaranteed: the chain head advances before the send and a full channel drops the entry, so the log is a record of what got through, not a ledger of what happened. |

**What it does not do.** It does not govern an agent you did not route. It does not
inspect payloads to hosts it is not intercepting. It does not keep a credential out of
the agent's own process — what it does is scan outbound requests on the inspected
hosts and remove recognised credentials before forwarding. Its audit chain is
tamper-*evident*, not signed: it is an unkeyed digest chain over the JSONL sink, so
anyone able to rewrite that file can recompute it, the database mirror carries no
chain, and a dropped entry fails verification the same way tampering does. Nor does a
passing verification mean the log is whole — it checks the links between the entries
that are there, so a deleted-and-recreated log verifies clean. On Windows there is no
local mediation at all.

### Level 4 — technical handoff

At this depth, stop paraphrasing and hand the reader the canonical sources. ADR 0033
describes the architecture as six *roles* — a control plane, managed execution
checkpoints, protocol/transport mediation, platform-specific host-level adapters, a
credential/capability boundary, and an evidence pipeline. A deployment instantiates
some subset of them, an absent role is a reportable state rather than a silent
fall-through to another role, and each role's authority is its own.

| Mechanism | Highest ADR 0033 §6 term it reaches today |
|---|---|
| Proxy — CONNECT, in-tunnel host re-check, credential block, MCP adjudication | **Denied before execution**, for traffic routed through it and intercepted |
| Gateway `check_action` | **Evaluated**; reaches *Denied before execution* only through a caller that blocks on the answer, and today that set is exactly two — the MCP path, plus an SDK shim that honours the answer |
| Runtime policy checkpoint | **Evaluated**; *Denied before execution* only if the SDK shim honours the answer |
| Runtime scanner | **Redacted** — it runs after the action and returns counters, not a verdict |
| SDK client | **Evaluated** (advisory) |
| eBPF TLS / file / exec probes | **Observed** / **Detected** |
| eBPF syscall guard | **Detected**, plus asynchronous process termination |
| WASM sandbox | **Denied before execution**, for tools handed to it — but it is not on an agent's normal tool-call path, so do not cite it as a general guarantee |
| Developer-tool config writes (`aa-devtool-*`) | **Not a data-path claim at all.** Writing a tool's own settings file is tool-governance: it takes effect only if the tool honours those keys, and for the macOS managed-settings path whether it does is unmeasured. Any data-path prevention these adapters deliver is the proxy's, borrowed through the launch environment they inject. This row is the bound on the mechanism Level 2 step 1 introduces — an integration writing proxy settings is not itself an enforcement point. |

Send the reader to ADR 0033 §5.3 for the per-platform matrix and §6 for the vocabulary
itself. Do not restate either here; both are snapshots of a specific release and are
maintained where they live. One thing §5.3 says that a summariser reliably drops: its
macOS row ends *"Do not read this as 'no host enforcement on macOS'."* Carry that
sentence with the row, not just the row.

## Approved plain-language wording

ADR 0033 §6's terms are precise but they are engineering vocabulary. Public copy
needs plain-language equivalents that mean the same thing to a PM, an SRE and a
security reviewer. These are the approved renderings. Use the plain form in body
copy; keep the §6 term available wherever a reader might need to verify the claim.

| Concept | §6 term(s) | Approved plain-language wording | Must not shorten to |
|---|---|---|---|
| **Governed path** (managed path) | — (a scope, not a verdict) | "the paths you route through Agent Assembly"; "an agent you launched under Agent Assembly"; "traffic you send through the proxy" | "your agents"; "your fleet"; "your environment" — all three quantify over things you did not route |
| **Pre-execution** | Denied before execution | "before the action runs"; "before the request leaves the machine"; "before the tool body executes" | "in real time"; "instantly"; "at runtime" — these describe *speed*, not *ordering*, and the ordering is the whole claim |
| **Evidence** | Observed | "a hash-chained audit record you can verify yourself"; "tamper-evident" | "immutable"; "tamper-proof"; "signed" — the chain is an unkeyed digest, and retention pruning deletes rows. Also avoid "verified" as a synonym for "complete": verification checks the links between the entries present, so an empty log — or one deleted and recreated — passes and exits 0 |
| **Host controls** | Observed / Detected (Linux); Unsupported (Windows); macOS is its own case — see below | "operating-system-level controls, where the platform has them"; on Linux, "kernel probes that report activity"; the opt-in guard "terminates a confined process after the fact" | "kernel-level enforcement"; "OS-level protection"; anything implying the Linux mechanism exists on macOS or Windows — **and equally**, any blanket "no host enforcement on macOS" |
| **Managed action** | Evaluated | "an action presented for a decision before it takes effect"; "an action that reached a checkpoint" | "any action"; "each action an agent takes" — the second silently re-adds the quantifier the first removed |
| **Planned** | Planned | "planned — decided, not built yet", with the ticket reference | "coming soon"; "available in Enterprise"; a roadmap item written in the present tense |
| **Not inspected** | Unmeasured | "nothing inspected this action, so nothing is known about it" | "allowed"; "clean"; "no issues found" — absence of a finding is a fact about the observer, not the agent |

Two subtleties worth carrying into copy, because both have already produced defects
in this repository:

- **Unmeasured is scoped to the action, not the connection.** A host the proxy does
  not intercept is still adjudicated at CONNECT by local egress policy, and that
  connection *is* recorded. The honest phrasing is "the connection was observed, the
  payload was not inspected" — not "nothing was observed".
- **An empty audit log is evidence about the observer.** It is not evidence that an
  agent did nothing. Never present a quiet log as a result.
- **macOS needs its own sentence, in both directions.** It has no kernel-level
  interception adapter, and saying so is required. But it is also the *only* platform
  on which the host-enforcement rung is reachable today, through an opt-in, authorized
  managed-settings write. Copy that flattens this into "no host enforcement on macOS"
  is an understatement defect, and it has been fixed once already — do not
  reintroduce it. State the route; leave the outcome under
  [Provisional](#provisional).

## Rejected wording

Each row was removed from published copy, or considered and refused, for the reason
given. The list is short on purpose: it names the *patterns* that keep recurring,
not every sentence ever corrected. The audited per-file record is the AAASM-5528
inventory.

<!-- claim-gate:ignore-start
     AAASM-5582 / AAASM-5536: the block below necessarily quotes the phrases the
     banned-absolutes gate looks for — a rejected-wording list cannot name its
     rejections otherwise. Skip this region rather than adding per-phrase
     exceptions, which would also silence the phrases in ordinary prose. -->

| Rejected | Why | Inventory rows |
|---|---|---|
| "catches everything, including bypass attempts" | The mechanism it described (eBPF) observes. It participates in no allow/deny decision, covers only OpenSSL-linked processes, and its file-I/O probes are x86_64-only. | W1 · W11 · A7 · A17 · A24 · A27 |
| "an action has nowhere to hide" | Asserts the union of the mechanisms is closed. It is not: an unmanaged launch, unrouted traffic, an unhooked TLS stack and an unsupported platform each leave an action outside the boundary. | A8 · A13 |
| "a security checkpoint an AI agent cannot walk around" | Walking around it is a *measured* bypass — start the agent outside `aasm run` and no proxy environment is injected. | A2 |
| "no code changes" | True of the agent's source, false as a prerequisite statement: the tool must be launched so its traffic reaches the proxy and the CA is trusted. Say what is required, not what is not. | D1 · D5 · D8 · A6 · A23 · A26 |
| "immutable audit log" / "signed with HMAC" | The chain is an unkeyed digest over the JSONL sink; retention pruning deletes rows; the database mirror carries no chain. It is verifiable and that is worth saying — but it is tamper-evident, not immutable and not signed. | D9 · D10 |
| "every action" / "every tool call" / "before every agent action" | Quantifies over agent behaviour rather than over what reached a checkpoint. The correct scope is the governed path. | A1 · A3 · A4 · A21 · A37 · D2 · D7 |
| "your whole fleet" / "full fleet" | Coverage is a per-agent, per-launch, per-platform fact. There is no fleet-wide switch. | D1 |
| "universal" / "comprehensive" / "complete" coverage | Each asserts a property no component here provides, and each is unfalsifiable in copy. | forbidden design 7 |
| "cannot be bypassed" / "unbypassable" | Bypass paths are enumerated and published. Claiming otherwise contradicts our own documentation. | A20 · forbidden design 7 |
| "secrets are injected at runtime and never enter the model context" | Advertises a capability a released build cannot reach. What ships is outbound scanning with redaction before forwarding. | W15 · W16 · W17 |
| "kernel-level enforcement" | Attributes the guarantee to the wrong component. The kernel mechanism reports; the proxy refuses. | D11 · W7 · A12 |
| "the SDK denies the action before it runs" | The SDK evaluates and is advisory. Refusal that holds is the proxy's, out of process. | W18 · A35 · D13 |
| "protects" / "enforces" / "catches", used without a timing and a posture | ADR 0033 §6 forbids the undifferentiated verb. Each of these can mean observed, detected, evaluated or refused, and the reader cannot tell which. | A36 · §6 |
| "three layers: SDK, proxy, eBPF" as *the* architecture | A superseded model. An ordered pipeline whose members cover for each other has no way to express an absent member, which is the inference this whole programme exists to stop. | forbidden design 1 |
| A hero that leads with "a governance layer for AI agents" | Accurate but not a user outcome — it names the category, not what changes for the reader. Correct at company altitude; too abstract for the product's own first screen. | — (new here) |

<!-- claim-gate:ignore-end -->

### On the constellation identity

AAASM-4084 introduces
Argo Navis as a product alias and visual identity. It is a naming and design layer,
and it composes with this brief in one direction only: **the metaphor may decorate
the promise, it may not stand in for it.** A page whose first screen explains a
constellation before it explains what happens to an agent's action has not made the
promise; it has deferred it. Where the two compete for the same space, the promise
wins.

### Altitude — how this relates to the company-level description

Horonomy describes Agent Assembly at company altitude as *a governance layer for AI
agents — permissions, approval checkpoints, and evidence*, which *decides which tools,
domains, and budgets an agent may use, holds risky actions for human review, and
records what happened*.

That is correct and this brief does not contradict it. The promise on this page sits
one layer below: it keeps the same three ideas — permissions, approval, evidence — and
adds the two things a product page must carry that a company page need not, namely
**when** the decision happens (before the action) and **where it applies** (the paths
you route through it). Do not "simplify" a product page back up to company altitude;
the boundary clause is what makes it a product claim rather than a category
description.

## Claim-to-evidence mapping

Every material statement above traces to a merged, re-verified source. `E1`–`E7` are
the evidence blocks in the AAASM-5528 inventory; `§n` refers to ADR 0033.

| Statement | §6 term | Evidence |
|---|---|---|
| The decision happens before the action runs, where the refusing component sits in front of it | Denied before execution | §2 caller table; §6 mechanism table; `E7` |
| The control plane decides but holds no traffic | Evaluated | §2 |
| The proxy refuses before dialling upstream | Denied before execution | `E2` (CONNECT 403, in-tunnel host re-check, credential block, MCP adjudication) |
| The SDK is advisory | Evaluated | `E3`, `E7`; ADR 0002 |
| A policy refusal blocks a wrapped tool only in the check-capable SDK mode, and asking for enforcement without it is refused at init | Evaluated | Verified directly in the Node SDK's client construction and init guards, not from `E3`/`E7` — those establish that the wrapper raises before the tool body, which is a different question from whether the default transport can produce a refusal at all. Tracked as AAASM-4991 |
| A hold blocks the check and fails closed on timeout | Approval required | Gateway approval path: the check awaits a decision, and an elapsed timeout yields a `Deny` fallback. Both OSS gateway bootstraps wire the queue, so this is not a degraded-mode artefact |
| …but the hold has **no shipped operator-facing sender** | — (a gap, not a claim) | The gateway's queue is answerable only over the gRPC `ApprovalService`, and the only clients of it in the tree are two gateway test files. The CLI and dashboard POST to the HTTP API, whose process constructs its **own** in-memory queue and resolves against that one; there is no gRPC channel and no shared store between the two processes. Verified with a positive control — the equivalent `PolicyService` client appears in 20+ files including shipped runtime source and a bench |
| Budget exhaustion resolves to a refusal | Evaluated → Denied before execution | Atomic spend reservation inside the same decision path |
| `llm_only` defaults on; three built-in LLM hosts are intercepted | Unmeasured (for other payloads) | `E2` |
| Egress allow/deny lists are empty by default; the SSRF guard is not, filters post-resolution, and cannot be disabled by configuration | — | `E2` understates this one: it establishes the guard denies unconditionally ahead of both lists, but not the resolved-address re-check or the absence of an opt-out. Both read directly in the proxy's dial path and config defaults. Understating a shipped control is a defect in the same way overstating one is |
| Credential handling defaults to redact-and-forward | Redacted | `E4` |
| The audit chain is an unkeyed digest over the JSONL sink, verifiable in the open-source build | Observed | `E5` |
| Emission is best-effort: the chain head advances before the send, a full channel drops the entry and the call returns anyway, and sibling sites discard the error uncounted | Observed, bounded | Read directly in the gateway's audit-record path and its sibling emit sites — **not** `E5`, which covers the chain's cryptography, not whether an entry reaches it. Open as AAASM-5626 |
| `verify-chain` proves integrity, not completeness — an empty or deleted-and-recreated log verifies clean and exits 0 | Observed, bounded | The verifier's loop body never runs on zero entries and the terminal return is `is_valid: true`; the CLI maps that to `ExitCode::SUCCESS` |
| Kernel probes observe; the syscall guard is opt-in and terminates asynchronously | Observed / Detected | `E1`, §5.1 |
| Windows has no local mediation | Unsupported | §5.3 |
| An unrouted action is not inspected | Unmeasured | §4 |

## Provisional

Not asserted in public copy until the owning work lands. Each is here because it is
*plausible and unverified*, which is exactly the category that produces an
overstatement.

| Statement | Why it is provisional | Owner |
|---|---|---|
| **"A person can review and release a held action."** Do not write "held for human review", "approval workflow", "a reviewer approves it", or any hero copy implying a human is in the loop | The hold itself is real and fail-closed, but the gateway's approval queue and the queue the CLI/dashboard resolve against live in **different processes with nothing joining them**. Until a bridge ships, the truthful account is "blocked pending a decision, which today no operator surface can supply, so it refuses at timeout." | Product ticket being filed — reference it here once the key is issued |
| Any coverage figure — a percentage, a count of governed actions, a fleet-level number | There is no machine-readable manifest to compute it from, and self-reported layer availability is not evidence of coverage (§7) | AAASM-5531 |
| "Host enforcement on macOS" | ADR 0030's `HostEnforced` rung *is* reachable there — it is the only platform where it is — but it rests on reading back a managed-settings file, and whether the tool honours those keys at runtime is unmeasured. State the route, not the outcome. | AAASM-5526 |
| "eBPF is available to you" as a property of an installed release | The privileged loader daemon that owns every kernel operation is not part of the published release artifacts, and the probe crates build only on a nightly toolchain. Describe eBPF as a Linux mechanism the architecture supports, not as something a reader can switch on today. | AAASM-5526 |
| A named prevented-outcome demonstration ("we stopped X") | The parent Epic requires a proof that a denied side effect did not execute. Until that harness exists, describe the decision, not the averted consequence. | AAASM-5532, AAASM-5529 |
| Any SaaS availability, region, SLA or compliance commitment | Planned, not available. See [Source of truth & status](source-of-truth.md). | The Cloud programme — **not** AAASM-5579, which is this page's narrative Epic and owns no SaaS delivery. Route a question here to the maturity map, not to the website backlog |

## Using this on a page

For the homepage rewrite
(AAASM-5585) and the
Product / How It Works rewrite
(AAASM-5586), and for
any page that makes a product claim:

1. **Quote the promise, do not paraphrase it.** A paraphrase is a new claim. If the
   layout needs a shorter line, use the headline — and put the subheadline with it.
2. **Keep the boundary clause above the fold.** Not a footnote, not a tooltip, not a
   "learn more".
3. **Pick a §6 term for every verb.** If the sentence works with "protects",
   "enforces" or "catches", it is not yet specific enough to publish.
4. **Name the mechanism that delivers the guarantee.** The right guarantee attributed
   to the wrong component is its own defect class, and it is the one a technical
   evaluator notices first.
5. **State the default.** A capability that exists but is off is a different product
   from one that is on. The Level 3 table is the reference.
6. **Check the direction of the error both ways.** Understatement is also a defect —
   approval holds, pre-dial refusal, the SSRF guard and chain verification all ship,
   and a page that hedges them away is as wrong as one that overstates.

---

*Last reviewed: 2026-08-06 — AI Agent Assembly Team*
