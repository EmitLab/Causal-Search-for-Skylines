import numpy as np
import pandas as pd

from skylines import n_bins
from skylines.common.utils import set_repr, cluster
from skylines.dataset import Dataset


def block_sum(block: np.ndarray) -> float:
    # remove zero-variance columns
    std = np.std(block, axis=0)
    mask = std > 0

    # not enough variables to correlate
    if np.sum(mask) < 2:
        return 0.0

    # compute correlation for block
    block = block[:, mask]
    block_corr = np.corrcoef(block, rowvar=False)

    # compute sum of pairwise correlations
    block_sum = 0.0
    for i in range(block.shape[1] - 1):
        for j in range(i + 1, block.shape[1]):
            block_sum += 2 * block_corr[i, j]

    return block_sum


def control_gain(data: np.ndarray, corr_sum: float, preferences: list[int], controls: list[int], bins: int) -> float:
    # cluster into groups
    groups = cluster(data, preferences, controls, bins)

    # compute sum of pairwise correlations
    block_corr = []

    for group in groups:
        if len(group) < 2:
            continue

        block = data[np.ix_(group, preferences)]
        block_corr.append(block_sum(block))

    # compute correlation gain
    corr_gain = sum(block_corr) / len(block_corr) - corr_sum

    return corr_gain


def compute_gain(data: np.ndarray, variates: dict[str, int], preferences: dict[str, int], controls: list[frozenset[str]], bins: int) -> pd.DataFrame:
    # compute sum of pairwise correlations
    block = data[:, list(preferences.values())]
    corr_sum: float = block_sum(block)

    # compute the gains
    gain_dict = {}
    for control in controls:
        gain_dict[set_repr(control)] = control_gain(data, corr_sum, list(preferences.values()), [variates[col] for col in control], bins)

    # convert to dataframe
    df = pd.Series(gain_dict, name='Gain').to_frame()
    df.index.name = 'Control'

    return df


def gain(dataset: Dataset, controls: list[frozenset[str]], bins: int = n_bins) -> pd.DataFrame:
    # convert dataframe to numpy
    data, variates, preferences = dataset.to_numpy()

    # compute the gains
    scores = compute_gain(data, variates, preferences, controls, bins)

    return scores
