<!-- BEGIN AA-PAGE-META
schema_version: 1
page_type: guide
audience: [evaluator, security-engineer, operator]
user_job: Choose the governed path that fits my platform and launch model
owner: L3:agent-assembly
canonical_source: https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/governance/capability-manifest.yaml
describes_capability: true
area: core
availability: available-with-limits
platforms:
  - channel: github-release
    platform: linux-x86_64
    status: available-verified
    evidence: capability-surface.toml, released_channels
  - channel: github-release
    platform: macos
    status: available-with-limits
    evidence: capability-surface.toml, released_matrix; aa-proxy is not packaged here
  - channel: homebrew
    platform: linux-x86_64
    status: available-verified
    evidence: capability-surface.toml, released_channels
  - channel: homebrew
    platform: macos
    status: available-with-limits
    evidence: capability-surface.toml, released_matrix; aa-proxy is not packaged here
  - channel: install-sh
    platform: linux-x86_64
    status: available-verified
    evidence: capability-surface.toml, released_channels
  - channel: install-sh
    platform: macos
    status: available-with-limits
    evidence: capability-surface.toml, released_matrix; aa-proxy is not packaged here
  - channel: crates-io
    platform: macos
    status: available-verified
    evidence: capability-surface.toml, released_channels; the only macOS route to aa-proxy
  - channel: ghcr
    platform: linux-x86_64
    status: available-with-limits
    evidence: capability-surface.toml, channel_absence; aa-proxy has no published image
last_verified:
  version: v0.0.1-rc.6
  ref: dc8ab13d656ac3398e064583150c7551be8e46a4
  date: 2026-08-13
  method: Rows generated from capability-surface.toml, a pinned extract of the capability manifest at that agent-assembly commit
claims:
  - term: Observed
    evidence: https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/governance/capability-manifest.yaml
  - term: Detected
    evidence: https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/governance/capability-manifest.yaml
  - term: Evaluated
    evidence: https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/governance/capability-manifest.yaml
  - term: Denied before execution
    evidence: https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/governance/capability-manifest.yaml
  - term: Redacted
    evidence: https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/governance/capability-manifest.yaml
  - term: Degraded
    evidence: https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/governance/capability-manifest.yaml
  - term: Unmeasured
    evidence: https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/governance/capability-manifest.yaml
  - term: Experimental
    evidence: https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/governance/capability-manifest.yaml
  - term: Unsupported
    evidence: https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/governance/capability-manifest.yaml
limitations: "#what-none-of-these-paths-gives-you"
disclosure_levels: [1, 3]
deeper: https://docs.agent-assembly.com/core/latest/adr/0033-canonical-governance-and-enforcement-architecture.html
END AA-PAGE-META -->

# Choose your enforcement path

## What governs this page

Three governed paths exist, they are independent of one another, and choosing between
them is a decision about **your** platform and launch model rather than about the
product's architecture. This page sets out what each one needs, when it decides, what
it does when it fails, and — at the same length — what it does not cover.

