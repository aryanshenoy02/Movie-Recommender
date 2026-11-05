
import numpy as np

from _load import load_solution


def train_val_split(
    input: np.ndarray, target: np.ndarray, val_fraction: float = 0.2, seed: int | None = None
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Shuffles `input`/`target` together (so a row's features and its
    target stay paired), then splits off `val_fraction` of the rows as
    a held-out validation set.

    Returns (input_train, target_train, input_val, target_val).
    """
    rng = np.random.default_rng(seed=42)
    shuffled_indices = rng.permutation(len(input))

    input = input[shuffled_indices]
    target = target[shuffled_indices]
    
    val_size = round(len(input) * val_fraction)

    input_val = input[:val_size]
    target_val = target[:val_size]
    
    input_train = input[val_size:]
    target_train = target[val_size:]

    return input_train, target_train, input_val, target_val
    
def generalization_gap(train_loss: float, val_loss: float) -> float:
    """
    The generalization gap: how much worse the model performs on data
    it never trained on, compared to the data it did. A large positive
    gap is the numerical signature of overfitting.
    """
    return val_loss - train_loss
