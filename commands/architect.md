---
description: Architectural design, capacity math, statechart invariants, and ADR before writing code
argument-hint: <system or component to design>
---

Execute architectural design:
1. Define functional and non-functional requirements (traffic, latency, scale, failure modes) with
   capacity estimates that state their assumptions (QPS from usage, storage from writes × bytes ×
   retention); prefer a modular monolith unless independent deployment/scaling genuinely earns the
   operational cost.
2. Model the core domain: statecharts, discriminated unions, and unrepresentable invalid states.
3. Quantify boundaries and component contracts; check the algorithmic cost of the core path
   (`algorithms-and-data-structures`) before committing.
4. Record an Architecture Decision Record (ADR): Context, Decision, Consequences, Alternatives
   (`adr-engineering`).

Target: $ARGUMENTS
