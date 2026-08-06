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

**2. Decide it.** Before the action takes effect, the control plane answers against
your policy, your team budgets and your approval rules. The answer is one of: allow
it, refuse it, hold it for a person, or forward it with recognised credentials
removed. Budget exhaustion, a suspended agent and an anomaly detection each resolve
to a refusal through the same path.

**3. Show it.** The decision is written to a hash-chained audit log that you can
verify yourself with `aasm audit verify-chain` — that command ships in the
open-source build. Where nothing inspected an action, the record reports it as
**Unmeasured** rather than as clean.

> **Who actually refuses.** The control plane decides but holds no traffic; a refusal
> takes effect through the component in front of the action. Today that is the proxy,
> which refuses before dialling upstream, or an SDK shim that honours the answer. This
> distinction is not pedantry — it is why "route it" is step one rather than a
> footnote.

### Level 3 — for an evaluator

Agent Assembly is a decision point you place in front of an AI agent's actions,
plus the evidence trail that shows what it decided.

**What it decides.** Which tools an agent may call, which network destinations it may
reach, how much it may spend, and which actions need a person's sign-off first.
Policy is versioned YAML/JSON you review through normal Git workflows.

**Where the decision is applied.** Three places, with different authority:

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
  **Detected**, not *Denied before execution*.

**What is on by default, and what is not.** This is the question that most changes an
evaluation:

| | Default posture |
|---|---|
| Approval holds | **On.** The gateway blocks awaiting the decision, and a timeout resolves to a refusal — fail-closed. Reachable in the open-source install. |
| Proxy inspection | **Narrow.** `llm_only` defaults to on, which TLS-intercepts three built-in LLM hosts. Any other host is tunnelled without payload inspection: the *connection* is Observed, the *payload* is Unmeasured. |
| Egress allow/deny lists | **Empty.** You configure them. The one always-on egress control is an SSRF guard that refuses IP-literal targets in loopback, private, link-local and cloud-metadata ranges. |
| Credential handling | **Redact and forward.** Blocking on a detected credential is opt-in. Model *responses* are not scanned. |
| SDK enforcement | **Off in the default mode.** A policy refusal blocks a wrapped tool only in the check-capable mode; asking for enforcement without it is refused loudly at init rather than silently allowed. |
| eBPF | **Off unless deployed.** Linux only, needs a privileged loader daemon, and its syscall guard needs an explicit opt-in on top of that. |
| Audit | **On.** Hash-chained JSONL, verifiable. |

**What it does not do.** It does not govern an agent you did not route. It does not
inspect payloads to hosts it is not intercepting. It does not keep a credential out of
the agent's own process — what it does is scan outbound requests on the inspected
hosts and remove recognised credentials before forwarding. Its audit chain is
tamper-*evident*, not signed: it is an unkeyed digest chain over the JSONL sink, so
anyone able to rewrite that file can recompute it, the database mirror carries no
chain, and a dropped entry fails verification the same way tampering does. On Windows
there is no local mediation at all.

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
| Gateway `check_action` | **Evaluated**; reaches *Denied before execution* only through a caller that blocks on the answer |
| Runtime policy checkpoint | **Evaluated**; *Denied before execution* only if the SDK shim honours the answer |
| Runtime scanner | **Redacted** — it runs after the action and returns counters, not a verdict |
| SDK client | **Evaluated** (advisory) |
| eBPF TLS / file / exec probes | **Observed** / **Detected** |
| eBPF syscall guard | **Detected**, plus asynchronous process termination |
| WASM sandbox | **Denied before execution**, for tools handed to it |

Send the reader to ADR 0033 §5.3 for the per-platform matrix and §6 for the vocabulary
itself. Do not restate either here; both are snapshots of a specific release and are
maintained where they live.

## Approved plain-language wording

ADR 0033 §6's terms are precise but they are engineering vocabulary. Public copy
needs plain-language equivalents that mean the same thing to a PM, an SRE and a
security reviewer. These are the approved renderings. Use the plain form in body
copy; keep the §6 term available wherever a reader might need to verify the claim.

| Concept | §6 term(s) | Approved plain-language wording | Must not shorten to |
|---|---|---|---|
| **Governed path** (managed path) | — (a scope, not a verdict) | "the paths you route through Agent Assembly"; "an agent you launched under Agent Assembly"; "traffic you send through the proxy" | "your agents"; "your fleet"; "your environment" — all three quantify over things you did not route |
| **Pre-execution** | Denied before execution | "before the action runs"; "before the request leaves the machine"; "before the tool body executes" | "in real time"; "instantly"; "at runtime" — these describe *speed*, not *ordering*, and the ordering is the whole claim |
| **Evidence** | Observed | "a hash-chained audit record you can verify yourself"; "tamper-evident" | "immutable"; "tamper-proof"; "signed" — the chain is an unkeyed digest, and retention pruning deletes rows |
| **Host controls** | Observed / Detected (Linux); Unsupported (Windows) | "operating-system-level controls, where the platform has them"; on Linux, "kernel probes that report activity"; the opt-in guard "terminates a confined process after the fact" | "kernel-level enforcement"; "OS-level protection"; anything implying the same mechanism exists on macOS or Windows |
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

---

*Last reviewed: 2026-08-06 — AI Agent Assembly Team*
