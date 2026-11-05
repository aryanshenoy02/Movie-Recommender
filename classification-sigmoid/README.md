# Sigmoid Function

Beginner | classical-ml | classification | activations

### The problem, from first principles

A linear score can be any real number, but a binary prediction needs a value that can be read as confidence for one of two outcomes. Sigmoid converts scores to that probability-like scale while retaining their ordering. This implementation also has to survive scores too extreme for a direct exponential.

### From theory to code

Implement `sigmoid(z)` elementwise. Theory gives the transform; the implementation first bounds the input so its exponential remains finite.

### Constraints

- `z` may have any NumPy array shape; preserve that shape.
- Return a finite numeric array that is monotonic in `z`.
- Return `0.5` for zero.
- Clip `z` to `[-500, 500]` before exponentiating.
- Do not use Python loops or mutate the caller's array.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

The transform is applied independently to every element, so NumPy already provides the iteration.

</details>

<details><summary>Hint 2</summary>

Clamp the raw scores before using the exponential; a negative raw score becomes a positive exponent argument.

</details>
