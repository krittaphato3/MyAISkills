---
description: Red-Green-Refactor test-driven bug fixing and feature development
argument-hint: <bug or feature description>
---

Execute strict Test-Driven Development:
1. Write the minimal executable failing test first that reproduces the bug or asserts the new requirement.
2. Run the test locally and confirm it fails for the expected reason.
3. Implement the minimal production code needed to pass the test.
4. Rerun the test to confirm green.
5. Refactor and eliminate slop without breaking tests.
6. Pick size and oracle per `testing-strategy`: assert observable behavior, not internal calls;
   builders with explicit per-test data over shared fixtures; never weaken an assertion or skip
   a test to reach green.

Target: $ARGUMENTS
