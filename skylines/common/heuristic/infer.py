from skylines import leakage, data_driven, skip_gain_le_zero
from skylines.heuristic import algorithm0, algorithm4_leaky
from skylines.common.utils import find_powerset, parse_set_repr, is_redundant
from skylines.dataset import Dataset


def best_controls(dataset: Dataset, weighted: bool = True, filter_supersets: bool = True) -> list[frozenset[str]]:
    # find controls
    controls = find_powerset(dataset.variates)

    if data_driven:
        # compute gain
        scores = algorithm0.gain(dataset, controls)

        # gain column
        column = 'Gain'

        # find best gains
        scores = scores[scores[column] == scores[column].max()]

    else:
        # compute gain
        scores = algorithm4_leaky.gain_all(dataset, controls, leakage)

        # gain column
        if weighted:
            column = 'Weighted Gain'
        else:
            column = 'Unweighted Gain'

        # skip if gain <= 0
        if skip_gain_le_zero and scores[column].max() <= 0:
            return scores[column].max()

        # find best gains
        scores = scores[scores[column] == scores[column].max()]

    # filter supersets
    if filter_supersets:
        accepted = []
        accepted_sets = []

        for idx in scores.index:
            curr = parse_set_repr(idx)

            if is_redundant(accepted_sets, curr):
                continue

            accepted.append(idx)
            accepted_sets.append(frozenset(curr))

    else:
        accepted_sets = [frozenset(parse_set_repr(idx)) for idx in scores.index]

    return accepted_sets
