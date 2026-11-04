# Stretch: Huber Loss, quadratic near zero and linear far from it

Intermediate | classical-ml | linear-regression | loss-functions

### The problem, from first principles

`08-l1-loss-mae` and `Mean Squared Error Loss` sit at two extremes: MSE has smooth, well-behaved gradients but is dragged around by outliers; L1 is outlier-robust but has a constant-magnitude gradient everywhere, including right at the optimum, which can make training oscillate rather than settle smoothly. Huber loss is the deliberate middle ground: behave like MSE (smooth, small gradients) for typical, small errors, and switch to behaving like L1 (bounded, outlier-resistant) once an error crosses a threshold.

The part that makes Huber loss genuinely well-designed, not just "average the two formulas", is that the two branches are chosen specifically so they meet seamlessly at the switch point: same value, same slope, no kink, no discontinuity a gradient-based optimizer would stumble on.

### From theory to code

Theory gives the exact piecewise formula and a threshold `delta` controlling where the switch happens. Implement it directly with `np.where`, reusing the reduction-mode pattern `Mean Squared Error Loss` and `08-l1-loss-mae` both already established.

Implement `huber_loss(input, target, delta=1.0, reduction="mean")` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- The branch boundary uses `<=` for the quadratic case (matching real PyTorch's convention at exactly `|error| == delta`).
- `delta` defaults to `1.0`, matching `torch.nn.functional.huber_loss`'s own default.
- Same `reduction` modes (`"mean"`, `"sum"`, `"none"`) as the other two losses in this track.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Compute both branches for every element (`0.5 * error**2` and `delta * (abs_error - 0.5*delta)`), then `np.where(abs_error <= delta, quadratic, linear)` picks the right one per element.

</details>

<details>
<summary>Hint 2</summary>

Plug `abs_error = delta` into both formulas by hand: `0.5*delta^2` and `delta*(delta - 0.5*delta) = 0.5*delta^2`, they agree exactly, that's the "seamless" property Theory describes.

</details>
