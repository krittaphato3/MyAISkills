---
name: ml-python-scientist
description: >-
  Writes Python for data science and machine learning: pandas and NumPy, scikit-learn,
  PyTorch or TensorFlow training loops, experiment tracking, reproducibility, and
  evaluation. Use for notebooks, model code, and analysis. Serving a model in a product
  routes to llm-engineer or ml-engineer; general Python services to
  systems-core-architect.
metadata:
  version: 3.0.0
  domain: languages
  grade: G2
  status: active
  last-reviewed: '2026-10-22'
  owned-by-agent: ml-engineer
---

# ml-python-scientist

G2 guidance for writing production-grade ML and data-science code. Optimizes for correct, deterministic, memory-bounded, vectorized pipelines. Applies to PyTorch, TensorFlow, JAX, Pandas, NumPy, and Polars. Read the DECISION TREE before writing the first training or transformation line.

## WHEN TO USE

- The task expresses a predictive or hypothesis-driven model: training a neural net, fitting a gradient-based model, or statistical inference over tensors with learned parameters.
- You are transforming row-column or tensor data at scale where naive per-element Python loops are the slow but tempting default.
- You need GPU acceleration (CUDA), automatic differentiation, or a framework-managed training loop.
- Outputs must be reproducible and auditable: train/validation/test splits, seeded sampling, and pinned dependency versions are first-class requirements.
- You must reason explicitly about tensor shapes, dtypes, memory residency (CPU vs GPU), gradient flow, and run-to-run variance.
- You are building a reusable data-loading, preprocessing, or evaluation utility that other model code will call.

## WHEN NOT TO USE

- Plain scripting and glue logic with no array math: file I/O, network calls, CLI parsing, string manipulation — use ordinary Python or a targeted skill.
- The correct answer is a managed service or hosted model (an inference API, a cloud AutoML endpoint) where in-process training code adds cost without benefit.
- A non-ML solution fits: a rule, a linear-algebra closed form, or a simple SQL aggregation solves the problem with less complexity and no learned parameters.
- Data volume is tiny (fewer than roughly 10^4 rows) and a clear comprehension or one-liner is the honest cost and faster to write than a framework pipeline.
- You are writing the orchestration around training (DAG runners, Kubernetes, experiment trackers, model registries) rather than the training itself.
- A signal is better expressed as lookups or joins and does not need gradient-based fitting.

## DECISION TREE

Trace each branch left-to-right and commit to the first leaf that matches. Record the decision (and the rejected alternatives) in a comment or the PR body.

- **Vectorize vs loop.** Prefer vectorized operations whenever a NumPy/Pandas/GPU primitive implements the operation over an axis. Fall back to a Python loop only when the operation is inherently sequential (rolling state, recursion, a scan with an order-dependent carry) or when the loop lane count is below ~10^4. When looping, iterate the smallest possible scalar lanes, keep the loop body allocation-free, and hoist any frozen intermediate out of the loop.
  - Size thresholds: for n below ~10^4 correctness and clarity matter more than speed; above that the vectorized form wins every time. Budget peak memory before committing: a broadcasted expression materializes intermediates, so multiply axis sizes by the element byte size. Example: `(x[:, None] - x[None, :])` on a 10k-element vector creates a 100M-cell 800 MB float64 array — an OOM waiting to happen; restructure or chunk.
- **Pandas vs NumPy vs Polars vs SQL.**
  - Pandas: heterogeneous tabular data, group-by, merges, pivot, missing-value handling; convenient but copy-heavy. Use for exploratory transformation and moderate frames.
  - NumPy: homogeneous numeric arrays, broadcasting, more than two dimensions, tight memory layout, zero-copy feeds into Torch. Use for raw numeric kernels and shape-disciplined math.
  - Polars: wide or deep columnar data with lazy query plans and multi-core execution; prefer when the table exceeds memory or parallel column ops matter more than ecosystem convenience.
  - SQL (via a database client): the data already lives in a warehouse; push filters, joins, and aggregations down and pull only the reduced result. Never copy a raw table just to select columns.