| Source | What it decides for this page |
|---|---|
| The capability and evidence manifest (AAASM-5531), in the `agent-assembly` repository | Every row in every table below |
| [ADR 0033 §1](https://docs.agent-assembly.com/core/latest/adr/0033-canonical-governance-and-enforcement-architecture.html) | The roles the three paths are named after, and which components implement each |
| [ADR 0033 §6](https://docs.agent-assembly.com/core/latest/adr/0033-canonical-governance-and-enforcement-architecture.html) | The words for what a path did to an action. This page prints them and does not define them |
| [What ships today](what-ships-today.md) | The whole-product inventory, the platform position, and the distribution channels |

Ticket references on this page are plain text, not links: the tracker is not publicly
readable, so a link would only reach a login wall — and a link checker scores that wall
as reachable, which makes the reference look verified when it is not.

<!-- BEGIN GENERATED:capability-surface:pin -->

> Every table below is generated from [`governance/capability-manifest.yaml`](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/governance/capability-manifest.yaml) in the `ai-agent-assembly/agent-assembly` repository — the capability and evidence manifest defined by AAASM-5531 — through the pinned extract `capability-surface.toml` in this repository.
>
> **Manifest version** `1.0.0` · **80 capability rows** · **taken at commit** [`dc8ab13d6`](https://github.com/ai-agent-assembly/agent-assembly/commit/dc8ab13d656ac3398e064583150c7551be8e46a4) · **the manifest's own evidence tree** `299de3883`, dated 2026-08-06 · **declared fix version** agent-assembly v0.0.1-rc.7.
>
> The extract is refreshed by hand, so it can lag the manifest. What this repository's CI proves is that **the generated tables** on these pages match the extract — prose outside the generated blocks is not checked, and proving the extract itself matches the manifest needs a cross-repository check, which is AAASM-5600.

<!-- END GENERATED:capability-surface:pin -->

## Level 1 — one sentence

Pick a path by what you can change — your agent's code, its network route, or its host
— then read what that path does not cover before you plan around it.

## Level 3 — for an evaluator

### The three paths, side by side

Grouping the manifest's rows onto these three is this page's doing; every fact rendered
under a group is the manifest's. The grouping follows the roles
[ADR 0033 §1](https://docs.agent-assembly.com/core/latest/adr/0033-canonical-governance-and-enforcement-architecture.html)
names and the components it lists against each. It is deliberately **not** a partition
of the whole manifest — the rows no path claims are
[listed further down](#rows-no-path-above-claims) rather than forced into one.

<!-- BEGIN GENERATED:capability-surface:paths-overview -->

| Path | Implemented today by | Rows | Outcomes its rows reach | Rows at Unmeasured or Unsupported |
|---|---|---|---|---|
| [Managed execution checkpoints](#path-checkpoints) | the SDK seams, `aa-runtime`'s `handle_policy_query`, `aa-sdk-client` and `aa-sandbox` | 17 | Observed 2 · Evaluated 4 · Denied before execution 6 · Unmeasured 5 | 5 of 17 |
| [Protocol and transport mediation](#path-transport) | `aa-proxy` | 26 | Evaluated 1 · Denied before execution 6 · Redacted 5 · Unmeasured 11 · Unsupported 3 | 14 of 26 |
| [Platform-specific host-level interception adapters](#path-host) | Linux eBPF via `aa-ebpf-loaderd`; on macOS and Windows, no adapter | 11 | Observed 2 · Detected 1 · Degraded 1 · Unmeasured 4 · Experimental 1 · Unsupported 2 | 6 of 11 |

<!-- END GENERATED:capability-surface:paths-overview -->

The paths do not form a chain. A path you do not deploy is **absent**, and its absence
is a reportable state rather than something the next one picks up. Deploying two does
not compose them into a stronger single control; it gives you two controls with two
separate boundaries.

### What is not a path

Three things are routinely mistaken for a fourth path, and each mistake changes what
you would plan for:

- **The control plane is not an interception point.** It holds policy, identity,
  budgets, approvals and audit, and it answers decision requests — but no agent bytes
  traverse it, so a refusal it issues stops something only when a component in front of
  the action blocks on the answer. Which components do, and which refuse on their own
  local configuration instead, is
  [ADR 0033 §2](https://docs.agent-assembly.com/core/latest/adr/0033-canonical-governance-and-enforcement-architecture.html)'s
  caller table. Attribute a refusal to whichever component actually made it.
- **eBPF is one Linux mechanism, not a cross-platform floor.** It is an implementation
  of the host-adapter role on Linux only, and on the other platforms nothing takes its
  place. See [what ships today](what-ships-today.md#platforms).
- **Writing a tool's own settings file is not data-path mediation.** It is
  tool-governance: it takes effect only if the tool honours those keys. Any data-path
  refusal such an integration delivers is the proxy's, borrowed through the launch
  environment the integration injects. These rows are
  [listed separately](#the-launch-route-which-is-not-itself-a-path) for that reason.

<a id="path-checkpoints"></a>

### Path 1 — Managed execution checkpoints

**What you change:** your agent's code, or the framework adapter it initialises. The
checkpoint is a call your process makes before running a tool.

**Who it suits:** teams that own the agent's source and can adopt an SDK.

<!-- BEGIN GENERATED:capability-surface:path-checkpoints -->

| | |
|---|---|
| **Implemented today by** | the SDK seams, `aa-runtime`'s `handle_policy_query`, `aa-sdk-client` and `aa-sandbox` |
| **Manifest rows** | 17 — `S1` `S2` `S3` `S4` `S5` `S6` `S7` `S8` `S9` `S10` `S11` `S12` `S13` `H5` `G1` `G2` `G5` |
| **Outcomes its rows reach** | Observed 2 · Evaluated 4 · Denied before execution 6 · Unmeasured 5 |
| **Decision timing** | before the action takes effect 12 · after the action 2 · no decision point 3 |
| **Failure posture** | fail closed 9 · fail open 1 · fail open, and silently 2 · no failure posture 5 |
| **Reachability** | shipped 17 |
| **Default state of its controls** | `on` 5 · `off` 2 · `open` 2 · `closed` 3 · `mixed` 1 · `not_applicable` 4 |
| **Declared preconditions** | `env:AA_AGENT_ID` |
| **Launch paths that reach it** | `aasm sandbox run, or POST /dispatch_tool with ToolKind::Wasm` · `any` · `assembly_Init_plus_explicit_WrapTools` · `auto_detected_at_initAssembly` · `default_go_build` · `in_process_after_init` · `in_process_after_init_assembly` · `initAssembly_with_defaults` · `tools_passed_as_config_langchain_tools` |

**What this path does not cover.** Every row below is one the
manifest records at *Unmeasured* or *Unsupported* — nothing is known
about the action, or the mechanism is not available at all.

| Id | What it is | ADR 0033 §6 term | Reachability |
|---|---|---|---|
| `S7` | Node default mode routes every policy check through an allow-all no-op client | Unmeasured | shipped |
| `S10` | Direct function call that does not pass a patched seam | Unmeasured | shipped |
| `S11` | Framework with no adapter | Unmeasured | shipped |
| `S12` | Raw HTTP, subprocess, filesystem, DB driver, browser automation from inside an SDK-adopting process | Unmeasured | shipped |
| `G2` | aa-runtime with no gateway configured, or fail_closed=false | Unmeasured | shipped |

<!-- END GENERATED:capability-surface:path-checkpoints -->

Two properties of this path decide whether it fits, and neither is visible from a
quickstart:

- **The checkpoint is voluntary.** It is a call the agent makes. A process that does
  not make it is outside the boundary, and the product knows nothing about that
  action — not that it was allowed, and not that it was clean.
- **Honouring a refusal is the shim's job, not the client's.** ADR 0033 §4 records
  that the in-repo decision helper has no caller that refuses to execute, and that one
  out-of-repo shim maps transport failures to *allow*. Read the per-language rows above
  before assuming a returned refusal stops anything.

<a id="path-transport"></a>

### Path 2 — Protocol and transport mediation

**What you change:** the agent's network route — an injected proxy environment and a
trusted certificate authority — rather than its code.

**Who it suits:** teams that cannot modify the agent, including closed-source and
vendor tools, on a platform where the mediator runs.

<!-- BEGIN GENERATED:capability-surface:path-transport -->

| | |
|---|---|
| **Implemented today by** | `aa-proxy` |
| **Manifest rows** | 26 — `N1` `N2` `N3` `N4` `N5` `N6` `N7` `N8` `N9` `N10` `N11` `N12` `M1` `M2` `M3` `M4` `M5` `M6` `M7` `M8` `M9` `C1` `C2` `C4` `G3` `G4` |
| **Outcomes its rows reach** | Evaluated 1 · Denied before execution 6 · Redacted 5 · Unmeasured 11 · Unsupported 3 |
| **Decision timing** | before the action takes effect 5 · in line with the request 8 · no decision point 13 |
| **Failure posture** | fail closed 10 · fail open 6 · silent truncation 1 · no failure posture 9 |
| **Reachability** | shipped 3 · shipped, with a platform exception 20 · no mechanism exists 3 |
| **Default state of its controls** | `on` 6 · `off` 4 · `open` 3 · `closed` 1 · `not_applicable` 12 |
| **Declared preconditions** | `env:AA_PROXY_DENIED_HOSTS` · `env:AA_PROXY_GATEWAY_ENDPOINT` · `env:AA_PROXY_LLM_ONLY` · `env:AA_PROXY_MCP_FAIL_OPEN` · `env:AA_PROXY_MITM_HOSTS` · `env:AA_PROXY_NETWORK_ALLOWLIST` · `env:AA_PROXY_PROVIDER_KEYS` · `env:HTTPS_PROXY` |
| **Launch paths that reach it** | `any` · `default_aa_proxy_run` · `provider keys configured in the proxy's environment` · `routed` · `routed through aa-proxy, CA trusted, gateway endpoint configured, request reaching a MitM'd non-LLM host` · `routed, CA trusted, AND llm_only=false or an operator mitm_hosts entry` · `routed_and_ca_trusted` · `same_as_M1` · `traffic_routed_to_the_proxy` |

**What this path does not cover.** Every row below is one the
manifest records at *Unmeasured* or *Unsupported* — nothing is known
about the action, or the mechanism is not available at all.

| Id | What it is | ADR 0033 §6 term | Reachability |
|---|---|---|---|
| `N5` | HTTPS to a host not under MitM | Unmeasured | shipped, with a platform exception |
| `N6` | Model response body scanning on LLM hosts | Unmeasured | shipped, with a platform exception |
| `N8` | HTTP/2, gRPC or WebSocket over a MitM'd host | Unsupported | shipped, with a platform exception |
| `N9` | Chunked transfer encoding | Unmeasured | shipped, with a platform exception |
| `N10` | Raw TCP that does not speak the proxy protocol | Unmeasured | shipped |
| `N11` | UDP, QUIC, HTTP/3 | Unsupported | shipped |
| `N12` | Local IPC (Unix domain sockets) between third-party processes | Unmeasured | shipped |
| `M2` | MCP enforcement with no gateway configured | Unmeasured | shipped, with a platform exception |
| `M4` | Every MCP method other than tools/call | Unmeasured | shipped, with a platform exception |
| `M5` | MCP over stdio (subprocess pipes) | Unmeasured | no mechanism exists |
| `M6` | MCP over SSE (text/event-stream) | Unmeasured | no mechanism exists |
| `M7` | MCP over Streamable HTTP | Unmeasured | shipped, with a platform exception |
| `M8` | MCP over WebSocket | Unsupported | no mechanism exists |
| `C4` | Model response credential scanning | Unmeasured | shipped, with a platform exception |

<!-- END GENERATED:capability-surface:path-transport -->

Three defaults on this path are worth setting expectations against before you plan:

- **Inspection is opt-in per host, not blanket.** Only a built-in set of provider hosts
  is intercepted by default; everything else is tunnelled through without its payload
  being looked at. Widening that is an operator decision with a latency and
  compatibility cost.
- **The egress lists are empty out of the box.** An allow/deny decision at connection
  time decides nothing until you populate them.
- **The mediator is not packaged everywhere.** On macOS it arrives through crates.io
  only; see the channel table in [what ships today](what-ships-today.md#where-the-artifacts-come-from).

<a id="path-host"></a>

### Path 3 — Platform-specific host-level interception adapters

**What you change:** the host — a privileged component installed beside the agent.

**Who it suits:** Linux operators who need a view of process, file and TLS activity
that does not depend on the agent cooperating.

<!-- BEGIN GENERATED:capability-surface:path-host -->

| | |
|---|---|
| **Implemented today by** | Linux eBPF via `aa-ebpf-loaderd`; on macOS and Windows, no adapter |
| **Manifest rows** | 11 — `H2` `H3` `H4` `N13` `I4` `G6` `G7` `P1` `P2` `P3` `P4` |
| **Outcomes its rows reach** | Observed 2 · Detected 1 · Degraded 1 · Unmeasured 4 · Experimental 1 · Unsupported 2 |
| **Decision timing** | in line with the request 1 · after the action 7 · no decision point 3 |
| **Failure posture** | fail closed 1 · fail open 8 · fail open, and silently 1 · no failure posture 1 |
| **Reachability** | shipped on crates.io only 10 · no mechanism exists 1 |
| **Default state of its controls** | `on` 6 · `off` 2 · `open` 2 · `not_applicable` 1 |
| **Declared preconditions** | `env:AA_EBPF_CONFINE_PID` |
| **Launch paths that reach it** | `AA_EBPF_CONFINE_PID set AND policy lowers a non-empty allowlist` · `any` · `none` · `privileged aa-ebpf-loaderd` · `privileged aa-ebpf-loaderd at /run/aa-ebpf-loaderd.sock` · `proxy start (CA install attempted automatically); managed-settings write` |

**What this path does not cover.** Every row below is one the
manifest records at *Unmeasured* or *Unsupported* — nothing is known
about the action, or the mechanism is not available at all.

| Id | What it is | ADR 0033 §6 term | Reachability |
|---|---|---|---|
| `H3` | Process exec observation | Unmeasured | shipped on crates.io only |
| `N13` | TLS plaintext observation without the proxy | Unmeasured | shipped on crates.io only |
| `I4` | Process-tree identity across fork/exec | Unmeasured | shipped on crates.io only |
| `G7` | eBPF policy file unreadable or unparseable | Unmeasured | shipped on crates.io only |
| `P3` | macOS host-level interception | Unsupported | shipped on crates.io only |
| `P4` | Windows mediation | Unsupported | no mechanism exists |

<!-- END GENERATED:capability-surface:path-host -->

This path is the one most often planned against optimistically:

- **It is predominantly an observation mechanism.** Its probes feed the evidence
  pipeline and are consulted in no allow/deny decision.
- **Its one terminating control is off unless you name a process**, and it acts after
  the offending call rather than before it — which is why the manifest records it at
  *Detected* rather than at a pre-execution refusal.
- **There is no adapter on macOS or Windows**, and the rows above say so rather than
  leaving it to inference. Read the macOS position together with
  [ADR 0033 §5.3](https://docs.agent-assembly.com/core/latest/adr/0033-canonical-governance-and-enforcement-architecture.html),
  whose macOS row carries a qualification a summary reliably drops.

<a id="the-launch-route-which-is-not-itself-a-path"></a>

### The launch route, which is not itself a path

A managed launch is how an agent or developer tool is *placed onto* one of the paths
above — it injects the environment, and it writes settings into the tool's own
configuration. Its rows are here rather than under a path because a settings write is
not a claim about the data path.

<!-- BEGIN GENERATED:capability-surface:launch -->

| Id | Route | ADR 0033 §6 term | Decision timing | Failure posture |
|---|---|---|---|---|
| `H8` | Shell / file rule declared in a tool's own settings file | Unmeasured | before the action takes effect | fail open, and silently |
| `M10` | MCP-server governance by configuration | Unmeasured | before the action takes effect | fail open, and silently |
| `L1` | Claude Code managed launch | Denied before execution | before the action takes effect | fail closed |
| `L2` | Codex managed launch | Unmeasured | before the action takes effect | fail open, and silently |
| `L3` | Windsurf managed launch | Unmeasured | before the action takes effect | fail open, and silently |
| `L4` | Copilot managed launch | Unsupported | no decision point | no failure posture |
| `L5` | SaaS / opaque agent | Observed | after the action | no failure posture |
| `L6` | Unmanaged launch — the user starts the tool directly | Unmeasured | no decision point | no failure posture |
| `L7` | Settings-layer governance surviving an unmanaged launch | Unmeasured | before the action takes effect | fail open, and silently |
| `L8` | aasm run --no-proxy | Unmeasured | no decision point | no failure posture |

<!-- END GENERATED:capability-surface:launch -->

*Supported tool* and *governable tool* are different lists. One shipped adapter returns
a launch failure rather than a governed command, and another is capped at observation;
for those, no proxy environment is injected and there is nothing to route into.

<a id="rows-no-path-above-claims"></a>

### Rows no path above claims

These are the manifest rows the three paths do not account for. They are published
rather than dropped, because a row that quietly belongs to no path is exactly the kind
of coverage assumption this page exists to prevent.

<!-- BEGIN GENERATED:capability-surface:unattached -->

| Area | Rows | Outcomes they reach | Capability ids |
|---|---|---|---|
| Host actions (`host_action`) | 3 | Unmeasured 3 | `H1` `H6` `H7` |
| Credentials (`credentials`) | 3 | Detected 1 · Unmeasured 2 | `C3` `C5` `C6` |
| Identity and attribution (`identity`) | 6 | Evaluated 5 · Unmeasured 1 | `I1` `I2` `I3` `I5` `I6` `I7` |
| Degraded and failure modes (`degraded_mode`) | 4 | Evaluated 1 · Unmeasured 3 | `G8` `G9` `G10` `G11` |
| *Total* | 16 | | |

<!-- END GENERATED:capability-surface:unattached -->

Most are cross-cutting — identity, credentials and the control plane's own failure
modes apply to whichever path you pick. The host-action rows are not: they are actions
for which no mediation mechanism exists at all.

### What none of these paths gives you

- **A durable audit record from the SDK's own interceptor.** On the shipped path, a
  governed tool call through an SDK's interceptor does not produce one — a
  caller-supplied handler does receive the record, but the SDK wires nothing itself.
  That capability is *Planned* in ADR 0033 §6's sense: decided, not implemented,
  tracked as AAASM-5750, and carrying no capability claim until it lands. Audit
  evidence produced elsewhere in the system is a different question, and
  [Check a published claim](verify.md) is how to take any single sentence about it to
  its evidence.
- **A statement that an uninspected action was fine.** Where nothing inspected an
  action, the honest report is that nothing is known about it. An absent audit entry is
  a fact about the observer, not about the agent.
- **Coverage as a property of the architecture.** It is a per-host, per-launch fact.
  Two hosts running the same version can have different answers.
- **Anything from the managed service.** The Cloud control plane and the Enterprise
  operations features are documented as intent, carry the status map's 🗺️ **Planned**
  documentation-area label, and have no rows in the capability manifest. Nothing here
  should be read as saying either can be provisioned today.

## Deeper

The role model these three paths are named after, the caller table behind the control
plane's position, and the verified platform matrix are all in
[ADR 0033](https://docs.agent-assembly.com/core/latest/adr/0033-canonical-governance-and-enforcement-architecture.html)
in the Core documentation. The manifest this page is generated from is
[`governance/capability-manifest.yaml`](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/governance/capability-manifest.yaml).

> Generated content on this page is rendered by
> `docs/scripts/generate_capability_surface.py` from `capability-surface.toml`. Do not
> hand-edit between the `BEGIN`/`END GENERATED` markers — AAASM-5609.

---

*Last reviewed: 2026-08-13 — AI Agent Assembly Team*
