<!-- BEGIN AA-PAGE-META
schema_version: 1
page_type: guide
audience: [operator]
user_job: Run the stack on a host and work out why a control did not fire
owner: L2:docs
canonical_source: self
describes_capability: false
disclosure_levels: [1, 3]
deeper: https://docs.agent-assembly.com/core/
END AA-PAGE-META -->

# Run and diagnose

This section routes you through running the stack on a host you control, from starting
an agent under it to working out why an expected control did not fire; the commands and
configuration themselves live in the pages linked below.

## The four questions, in order

Most operator sessions are one of these four, and they are ordered because each one
assumes the previous is already true.

| # | The question | Where it is answered | Content layer |
| --- | --- | --- | --- |
| 1 | How do I start an agent under this? | [core documentation](https://docs.agent-assembly.com/core/) | L3 |
| 2 | How do I install it on this platform? | [Docker and containers](docker-containers.md) · [core documentation](https://docs.agent-assembly.com/core/) | L2 · L3 |
| 3 | What does the running stack expose? | [Self-host observability](self-host-observability.md) | L2 |
| 4 | Why did a control not fire? | [Troubleshooting](troubleshooting.md) | L2 |

Question 1 is first for a reason: what reaches a checkpoint at all depends on how the
agent was launched, so an agent started outside that path is a common answer to
question 4.

## Before you start

Which components you need, and which versions of them work together, are two different
lookups and both are in [Reference](compatibility.md):

- [Compatibility matrix](compatibility.md) pairs versions across components.
- [Status map](source-of-truth.md) says who owns each area and how mature its
  documentation is.
- [Choose your enforcement path](choose-your-enforcement-path.md) says which governed
  paths exist, what each one needs on a host, and what each one does not cover.

## The managed service is not an operating route today

The **Cloud** area is marked `🗺️ Planned` in the
[status map](source-of-truth.md), on the documentation-area axis. There is no managed
service to operate from this section, and the two pages that discuss one
([Managed SaaS onboarding (design preview)](quickstart-saas.md) and [Managed control plane (design preview)](cloud-deployment.md))
sit in **Evaluate**, where their reader is someone deciding what to tell a stakeholder
rather than someone running it.

Those pages move into this section when, and only when, their area's `Maturity` cell in
the status map stops reading `🗺️ Planned`. That is a string comparison against a
generated table, not a judgement any page may make on its own.

## What this page does not do

- **It does not describe a mechanism.** What each component does with an action is
  documented at depth in the [core documentation](https://docs.agent-assembly.com/core/).
- **It does not restate a command or a configuration key.** Those belong to the pages
  in the table above.
- **It does not cover adding a checkpoint to code you are writing.** That is
  [Integrate](integrate.md).
- **It does not cover checking a published statement against its evidence.** That is
  [Verify](verify.md).

## Going deeper

The components, their configuration and their behaviour are documented in the
[core documentation](https://docs.agent-assembly.com/core/).
