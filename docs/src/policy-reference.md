<!-- BEGIN AA-PAGE-META
schema_version: 1
page_type: guide
audience: [developer, operator]
user_job: Find the policy field or block you need in the Core reference
owner: L3:agent-assembly
canonical_source: https://docs.agent-assembly.com/core/latest/policy-reference.html
describes_capability: false
disclosure_levels: [1, 3]
deeper: https://docs.agent-assembly.com/core/latest/policy-reference.html
END AA-PAGE-META -->

# Policy Reference

The field-by-field policy reference is maintained in Core, generated from the
same schema `aa-gateway` validates against:
[Core policy reference](https://docs.agent-assembly.com/core/latest/policy-reference.html).
This page is a summary and a router to it — it does not restate field types,
defaults, or validation rules, so it cannot drift out of sync with the schema
the way a second hand-written copy can.

## What a policy document is

A policy is a YAML document that scopes what an agent may do — which domains
it can reach, which tools it can call, how much it can spend, and more. The
gateway evaluates it and returns an allow, deny, or rate-limit decision;
whether that decision is enforced before the action runs depends on which
path the request took — see [Security model](security-model.md) for the
per-path posture.

## Where each block is documented

| Block | What it controls | Core section |
|---|---|---|
| Document formats | Envelope vs. flat YAML | [Document formats](https://docs.agent-assembly.com/core/latest/policy-reference.html#document-formats) |
| Top-level fields, `scope` | Which agents a policy applies to, cascade order | [Top-level fields](https://docs.agent-assembly.com/core/latest/policy-reference.html#top-level-fields) |
| `network` | Outbound domain allowlisting | [`network`](https://docs.agent-assembly.com/core/latest/policy-reference.html#network) |
| `schedule` | Active-hours time windows | [`schedule`](https://docs.agent-assembly.com/core/latest/policy-reference.html#schedule) |
| <a id="budget"></a>`budget` | Spend caps, currency, reset behaviour | [`budget`](https://docs.agent-assembly.com/core/latest/policy-reference.html#budget) |
| `data` | Sensitive-data detection and redaction | [`data`](https://docs.agent-assembly.com/core/latest/policy-reference.html#data) |
| `tools` | Per-tool allow/deny/approval and rate limits | [`tools`](https://docs.agent-assembly.com/core/latest/policy-reference.html#tools) |
| `capabilities` | Coarse-grained capability grants | [`capabilities`](https://docs.agent-assembly.com/core/latest/policy-reference.html#capabilities) |
| `approval` | Escalation overrides | [`approval`](https://docs.agent-assembly.com/core/latest/policy-reference.html#approval) |

Core also documents `filesystem` and `syscalls` blocks (Linux host-level
scope) that this hub does not summarise separately — see
[`filesystem`](https://docs.agent-assembly.com/core/latest/policy-reference.html#filesystem)
and [`syscalls`](https://docs.agent-assembly.com/core/latest/policy-reference.html#syscalls)
in the Core reference.

## What this page does not cover

Field types, defaults, validation rules, and enumerated valid values live only
in the Core reference above — restating them here is exactly the duplication
that let this page fall out of sync with ADR 0033 §2/§4 on when a policy
decision actually binds before execution. If you need a field's type or
default, follow the link.

## Going deeper

For worked example policies (minimal budget-only, network allowlist,
capability control, rate-limiting with approval, business-hours schedule, PII
detection, and a full policy exercising every section), see
[Core's example policies](https://docs.agent-assembly.com/core/latest/policy-reference.html#three-complete-example-policies).

## Related documentation

- [Security model](security-model.md) — IronClaw layers and policy engine position in the stack
- [Managed control plane — design preview](cloud-deployment.md) — planned, not available
- [Managed SaaS onboarding — design preview](quickstart-saas.md) — planned, not available
