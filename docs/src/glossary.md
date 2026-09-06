# Glossary

Plain-language definitions of the terms and acronyms used across this
documentation. It exists so a first-time or non-specialist reader can decode
the security and architecture jargon without leaving the page they are on.

## Product concepts

**AI Agent Assembly (AAASM)**
: The product this hub documents: a governance layer that sits between your AI
agents and the outside world and enforces policy, tracks cost, and intercepts
unsafe actions before they run.

**Governance layer**
: The one-line description of what AI Agent Assembly *is* — a control that
evaluates and enforces what an agent is allowed to do, rather than only
observing what it did after the fact.

**Gateway (`aa-gateway`)**
: The central service that holds the agent registry, evaluates policy, and
tracks per-team budgets. Every interception mechanism reports to it.

**Agent**
: An autonomous or semi-autonomous program that calls tools, models, or
network services on your behalf — the thing AI Agent Assembly governs.

**Policy**
: A set of allow / deny / audit rules that decide whether an agent action is
permitted. See the [Policy reference](policy-reference.md).

**Policy-as-code**
: Expressing those rules as versioned YAML/JSON documents that can be reviewed
and deployed through normal Git workflows, instead of clicking through a UI.

**Budget**
: A per-team cap on token or dollar spend. When exceeded, the gateway can deny
further agent calls.

## Interception mechanisms

**SDK layer**
: In-process governance: the language SDK wraps your agent's calls and asks the
gateway for a decision. It is **advisory** — *Evaluated*, not *Denied before
execution* — since whether a refusal actually holds depends on the calling
shim honouring the answer. See [Security model](security-model.md).

**Sidecar proxy (`aa-proxy`)**
: A companion process that intercepts an agent's outbound HTTPS traffic to
enforce policy without changing the agent's code.

**eBPF sensor (`aa-ebpf`)**
: A kernel-level sensor (Linux only) that watches TLS libraries and process
syscalls and *reports* what it sees. Observe-only: it returns no verdict, blocks
nothing, and is consulted in no allow/deny decision, so it observes and detects
rather than preventing. It is deployed on its own, not as a tier the other
mechanisms fall back to.

## Security & identity terms

**eBPF** (extended Berkeley Packet Filter)
: A Linux kernel technology for safely running small sandboxed programs inside
the kernel to observe or filter events, without modifying kernel source.

**uprobe** (user-space probe)
: An eBPF hook attached to a function in a user-space library (for example, an
SSL library) so the sensor can observe calls at that point.

**Sidecar**
: A deployment pattern where a helper process runs alongside your application
and handles a cross-cutting concern (here, traffic interception).

**MitM** (man-in-the-middle)
: Sitting in the path of a connection to inspect or control it. The proxy
performs *authorized* MitM of an agent's HTTPS using a per-host certificate
authority so it can apply egress policy.

**mTLS** (mutual TLS)
: TLS where **both** the client and the server present certificates, so each
side cryptographically verifies the other's identity.

**STRIDE**
: A threat-modeling framework categorizing risks as Spoofing, Tampering,
Repudiation, Information disclosure, Denial of service, and Elevation of
privilege. Used in the [Security model](security-model.md).

**SCIM** (System for Cross-domain Identity Management)
: A standard protocol for automatically provisioning and de-provisioning users
and groups from your identity provider into an application.
🗺️ **Planned — not implemented in AI Agent Assembly.** Listed here as a term you
will meet in identity tooling, not as a capability that ships.

**SSO / SAML 2.0 / OIDC**
: Single sign-on and the two federation protocols (SAML 2.0 and OpenID
Connect) that let operators log in with an enterprise identity provider.
🗺️ **Planned — not implemented in AI Agent Assembly.** There is no SSO
implementation in `aa-api`, `aa-gateway`, or `aa-auth`, and no console to sign
in to; operators authenticate with an API key or a JWT. Do not plan an IdP
integration against it — see
[Authentication flow](security-model.md#authentication-flow).

**Ed25519**
: A modern public-key signature algorithm. Used here for the **one-time
possession proof** an agent presents at registration — a signature over a
server-issued nonce. It is not a reusable bearer credential: subsequent calls
carry a random credential token instead. See the
[Security model](security-model.md#cryptographic-primitives).

**AES-256-GCM**
: A symmetric authenticated-encryption algorithm.
🗺️ **AI Agent Assembly does not use it.** This entry previously described it as encrypting stored secrets at
rest; there is no AES-256-GCM implementation in the workspace crates, no HSM or
KMS integration, and no managed secret vault. **Do not treat this stack as a
secret store** — see [Secrets management](security-model.md#secrets-management).
The term is retained here only so a reader who met the old claim can find its
correction.

**HMAC-SHA256**
: A keyed hash. Used here for the REST/admin session JWT, and to **verify
inbound** audit webhooks received from SaaS coding-agent providers — there is no
outbound webhook signing path. It is **not** used on audit-log entries: there is
no log-signing key anywhere in the codebase; see **Audit log** below.

**IronClaw five-layer defense**
: The name for AI Agent Assembly's defense-in-depth model — five security
*layers* (Boundary, Identity, Policy, Vault, Telemetry). These are distinct
from the *interception mechanisms* (SDK, proxy, eBPF), which each live inside
the Boundary layer and are deployed independently of one another. **The Vault layer is largely aspirational:** an in-memory
secrets store is mounted but is empty in every shipped build with nothing able to
populate it, there is no encryption at rest or key management, and where
resolution does succeed the plaintext is returned to the caller. See
[Secrets management](security-model.md#secrets-management).

**Audit log**
: The record of policy decisions and agent-reported events, written to
JSON Lines files, with database tables holding a queryable mirror. A shipped
gateway writes **one fixed `gateway-default.jsonl`**, not per-session files.
Four bounds matter and are easy to assume away: the JSONL files are chained with
an **unkeyed** SHA-256 digest (verify with `aasm audit verify-chain`), so the
chain detects casual edits but not an actor who can rewrite the file and re-chain
it; the database mirror carries **no** chain metadata and cannot be verified;
the log is append-only **by convention**, not by an enforced constraint; and
emission is **best-effort**, so an entry can be dropped under backpressure and
budget debits produce none at all. Absence of an entry is not proof that an
action did not occur. See [Audit log](security-model.md#audit-log) for the full
statement.
