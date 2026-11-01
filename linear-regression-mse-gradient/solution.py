import numpy as np


def mse_gradient(
    input: np.ndarray,
    weight: np.ndarray,
    bias: np.ndarray | None,
    target: np.ndarray,
) -> tuple[np.ndarray, np.ndarray | None]:
    """
    input:  shape (batch_size, in_features)
    weight: shape (out_features, in_features)
    bias:   shape (out_features,), or None
    target: shape (batch_size, out_features)

    Returns:
        grad_weight: same shape as weight
        grad_bias: same shape as bias, or None if bias is None
    """
    # TODO: Implement the gradient formulas derived in Theory.
    # Do not use an autograd library -- these are the manual derivatives.
    if bias is None:
        pred = (input @ weight.T)
    else:
        pred = (input @ weight.T) + bias

    N = np.size(target)
    
    MSE = np.sum((pred - target)**2)/N

    grad = (2/N)*(pred - target)

    wgrad = grad.T @ input #should be same shape as weight matrix 
    if bias is None:
        wbias = None
    else:
        wbias = np.sum(grad, axis = 0) #should be same shape as bias matrix

    return wgrad,wbias
