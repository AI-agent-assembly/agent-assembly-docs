# Risk scenarios — the flagship story and three supporting threats

This page selects the four stories the product's public surfaces tell: one flagship
scenario for the homepage, and three supporting scenarios covering secret
exfiltration, a destructive production action, and runaway cost. It exists so that
the website, this hub and the demo assets tell the *same* four stories in the *same*
words, and so that each of those words can be traced to something the product
actually does.

It is narrative source material, not a product page. Downstream surfaces
(AAASM-5585, AAASM-5589) copy the wording in
[Approved wording for reuse](#approved-wording-for-reuse) verbatim rather than
paraphrasing it — a paraphrase is a new claim and carries its own evidence burden.

## What governs this page

This page adds no claims to its sources. Where it appears to, that is a defect in
this page.

| Source | What it supplies |
|---|---|
| **[Product promise & message hierarchy](product-promise.md)** (AAASM-5582) | The one approved promise, the boundary clause, the plain-language wording table, and the Provisional list. Every scenario below is a rendering of that promise applied to one threat. |
| **ADR 0033 §6 — claim vocabulary** | The eleven terms every "policy decision" and "evidence" field below is written in: Observed, Detected, Evaluated, Denied before execution, Redacted, Approval required, Degraded, Unmeasured, Experimental, Planned, Unsupported. |
| **AAASM-5527 — capability coverage matrix** (`verification-reports/AAASM-5527-capability-coverage-matrix.yaml` in the core repo) | 80 rows carrying `reachability`, `released_channels`, `released_platforms`, `default_state`, `failure_posture` and `known_bypasses`. Each scenario below names the row IDs it rests on. |

Ticket references are plain text, not links: the tracker is not publicly readable, so
a link would only reach a login wall — and a link checker scores that wall as
reachable, which makes the reference look verified when it is not.

> **The promise these scenarios render.** *Agent Assembly decides whether an AI
> agent's action is allowed before that action runs — on the paths you route through
> it — and records what was decided, so a risky call can be refused, or blocked
> pending a decision, instead of discovered afterwards.*
>
> The clause **"on the paths you route through it"** is load-bearing in every
> scenario below. None of these stories is a claim about an agent you did not route,
> a host you are not intercepting, or a platform without the component installed.

## How to read a scenario

Each scenario carries eight fields, plus a determination.

| Field | What it answers |
|---|---|
| **Threat source** | Who or what causes the action. Usually not malice — a plausible instruction, an injected one, or a loop. |
| **Requested action** | The concrete thing the agent tries to do. |
| **Existing-system gap** | Why the tools already in place do not stop it. |
| **Governed path** | What the operator did to put this action in front of a decision. Routing is a thing you do, per agent and per launch. |
| **Policy decision** | An ADR 0033 §6 term, plus **which component actually decided**. The right guarantee attributed to the wrong component is its own defect class. |
| **Prevented outcome** | The specific effect that did not occur — stated as an absence, not as an error. |
| **Evidence** | An ADR 0033 §6 term, plus the test or record that substantiates it. |
| **Known boundary** | Defaults, platforms, channels and bypasses. A capability that exists but is off by default is a different product from one that is on. |

**Determination** is one of:

- **Executable today** — the mechanism exists, a released binary can reach it, and a
  standing test on the core repo's default branch exercises it. The scenario's
  defaults and platform boundaries are still stated.
- **Executable, default-off** — as above, but nothing happens until an operator turns
  it on. A sentence that is true "once enabled" is false as written.
- **Illustrative / planned** — the story is useful for explaining the product's shape
  but does not correspond to a capability a reader can exercise. It must be labelled
  wherever it is used.

Every capability cited below was checked against four questions, each of which is
invisible to the one before it: is it worded without absolutes; does the guarantee
hold in code; is it on by default; and does the named mechanism exist at all *and can
a released binary reach it*. Distribution is per channel **and** per platform — the
core repo publishes through five channels, and absence from the release workflow
proves nothing about crates.io.

## Scenario status at a glance

| # | Scenario | Mechanism | §6 term reached | Determination | 5527 rows |
|---|---|---|---|---|---|
| **F** | **Flagship** — the upload that never happened | `aa-proxy` CONNECT-time egress refusal | **Denied before execution** | Executable, default-off (Linux; macOS crates.io only) | N1, N2, L1 |
| **S1** | Secret exfiltration | `aa-proxy` outbound credential scan on inspected LLM hosts | **Redacted** | Executable today (redact-and-forward is the default, not block) | C1, C6, N3 · C2 default-off · C3 **dead code** |
| **S2** | Destructive production action | Gateway adjudication of an MCP `tools/call` | **Denied before execution** | Executable, default-off — **Streamable HTTP only**; stdio and SSE absent | M1, M3 · M5/M6 absent |
| **S3** | Runaway cost | Gateway budget reservation | **Evaluated → Denied before execution** | Executable today, with a silent fail-open | *(no positive row — see the scenario)* · G9 |
| **S3b** | Unauthorized payment | — | — | **Illustrative** — no payment capability exists | — |

---

## Flagship — the upload that never happened

A coding agent tries to send the repository it is working on to an endpoint nobody
approved. The connection is refused before it is dialled, and the endpoint never
receives a byte.

This is the flagship because the denied side effect is *objectively testable in the
negative*: a socket either accepted a connection or it did not, and the check does
not depend on trusting anything inside the agent's process.

| Field | |
|---|---|
| **Threat source** | Not necessarily malice. A coding agent reads an issue, a README or a dependency's docs that contains an instruction to "back up the working tree" to a paste or file-sharing endpoint; or the agent picks a convenient endpoint itself to "share the diff". The agent is doing what it was told by content it was asked to read. |
| **Requested action** | An outbound HTTPS connection from the agent's process to a host outside the approved set, carrying the contents of the working tree. |
| **Existing-system gap** | The agent's process has ordinary network access, and nothing in the agent framework distinguishes "fetch the docs page I need" from "POST the repository somewhere". Code review is after the fact; egress happens at machine speed. Outbound logging tells you it happened — it does not stop it. |
| **Governed path** | The agent is started through a managed launch (`aasm run`), which writes the proxy settings and the CA into the child process's environment, so the tool's outbound connections are dialled through `aa-proxy` rather than directly (`aa-devtool-claude-code/src/lib.rs:356-383`). The operator has configured which hosts are approved. |
| **Policy decision** | **Denied before execution.** The proxy evaluates the CONNECT target and returns 403 before it dials upstream (`aa-proxy/src/proxy/mod.rs:934`, run at `:1308`). **The decider is the proxy's own local egress configuration, not the gateway** — this code path contains no gateway call. Copy that attributes this refusal to the policy engine is wrong. |
| **Prevented outcome** | No TCP connection to the destination is established, so no byte of the working tree leaves the machine by that route. |
| **Evidence** | **Observed** — the proxy records the refusal as a `Blocked` decision (`aa-proxy/src/proxy/mod.rs:969`, alongside the deny at `:934`). **Bounded twice, and both bounds are default-off or best-effort — see below.** Standing tests: `aa-integration-tests/tests/e2e_policy_proxy.rs`, `cli_proxy_remote_bind_refusal.rs`. |
| **Known boundary** | See below — this one has five parts and all five are load-bearing. |

**Known boundary, in full:**

- **The lists are empty by default.** `AA_PROXY_DENIED_HOSTS` and
  `AA_PROXY_NETWORK_ALLOWLIST` are both empty out of the box
  (`aa-proxy/src/config.rs:75-85`), and the row's `default_state` is *open*. This
  refusal exists **because the operator configured it**. Never tell this story as
  something that happens on first run.
- **The always-on egress control is a different one.** The SSRF guard (N2) is on by
  default, fails closed, cannot be relaxed by configuration, and re-checks every
  resolved address before dialling — but it blocks private and loopback address
  space, not an arbitrary public paste endpoint. It does not deliver this scenario;
  do not credit it with doing so.
- **Bypasses are enumerated and published.** Unsetting the proxy environment, a
  client that ignores it, raw TCP that does not speak the proxy protocol (N10), and
  UDP/QUIC/HTTP/3 (N11) all leave the boundary. The scenario's scope is **B3 —
  universal within one process**, conditional on that process honouring the injected
  proxy environment. It is **not** host-wide.
- **Channel and platform.** `aa-proxy` ships in the GitHub Release, the Homebrew tap
  and the install script for `linux_x86_64` and `linux_aarch64` only — the release
  workflow states the proxy is a Linux-only component. On **macOS the sole route is
  `cargo install aa-proxy`** from crates.io (AAASM-5653). On **Windows there is no
  local mediation at all** (P4, Unsupported). A demo recorded on a macOS laptop is
  running a crates.io build, not a released artifact.
- **Failure posture is fail-open** on this path. If the proxy is not in front of the
  connection, the connection is simply made.
- **The proxy writes no local evidence unless you configure a path.** The proxy's
  JSONL sink is built from `AA_PROXY_AUDIT_JSONL_PATH`
  (`aa-proxy/src/config.rs:482-483`, wired at `aa-proxy/src/lib.rs:81`); with the
  variable unset there is no writer and nothing lands on disk, which the crate's own
  test pins as the default. The refusal still happens — this is a bound on the
  *evidence*, not on the decision — but a demo that promises a record must set the
  variable, and a page that promises one must say it is configured. Note also that
  this sink is the **proxy's own**; the separate best-effort emission defect tracked
  as AAASM-5626 is on the *gateway's* audit path, and attributing it here would be the
  wrong component.

**Determination: executable, default-off.** Rows N1 (`reachability:
shipped_with_platform_exception`, standing evidence), N2, L1 (`reachability:
shipped`, `current_level: host_enforced`, standing evidence).

### Negative control for the flagship (AC 1)

A negative control proves the **absence of the effect**, not that an error was
raised. An agent can receive a 403 and still have reached the endpoint by another
route; an agent can raise an exception without ever having tried. Neither an error
nor a stack trace is evidence that nothing arrived.

**The observable side effect** is a TCP connection carrying payload bytes arriving at
the destination.

**Instrumentation.** Stand up a real listener on the address the egress configuration
denies. It records, independently of the agent and of the proxy: the count of
accepted connections, and the total bytes received. It is the only witness that
matters, because it sits on the far side of the boundary — a probe on the near side
can observe that its request went out and that nothing obviously failed, and neither
fact is evidence.

**Three runs are required.** All three, or the result proves nothing.

1. **Positive control — the check can see the effect.** With the destination host
   **allow-listed**, run the same agent action. Assert
   `listener.accepted_connections == 1` and that the payload bytes arrived. This is
   what makes a later zero meaningful. Without it, "zero connections" is
   indistinguishable from a listener that was never listening, a harness that never
   started the agent, or a test that silently skipped.

2. **Negative run — the effect is absent.** With the destination **denied**, run the
   same agent action, then assert **in this order**:

   1. **First:** `listener.accepted_connections == 0` **and**
      `listener.bytes_received == 0`. This is the load-bearing assertion and it must
      execute before anything that can throw, return early, or short-circuit.
   2. **Then:** the caller observed a refusal (403).
   3. **Then:** a decision record exists attributing the refusal to the proxy's
      CONNECT-time egress check. The harness must set `AA_PROXY_AUDIT_JSONL_PATH` for
      this to be checkable at all — unset, the proxy writes no local evidence, and
      the assertion would fail for a reason that has nothing to do with enforcement.

3. **Attempt witness — the agent actually tried.** In the negative run, assert that
   the proxy recorded a CONNECT attempt for that host. Without this, zero connections
   at the listener is also consistent with an agent that never attempted the upload,
   which would make the test pass for the wrong reason.

**Ordering is the whole point, and it has already gone wrong here — twice.** Assert
the absence **before** the error, never after.

State the defect precisely, because the loose version of it is wrong and gets
dismissed. In the *passing* run both assertions execute, so nothing looks broken.
The defect appears under **falsification**: if enforcement is removed or mutated, a
test that asserts the error first aborts on that assertion, and the absence check —
the one the control exists for — is never reached. The control therefore passes
whether or not it can detect the thing it was written to detect, and it fails for
the weak reason ("no error was raised") rather than the load-bearing one ("the effect
happened"). It has never been shown to bite.

This is the exact defect corrected across the three SDK negative-control suites under
AAASM-5529 — in each repository one control had the wrong order while its siblings
were already correct. Those corrections sit on unmerged branches at the time of
writing, and AAASM-5529 is still open, so treat this as a known pattern to design
against rather than as a solved problem. The same shape is present today in this
scenario's own area:
in `aa-integration-tests/tests/e2e_policy_proxy.rs`, `proxy_intercepts_and_enforces_deny`
binds a real upstream listener and asserts it is never accepted (`:157-162`), which is
a genuine negative control — but its 403 assertion at `:152` precedes that check. The
other three deny tests in that file have no negative control at all: they target a
hostname with no listener behind it, so there is nothing that could have observed an
arrival. Whoever implements the flagship harness should treat
`proxy_intercepts_and_enforces_deny` as the starting point and fix the order, not
write a fourth test alongside it.

If the harness uses a construct that asserts a raise around a block, the absence
check must sit **outside and after that block**, not inside it.

**What this negative control does not prove.** That the upload was impossible — only
that it did not happen on this path, in this configuration, on this platform. The
bypass list above is the honest scope, and it belongs next to the demo.

---

## S1 — Secret exfiltration

An agent puts a live credential into a request to a model provider. The credential is
recognised and removed before the request is forwarded.

Note the verb: **Redacted**, not *Denied*. The request proceeds. Copy that turns this
scenario into a blocked request is wrong, and the difference is the default.

| Field | |
|---|---|
| **Threat source** | An injected instruction, or an ordinary "help me debug this" that pastes a config file, an environment dump or a stack trace containing a live key into the model context. |
| **Requested action** | An outbound HTTPS request to a model provider whose body or headers carry a credential. |
| **Existing-system gap** | The provider is a *legitimate* destination, so a host allowlist does not help. The key is already in the process environment or the repository. Once the request lands, the credential is in a third party's logs, and rotation is the only remedy. |
| **Governed path** | Traffic routed to the proxy **and** the proxy's CA trusted, so the request is inspected rather than tunnelled. |
| **Policy decision** | **Redacted.** The `aa-security` scanner runs in line on the intercepted request and the recognised credential is removed before forwarding (`aa-security` scanner via `intercept_request`; the LLM-host path is `aa-proxy/src/proxy/mod.rs:1038`). Local proxy policy, not a gateway decision. |
| **Prevented outcome** | The recognised credential does not reach the provider in cleartext. **Not** "the request was stopped" — it was forwarded with the credential removed. |
| **Evidence** | **Redacted** — a redaction record naming the fields. Standing test: `aa-integration-tests/tests/e2e_secret_interception.rs`, whose `proxy_path` module terminates TLS at a capturing upstream and asserts on the bytes it actually received — the redaction marker present and the raw key absent (`:718-731`). That is a true non-arrival assertion, not merely "a redaction occurred". |
| **Known boundary** | See below. |

**Known boundary, in full:**

- **Redact-and-forward is the default; blocking is opt-in.** The default action is
  `RedactOnly` (`aa-proxy/src/config.rs:16-27`). A third mode, `AlertOnly`, forwards
  the credential **unmodified and raises no alert** — if a page says "alerts you", it
  must not mean this mode.
- **Three hosts, by default.** `llm_only` defaults on, which intercepts
  `api.openai.com`, `api.anthropic.com` and `api.cohere.com`
  (`aa-proxy/src/intercept/detect.rs:31-34`). Any other host is tunnelled without
  payload inspection: the *connection* is Observed, the *payload* is **Unmeasured**.
  The honest phrasing is "the connection was observed, the payload was not
  inspected" — never "nothing was observed".
- **Recall is bounded by the pattern set.** There is no Stripe detector, and the
  OpenAI detector keys on `sk-` while Stripe uses `sk_`. Splitting a secret across a
  multi-character gap still evades detection
  (`aa-security/src/scanner.rs:3960-4005`); AAASM-5368 narrowed the single-separator
  case but did not close the class. State the pattern-set bound wherever recall is
  implied.
- **Model responses are not scanned.** A credential coming *back* from the provider
  is Unmeasured.
- **The stronger variant is real, off by default, and unit-evidenced only.**
  Credential *substitution* — where the operator's real provider key is appended at
  egress and the agent's own header stripped, so the real key never enters the agent
  (`aa-proxy/src/credentials.rs:198`, `aa-proxy/src/proxy/http.rs:353,371-383`) — is a
  genuine shipped mechanism. But its `default_state` is **false** (the operator must
  set `AA_PROXY_PROVIDER_KEYS`), it covers only the intercepted hosts, and its
  evidence is **unit-only: no end-to-end test proves the substitution reaches
  upstream**. A bounded version of the "never enters the agent" claim is defensible
  with all of those conditions named, and not otherwise.
- **Do not tell the credential-*injection* story.** A separate mechanism —
  credential injection via `SecretsService.DispatchTool` — is **dead code**
  (`reachability: dead_code`, row C3). Copy claiming "secrets are injected at runtime
  and never enter the model context" advertises a capability no released build can
  reach, and it is already on the rejected-wording list. Conflating C3 with the
  substitution mechanism above is exactly what produced that defect.
- **Channel and platform** are the proxy's, identical to the flagship's.

**Determination: executable today** for the redaction path — rows C1
(`shipped_with_platform_exception`, standing evidence), C6 (`detected`, standing
evidence), N3 (standing evidence). The substitution variant (C2) is **executable,
default-off, unit-evidenced**. The injection variant (C3) is **not executable — dead
code** and must not be told at all.

---

## S2 — Destructive production action

An agent calls a tool that would drop or rewrite production data. The call is
evaluated against policy and refused before it is forwarded, so the tool server never
receives it.

This is the one scenario in the set where the **control plane** makes the decision
that stops the bytes. Everywhere else in this page, the refusal is the proxy's own
local configuration.

| Field | |
|---|---|
| **Threat source** | An agent asked to "clean up the staging database" that resolves the wrong connection string; or an injected instruction in data the agent was asked to process. The plan reads as reasonable in the transcript. |
| **Requested action** | An MCP `tools/call` carrying a destructive operation — a `DROP TABLE`, a migration that rewrites rows, a delete against a production namespace. |
| **Existing-system gap** | Tool servers execute what they are asked. Nothing sits between the agent's intent and the tool server, and the destructive step is indistinguishable in shape from the routine ones the agent is supposed to perform. |
| **Governed path** | Traffic routed to the proxy, CA trusted, a gateway endpoint configured, and the MCP host intercepted as a non-LLM host. The only supported route sets both and forces whole-machine interception (`aa-cli/src/commands/proxy/start.rs:128-135`). |
| **Policy decision** | **Denied before execution**, and the decider is the **gateway**: `evaluate_mcp_request` (`aa-proxy/src/proxy/mod.rs:614`, invoked at `:834`) calls `aa-gateway PolicyService.CheckAction`. This is the only gateway-bound pre-dial block in the system. |
| **Prevented outcome** | The `tools/call` envelope is not forwarded. The MCP server never receives the call, so the table is not dropped. |
| **Evidence** | **Observed** — a decision record. Standing tests: `aa-integration-tests/tests/e2e_mcp_interceptor.rs`, `e2e_mcp_redact.rs`. Malformed and batched envelopes carrying `tools/call` are adjudicated too (row M3). |
| **Known boundary** | See below — the transport bound is the one that matters most. |

**Known boundary, in full:**

- **Streamable HTTP only. stdio and SSE are absent mechanisms.** MCP over **stdio**
  (subprocess pipes) and over **SSE** both carry `reachability: absent_mechanism`
  (rows M5, M6), and MCP over WebSocket is Unsupported (M8). Since stdio is the
  default transport for most locally-run MCP servers, **the common case is not
  covered**. This sentence must travel with the scenario; without it the story
  implies a coverage that does not exist.
- **Off by default, and coupled to whole-machine interception.** The row's
  `default_state` is false. Turning it on requires disabling the LLM-only default,
  which means the proxy intercepts every host, not just the MCP one. That is a
  material operational consequence, not a footnote.
- **Only `tools/call`.** Every other MCP method is **Unmeasured** (row M4).
- **A hold cannot be reached here.** A gateway `Pending` decision is downgraded to
  `Deny` inside the tunnel (`mcp_enforce.rs:135-144`), so this path cannot produce
  "blocked pending a human decision". Separately, and more broadly, **no shipped
  operator surface can answer a hold at all** — see the Provisional row in
  [Product promise](product-promise.md#provisional) (AAASM-5657). Do not attach an
  approval narrative to this scenario.
- **Per-agent MCP policy and per-agent MCP audit do not exist** and must not be
  claimed (AAASM-5533). The decision is not attributed to an individual agent on this
  path.
- **Channel and platform** are the proxy's, identical to the flagship's.

**Determination: executable, default-off**, over Streamable HTTP on Linux — rows M1
and M3 (`shipped_with_platform_exception`, standing evidence). **Not executable over
stdio or SSE** (M5, M6: `absent_mechanism`); a demo or a page that shows a local
stdio MCP server being governed this way would be showing something that does not
happen.

---

## S3 — Runaway cost

An agent enters a retry loop, or fans out across a large repository, and keeps
spending. The call that would cross the declared cap is refused rather than billed.

| Field | |
|---|---|
| **Threat source** | No adversary at all. A retry loop, a recursive plan, or a fan-out over more files than anyone estimated. |
| **Requested action** | The next model call, after the team's declared spend cap has been reached. |
| **Existing-system gap** | Provider dashboards settle hours to a day late, and none of them refuse the next call. By the time the number is visible the spend has happened. |
| **Governed path** | An action evaluated by the gateway, under a policy that **declares** a budget. |
| **Policy decision** | **Evaluated → Denied before execution.** Spend is reserved atomically inside the same decision path, serialised per tenant (`aa-gateway/src/budget/tracker.rs:126`, AAASM-4124), and the over-cap case resolves to `BudgetStatus::LimitExceeded` (`tracker.rs:33`, `:617`, `:643`, `:662`). |
| **Prevented outcome** | The over-cap call is refused instead of billed. |
| **Evidence** | **Observed** — a decision record. Standing tests: `aa-gateway/tests/policy_service_test.rs:245` and `:339`, which drive `check_action` over the wire and assert `Decision::Deny` with a "budget exceeded" reason; plus the engine unit test `budget_denies_when_exceeded` (`aa-gateway/src/engine/mod.rs:4167`). **Not** `e2e_budget.rs` — see the boundary below. |
| **Known boundary** | See below — including an evidence correction and a matrix gap this page must not paper over. |

**Known boundary, in full:**

- **No cap unless you declare one.** Limit resolution returns nothing when neither a
  per-agent nor a global limit is configured, so an undeclared budget is uncapped
  spend. Most shipped policy examples declare a daily cap, so an evaluator who starts
  from one usually gets a cap — but a hand-written policy that omits the block has
  none.
- **A corrupt or unreadable budget store fails open, silently, and resets the cap to
  zero spend.** The gateway falls back on a load failure
  (`aa-gateway/src/server.rs:155-163`), and a write failure prints to stderr and
  continues (`aa-gateway/src/budget/persistence.rs:85-86`). Row G9's `failure_posture`
  is `fail_open_silent`. This is the sharpest boundary in this page: the control is
  real, and the mode in which it stops working produces no signal. Any page that
  claims a spend guarantee must carry it.
- **A refusal only stops something through a caller that blocks on the answer.** The
  gateway holds no traffic. Budget exhaustion resolves to a refusal *in the decision*;
  whether that refusal prevents the call depends on the same two blocking callers as
  every other gateway decision — the MCP path, and an SDK shim that honours the
  answer.
- **The obvious test does not prove this scenario.**
  `aa-integration-tests/tests/e2e_budget.rs` looks like the evidence and is not: all
  of its tests drive `record_raw_spend` directly and assert on the returned
  `BudgetStatus`, never calling `check_action` or the policy engine — its own header
  records the substitution at `:15`. `record_raw_spend` accounts for spend; it is not
  an authorization gate. Citing it for pre-execution denial would be a wrong-reason
  pass, which is why the Evidence field above names the gateway tests instead.
- **A matrix gap, stated rather than hidden.** AAASM-5527 assigns **no positive
  capability row to budget enforcement** — the only budget row in the matrix is G9,
  the failure mode, whose own `evidence` field is marked `GAP`. So this scenario's
  determination does **not** rest on a matrix row the way the other three do; it rests
  on the call path and the gateway tests cited above. That is different provenance,
  and a reader is entitled to know which of these four scenarios has it.

**Determination: executable today**, with the silent fail-open stated alongside it.
The call path is `check_action` (`aa-gateway/src/service/policy_service.rs:1599`) →
`evaluate` → Stage 7's budget check (`aa-gateway/src/engine/mod.rs:1687-1691`) →
`EvaluationResult::deny_with`, with a TOCTOU-safe reservation for LLM spend rewriting
the response to a hard `Deny` (`policy_service.rs:1341`, called at `:1669`). Derived
from that path and its gateway tests, **not** from a 5527 capability row, because
none exists.

### S3b — Unauthorized payment: illustrative only

The parent scope pairs runaway cost with "unauthorized payment". These do not have
the same answer, and they must not be told as one story.

**There is no payment, purchase, checkout or spend-authorization capability in the
product.** Nothing evaluates a transaction, understands a payee, or holds a purchase
for release. A sweep of the core repository for payment, purchase, checkout, invoice
and charge vocabulary — run with a positive control in the same query, so an empty
result is a real absence and not a failed search — returns only three unrelated
classes: `"payments"` used as a team name in test fixtures, a
`PaymentCardNumber` **detection** category in the credential/PII scanner
(`aa-security/src/canonical/category.rs:34`), and "charge" in the budget
sense of accounting for spend. There is no purchase action type and no payment tool.

The nearest real controls are generic, and none of them knows what a payment is:

- refusing the connection to a payment API host — the flagship's mechanism, and it
  treats that host like any other unapproved host;
- refusing an MCP `tools/call` that happens to be a payment tool — S2's mechanism,
  with S2's transport bound;
- the spend cap above, which counts model tokens, not money moved.

**Determination: illustrative.** If a surface needs a payment story to make the
category legible, it must be labelled *illustrative* in place, and it must not be
demonstrated as a product capability. In particular it must not be told as "held for
human review" — that is a Provisional claim on the promise page, blocked on
AAASM-5657, because no shipped operator surface can answer a hold.

---

## Approved wording for reuse

These are the sentences downstream surfaces may use verbatim. They are approved
because each one is bounded where the underlying capability is bounded. Shortening
one generally breaks it — the boundary clause is usually the part that gets cut.

**Flagship, long form (for a homepage section):**

> A coding agent decided to upload the repository it was working on to an endpoint
> nobody had approved. Because the agent was launched through Agent Assembly, the
> connection was refused before it was dialled. The endpoint never received a byte —
> and the refusal is recorded, with the reason.

**Flagship, short form (for a hero panel or a card):**

> The upload was refused before it was dialled. The endpoint never received a byte.

**Flagship, boundary clause — required on the same screen, above the fold:**

> This applies to the connections you route through Agent Assembly, on a host where
> the proxy is installed, against an approved-destination list you configure. An
> agent you did not route is not inspected — and the record says so.

**S1 — secret exfiltration:**

> An agent pasted a live API key into a request to its model provider. On the
> provider hosts Agent Assembly inspects, the key was recognised and removed before
> the request was forwarded. Detection is bounded by the patterns it knows, and the
> default is to redact and forward, not to block.

**S2 — destructive production action:**

> An agent called a tool that would have dropped a production table. The call was
> evaluated against your policy and refused before it was forwarded, so the tool
> server never received it. This covers MCP tool calls over Streamable HTTP; tool
> servers you run over stdio are not on this path.

**S3 — runaway cost:**

> An agent in a retry loop reached the spend cap its team had declared. The next call
> was refused rather than billed. A cap exists only where a policy declares one.

**The four verbs these scenarios are allowed to use**, and nothing vaguer: *refused
before it ran* (Denied before execution), *removed before it was forwarded*
(Redacted), *evaluated against your policy* (Evaluated), *recorded* (Observed). If a
sentence works with "protects", "enforces" or "catches", it is not specific enough to
publish.

## What these scenarios must not be used to say

<!-- claim-gate:ignore-start
     AAASM-5583: the block below necessarily quotes the phrases a banned-absolutes
     gate would look for — a rejected-wording list cannot name its rejections
     otherwise. Skip this region rather than adding per-phrase exceptions. This
     follows the convention product-promise.md proposes for AAASM-5536; as that page
     records, no gate consumes this marker today. -->

- **Not** "Agent Assembly stops your agents from leaking data." Each scenario is
  scoped to one process, one routed path, one configured rule and one platform.
- **Not** "nothing gets past it", "catches everything", or "an agent cannot walk
  around it". The bypasses are enumerated in each scenario and are published.
- **Not** a count, a percentage or any coverage figure derived from these four
  stories. There is no machine-readable manifest to compute one from, and
  self-reported layer availability is not evidence of coverage.
- **Not** "held for human review" on any of them. A hold is real and fails closed,
  but no shipped operator surface can answer it (AAASM-5657).
- **Not** an audit claim stronger than *tamper-evident*. The chain is an unkeyed
  digest, emission is best-effort, and a passing verification does not mean the log
  is whole.
- **Not** a story told on a macOS or Windows screenshot without its platform
  sentence. The proxy that delivers three of these four scenarios is a Linux release
  artifact; on macOS it is a crates.io install, and on Windows there is no local
  mediation.
- **Not** the credential-injection framing for S1. That mechanism is dead code.
- **Not** S2 over a stdio MCP server. That transport has no interception mechanism.

<!-- claim-gate:ignore-end -->

## How this page meets its acceptance criteria

| Criterion | How it is met |
|---|---|
| The flagship can be demonstrated with a negative control proving the denied side effect did not happen | [Negative control for the flagship](#negative-control-for-the-flagship-ac-1) specifies the observable side effect (accepted connections and bytes at an independent listener), the absence check, the paired positive control that proves the check can see the effect, an attempt witness that proves the agent tried, and the assertion ordering — absence first, error second. |
| Scenarios do not imply host-wide or cross-platform coverage when only a managed path is exercised | Every scenario carries its `boundary_class`, its routing precondition, its default state and its per-channel, per-platform release position. The flagship is stated as **B3 — universal within one process**, and the Windows and macOS positions are stated in each. |
| The story is understandable without SDK/eBPF knowledge | No scenario in the set is an SDK scenario, and none relies on eBPF. Each is told as an action, a decision and an outcome. The mechanism names appear only in the boundary and evidence fields, where a technical reader needs them to verify. |
| Scenario wording is approved for reuse by website, Docs Hub and demo assets | [Approved wording for reuse](#approved-wording-for-reuse) gives the verbatim sentences, in long, short and boundary forms, with the required co-location rule for the flagship's boundary clause. |

---

*Last reviewed: 2026-08-06 — AI Agent Assembly Team*
