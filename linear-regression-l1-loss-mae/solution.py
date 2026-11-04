import numpy as np


def l1_loss(input: np.ndarray, target: np.ndarray, reduction: str = "mean") -> float | np.ndarray:
    """
    input, target: same shape, any shape.
    reduction: "mean" (default), "sum", or "none".

    Mirrors torch.nn.functional.l1_loss: mean absolute error, not
    squared error. See Theory for why this changes MSE Loss's
    behavior around outliers.
    """
    error = (np.abs(target-input))

    if reduction == "mean":
        return float(np.mean(error))
    elif reduction == "sum":
        return float(np.sum(error))
    elif reduction == "none":
        return error
    else:
        raise ValueError("Invalid Reduction")
