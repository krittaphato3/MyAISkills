# requirements-elicitation — Flagship Eval

## 1. Trigger test

Fire (for 5):
1. "I want a notifications feature for my app" — no who/why/success. (missing definition)
2. "The ask says 'click-able checkout' but success criteria are absent — interview."
3. "Two constraints conflict (fastest-to-ship vs most-features) and must be resolved."
4. "The user describes it 'like the X flow but for claims' — a metaphor to disambiguate."
5. "No stakeholders beyond the requester; I need a confirmed intent to hand to deep-planner."

Not fire (for 3):
6. "Fix that typo (already unambiguous)." — no interview.
7. "Which env, prod or staging?" — factual, direct answer.
8. "The request already names exact actor + success + no tension; confident ≥95%" — skip.

## 2. Quality rubric (1-5)
(a) decision tree covers branches: 5/5 — hypothesis→single-question→want-vs-should→restate→explicit-yes→stop-at-95%; guarded steps.
(b) failure modes have detection+mitigation: 5/5 — batching, guessing-without-hypothesis, accept-whatever-yes, support-interview, drift-to-how, save-preconfirm, answer-for-user, missed-tension.
(c) quantitative rules are numbers: 5/5 — stop predict-3, confidence 70/95, restate 5-8 lines, single-question, 5-7 questions budget, guess-hit-rate.
(d) verification gate executable: 5/5 — hypothesis-conf first, one-question-per-turn, restate delivered, explicit-yes-present, tie-break, predict-next-3, output-shape no-blank.
(e) references authoritative: 4/5 — addyosmani interview-me, Mom Test, Five Whys, Socratic, coaching are recognized; strongest standalone are concrete.
(f) no contradictions: 5/5 — feeds deep-planner explicitly, consistent with doctrine (requirements clear before planning).

## 3. Reference task
A stakeholder says "make our checkout faster and smarter" with no success definition, whom it serves, or deadline. The skill must run one-question-at-a-time, restate in Outcome/User/Why now/Success/Constraint/Out-of-scope, get an explicit yes, and emit a confirmed intent doc.
