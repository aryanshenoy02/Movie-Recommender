# Mean Squared Error Loss

Beginner | classical-ml | linear-regression | loss-functions

### The problem, from first principles

A model that guesses is only useful if you can measure how wrong its guesses are. One number, one clear rule: given what the model predicted and what actually happened, produce a single score where lower means better.

The obvious first idea, average the raw difference, breaks immediately: a guess that's 5 too high and one that's 5 too low average out to zero error, which is wrong, both guesses were equally bad. Squaring each difference before averaging fixes that (every error becomes positive) and, as a side effect, punishes big misses harder than small ones: an error of 10 contributes 100, not 10. That score is mean squared error, and it's what `torch.nn.functional.mse_loss` computes.

### From theory to code

Theory derives the elementwise error, square each difference, then a reduction step: average them (`'mean'`), add them up (`'sum'`), or hand back every squared error untouched (`'none'`). Real PyTorch exposes all three, because different callers want different things: training almost always wants `'mean'` (a batch-size-independent score), some manual bookkeeping wants `'sum'`, and anything that needs to look at individual errors before combining them, like weighting some samples more than others, needs `'none'`.

Implement `mse_loss(input, target, reduction='mean')` against that reasoning. The signature and docstring are already in the editor.

### Constraints

- `input`, `target`: same shape as each other, any shape.
- `reduction`: `'mean'`, `'sum'`, or `'none'`. Anything else raises `ValueError`.
- Return type depends on `reduction`: a plain Python `float` for `'mean'`/`'sum'`, an array shaped like `input` for `'none'`.
- One vectorized expression per branch, no loop over elements.
- `input` and `target` are never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Compute the elementwise squared error once, before branching on `reduction`. All three modes start from the exact same array.

</details>

<details>
<summary>Hint 2</summary>

`'mean'` and `'sum'` both need a `float(...)` cast around a NumPy reduction. Returning a bare NumPy scalar (like `np.float64`) instead of a real `float` is a common, easy-to-miss mismatch.

</details>

<details>
<summary>Hint 3</summary>

Handle the invalid-reduction case last, as an `else` that raises `ValueError`, not a silent fallback to one of the other two. A typo in the caller's `reduction` argument should never quietly compute the wrong thing.

</details>
