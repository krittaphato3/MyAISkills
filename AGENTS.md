# ZCODE AUTONOMOUS AGENTIC CODING SYSTEM

## CORE PRINCIPLE
**Quality First. Understand fully before building. Never rush to code.**

## GOVERNANCE
**GOLDEN RULE**: The main thread orchestrates; ALL file work and coding goes through subagents. Full delegation protocol: skills/system-instructions.
**PRECEDENCE**: Task-specific skill > family skill > system-instructions > AGENTS.md > harness defaults.
**GRADE STANDARD**: every skill is G2+ (3 transitional G1 language skills upgrade in Phase 2; see docs/skills/SKILLS.md); quality gates enforced by tools/skill_lint.py.

## RULES
1. Confidence ≥ 80% before coding (80–89 proceed with caution — see skills/system-instructions)
2. Build it right first time — no "cheap version then improve"
3. ALL coding through subagents — main thread orchestrates only
4. Never skip QA — red-team-qa before every commit

## CODING ETHICS
- **Performance**: Never write O(n²) when O(n) is possible
- **Security**: Never store secrets in code, always validate input
- **Accessibility**: WCAG 2.1 AA minimum for all UI
- **Quality**: Write code others can understand
- **Data**: Minimize collection, encrypt sensitive data

## AGENTS (23)
**Core**: planner, solution-architect, code-implementer, db-architect, deep-researcher, red-team-qa, ui-ux-architect
**Specialized**: ml-engineer, performance-engineer, devops-engineer, security-auditor, api-architect, refactoring-specialist, accessibility-specialist, dependency-guardian, cybersecurity-specialist
**MCP/Automation**: mcp-agent, browser-automation, test-engineer, documentation-engineer, data-engineer, game-developer, mobile-developer

## PIPELINE
1. Context Gathering (mandatory, confidence ≥ 80%)
2. Subagent Dispatch (spawn appropriate agents)
3. Quality Assurance (phase gates: skill lint + red-team-qa; tests)
4. Version Control (branch, commit, push/PR)

## QUALITY GATES
- Before implementation: confidence ≥ 80%, context gathered, memory checked
- Before commit: tests passing, lint clean, QA approved, no regressions
