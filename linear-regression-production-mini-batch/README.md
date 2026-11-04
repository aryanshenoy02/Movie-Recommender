# Production Engineering: Mini-Batch Training

Advanced | classical-ml | linear-regression | production-engineering | mini-batch

### The problem, from first principles

`05-training-loop` uses every row for every update, which is clear but becomes expensive as datasets grow. Mini-batches let training update from small groups while still eventually seeing the whole dataset. The practical challenge is preserving feature-target pairing, handling the final short group, and making shuffled training reproducible when a seed is supplied.

### From theory to code

Implement `train_linear_regression_production`. Use the earlier MSE gradient and gradient-descent step for one shuffled batch at a time; Theory explains the epoch-level ordering and the single long-lived random generator.

### Constraints

- `input` has shape `(n_samples, in_features)` and `target` has shape `(n_samples,)`.
- Return zero-initialized then trained `weight` with shape `(1, in_features)` and `bias` with shape `(1,)`.
- Reshape targets to `(n_samples, 1)` once before training.
- Shuffle sample indices once per epoch and take one step for each batch, including a final batch smaller than `batch_size`.
- Construct `np.random.default_rng(seed)` once before the epoch loop.
- The same non-`None` seed and arguments must produce bit-identical parameters; `seed=None` must not force a fixed order.
- Slice only the current batch from `input` and `target`; reuse `mse_gradient` and `gd_step`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Shuffle row indices, not features and targets separately. One index array preserves their pairing.

</details>

<details>
<summary>Hint 2</summary>

`range(0, n_samples, batch_size)` naturally visits the start of a final short batch.

</details>

<details>
<summary>Hint 3</summary>

Create one generator before training. In each epoch, call its `permutation(n_samples)`, then use `order[start : start + batch_size]` to select both batch arrays.

</details>
