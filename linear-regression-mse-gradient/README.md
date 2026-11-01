# Gradient of MSE with Respect to w and b

Intermediate | classical-ml | linear-regression | manual-calculus | gradients

### The problem, from first principles

`01-hypothesis-function` computes a prediction. `02-mse-loss` scores how wrong that prediction is. Neither one tells you which direction to nudge `weight` and `bias` to make that score smaller — that's a separate question, and it's the one this exercise answers.

The score is a single number computed from every prediction at once, so "which direction" isn't one number either — it's one number per entry of `weight` and one per entry of `bias`, each telling you how much that specific parameter contributed to the current wrongness. That collection of per-parameter directions is the gradient, and it's the only thing a training loop actually needs to know before it can improve anything.

### From theory to code

Theory derives it in two matched pieces: how the loss changes with the prediction, then how that flows back through the linear forward pass to `weight` and `bias`. The first piece is a direct derivative of the squared-error formula. The second piece reuses the exact shape relationship `01-hypothesis-function` established, just run in the opposite direction.

Implement `mse_gradient(input, weight, bias, target)` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- `input`: shape `(batch_size, in_features)`.
- `weight`: shape `(out_features, in_features)`.
- `bias`: shape `(out_features,)`, or `None`.
- `target`: shape `(batch_size, out_features)`.
- Returns `(grad_weight, grad_bias)`: `grad_weight` always has `weight`'s shape; `grad_bias` has `bias`'s shape, or is exactly `None` when `bias` is `None` — never a zero array standing in for it.
- The mean reduction is over every element (`batch_size * out_features` total), the same convention `02-mse-loss` uses.
- No autograd library. These are the manual derivatives.
- `input`, `weight`, `bias` and `target` are never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Start from the prediction, not from `weight` directly. `d(loss)/d(weight)` is easiest to find by first finding `d(loss)/d(prediction)`, then asking how `prediction` itself depends on `weight`.

</details>

<details>
<summary>Hint 2</summary>

`prediction = input @ weight.T (+ bias)`. Differentiating the mean of squares gives `d(loss)/d(prediction) = (2/N) * (prediction - target)`, where `N` is the total element count — not the batch size alone.

</details>

<details>
<summary>Hint 3</summary>

`weight`'s gradient is a matrix product (`d(loss)/d(prediction).T @ input`) because `weight` interacts with every feature of `input`. `bias`'s gradient is a plain sum over the batch axis, because `bias` is added identically to every row and doesn't interact with anything else.

</details>
