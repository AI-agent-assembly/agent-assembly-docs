<!-- BEGIN AA-PAGE-META
schema_version: 1
page_type: guide
audience: [developer]
user_job: Choose the SDK for the language my agent is written in and reach its documentation
owner: L2:docs
canonical_source: self
describes_capability: false
disclosure_levels: [1, 3]
deeper: https://docs.agent-assembly.com/core/
END AA-PAGE-META -->

# Choose your SDK

Pick the SDK for the language your agent is already written in; this page hands you to
that SDK's own documentation, which is where every install step and API surface lives.

## Choose your language

Each SDK is a separately versioned program with its own documentation site and its own
version selector.

| Language | SDK documentation | Content layer | Component | Documentation-area maturity |
| --- | --- | --- | --- | --- |
| Python | [Python SDK docs](https://docs.agent-assembly.com/python-sdk/) | L3 | `python-sdk` | 🧪 Release candidate |
| TypeScript / JavaScript | [Node SDK docs](https://docs.agent-assembly.com/node-sdk/) | L3 | `node-sdk` | 🧪 Release candidate |
| Go | [Go SDK docs](https://docs.agent-assembly.com/go-sdk/) | L3 | `go-sdk` | 🧪 Release candidate |

Prefer reading working code first? The
[runnable examples](https://github.com/ai-agent-assembly/examples) carry end-to-end
walk-throughs for all three languages.

### Two different words spelled the same way

The **Documentation-area maturity** column above is the maturity of a *documentation
area*, read from the [status map](source-of-truth.md), which defines what each label
means. That page owns the definitions and this one does not restate them.

It is **not** a statement about what happens to one of your agent's actions. That is a
separate vocabulary, defined once in ADR 0033 §6, and this page makes no claim in it.
[Verify](verify.md) is the page that maps a published sentence onto that vocabulary.

## Before you choose

Choosing a language is not the same decision as choosing *where* a decision about an
action is made, and the second one is made before this page rather than on it. It is an
evaluation decision: [Choose your enforcement path](choose-your-enforcement-path.md)
is where it is made, and [Evaluate](product-promise.md) carries the default posture.

## What this page does not do

This page is a router, and it is deliberately thin:

- **It does not carry install steps or an API surface.** Those belong to each SDK's own
  documentation, which is the canonical source for them, and duplicating them here is
  how the copies drift apart.
- **It does not describe a mechanism.** What a given component does with an action is
  documented at depth in the [core documentation](https://docs.agent-assembly.com/core/).
- **It does not cover running the stack.** That is [Operate](operate.md).
- **It does not cover checking a published statement.** That is [Verify](verify.md).

## Going deeper

The contract every SDK speaks to, and the components behind it, are documented in the
[core documentation](https://docs.agent-assembly.com/core/).
