---
name: bro
description: Restates the last message in plain human language with no jargon. Use when the user asks
  for plain language, says 'bro', or signals the previous explanation was unclear. Precision specs and
  contracts keep their technical vocabulary.
metadata:
  version: 1.1.0
  domain: doctrine
  grade: G2
  status: active
  last-reviewed: '2026-11-09'
  authored-by: meta-architect
---


Restate your last message. Stop using jargon and speak coherently. State it more simply and concisely, like one human talking to another.

## WHEN TO USE

The user asks for plain language, says "bro", or signals the last explanation was unclear.

## WHEN NOT TO USE

Precision specs and contracts keep their technical vocabulary.

## DECISION TREE

- The last message was a technical explanation and the user signals confusion -> restate it in plain words, same content.
- The user says "bro" after a decision -> state the decision and what happens next, in one short paragraph.
- The content is a spec, contract, or legal text -> keep its technical nouns; simplify only the sentences around them.
- The user wants a different answer rather than a simpler one -> answer the question; do not restate.
- There is nothing to restate -> ask what to clarify.

## FAILURE MODES & MITIGATIONS

- **Simplified into vagueness.** Mitigation: keep every fact; only the wording changes.
- **Dropped the decision.** Mitigation: the restatement leads with what was decided or asked.
- **Translated proper nouns.** Mitigation: API names, file paths, and product names stay verbatim.
- **Restated the wall of text at the same length.** Mitigation: one short paragraph, or a few labeled lines.
- **Patronizing tone.** Mitigation: plain, not childish; no "in simple terms for you".
- **A different claim smuggled in.** Mitigation: same facts, shorter; check each fact against the original.

## VERIFICATION GATE

Same facts, shorter; no jargon left undefined; every proper noun unchanged.

## REFERENCES

- `unslop` - cutting filler without dropping meaning.
- `teach` - when the goal is understanding, not a restatement.
- `principles/minimize-reader-load` - what the reader has to hold.
