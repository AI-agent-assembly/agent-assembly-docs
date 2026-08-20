<!-- BEGIN AA-PAGE-META
schema_version: 1
page_type: reference
audience: [evaluator, developer, operator, security-engineer, auditor]
user_job: Look up one capability's real support, coverage and protection state
owner: L2:docs
canonical_source: self
describes_capability: false
disclosure_levels: [3, 4]
END AA-PAGE-META -->

# Capability & protection status

This page is generated, row for row, from
[`governance/capability-manifest.yaml`](https://github.com/ai-agent-assembly/agent-assembly/blob/HEAD/governance/capability-manifest.yaml)
in the `agent-assembly` monorepo — ADR 0034's layer T2, the strongest layer any page
on this hub (T5) may draw from. It does not restate or interpret those rows in prose;
it renders them, so nothing here can broaden what the manifest itself claims (ADR 0034
Decision 2).

Every row is shown, including rows carrying `Unsupported` or `Unmeasured` coverage and
`Not applicable` or `Not measured` protection state — those are the manifest's own
answer for that capability, not an omission.

## What the columns mean

- **Coverage** — behaviour on evidence, ADR 0033 §6's closed eleven-term vocabulary
  (`Observed`, `Detected`, `Evaluated`, `Denied before execution`, `Redacted`,
  `Approval required`, `Degraded`, `Unmeasured`, `Experimental`, `Planned`,
  `Unsupported`). One action, one host, one time.
- **Protection state** — ADR 0030 §4.1's integration ladder for one dev-tool
  integration on one host: whether agent-assembly is installed, integrated and
  enforcing there at all. Distinct from coverage — a row can be `Integrated` and still
  carry no coverage evidence; see the manifest's own `governance/README.md` "Three
  axes, three owners" section.
- **Released channels** / **Platform** — where the artifact that delivers this row's
  capability is actually obtained, and on which platform families. Never a promise
  about what happens once installed — that's coverage and protection state.

These three are never mixed into one cell. A capability can be released everywhere,
integrated nowhere, and denied-before-execution on the one platform it does run —
each of those is a separate, independently true statement, and folding them together
would make one of the three appear to certify the others.

## Provenance

<!-- BEGIN GENERATED:capability-manifest:provenance -->

- **Manifest version:** `1.0.0`
- **Ticket:** AAASM-5531
- **Fix version:** agent-assembly v0.0.1-rc.7
- **Extract taken at commit:** `e2730ddaf422`
- **Evidence surveyed at:** `299de38830b5` (2026-08-06)

<!-- END GENERATED:capability-manifest:provenance -->

The **evidence surveyed at** commit is not this page's own commit — it is the point in
`agent-assembly`'s history the manifest's rows were last verified against. A row is
only as current as that commit, regardless of when this page itself was last
regenerated.

## Capability table

<!-- BEGIN GENERATED:capability-manifest:table -->

| ID | Capability | Owner | Framework / tool | Platform | Released channels | Coverage | Protection state |
|---|---|---|---|---|---|---|---|
| C1 | Outbound credential scan and redact on an inspected request | aa-security | aa-proxy, aa-security | linux, macos | crates_io, github_release, homebrew, install_script | Redacted | Not applicable |
| C2 | Credential substitution at egress — the real provider key never enters the agent | aa-proxy | aa-proxy | linux, macos | crates_io, github_release, homebrew, install_script | Redacted | Not applicable |
| C3 | Credential injection via SecretsService.DispatchTool | aa-api | aa-api, aa-gateway | linux, macos, windows | crates_io, github_release, homebrew, install_script | Unmeasured | Not applicable |
| C4 | Model response credential scanning | aa-proxy | aa-proxy | linux, macos | crates_io, github_release, homebrew, install_script | Unmeasured | Not applicable |
| C5 | Environment inheritance by aasm run | aa-cli | aa-cli | linux, macos, windows | crates_io, ghcr, github_release, homebrew, install_script | Unmeasured | Not applicable |
| C6 | Credential scanner recall | aa-security | aa-security | linux, macos, windows | crates_io, github_release, homebrew, install_script | Detected | Not applicable |
| G1 | aa-runtime to gateway unreachable on a policy query | aa-runtime | aa-runtime | linux, macos, windows | crates_io, ghcr, github_release, homebrew, install_script | Denied before execution | Not applicable |
| G10 | Audit emission failure | aa-gateway | aa-gateway | linux, macos, windows | crates_io, ghcr, github_release, homebrew, install_script | Unmeasured | Not applicable |
| G11 | Degradation visibility to a user | aa-runtime | aa-api, aa-runtime, dashboard | linux, macos, windows | crates_io, ghcr, github_release, homebrew, install_script | Unmeasured | Not applicable |
| G2 | aa-runtime with no gateway configured, or fail_closed=false | aa-runtime | aa-runtime | linux, macos, windows | crates_io, ghcr, github_release, homebrew, install_script | Unmeasured | Not applicable |
| G3 | aa-proxy to gateway unreachable for MCP adjudication | aa-proxy | aa-proxy | linux, macos | crates_io, github_release, homebrew, install_script | Denied before execution | Not applicable |
| G4 | Credential and DLP default action | aa-proxy | aa-proxy | linux, macos | crates_io, github_release, homebrew, install_script | Redacted | Not applicable |
| G5 | SDK cannot reach the aa-runtime UDS socket | SDK fail-closed posture on an unreachable runtime | go-sdk, node-sdk, python-sdk | linux, macos, windows | crates_io, ghcr, go_modules, npm, pypi | Evaluated | Not applicable |
| G6 | eBPF load or attach failure | aa-runtime | aa-ebpf, aa-runtime | linux | crates_io | Degraded | Not applicable |
| G7 | eBPF policy file unreadable or unparseable | aa-runtime | aa-runtime | linux | crates_io | Unmeasured | Not applicable |
| G8 | Gateway policy load or schema failure | aa-gateway | aa-gateway, aa-runtime | linux, macos, windows | crates_io, ghcr, github_release, homebrew, install_script | Evaluated | Not applicable |
| G9 | Budget state unreadable or corrupt | aa-gateway | aa-gateway | linux, macos, windows | crates_io, ghcr, github_release, homebrew, install_script | Unmeasured | Not applicable |
| L1 | Claude Code managed launch | aa-devtool-claude-code | claude_code | macos | crates_io, github_release, homebrew, install_script | Denied before execution | Host-enforced |
| L2 | Codex managed launch | aa-devtool-codex | codex | linux, macos | crates_io, github_release, homebrew, install_script | Unmeasured | Integrated |
| L3 | Windsurf managed launch | aa-devtool-windsurf | windsurf | linux, macos | crates_io, github_release, homebrew, install_script | Unmeasured | Integrated |
| L4 | Copilot managed launch | aa-devtool-copilot | github_copilot | linux, macos, windows | crates_io, github_release, homebrew, install_script | Unsupported | Integrated |
| L5 | SaaS / opaque agent | aa-devtool-saas | claude_ai_and_siblings | not_applicable | crates_io, github_release, homebrew, install_script | Observed | Not measured |
| L6 | Unmanaged launch — the user starts the tool directly | none | any | linux, macos, windows | crates_io, github_release, homebrew, install_script | Unmeasured | Not applicable |
| L7 | Settings-layer governance surviving an unmanaged launch | aa-devtool-claude-code | claude_code | macos | crates_io, github_release, homebrew, install_script | Unmeasured | Integrated |
| L8 | aasm run --no-proxy | aa-cli | any | linux, macos, windows | crates_io, ghcr, github_release, homebrew, install_script | Unmeasured | Not applicable |
| H1 | Shell command / subprocess spawn by a native agent process | none | any | linux, macos, windows | not_applicable | Unmeasured | Not applicable |
| H2 | Shell command intercepted by the eBPF syscall guard | aa-ebpf-probes | any | linux_aarch64, linux_x86_64 | crates_io | Detected | Not applicable |
| H3 | Process exec observation | aa-ebpf-probes | any | linux_aarch64, linux_x86_64 | crates_io | Unmeasured | Not applicable |
| H4 | File read / write / unlink observation | aa-ebpf | any | linux_x86_64 | crates_io | Observed | Not applicable |
| H5 | File access by a WASM-marked tool | aa-sandbox | aa-sandbox | linux, macos, windows | crates_io, github_release, homebrew, install_script | Denied before execution | Not applicable |
| H6 | Browser action (Playwright / Selenium / Puppeteer) | none | any | linux, macos, windows | not_applicable | Unmeasured | Not applicable |
| H7 | Database query | none | any | linux, macos, windows | not_applicable | Unmeasured | Not applicable |
| H8 | Shell / file rule declared in a tool's own settings file | aa-devtool-claude-code | claude_code | macos | crates_io, github_release, homebrew, install_script | Unmeasured | Integrated |
| I1 | Agent identity — Ed25519 did:key with a possession proof | aa-sdk-client | aa-gateway, aa-sdk-client | linux, macos, windows | crates_io, github_release, homebrew, install_script | Evaluated | Not applicable |
| I2 | Transport key for the runtime UDS handshake | aa-sdk-client | aa-runtime, aa-sdk-client | linux, macos | crates_io, github_release, homebrew, install_script | Evaluated | Not applicable |
| I3 | Sub-agent / delegation lineage | aa-core | aa-gateway | linux, macos, windows | crates_io, ghcr, github_release, homebrew, install_script | Evaluated | Not applicable |
| I4 | Process-tree identity across fork/exec | aa-ebpf-probes | aa-ebpf, aa-runtime | linux | crates_io | Unmeasured | Not applicable |
| I5 | Tenant / org isolation | aa-gateway | aa-gateway, aa-storage-memory, aa-storage-postgres, aa-storage-sqlite | linux, macos, windows | crates_io, ghcr, github_release, homebrew, install_script | Evaluated | Not applicable |
| I6 | Agent attribution of proxy traffic | none | aa-proxy | linux, macos | crates_io, github_release, homebrew, install_script | Unmeasured | Not applicable |
| I7 | Gateway agent-plane authentication | aa-gateway | aa-gateway | linux, macos, windows | crates_io, ghcr, github_release, homebrew, install_script | Evaluated | Not applicable |
| M1 | MCP tools/call adjudication by the control plane | aa-proxy | any_mcp_client | linux, macos | crates_io, github_release, homebrew, install_script | Denied before execution | Not applicable |
| M10 | MCP-server governance by configuration | aa-devtool-claude-code | claude_code, copilot, windsurf | linux, macos, windows | crates_io, github_release, homebrew, install_script | Unmeasured | Integrated |
| M2 | MCP enforcement with no gateway configured | none | any_mcp_client | linux, macos | crates_io, github_release, homebrew, install_script | Unmeasured | Not applicable |
| M3 | JSON-RPC batch array or malformed envelope carrying tools/call | aa-proxy | any_mcp_client | linux, macos | crates_io, github_release, homebrew, install_script | Denied before execution | Not applicable |
| M4 | Every MCP method other than tools/call | none | any_mcp_client | linux, macos | crates_io, github_release, homebrew, install_script | Unmeasured | Not applicable |
| M5 | MCP over stdio (subprocess pipes) | none | any_mcp_client | linux, macos, windows | not_applicable | Unmeasured | Not applicable |
| M6 | MCP over SSE (text/event-stream) | none | any_mcp_client | linux, macos | not_applicable | Unmeasured | Not applicable |
| M7 | MCP over Streamable HTTP | aa-proxy | any_mcp_client | linux, macos | crates_io, github_release, homebrew, install_script | Unmeasured | Not applicable |
| M8 | MCP over WebSocket | none | any_mcp_client | linux, macos | not_applicable | Unsupported | Not applicable |
| M9 | MCP on a built-in LLM host | none | any_mcp_client | linux, macos | crates_io, github_release, homebrew, install_script | Redacted | Not applicable |
| N1 | CONNECT-time egress allow/deny | aa-proxy | aa-proxy | linux, macos | crates_io, github_release, homebrew, install_script | Denied before execution | Not applicable |
| N10 | Raw TCP that does not speak the proxy protocol | none | any | linux, macos, windows | crates_io, github_release, homebrew, install_script | Unmeasured | Not applicable |
| N11 | UDP, QUIC, HTTP/3 | none | any | linux, macos, windows | crates_io, github_release, homebrew, install_script | Unsupported | Not applicable |
| N12 | Local IPC (Unix domain sockets) between third-party processes | none | any | linux, macos | crates_io, github_release, homebrew, install_script | Unmeasured | Not applicable |
| N13 | TLS plaintext observation without the proxy | aa-ebpf-probes | aa-ebpf | linux_aarch64, linux_x86_64 | crates_io | Unmeasured | Not applicable |
| N2 | SSRF guard | aa-proxy | aa-proxy | linux, macos | crates_io, github_release, homebrew, install_script | Denied before execution | Not applicable |
| N3 | HTTPS payload inspection and credential DLP on the built-in LLM hosts | aa-proxy | aa-proxy | linux, macos | crates_io, github_release, homebrew, install_script | Denied before execution | Not applicable |
| N4 | HTTPS payload inspection on any other host | aa-proxy | aa-proxy | linux, macos | crates_io, github_release, homebrew, install_script | Evaluated | Not applicable |
| N5 | HTTPS to a host not under MitM | aa-proxy | aa-proxy | linux, macos | crates_io, github_release, homebrew, install_script | Unmeasured | Not applicable |
| N6 | Model response body scanning on LLM hosts | none | aa-proxy | linux, macos | crates_io, github_release, homebrew, install_script | Unmeasured | Not applicable |
| N7 | Plain http:// request | aa-proxy | aa-proxy | linux, macos | crates_io, github_release, homebrew, install_script | Redacted | Not applicable |
| N8 | HTTP/2, gRPC or WebSocket over a MitM'd host | none | aa-proxy | linux, macos | crates_io, github_release, homebrew, install_script | Unsupported | Not applicable |
| N9 | Chunked transfer encoding | aa-proxy | aa-proxy | linux, macos | crates_io, github_release, homebrew, install_script | Unmeasured | Not applicable |
| P1 | Linux x86_64 host-level interception | aa-proxy | aa-ebpf, aa-proxy | linux_x86_64 | crates_io | Experimental | Not applicable |
| P2 | Linux aarch64 host-level interception | aa-proxy | aa-ebpf, aa-proxy | linux_aarch64 | crates_io | Observed | Not applicable |
| P3 | macOS host-level interception | aa-proxy | aa-devtool-claude-code, aa-proxy | macos | crates_io | Unsupported | Integrated |
| P4 | Windows mediation | none | not_applicable | windows | not_applicable | Unsupported | Not installed |
| S1 | Wrapped framework tool call, deny raised before the tool body | python-sdk | google_adk, langchain_handler, mcp_client_session, microsoft_agent_framework, pydantic_ai | linux, macos, windows | crates_io, ghcr, go_modules, npm, pypi | Denied before execution | Not applicable |
| S10 | Direct function call that does not pass a patched seam | none | any | linux, macos, windows | crates_io, ghcr, go_modules, npm, pypi | Unmeasured | Not applicable |
| S11 | Framework with no adapter | none | any_unadapted | linux, macos, windows | crates_io, ghcr, go_modules, npm, pypi | Unmeasured | Not applicable |
| S12 | Raw HTTP, subprocess, filesystem, DB driver, browser automation from inside an SDK-adopting process | none | any | linux, macos, windows | crates_io, ghcr, go_modules, npm, pypi | Unmeasured | Not applicable |
| S13 | The SDK honouring a Deny it received | aa-sdk-client | aa-sdk-client | linux, macos, windows | crates_io, github_release, homebrew, install_script | Evaluated | Not applicable |
| S2 | Wrapped framework tool call, deny returned as a sentinel string | python-sdk | agno, crewai, haystack, llamaindex, openai_agents, smolagents | linux, macos, windows | crates_io, ghcr, go_modules, npm, pypi | Denied before execution | Not applicable |
| S3 | Graph / workflow node execution | python-sdk | langgraph, mastra | linux, macos, windows | crates_io, ghcr, go_modules, npm, pypi | Observed | Not applicable |
| S4 | LangChain tool call via the callback handler | node-sdk | @langchain/core | linux, macos, windows | crates_io, ghcr, go_modules, npm, pypi | Observed | Not applicable |
| S5 | LangChain tool call via the explicit wrapper | node-sdk | @langchain/core | linux, macos, windows | crates_io, ghcr, go_modules, npm, pypi | Denied before execution | Not applicable |
| S6 | Vercel AI SDK / OpenAI Agents tool call | node-sdk | @openai/agents, ai | linux, macos, windows | crates_io, ghcr, go_modules, npm, pypi | Evaluated | Not applicable |
| S7 | Node default mode routes every policy check through an allow-all no-op client | node-sdk | all_node_frameworks | linux, macos, windows | crates_io, ghcr, go_modules, npm, pypi | Unmeasured | Not applicable |
| S8 | Wrapped tool call, Go | go-sdk | any | linux, macos, windows | crates_io, ghcr, go_modules, npm, pypi | Denied before execution | Not applicable |
| S9 | Go default build without -tags aa_ffi_go and CGO | go-sdk | any | linux, macos, windows | crates_io, ghcr, go_modules, npm, pypi | Evaluated | Not applicable |

<!-- END GENERATED:capability-manifest:table -->

<!-- The two blocks above are generated from governance/capability-manifest.yaml
     (ai-agent-assembly/agent-assembly) by docs/scripts/generate_capability_tables.py
     — do not hand-edit between the BEGIN/END GENERATED markers. See AAASM-5600. -->

## Unknown capability references

A page elsewhere in this hub that cites a manifest row (a `capability_ids` entry in
its own metadata block, per [Page standards](page-standards.md)) is checked against
this same manifest by
[`docs/scripts/validate_capability_ids.py`](https://github.com/ai-agent-assembly/docs/blob/HEAD/docs/scripts/validate_capability_ids.py) —
a reference to an id that does not resolve to a row here fails CI rather than
publishing silently.

---

*This page is regenerated from the capability manifest, not hand-edited — see
[Page standards](page-standards.md) for the metadata block every hub page carries.*
