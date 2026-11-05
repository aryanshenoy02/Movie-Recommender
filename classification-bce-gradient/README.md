# Gradient of BCE

Intermediate | classical-ml | classification | manual-calculus | gradients

### The problem, from first principles

`02-bce-loss` says how wrong probability predictions are; training still needs to know how to change the linear parameters that produced them. Once sigmoid and BCE are combined, their derivatives simplify into a residual-like quantity. This question computes its full-batch weight and bias gradients with the column shapes used by the preceding linear-regression exercises.

### From theory to code

Implement `bce_gradient(input, p, target)`. Form the probability error once, then reduce it against features for weights and across samples for bias.

### Constraints

- `input` has shape `(batch_size, in_features)`.
- `p` and `target` both have shape `(batch_size, 1)`.
- Return `grad_weight` with shape `(1, in_features)` and `grad_bias` with shape `(1,)`.
- Average by `n_samples`, not `2 * n_samples`.
- Use matrix multiplication and reductions; do not use autograd or Python loops.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Keep the per-sample discrepancy as a one-column array so it can line up with the feature matrix.

</details>

<details><summary>Hint 2</summary>

Transpose that discrepancy before multiplying by `input`; sum it along axis 0 for the bias.

</details>
