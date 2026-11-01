# One Gradient-Descent Update

Beginner | classical-ml | linear-regression | gradient-descent | optimization

### The problem, from first principles

`03-mse-gradient` told you which direction the loss gets WORSE in. To make it better, you move the opposite way — that's the entirety of gradient descent, one arithmetic step repeated many times.

The only design decision is how big a step to take. Too small and training crawls; too large and you can overshoot the minimum entirely, or bounce around it forever without settling. That step size is the learning rate, and it's the one number a training loop has to pick.

### From theory to code

Theory gives the update as a single subtraction per parameter: current value minus (step size times gradient). Both `weight` and `bias` follow the identical rule — the only branch is what happens when there's no `bias` to begin with.

Implement `gd_step(weight, bias, grad_weight, grad_bias, lr)` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- Move `weight` and `bias` one step in the direction that reduces loss, scaled by `lr`, using the update rule from Theory.
- Return new values — never mutate `weight`, `bias`, `grad_weight` or `grad_bias` in place.
- If `bias` is `None` (no bias parameter, matching `01-hypothesis-function` and `03-mse-gradient`), return `None` for `updated_bias` too — there is nothing to step.
- Works for `weight`/`grad_weight` of any matching shape (scalar, vector, or matrix) — the update rule itself has no shape-specific logic.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

The update is one line per parameter: `new_value = value - lr * grad`. There's no loop, no reshaping — the same expression works whatever shape `weight` happens to be.

</details>

<details>
<summary>Hint 2</summary>

Return `weight - lr * grad_weight`, not `weight -= lr * grad_weight`. NumPy arrays are passed by reference, so the in-place version would silently mutate the caller's original array.

</details>
