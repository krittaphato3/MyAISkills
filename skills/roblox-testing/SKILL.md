---
name: roblox-testing
description: >-
  Tests Roblox games: TestEZ/Jest-Lua unit suites, in-Studio runners, MCP-driven playtests with real
  input, multiplayer and network checks, visual regression from fixed cameras, data isolation, and
  performance gates. Use when writing tests, automating a playtest, reproducing a runtime-only bug,
  or deciding whether a build is shippable. Test content authored from a spec before implementation
  routes to test-oracle.
metadata:
  version: 1.0.0
  domain: roblox
  grade: G3
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: roblox-qa-engineer
---

# Roblox Testing

Roblox has three kinds of truth: what unit tests say, what a playtest does, and what a phone does.
They fail independently. A green suite with a broken remote is normal; a clean playtest on desktop
with a 12 fps mobile build is normal. Testing here means covering all three with the cheapest check
that can catch each class of bug.

## WHEN TO USE

- Writing unit tests for pure logic, data transforms, validation, and economy rules.
- Automating a playtest: spawn, move, press keys, click, assert state, read console.
- A bug that only reproduces at runtime, under multiple players, or after rejoin.
- Verifying persistence, purchases, or anti-exploit rejection.
- Building a release checklist for a milestone.
- Measuring performance before/after a change.

## WHEN NOT TO USE

- Writing independent acceptance tests from a spec before code exists — `test-oracle` agent.
- Designing the feature or the loop — `roblox-game-production`.
- Exploit taxonomy itself — `roblox-security` (this skill automates the attacks).
- Non-Roblox test frameworks — `test-driven-development` / `test-engineer`.

## DECISION TREE

```text
1. WHAT CLASS OF BUG?
   Pure logic / validation / economy math → unit test (TestEZ or Jest-Lua), fast, in Edit or a test run
   Wiring / replication / input / state      → playtest with assertions (MCP)
   Persistence / purchases / rejoin          → multi-session playtest with isolated data
   Visual / layout / effects                 → fixed-camera captures at multiple viewports
   Performance                               → measured frame time/memory in the densest scene
   Exploit rejection                         → attack script per surface (roblox-security)

2. CAN IT BE A UNIT TEST?
   If yes, make it one. Unit tests are seconds; playtests are minutes. Push assertions down.

3. WHAT IS THE ACCEPTANCE CRITERION?
   One observable outcome ("health reaches 0 on the server and the HUD shows 0 within 1 frame").
   Write it before running anything.

4. ISOLATE DATA
   Never test against production DataStore keys. Use a test store/scope, seeded profiles, and clean
   up. A test that mutates real player data is an incident, not a test.

5. AUTOMATE THE PLAYER PATH
   start_stop_play(true) → wait for character → character_navigation to the area →
   user_keyboard_input / user_mouse_input for the real input path → execute_luau assertions in
   Server and Client → get_console_output → screen_capture → stop play.

6. RECORD EVIDENCE
   Console output (clean or the exact error), assertion results, capture paths, frame-time numbers.
   "It worked" is not a result.
```

## PATTERNS

### 1. Unit test shape (TestEZ-style)
```lua
local TestEZ = require(ReplicatedStorage.Packages.TestEZ)

TestEZ.describe("RateLimiter", function()
    TestEZ.it("allows up to capacity then rejects", function()
        local limiter = RateLimiter.new({ rate = 2, capacity = 2 })
        expect(limiter:allow("u1", "attack")).to.equal(true)
        expect(limiter:allow("u1", "attack")).to.equal(true)
        expect(limiter:allow("u1", "attack")).to.equal(false)  -- burst exhausted
    end)
end)
```
Test the rule, not the implementation: token bucket behavior, validation rejection, reward math,
migration output.

### 2. Playtest harness (MCP)
```text
get_studio_state                        → confirm Edit
start_stop_play(is_start=true)          → run
execute_luau(Server)                    → wait for players/character, seed state
character_navigation(targetInstance)    → reach the test area
user_keyboard_input / user_mouse_input  → exercise the real input path
execute_luau(Server) / (Client)         → assert authoritative + replicated state
get_console_output                      → errors/warnings
screen_capture(capture_id)              → visual state
start_stop_play(is_start=false)         → always restore Edit
```
One behavior per cycle; stop play before the next edit (`roblox-studio-mcp`).

