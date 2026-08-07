# distributed-systems-engineer — Flagship Eval

## 1. Trigger test

FIRE (5):
1. "Design leader election and fencing tokens for a 50-node cluster so two partitions never both write."
2. "Our cross-region writes race under a network partition and we see lost updates — fix the topology."
3. "Choose single-leader vs multi-leader vs quorum replication for a 3-region inventory service."
4. "Add an outbox pattern so local DB writes publish exactly-once to the event bus without 2PC."
5. "A distributed test passes in staging but misbehaves under clock skew and a slow follower — why?"

NOT FIRE (3):
6. "Write a CRUD endpoint that reads and writes a single Postgres table."
7. "Add a REST route handler in Node that calls one database client."
8. "Fix a one-line typo in a JSON config file."

## 2. Quality rubric (1-5)
(a) decision tree covers stated branches: 5 — consistency, replication, partitioning, transactions each branch top-down with worked example.
(b) failure modes have detection + mitigation: 5 — 8+ failure modes, each DETECT then FIX, plus anti-pattern list.
(c) quantitative rules are numbers: 5 — quorum W+R>N math, latency spans, retry budget worked calc, node-count limits.
(d) verification gate executable: 5 — fault-injection matrix with commands (iptables, kill, NTP pause) and Jepsen-style checks.
(e) references authoritative: 5 — DDIA, Raft paper, Jepsen/Knossos, Spanner/TrueTime all canonical sources.
(f) no contradictions: 4 — consistent with database-at-scale on RYW/quorum; slight overlap with system-design-architect on replication but scoped.

## 3. Reference task
A 3-region e-commerce checkout service (250ms P95) needs a consistency model and replication topology so stock can't oversell and a lock can't be silently lost. The skill: should return a per-key, not-globally-linearizable, read-your-writes choice, an outbox/partitioning plan, fencing + lease tokens, and a fault-injection matrix.
