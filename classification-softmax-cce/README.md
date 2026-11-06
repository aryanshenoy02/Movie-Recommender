# Stretch: Softmax + Categorical Cross-Entropy

Intermediate | classical-ml | classification | multi-class | stretch

### The problem, from first principles

Binary sigmoid chooses between two outcomes. Multiclass classification needs every candidate class to compete for one shared unit of confidence, then needs a loss that scores only the probability assigned to each example's true class.

### From theory to code

Implement row-wise `softmax(Z)` and `cce_loss(P, y_indices)`. Theory maps the stable normalization and the one-correct-class lookup to the exact NumPy operations.

### Constraints

- `Z` and `P` have shape `(n_samples, n_classes)`; each softmax row sums to one.
- `y_indices` has one integer class index per sample.
- Subtract every row's maximum before exponentiating.
- Select one correct-class probability per row, clip it to `[1e-12, 1.0]`, and return a Python `float`.
- Use `P[np.arange(n), y_indices]`, not an all-rows column selection.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Rows are independent probability distributions, so reductions must use `axis=1` and preserve the column dimension.

</details>

<details><summary>Hint 2</summary>

Build row indices with `np.arange(P.shape[0])`; pair them with `y_indices` to gather exactly one value from each row.

</details>