- **Framework by deployment target.**
  - PyTorch: research iteration, dynamic graphs, richest eager-mode debugging, broad ecosystem. Default for new training code.
  - TensorFlow/Keras: serving at scale, stable static graphs, TF Serving and TFLite, TPU execution, portable export. Choose when the serving artifact and cloud TPU target dominate research convenience.
  - JAX: functional, transformable programs (jit/vmap/grad), first-class TPU arrays, explicit device placement. Choose for scientific computing and function-purity guarantees.
  - Otherwise: use PyTorch behind a clean model boundary so it can be exported to ONNX or TorchServe later without rewriting. Never pick a framework for a benchmark win; pick for the shipping path.

## PATTERNS

- **Vectorized idioms.** Replace loops with array operations: boolean-mask assignment instead of element branches; axis reductions instead of accumulating scalars; sorting then slicing instead of index surgery. Comment each non-obvious op with its semantic (mask, cast, clamp, one-hot, normalize). Example:

  ```python
  # Clip out-of-range rows, then mask negatives in place (vectorized, no loop)
  scores = np.clip(raw, -1.0, 1.0)
  scores[scores < 0.0] = 0.0
  mean = scores.mean(axis=-1)  # per-sample axis reduction
  ```

- **Tensor shape discipline.** Label every tensor with a `[B, T, D]`-style comment naming batch, time/sequence, and hidden/feature axes. Annotate at creation and after every reshape, permute, transpose, flatten, or expand; comment why a shape changes; note which axes stay implicit during broadcasting. Example:

  ```python
  # x: [B, T, D] hidden states -> permute to [B, D, T] for a temporal conv
  x = hidden.permute(0, 2, 1)
  assert x.shape == (B, D, T)
  ```

- **GPU memory hygiene.** Keep validation intermediates out of autograd; wrap eager validation loops in `no_grad`; build the DataLoader with `pin_memory=True`; assert `torch.cuda.max_memory_allocated` stays under a ceiling. When full-batch memory is tight, accumulate gradients over micro-batches and step once. Release references promptly and re-check the allocator after each epoch.

  ```python
  with torch.no_grad():                      # inference path: no graph retained
      out = model(batch.to(device))          # batch moved once, reused via pin_memory
  torch.cuda.reset_peak_memory_stats(device)
  ```

- **Distributed training.** Prefer `DistributedDataParallel` over data-parallel replication; clip the global gradient norm before the optimizer step; place modules on the worker device with `.to(rank)`; gate the launch on the correct backend and guard the loop with `if __name__ == "__main__":`. Use deterministic tie-breaking for DDP process order.
- **Reproducibility.** Seed Torch, NumPy, Python random, and CUDA in one call site; force deterministic kernel flags; pin every dependency to an exact version; persist split identifiers and the data-hash per fold; record a run-to-run tolerance and assert the pass difference stays within it.

  ```python
  torch.manual_seed(7); np.random.seed(7); random.seed(7)
  torch.backends.cudnn.deterministic = True
  torch.backends.cudnn.benchmark = False
  ```

- **Data loading.** Precompute canonical ids and disjoint fold memberships; compute normalization statistics only from the Train fold; use worker sub-processes for I/O; cache heavy parquet/blob transforms outside the hot loop.
- **Batching and mixed precision.** Keep batch shapes constant where possible; use an automatic-mixed-precision context for forward/backward; keep the loss and master weights in float32 to prevent drift.

## FAILURE MODES & MITIGATIONS

