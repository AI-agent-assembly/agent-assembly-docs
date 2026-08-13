<!-- BEGIN AA-PAGE-META
schema_version: 1
page_type: guide
audience: [evaluator, security-engineer]
user_job: Find out what is available today before I plan an integration
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
limitations: "#what-this-page-does-not-answer"
disclosure_levels: [1, 3]
deeper: https://docs.agent-assembly.com/core/latest/adr/0033-canonical-governance-and-enforcement-architecture.html
END AA-PAGE-META -->

# What ships today

## What governs this page

This page is an **inventory**, not a promise. It answers one question — *what is
available right now, and on what evidence* — and it answers it from a machine-readable
source rather than from prose.

| Source | What it decides for this page |
|---|---|
| The capability and evidence manifest (AAASM-5531), in the `agent-assembly` repository | Every row in every table below. Nothing inside a generated block is hand-written |
| [ADR 0033 §6](https://docs.agent-assembly.com/core/latest/adr/0033-canonical-governance-and-enforcement-architecture.html) | The eleven words for what the product did to an action. This page prints them and does not define them — [Check a published claim](verify.md) names them and links their definitions |
| [Product promise](product-promise.md) | The approved wording, the default-posture table, and which term each mechanism reaches. This page does not restate any of the three |
| [Source of truth & status](source-of-truth.md) | Which repository owns an area of documentation, and how finished that area is |

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

> **Two different words are spelled *Planned*, and this page prints one of them.**
> In the tables below it is [ADR 0033 §6](https://docs.agent-assembly.com/core/latest/adr/0033-canonical-governance-and-enforcement-architecture.html)'s
> term, about **an action**: decided but not implemented, carrying a ticket reference
> and no capability claim. The 🗺️ **Planned** beside a page title in the sidebar is a
> **documentation-area** label from the [status map](source-of-truth.md), about how
> finished an area of this documentation is. Neither licenses a conclusion about the
> other: a `🧪 Release candidate` area can be *Unsupported* on a platform, and a
> shipped feature can be *Unmeasured* on a path.

## Level 1 — one sentence

Agent Assembly ships a governance decision point and an evidence trail for actions you
have routed onto a governed path, on Linux and macOS, and this page lists what each
area reaches and where it stops.

## Level 3 — for an evaluator

### What each claim term covers today

Every manifest row carries exactly one ADR 0033 §6 term. Two of §6's eleven have **no
row at all**, and that is shown rather than left out — their absence is a fact about
the manifest, not a hole in this table.

<!-- BEGIN GENERATED:capability-surface:terms -->

| ADR 0033 §6 term | Rows | Areas | Capability ids |
|---|---|---|---|
| **Observed** | 5 | Developer-tool launch, Host actions, Platform host-level interception, SDK and framework seams | `S3` `S4` `H4` `L5` `P2` |
| **Detected** | 2 | Credentials, Host actions | `H2` `C6` |
| **Evaluated** | 11 | Degraded and failure modes, Identity and attribution, Network traffic, SDK and framework seams | `S6` `S9` `S13` `N4` `I1` `I2` `I3` `I5` `I7` `G5` `G8` |
| **Denied before execution** | 13 | Degraded and failure modes, Developer-tool launch, Host actions, MCP, Network traffic, SDK and framework seams | `S1` `S2` `S5` `S8` `H5` `N1` `N2` `N3` `M1` `M3` `L1` `G1` `G3` |
| **Redacted** | 5 | Credentials, Degraded and failure modes, MCP, Network traffic | `N7` `M9` `C1` `C2` `G4` |
| **Approval required** | 0 | — | — *no row in the manifest carries this term* |
| **Degraded** | 1 | Degraded and failure modes | `G6` |
| **Unmeasured** | 36 | Credentials, Degraded and failure modes, Developer-tool launch, Host actions, Identity and attribution, MCP, Network traffic, SDK and framework seams | `S7` `S10` `S11` `S12` `H1` `H3` `H6` `H7` `H8` `N5` `N6` `N9` `N10` `N12` `N13` `M2` `M4` `M5` `M6` `M7` `M10` `L2` `L3` `L6` `L7` `L8` `C3` `C4` `C5` `I4` `I6` `G2` `G7` `G9` `G10` `G11` |
| **Experimental** | 1 | Platform host-level interception | `P1` |
| **Planned** | 0 | — | — *no row in the manifest carries this term* |
| **Unsupported** | 6 | Developer-tool launch, MCP, Network traffic, Platform host-level interception | `N8` `N11` `M8` `L4` `P3` `P4` |
| *Total* | 80 | | |

<!-- END GENERATED:capability-surface:terms -->

*Approval required* having no row does not mean approvals are absent from the product;
it means no capability row's outcome is recorded as that term. *Planned* having no row
is what §6 asks for: the term carries a ticket reference and no capability claim, so it
belongs beside a ticket rather than in an inventory of what exists.

### Where those outcomes sit

<!-- BEGIN GENERATED:capability-surface:areas -->

| Area | Rows | Outcomes its rows reach today |
|---|---|---|
| SDK and framework seams (`sdk`) | 13 | Observed 2 · Evaluated 3 · Denied before execution 4 · Unmeasured 4 |
| Network traffic (`network`) | 13 | Evaluated 1 · Denied before execution 3 · Redacted 1 · Unmeasured 6 · Unsupported 2 |
| MCP (`mcp`) | 10 | Denied before execution 2 · Redacted 1 · Unmeasured 6 · Unsupported 1 |
| Host actions (`host_action`) | 8 | Observed 1 · Detected 1 · Denied before execution 1 · Unmeasured 5 |
| Developer-tool launch (`devtool_launch`) | 8 | Observed 1 · Denied before execution 1 · Unmeasured 5 · Unsupported 1 |
| Credentials (`credentials`) | 6 | Detected 1 · Redacted 2 · Unmeasured 3 |
| Identity and attribution (`identity`) | 7 | Evaluated 5 · Unmeasured 2 |
| Degraded and failure modes (`degraded_mode`) | 11 | Evaluated 2 · Denied before execution 2 · Redacted 1 · Degraded 1 · Unmeasured 5 |
| Platform host-level interception (`platform`) | 4 | Observed 1 · Experimental 1 · Unsupported 2 |

<!-- END GENERATED:capability-surface:areas -->

*Host actions* are shell and subprocess, files, browser automation and database
queries. The other area names carry their scope on their face; the manifest's own enum
value is printed beside each so a rename cannot hide in a display label.

Read the counts as counts of **manifest rows**, not of features and not of code paths.
A row is one question the manifest asked and answered; an area with more rows was
examined in more places, not necessarily covered in more places. The per-mechanism
version of this question — which term each named mechanism reaches — is
[Product promise](product-promise.md)'s, and is not repeated here.

### Platforms

Host-level interception is **per platform**, and a platform without an adapter has
none. There is no lower mechanism that picks up what an absent one would have done, and
eBPF is one Linux mechanism rather than a cross-platform floor.

<!-- BEGIN GENERATED:capability-surface:platforms -->

| Platform | Capability rows released on it | Host-level interception today | Reachability of that row |
|---|---|---|---|
| **Linux x86_64** | 71 | Experimental (`P1`) | shipped on crates.io only |
| **Linux aarch64** | 70 | Observed (`P2`) | shipped on crates.io only |
| **macOS** | 64 | Unsupported (`P3`) | shipped on crates.io only |
| **Windows** | 13 | Unsupported (`P4`) | no mechanism exists |

<!-- END GENERATED:capability-surface:platforms -->

The authoritative platform matrix — including what transport mediation reaches on each
platform, and the macOS row, which ends with an instruction not to read it as *no host
enforcement on macOS* — is
[ADR 0033 §5.3](https://docs.agent-assembly.com/core/latest/adr/0033-canonical-governance-and-enforcement-architecture.html).
The table above is the manifest's view of the same question and defers to it.

### Where the artifacts come from

Distribution is per channel **and** per platform: a capability can ship on one channel
and not another, and *absent from a list* is not the same statement as *not shipped
there*. The manifest can record the second only for the container-image channel today.
That mechanism was added by AAASM-5680 and has not been extended to the other seven.

<!-- BEGIN GENERATED:capability-surface:channels -->

| Channel | Rows delivered on it | Rows recorded as not published there | Rows recorded as not surveyed |
|---|---|---|---|
| GitHub Release assets (`github_release`) | 50 | — *not recorded* | — *not recorded* |
| Homebrew tap (`homebrew`) | 50 | — *not recorded* | — *not recorded* |
| Install script (`install_script`) | 50 | — *not recorded* | — *not recorded* |
| crates.io (`crates_io`) | 73 | — *not recorded* | — *not recorded* |
| PyPI (`pypi`) | 13 | — *not recorded* | — *not recorded* |
| npm (`npm`) | 13 | — *not recorded* | — *not recorded* |
| Go modules (`go_modules`) | 13 | — *not recorded* | — *not recorded* |
| GHCR container images (`ghcr`) | 24 | 32 | 17 |
| No distribution question (`not_applicable`) | 7 | — *not recorded* | — *not recorded* |

Channels the manifest surveyed: `github_release`, `homebrew`, `install_script`, `crates_io`, `pypi`, `npm`, `go_modules`, `ghcr`, `not_applicable`. Channels it did not survey: none.

<!-- END GENERATED:capability-surface:channels -->

So on every channel except `ghcr`, a row that does not list a channel is telling you
only that it does not list it. Do not read a *not recorded* cell as a zero. Which
container images exist, and how their tags move, is
[Docker & containers](docker-containers.md)'s.

### What stands behind the rows

A capability row is worth what its evidence is worth. The manifest separates a test it
can point at from a test it was told exists but could not locate, and separates both
from a recorded gap — then separates all three from whether that evidence actually runs.

<!-- BEGIN GENERATED:capability-surface:evidence -->

| What stands behind the row | Rows |
|---|---|
| At least a located test | 26 |
| No located test, but a test asserted but not locatable from the manifest's repository | 10 |
| A recorded gap — no test | 44 |

| Does that evidence run? | Rows |
|---|---|
| It runs on every push to `main` | 42 |
| It is path-gated, with a schedule | 5 |
| It does not run | 33 |

<!-- END GENERATED:capability-surface:evidence -->

A recorded gap is not a silence. It is the manifest saying, in the row itself, that no
test backs this and why. To take any single published sentence to the evidence behind
it, start at [Check a published claim](verify.md).

### What this page does not answer

- **Whether a control is on.** Shipping, buildable and activated are three separate
  questions. A capability can be in an artifact you installed and still be off, or
  reachable only when an environment variable names a process.
- **Whether your agent is on a governed path.** Coverage is a per-host, per-launch
  fact rather than a property of the architecture. Start at
  [Choose your enforcement path](choose-your-enforcement-path.md).
- **What a term means.** ADR 0033 §6 defines the vocabulary; this page prints it.
- **How finished an area of documentation is.** That is the status map's maturity
  label, on a different axis from anything here.
- **Whether the extract is current with the manifest.** This repository's CI proves the
  pages match the extract. Nothing here proves the extract matches upstream; that check
  is AAASM-5600.

### The managed service is not in these numbers

The **Cloud** control plane and the **Enterprise** operations features are documented as
intent. Their documentation areas carry the status map's 🗺️ **Planned** label, they have
no rows in the capability manifest, and nothing on this page should be read as saying
that either can be provisioned or operated today. What is written about them describes
a design. Where the line between the open and the commercial side falls is the
[Open core boundary](open-core-boundary.md)'s to state.

## Deeper

The implementation-level answer — which crate does what, at which source line, and the
highest term each mechanism can legitimately reach — is
[ADR 0033](https://docs.agent-assembly.com/core/latest/adr/0033-canonical-governance-and-enforcement-architecture.html)
in the Core documentation. The manifest this page is generated from is
[`governance/capability-manifest.yaml`](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/governance/capability-manifest.yaml).

> Generated content on this page is rendered by
> `docs/scripts/generate_capability_surface.py` from `capability-surface.toml`. Do not
> hand-edit between the `BEGIN`/`END GENERATED` markers — AAASM-5609.

---

*Last reviewed: 2026-08-13 — AI Agent Assembly Team*
