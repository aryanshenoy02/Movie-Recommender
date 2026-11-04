# Stretch: L1 Loss (MAE), contrasted against MSE

Beginner | classical-ml | linear-regression | loss-functions

### The problem, from first principles

Mean Squared Error Loss squares every error before averaging, which means one prediction that's wildly off (a data-entry error in the target, a genuinely unusual house that sold for 10x its neighbors) can dominate the entire loss and drag the fitted line toward accommodating that single outlier, at the expense of fitting everything else well. Mean Absolute Error takes the error's magnitude directly, no squaring, and behaves very differently in exactly this situation.

This question asks: implement L1 loss, then understand precisely why swapping MSE for L1 changes how a model responds to outliers, the same robustness distinction `02-imputing-missing-values` and `01-outlier-detection` (Math & Statistics) already introduced for mean vs. median.

### From theory to code

Theory gives the direct formula (mean of `|input - target|`, not squared). Implement it with the exact same reduction-mode signature `Mean Squared Error Loss` already established, so both losses are drop-in interchangeable in a training loop.

Implement `l1_loss(input, target, reduction="mean")` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- `input` and `target` share a shape; any shape is valid, not just 2D.
- `reduction`: `"mean"` (default), `"sum"`, or `"none"`, raise `ValueError` for anything else.
- No squaring anywhere, this is absolute error, not squared error.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.abs(input - target)` replaces MSE Loss's `(input - target) ** 2`, everything else about the reduction logic is identical.

</details>

<details>
<summary>Hint 2</summary>

Copy `Mean Squared Error Loss`'s three-branch reduction structure directly, only the elementwise error formula changes.

</details>
