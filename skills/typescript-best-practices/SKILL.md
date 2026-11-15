---
name: typescript-best-practices
description: TypeScript-specific rules for types, unions, brands, and boundary parsing. Use when reading
  or editing any .ts or .tsx file, or when designing types or signatures in TypeScript. Other languages
  route to their own idiom skills; the general doctrine lives in principles.
metadata:
  version: 1.1.0
  domain: languages
  grade: G2
  status: active
  last-reviewed: '2026-11-09'
  authored-by: code-implementer
---


# TypeScript best practices

Apply the **type-system-discipline** principle skill first; this skill grounds it in TypeScript syntax.

| Rule | Summary |
|------|---------|
| Discriminated unions | Model variants with a `kind` literal discriminant so impossible states can't be represented. No optional-field bags. |
| Branded types | Brand primitives with `& { readonly __brand: "X" }` so they can't be mixed up. Validate once at creation. |
| Constructive modeling | Build the shape so the illegal value can't be constructed. `[T, ...T[]]` for non-empty, `[T, T][]` for even length, `start` plus `duration` for a range. Not a runtime guard, not a wish for refinement types. |
| Simplest total type | Keep `T[]` while every operation on it stays total. Strengthen to `NonEmpty<T>` only where the loose type forces `!`, a cast, or a "should never happen" throw. |
| `unknown` over `any` | External data is `unknown`. `any` disables type checking everywhere it touches. |
| No `as` casts | Every `as` is a runtime crash waiting. Cast only after validation. |
| Narrowing hierarchy | Discriminant switch > `in` operator > `typeof`/`instanceof` > user-defined type guard > `as`. |
| Type guards | Must verify the claim. A lying guard is worse than `as` because the bug hides behind a name that says it's safe. Name them `isX` or `hasX`. |
| Exhaustiveness | Inline `const _exhaustive: never = x;` in default arms so the compiler errors when a new variant is added. |
| `satisfies` over `as` | Validates the value without widening literal types. |
| Boundary validation | Parse where data crosses in, into a named domain type. `Record<string, unknown>` (however spelled) stops at that parse. Trust types inside. See the **boundary-discipline** principle skill. |
| Schema-derived types | Reach for `Pick`/`Omit`/`Parameters`/`ReturnType`/`Awaited`/`typeof` before declaring a new interface. |
| Object args | Pass objects, not positional, so argument order is self-documenting. Skip on hot paths (per-frame render, tokenizers, parsers). |
| Real tests | Don't mock what you can run. Prefer the framework's real test primitives with leak/disposable checks, and verify UI in a running build. Mock only what you can't run locally. |
| Structured telemetry | Prefer structured logger diagnostics with enough context to debug from an id. No `console.log` in shipped code. |

Examples: `references/patterns.md`.

## DECISION TREE

- Data arrives from outside (HTTP, file, env) -> parse at the boundary into a typed value.
- A primitive carries meaning (`userId`, cents, ISO date) -> brand it.
- A boolean pair encodes one state -> replace with a discriminated union.
- A type is asserted with `as` -> narrow or parse instead; `as` is a claim, not a check.
- A union is switched on -> add the exhaustive `never` check.
- The type exists as a schema -> derive the type from it; do not hand-write a parallel interface.
- A value can be absent -> model absence as a union member, not `?:`.

## FAILURE MODES & MITIGATIONS

- **`any` at the boundary.** Mitigation: `unknown` plus a parser; `any` disables every downstream check.
- **Optionality used for "maybe absent".** Mitigation: a union member makes the empty case explicit.
- **Stringly-typed identifiers.** Mitigation: branded types with one constructor per source.
- **Type lies in tests.** Mitigation: tests import the same parser the app uses.
- **`Partial<T>` updates.** Mitigation: explicit patch types that cannot express "set to undefined" by
  accident.
- **Type-only correctness with no runtime check.** Mitigation: parse at the edge; types erase.

## WHEN TO USE

Reading or editing any .ts or .tsx file; designing types or signatures in TypeScript.

## WHEN NOT TO USE

Other languages have their own idiom skills.
General type doctrine lives in `principles`.

## VERIFICATION GATE

Illegal states unrepresentable where practical; external data parsed at boundaries.
No `any` leaking across a boundary; typecheck passes.

## REFERENCES

- `principles/type-system-discipline` - make illegal states unrepresentable.
- `principles/boundary-discipline` - parsing only at the edge.
- `source-driven-development` - verify the signature before relying on it.
