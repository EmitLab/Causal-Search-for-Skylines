import re
import time
from collections import defaultdict
from itertools import chain, combinations

import numpy as np
import pandas as pd

from skylines.common.kmeans import KMeans


def list_of_sets_repr(ls: list[set | frozenset]) -> (str | None):
    if len(ls) == 0:
        return 'None'
    return str(', '.join([set_repr(s) for s in ls]))


def set_repr(s: set | frozenset) -> (str | None):
    return '{' + ', '.join(sorted(s)) + '}'


def parse_set_repr(s: str) -> set:
    content = s.strip('{}')
    if not content:
        return set()
    return set(content.split(', '))


def safe_str(s: str) -> str:
    return re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', s)


def format_num(n_samples: int) -> str:
    if n_samples >= 1000000:
        return f'{n_samples // 1000000}M'
    elif n_samples >= 1000:
        return f'{n_samples // 1000}K'
    else:
        return str(n_samples)


def scale_minmax(data: np.ndarray | pd.DataFrame) -> np.ndarray | pd.DataFrame:
    """ min-max normalization """
    mins = np.min(data, axis=0)
    maxs = np.max(data, axis=0)
    ranges = maxs - mins
    
    ranges[ranges == 0] = 1.0

    return (data - mins) / ranges


def scale_variance(data: np.ndarray| pd.DataFrame) -> np.ndarray | pd.DataFrame:
    """ z-score normalization """
    means = np.mean(data, axis=0)
    stds = np.std(data, axis=0, ddof=0)

    stds[stds == 0] = 1.0

    return (data - means) / stds


def find_powerset(iterable) -> list[frozenset]:
    s = list(iterable)
    p = chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))
    powerset = [frozenset(t) for t in p if t]
    return sorted(powerset, key=len)


def is_redundant(existing_sets, target_set):
    existing_sets = [existing_set for existing_set in existing_sets if target_set.issuperset(existing_set)]
    if not existing_sets:
        return False
    return set().union(*existing_sets) != target_set


def reassign_clusters(data, labels):
    n_samples, n_features = data.shape
    k = np.max(labels) + 1

    # Compute cluster centroids efficiently
    counts = np.bincount(labels, minlength=k)
    centroids = np.zeros((k, n_features), dtype=data.dtype)
    np.add.at(centroids, labels, data)
    centroids /= counts[:, None]  # Broadcasting division

    # Assign points to nearest centroid using vectorized distance computation
    diff = data[:, None, :] - centroids[None, :, :]
    squared_diff = np.square(diff)
    sum_squared_diff = squared_diff.sum(axis=2)

    # Assign labels based on the minimum distance
    return np.argmin(sum_squared_diff, axis=1)


def cluster(data: np.ndarray, preferences: list[int], controls: list[int], bins: int, voronoi: bool = False) -> list[np.ndarray]:
    # variance normalization
    data = scale_variance(data)

    # group based on clusterby
    kmeans = KMeans(bins=bins, max_iterations=10, tolerance=0.01, seed=42)
    kmeans.cluster(data[:, controls])
    labels = kmeans.labels

    # reassign cluster labels
    if voronoi:
        labels = reassign_clusters(data[:, preferences], labels)

    # convert to list of arrays of indices
    clusters = [np.where(labels == i)[0] for i in range(bins)]
    clusters = [c for c in clusters if len(c) > 0]

    return clusters


def groupby(data: np.ndarray, controls: list[int]) -> list[np.ndarray]:
    # group based on unique combinations
    keys = np.unique(data[:, controls], axis=0)
    clusters = [np.where(np.all(data[:, controls] == key, axis=1))[0] for key in keys]

    # convert to list of arrays of indices
    clusters = [c for c in clusters if len(c) > 0]

    return clusters


def time_function(func, *args, **kwargs):
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    elapsed = end - start
    return result, elapsed
