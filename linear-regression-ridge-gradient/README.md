# Stretch: L2 Regularization (Ridge)

Intermediate | classical-ml | linear-regression | regularization | stretch

### The problem, from first principles

Ordinary MSE only rewards matching the observed data. When features carry nearly the same information, many large, fragile weight combinations can fit equally well. Ridge regularization makes such solutions less attractive by charging for weight magnitude. It extends the gradient from `03-mse-gradient` without changing the model or the bias convention.

### From theory to code

Implement `ridge_grad` by asking `mse_gradient` for the data-fit gradient, then add the regularizer's contribution to the weight part only. Theory derives why the bias follows the original result unchanged.

### Constraints

- `input`, `weight`, `bias`, and `target` use the same shapes accepted by `mse_gradient`.
- Return a weight gradient with the same shape as `weight`.
- Return the exact base bias gradient, including `None` when `bias is None`.
- `lam=0` must match the unregularized MSE gradient.
- Penalize weights only; never add a penalty to the bias gradient.
- Reuse `mse_gradient` and do not mutate its returned arrays in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Treat regularization as an additional objective term, not a replacement for the MSE calculation.

</details>

<details>
<summary>Hint 2</summary>

The derivative of the squared-weight penalty has the same shape as `weight`, so it can be added directly to `grad_weight`.

</details>
