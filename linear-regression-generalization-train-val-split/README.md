# Generalization: train/val split and the generalization gap

Intermediate | classical-ml | linear-regression | evaluation

### The problem, from first principles

`Full Linear Regression Training Loop` trains a model and reports its loss, but a subtle trap lurks in that number: a loss computed on the EXACT data the model trained on tells you how well the model memorized that data, not how well it will perform on new data it's never seen. A model with enough flexibility (enough parameters relative to how much data it has) can drive training loss arbitrarily close to zero by essentially memorizing quirks and noise specific to the training set, while performing badly on anything new, the textbook definition of overfitting.

The fix is procedural, not algorithmic: hold out a chunk of data the model NEVER trains on, and evaluate on that held-out set instead. The gap between training performance and held-out performance is itself a measurement, the generalization gap, and it's the single most important diagnostic for "is this model actually learning something general, or just memorizing."

### From theory to code

Theory splits data into a training portion and a validation portion (shuffled first, so the split isn't accidentally biased by whatever order the data happened to arrive in), then defines the generalization gap as simply validation loss minus training loss.

Implement `train_val_split(input, target, val_fraction=0.2, seed=None)` first, then `generalization_gap(train_loss, val_loss)` on top of it.

### Constraints

- Shuffle `input` and `target` TOGETHER using the same permutation, a row's features must stay paired with its own target.
- `val_fraction` controls the split size; `round(n * val_fraction)` rows go to validation.
- Same `seed` must produce the same split (reproducibility, matching `01-sampling-estimating-distribution`'s convention).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`rng.permutation(n)` gives one shuffled order; index BOTH `input` and `target` with that same order to keep pairs aligned.

</details>

<details>
<summary>Hint 2</summary>

`generalization_gap` is a one-line subtraction, `val_loss - train_loss`.

</details>