- **GPU out of memory.** Detect a CUDA OOM at a specific layer or allocation. Fix with gradient checkpointing (trade compute for memory), trimming the batch or micro-batch, using a no-grad region for inference passes, and releasing stale references; enforce a memory ceiling via the CUDA allocator and profile the top allocations.
- **Data leakage in splits.** Detect when validation/test metrics look implausibly high or a train-time feature correlates perfectly with the target. Fix by splitting on time for series (train/test on timestamps, never random), keeping the raw id group together within a fold, and computing any normalization only from the Train fold.
- **Nondeterminism.** Detect: two identical runs with the same seed give different results. Fix: seed all generators, enable deterministic kernel flags, pin tie-breaking order in DDP and batch order, pin dependency versions, and record which CUDA kernel may stay nondeterministic.
- **dtype/precision bugs.** Detect: mean or sum drift over steps, inf/nan under float16, or accumulated rounding. Fix: cast inputs to one precision up front (float32 vs float16), accumulate float16 in float32, use autocast for mixed precision, and assert dtype consistency in any metric op.
- **NaN propagation.** Detect: loss prints NaN early or a weight tensor becomes NaN mid-training. Fix: use a bounded or log-space loss/activation, check isfinite per fold or step, clip gradients, add a warmup, and locate and repair the first NaN-producing layer.
- **Stale tensor references.** Detect: a `to(device)` or detached copy is mutated while its origin is reused, or a slice is written after a split was derived from it. Fix: finally clone before in-place writes, never hold a view across an in-place mutation, prefer functional transforms, and audit aliasing in review.
- **Shape mismatch / broadcast surprise.** Detect: a runtime size mismatch or a broadcast that silently padded an axis. Fix: assert equal shapes at module boundaries before ops, log axis footprints, prefer explicit reshape over a raveled view, and wrap the boundary with a shape-verifying helper.
- **Gradient explosion / vanishing.** Detect: loss becomes inf or the update norm spikes after a few steps. Fix: clip the global gradient norm, add warmup and layer norm, reduce the learning rate or step schedule, and inspect the gradient norm once per fold as a canary.
- **Imbalanced batches and class priors.** Detect: loss saturates or accuracy stalls while class distribution skews. Fix: stratified sampling on the fold, class weights in the loss, a precise evaluator for the under-represented class, and never tune on the holdout.

## VERIFICATION GATE

- **Shape assertions.** Assert shape and dtype at data and module boundaries (inputs, hidden, logits). Log a shape-consistency manifest per step and fail fast on drift.

  ```python
  assert logits.shape == (B, num_classes), f"got {logits.shape}"
  ```

- **Gradient checks.** Before training, verify a small-scale numeric/autograd difference on any new op (`torch.autograd.gradcheck` or finite differences). Never run a long training job on an unverified op.
- **Holdout discipline.** Train only on the Train split; keep validation and test holdout untouched; then report a final metric on a single pre-selected holdout exactly once. Do not tune hyperparameters on the saved holdout.
- **Memory assertion.** On GPU, print `torch.cuda.memory_summary()` and enforce the budget bound using `torch.cuda.max_memory_allocated`.

  ```python
  peak = torch.cuda.max_memory_allocated(device) / (1024**3)
  assert peak < BUDGET_GB, f"peak {peak:.2f} GiB exceeds {BUDGET_GB} GiB"
  print(torch.cuda.memory_summary())
  ```

- **Run-to-run variance.** Run two identical-seed passes and assert the final metric differs by less than a stated tolerance. Report the variance and the exact seed in the README or handoff.

  ```python
  # two passes with the same seed must agree within TOL
  assert abs(run_a_metric - run_b_metric) <= TOL, "run-to-run variance too high"
  ```
- **Backend and device sanity.** Confirm the expected device (`is_cuda`), confirm the loss and master-weight dtypes match before any step, and confirm the DataLoader worker count does not race with any global random seed.

## REFERENCES

- PyTorch documentation: the Determinism, DistributedDataParallel, and Serialization pages.
- NumPy guidelines: the numpy.org devdocs on broadcasting, vectorization, and memory layout.
- CUDA memory documentation: the torch.cuda memory-management API and `torch.cuda.max_memory_allocated`; the cuDNN thread-safety note.
- Reproducibility guides: the PyTorch Reproducibility how-to, the CUDA deterministic flags, and the pinned-environment best practice.
- Mixed precision: the automatic-mixed-precision page in each framework.