### 3. Persistence test (two sessions)
1. Session A: grant currency/item, force a save, record the values.
2. Stop play. Start play again (or use a second test profile).
3. Session B: assert the values survived; assert no duplicate grant.
4. Simulate failure: kill before save, confirm the profile is not replaced by defaults.
Use a test DataStore scope, never the live one.

### 4. Multiplayer / replication test
- Use Studio's multi-client playtest when available; otherwise two account sessions or a test
  harness that simulates two players server-side.
- Assert: both clients see the same animation/state; a client's local change does not persist; the
  server rejects a second player acting on the first player's object.
- Check latency-sensitive behavior with network emulation where the harness supports it.

### 5. Visual regression
- Fixed camera position and look-at per shot; same viewport per comparison.
- Capture baseline after a known-good build, compare after changes.
- Cover phone + desktop layouts and at least one effect-heavy frame.
- A screenshot proves pixels; assert logic separately.

### 6. Performance gate
- Measure in the densest gameplay moment (combat, crowded lobby), not an empty baseplate.
- Record: frame time / fps, memory, instance count, particle count, draw calls where available.
- Compare before/after with the same build settings and device tier; ≥5 samples if noisy.
- On mobile/low quality, verify the fallback path is active.

### 7. Release checklist
```text
[ ] Unit suite green
[ ] Playtest: new-player flow, core loop, death/respawn, rejoin
[ ] Server + client console clean
[ ] Persistence: grant → save → rejoin → no duplication
[ ] Purchases: receipt replay grants once
[ ] Exploit: one rejection test per remote
[ ] Multiplayer: two clients agree on state
[ ] Visual: phone + desktop captures
[ ] Perf: densest scene measured on low-end
[ ] Mobile fallback verified
```

## FAILURE MODES & MITIGATIONS

1. **Green suite, broken game** — only unit tests. *DETECT:* runtime bugs in every build. *FIX:* add
   playtest assertions for wiring and replication.
2. **Playtest theater** — started a playtest, looked at it, declared success. *DETECT:* no assertion
   output. *FIX:* every playtest ends with an `execute_luau` assertion + console check.
3. **Production data in tests** — test writes real profiles. *DETECT:* test keys in prod store.
   *FIX:* isolated store/scope and seeded fixtures.
4. **Flaky input timing** — fixed `wait()` before asserting. *DETECT:* intermittent failures. *FIX:*
   poll for the condition with a timeout, assert on state not on elapsed time.
5. **Desktop-only evidence** — no mobile layout or perf check. *DETECT:* mobile bugs at launch.
   *FIX:* viewport matrix + low-quality fallback test.
6. **Screenshot-only proof** — visual claim, no logic assertion. *DETECT:* pixels look right, state is
   wrong. *FIX:* pair capture with a Server/Client assertion.
7. **Unrestored play state** — test leaves Studio in play mode. *DETECT:* next edit rejected.
   *FIX:* always stop play in a finally-style path.

## QUANTITATIVE RULES

- Unit tests: <100 ms each; cover validation, economy math, migrations, state machines.
- Playtest: one behavior per cycle; assert within a bounded wait (not a fixed sleep).
- Persistence: two sessions minimum; one failure-injection case.
- Visual: fixed camera, ≥2 viewports; baseline stored for comparison.
- Perf: ≥5 samples in the densest scene on the lowest target device; report median + p95.
- A release candidate needs all checklist items with attached evidence.

## VERIFICATION GATE

- [ ] Acceptance criterion written before the test.
- [ ] Unit coverage for pure logic; playtest coverage for wiring and replication.
- [ ] Test data isolated from production stores.
- [ ] Server and client assertions captured, console clean.
- [ ] Persistence and receipt replay tested across two sessions.
- [ ] Visual baseline captured on phone + desktop.
- [ ] Performance measured in the worst-case scene, with a comparison.
- [ ] Studio returned to Edit; no leaked test state or leftover instances.

## REFERENCES

- `roblox-studio-mcp` — tool loop and session safety
- `roblox-scripting` — the systems being tested
- `roblox-security` — attack tests per surface
- `roblox-ui-ux` — viewport and input coverage
- `test-driven-development` / `test-oracle` — test-first and independent-oracle discipline
- Roblox docs: testing modes, TestEZ, Jest Roblox, StudioTestService
