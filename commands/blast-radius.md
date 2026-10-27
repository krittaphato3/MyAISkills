---
description: Analyze impact, dependent files, and regression risks before refactoring or changing shared code
argument-hint: <file or module path>
---

Perform a static blast radius assessment on:
$ARGUMENTS

1. Identify all consumers, callers, and import sites of the target module.
2. Check for public interface modifications or breaking changes.
3. List the test suites that must pass after the change.
4. Estimate risk and recommend an incremental migration sequence.
