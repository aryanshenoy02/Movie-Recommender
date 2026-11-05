# Full Training Loop

Intermediate | classical-ml | classification | training-loop

### The problem, from first principles

The earlier classification questions define a score, turn it into a probability, and determine the direction to correct it. Training is the repeated process that connects those pieces so a classifier learns its parameters from all examples.

### From theory to code

Implement `train_logistic_regression` by reusing `linear`, `sigmoid`, `bce_gradient`, and `gd_step` in their forward-to-update order.

### Constraints

- `input` is `(batch_size, in_features)` and binary `target` is `(batch_size,)`.
- Return `(weight, bias)` with shapes `(1, in_features)` and `(1,)`.
- Initialize both parameters to zero and reshape targets once to `(batch_size, 1)`.
- Run exactly `epochs` full-batch updates; zero epochs returns the initialization.
- Do not reimplement the imported helpers or use loops over samples.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

The forward pass has two stages: a linear score followed by a probability activation.

</details>

<details><summary>Hint 2</summary>

Within each epoch, pass `sigmoid(linear(...))` and the reshaped targets to `bce_gradient`, then hand its results to `gd_step`.

</details>
