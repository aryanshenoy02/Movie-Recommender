# Hypothesis Function

Beginner | classical-ml | linear-regression | forward-pass

### The problem, from first principles

Say you want to estimate a house's price from things you can measure: square footage, mileage on the neighborhood, today's temperature. Each measurement matters a different amount. So the simplest possible estimator is: multiply each measurement by "how much it matters," add those up, then add one more number for the baseline value before any measurement counts.

That's the whole problem, and it has nothing to do with neural networks yet. What makes it worth a question is doing this for many houses at once, and for more than one estimate at a time, without a Python loop. Solve that, and you've implemented `torch.nn.functional.linear`: the operation inside every `nn.Linear` you'll build in this curriculum.

### From theory to code

Theory derives the one-row version: multiply each feature by its weight, sum them, add the bias. That's a dot product, `x · w`. Stack rows into a matrix `X` and the same dot product repeated per row is matrix multiplication: `X @ w`.

The one thing that doesn't fall out automatically is more than one output. `weight` has shape `(out_features, in_features)`, so each of its rows is its own independent weight vector. `input @ weight.T` lines `input` up against every one of those rows at once, computing every output feature for every sample in a single expression.

Implement `linear(input, weight, bias=None)` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- `input`: shape `(batch_size, in_features)`.
- `weight`: shape `(out_features, in_features)`.
- `bias`: shape `(out_features,)`, or `None` (no bias term added, not a zero one).
- Output: shape `(batch_size, out_features)`, always, never squeezed. Theory explains why.
- Output dtype matches `input`'s dtype exactly.
- One vectorized expression, no loop over `batch_size` or `out_features`.
- `input`, `weight` and `bias` are never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`input` and `weight` share their last dimension, not their first. Which one needs transposing before a matmul lines up?

</details>

<details>
<summary>Hint 2</summary>

`bias=None` is a real branch, not a default-to-zero. Adding `None` to an array raises a `TypeError`. Check `bias is not None` first.

</details>

<details>
<summary>Hint 3</summary>

If you reach for `.reshape`, `.squeeze()`, or `.flatten()` anywhere here, stop. A correct implementation produces the right shape directly from `input @ weight.T (+ bias)`.

</details>
