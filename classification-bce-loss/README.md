# Binary Cross-Entropy Loss

Beginner | classical-ml | classification | loss-functions

### The problem, from first principles

Classification needs to distinguish uncertainty from confidently choosing the wrong class. A loss should therefore charge a much larger cost when a predicted probability disagrees with the true binary label. The logarithm does that, but only if its input is kept away from zero.

### From theory to code

Implement `bce_loss(p, y)` as a batch mean. Theory gives the two label cases; clip probabilities before either logarithm and return a Python `float`.

### Constraints

- `p` and binary `y` have matching `(n_samples,)` shapes.
- Clip `p` to `[1e-12, 1 - 1e-12]` before logs.
- Average one loss value per sample and return a plain `float`.
- Saturated `0.0` and `1.0` inputs must produce a finite loss.
- Use vectorized NumPy operations only.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Each label selects one of two complementary probability terms.

</details>

<details><summary>Hint 2</summary>

Clip once, then form both `log(p)` and `log(1 - p)` before taking the negative mean.

</details>
