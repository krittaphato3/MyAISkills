# Skills Catalog Changelog
All catalog changes are recorded here. Format: `YYYY-MM-DD | <change> | <skills affected>`
2026-08-06 | Phase 0.1: baseline inventory captured (43 skills, 35 dup pairs, 11 empty dirs) | all
2026-08-06 | Errata: actual baseline is 44 skills / 41 dup pairs / 7 broken symlinks + 4 empty dirs (supersedes the counts in the Phase 0.1 line) | all
2026-08-06 | Phase 0.2: consolidated to canonical store — moved find-skills/skill-creator/mcp-builder from .agents; deleted 37 dup copies + 4 empty dirs + .agents/skills root; materialized 4 .claude symlinks (java-jvm-expert, ml-python-scientist, readme-architect, systems-core-architect); unlinked 7 broken symlinks in the canonical store (banner-design, brand, design, design-system, slides, ui-styling, ui-ux-pro-max). .claude/skills untouched | all
2026-08-06 | Phase 0.3: standard frontmatter applied to 44 skills (apply_metadata.py) | all
2026-08-06 | Phase 0.3 fix: refactoring-intelligence domain/owner corrected (architecture/refactoring-specialist); META table completed | refactoring-intelligence
2026-08-06 | Phase 0.4: skill_lint v1 built and tested (tests 9/9); baseline 119 E4 / 114 W3 / 0 E1-E3 recorded | tools/skill_lint.py
2026-08-06 | Phase 0.5: manifest skeleton (SKILLS.md, skills.json) created | all
2026-08-06 | Phase 1.1: system-instructions v2 (doctrine, precedence, trigger policy, workflow standards) | system-instructions
2026-08-06 | Phase 1.2: AGENTS.md aligned with system-instructions v2 (precedence + grade standard + confidence harmonized) | doctrine
2026-08-06 | Phase 1.2 fix: grade-standard line qualified (3 transitional G1 skills) | doctrine
2026-08-06 | Phase 1.3: agent↔skill matrix created; 3 missing agent definitions restored (cybersecurity-specialist, game-developer, mobile-developer) | docs/skills/AGENT-SKILL-MATRIX.md, agents/*; AGENTS.md registry count corrected 17→20
2026-08-06 | Phase 1.4: delivery-discipline doc (WORKFLOW.md) created | docs/skills/WORKFLOW.md
2026-08-06 | Phase 1.1 note: lint baseline updated to 113 E4 / 94 W3 (system-instructions v2 resolved its own 6 E4 + 20 W3) | system-instructions
2026-08-06 | Phase 2.0: Roblox suite consolidated 21→1 (roblox-lua-developer); 21 skills superseded and deleted | roblox-*
2026-08-06 | Phase 2.1: systems-core-architect rebuilt 5-lines → G3 (memory/concurrency models, unsafe review, quantitative rules, verification gate) | systems-core-architect
2026-08-06 | Phase 2.2: java-jvm-expert rebuilt 5-lines → G2 (GC tuning, JFR/async-profiler, heap analysis, failure modes) | java-jvm-expert
2026-08-06 | Phase 2.3: ml-python-scientist rebuilt 5-lines → G2 (vectorization, training pipeline, GPU memory, reproducibility) | ml-python-scientist
2026-08-06 | Phase 2.4: performance-profiler deepened to G2 (decision tree, failure modes, verification gate, references) | performance-profiler
2026-08-06 | Phase 2.5: resilience-pattern-engineer deepened to G2 (decision tree, failure modes, verification gate, references) | resilience-pattern-engineer
2026-08-06 | Phase 2.6: security-hardening-specialist deepened to G2 (threat modeling, decision tree, failure modes, verification gate) | security-hardening-specialist
2026-08-06 | Phase 2.7: refactoring-intelligence deepened to G2 (decision tree, failure modes, verification gate, references) | refactoring-intelligence
2026-08-06 | Phase 2.8: api-design-architect deepened to G2 (decision tree, failure modes, verification gate, references) | api-design-architect
2026-08-06 | Phase 2.9: query-performance-engineer deepened to G2 (decision tree, failure modes, verification gate, references) | query-performance-engineer
2026-08-06 | Phase 3.3: system-design-architect created (G3: capacity estimation, ADRs, trade-off framework, quantitative rules) | system-design-architect
2026-08-06 | Phase 3.4: concurrency-engineer created (G3: parallelism, locking, lock-free, race/deadlock detection, quantitative rules) | concurrency-engineer
2026-08-06 | Phase 3.7: general-orchestrator created (G3: gate-driven execution, subagent routing, verification per subtask, token-smart fan-out) | general-orchestrator
2026-08-06 | Phase 3.8: deep-planner skill + planner agent created (G3 planning methodology) | deep-planner, agents/planner.md
2026-08-06 | Phase 3.9: solution-architect + ml-engineer agents created; owners updated; registry 20->23 | agents/*, system-design-architect, distributed-systems-engineer, ml-python-scientist, AGENTS.md
2026-08-06 | Phase 3.9a: requirements-elicitation created (G3, adapted from addyosmani/agent-skills interview-me) | requirements-elicitation
2026-08-06 | Phase 3.9b: spec-driven-development created (G3, adapted from addyosmani) | spec-driven-development
2026-08-06 | Phase 3.9c: source-driven-development created (G3, adapted from addyosmani) | source-driven-development
2026-08-06 | Phase 3.9d: doubt-driven-development created (G3, adapted from addyosmani) | doubt-driven-development
2026-08-06 | Phase 3.9e: adr-engineering created (G3, adapted from addyosmani documentation-and-adrs) | adr-engineering
2026-08-07 | Phase 3.10: flagship evals (14 skills) — results at docs/skills/evals/results-2026-08-07.md | 14 G3 skills
2026-08-07 | Phase 4.1: skill_lint v2 (--stale, E5 blanket-invoke, W3 code-token allowlist, review summary) | tools/skill_lint.py
2026-08-07 | Phase 4.2: upgrade-process doc (CONTRIBUTING.md) | docs/skills/CONTRIBUTING.md
2026-08-07 | Phase 4.3: G2 sweep — added grade-sections + fixed blanket-invoke descriptions across remaining general skills | animation-web-builder, container-optimizer, cybersecurity-specialist, dependency-supply-chain-guardian, devops-pipeline-engineer, find-skills, game-developer, github-flow-master, mcp-builder, mobile-developer, monorepo-workspace-architect, readme-architect, skill-creator (G2 sections); description rewrites across api-design-architect, container-optimizer, cybersecurity-specialist, dependency-supply-chain-guardian, devops-pipeline-engineer, game-developer, github-flow-master, mobile-developer, monorepo-workspace-architect, performance-profiler, query-performance-engineer, readme-architect, refactoring-intelligence, resilience-pattern-engineer, security-hardening-specialist, system-design-architect
