# Test Behavior, Not Implementation

Apply when you write, change, or keep a test. Assert what the code's users can observe, so the
test fails when that behavior breaks and keeps passing when only the internals change.

## Rule

A test is a contract with a caller, not a transcript of the implementation.

- **Assert the observable outcome.** Return values, state a caller can read, HTTP responses,
  rendered text, emitted events, persisted rows. Not private methods, not call counts on
  collaborators, not the shape of an internal data structure.
- **Name the behavior, not the function.** `rejects_expired_token` beats `test_validate_2`.
- **One reason to fail.** A test that breaks for three unrelated reasons tells you nothing when
  it goes red.
- **Mock at the boundary you do not own.** Network, clock, filesystem, third-party SDK. Not your
  own modules — mocking your own code turns the test into a change detector.
- **A refactor that changes no behavior must not change a test.** If it does, the test was pinned
  to structure.
- **Delete tests that assert nothing.** `expect(x).toBeDefined()` on a value you just built is
  noise that inflates coverage.

## WHEN NOT TO USE

- Snapshot tests of intentional output (generated markup, CLI help text). There the exact string
  *is* the contract; keep them small and reviewed.
- Characterization tests written before a legacy refactor. They pin current behavior on purpose,
  including behavior you intend to keep by accident.
- Probing a third-party API to learn its real shape. That is a spike, not a test.

## FAILURE MODES & MITIGATIONS

| Failure | Mechanism | Mitigation |
|---|---|---|
| Change detector | Test asserts internal call order or private state | Assert the public outcome; assert collaboration only at a boundary |
| Mock theater | Everything mocked, test passes with the implementation deleted | Keep one test per module that runs the real thing end to end |
| Coverage inflation | Many assertions, no behavior | Delete assertions that cannot fail |
| Refactor tax | Every rename breaks 40 tests | Test through the public surface only |
| Flaky timing | `sleep` and wall-clock assertions | Inject the clock; assert on a deterministic seam |

## VERIFICATION GATE

- [ ] The test fails if the behavior is removed (prove it: break the code, watch it go red).
- [ ] The test passes if only internals are renamed or restructured.
- [ ] The assertion names a caller-visible outcome.
- [ ] No new mock of a module this repository owns.
