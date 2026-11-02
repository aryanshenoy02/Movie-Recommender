# Full Linear Regression Training Loop

Intermediate | classical-ml | linear-regression | training-loop

### The problem, from first principles

`01-hypothesis-function`, `02-mse-loss`, `03-mse-gradient`, and `04-gd-step` each solve one part of fitting a line. A model becomes useful only when those parts run repeatedly: make predictions, measure their error, find which direction reduces it, and move the parameters. This question wires that full-batch loop together without losing the single-output shapes established earlier.

### From theory to code

Implement `train_linear_regression`. Initialize the parameters once, turn the one-dimensional targets into the one-column form expected by the earlier helpers, then use their gradient and update operations for each epoch.

### Constraints

- `input` has shape `(batch_size, in_features)` and `target` has shape `(batch_size,)`.
- Return `weight` with shape `(1, in_features)` and `bias` with shape `(1,)`.
- Start both returned parameters at zero before any updates.
- Reshape `target` once to `(batch_size, 1)` before computing gradients.
- Run exactly `epochs` full-batch gradient-descent steps; `epochs=0` returns the zero initialization.
- Reuse `mse_gradient` and `gd_step`; do not reimplement either calculation.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

The output of a single-output `linear` call is a column, even when the caller supplies targets as a flat array.

</details>

<details>
<summary>Hint 2</summary>

Create the zero `weight` from `input.shape[1]`, create `bias` with one element, and reshape `target` before the loop.

</details>

<details>
<summary>Hint 3</summary>

Each loop iteration is just `grad_weight, grad_bias = mse_gradient(...)` followed by `weight, bias = gd_step(...)` using the same `lr`.

</details>
