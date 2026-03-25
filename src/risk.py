import numpy as np


def summarize_with_uncertainty(predictions):
    return {
        "mean": float(np.mean(predictions)),
        "p5": float(np.percentile(predictions, 5)),
        "p95": float(np.percentile(predictions, 95)),
    }