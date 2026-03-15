import networkx as nx
import pandas as pd

from skylines.common.utils import set_repr
from skylines.dataset import Dataset


def count_endpoints(path: list[str], controls: frozenset) -> (int, int):
    unblocked = 0
    blocked = 0

    if path[0] in controls:
        blocked += 1
    else:
        unblocked += 1

    if path[-1] in controls:
        blocked += 1
    else:
        unblocked += 1

    return unblocked, blocked


def count_mediators(graph: nx.DiGraph, path: list[str], controls: frozenset) -> (int, int):
    unblocked = 0
    blocked = 0

    for i in range(len(path) - 2):
        for j in range(i + 1, len(path) - 1):
            if ((graph.has_edge(path[i], path[j]) and graph.has_edge(path[j], path[j + 1])) or
                    (graph.has_edge(path[j], path[i]) and graph.has_edge(path[j + 1], path[j]))):
                # mediator is in controls
                if path[j] in controls:
                    blocked += 1
                else:
                    unblocked += 1

    return unblocked, blocked


def count_forks(graph: nx.DiGraph, path: list[str], controls: frozenset) -> (int, int):
    unblocked = 0
    blocked = 0

    for i in range(len(path) - 2):
        for j in range(i + 1, len(path) - 1):
            if graph.has_edge(path[j], path[i]) and graph.has_edge(path[j], path[j + 1]):
                # fork is in controls
                if path[j] in controls:
                    blocked += 1
                else:
                    unblocked += 1
    return unblocked, blocked


def count_colliders(graph: nx.DiGraph, path: list[str], controls: frozenset) -> (int, int):
    unblocked = 0
    blocked = 0

    for i in range(len(path) - 2):
        for j in range(i + 1, len(path) - 1):
            if graph.has_edge(path[i], path[j]) and graph.has_edge(path[j + 1], path[j]):
                # collider is in controls
                if path[j] in controls:
                    unblocked += 1

                else:
                    # any descendant of collider is in controls
                    for descendant in nx.descendants(graph, path[i]):
                        if descendant in controls:
                            unblocked += 1
                            break

                    # collider and none of its descendants are in controls
                    else:
                        blocked += 1

    return unblocked, blocked


def path_weight(dataset: Dataset, graph: nx.DiGraph, undirected: nx.Graph, path: list[str], controls: frozenset, leakage: tuple[float, float], weighted: bool) -> float:
    # get number of unblocked and blocked colliders, mediators, and forks
    unblocked_colliders, blocked_colliders = count_colliders(graph, path, controls)
    unblocked_mediators, blocked_mediators = count_mediators(graph, path, controls)
    unblocked_forks, blocked_forks = count_forks(graph, path, controls)
    unblocked_endpoints, blocked_endpoints = count_endpoints(path, controls)

    weight = (-1) ** unblocked_colliders

    if dataset.dominance[path[0]] != dataset.dominance[path[-1]]:
        weight *= -1

    for i in range(len(path) - 1):
        edge_weight = undirected.get_edge_data(path[i], path[i + 1])['weight']
        weight *= edge_weight

    unblocked_information = leakage[0] ** (unblocked_colliders + unblocked_mediators + unblocked_forks + unblocked_endpoints)
    blocked_information = leakage[1] ** (blocked_colliders + blocked_mediators + blocked_forks + blocked_endpoints)

    if weighted:
        return weight * unblocked_information * blocked_information

    else:
        sign = (weight > 0) - (weight < 0)  # +1, -1, or 0
        return sign * unblocked_information * blocked_information


def count_open_paths(dataset: Dataset, controls: frozenset, source: any, target: any, weighted: bool, leakage: tuple[float, float]) -> (float, float):
    # convert to undirected graph
    graph = dataset.masked_graph
    undirected = graph.to_undirected()

    # find all paths between source and target
    paths = nx.all_simple_paths(undirected, source, target)

    # count positive and negative open paths
    positive = 0
    negative = 0

    for path in paths:
        # compute the path weight
        weight = path_weight(dataset, graph, undirected, path, controls, leakage, weighted)

        # positive path
        if weight > 0:
            positive += weight

        # negative path
        elif weight < 0:
            negative += weight

    return positive, negative


def control_gain(dataset: Dataset, controls: frozenset, weighted: bool, leakage: tuple[float, float]) -> float:
    overall_gain = 0

    for i in range(len(dataset.preference) - 1):
        for j in range(i + 1, len(dataset.preference)):
            # count open paths before conditioning
            positive, negative = count_open_paths(dataset,
                                                  frozenset(),  # unconditioned
                                                  dataset.preference[i],  # source
                                                  dataset.preference[j],  # sink
                                                  weighted,
                                                  leakage)

            # count open paths after conditioning
            positive_control, negative_control = count_open_paths(dataset,
                                                                  controls,  # conditioned
                                                                  dataset.preference[i],  # source
                                                                  dataset.preference[j],  # sink
                                                                  weighted,
                                                                  leakage)

            # compute impact
            imp_positive = positive_control - positive
            imp_negative = -(negative_control - negative)

            # compute gain
            overall_gain += imp_positive - imp_negative

    return overall_gain


def gain(dataset: Dataset, weighted: bool, controls: list[frozenset[str]], leakage: tuple[float, float]) -> pd.DataFrame:
    # compute the gains
    gain_dict = {}
    for control in controls:
        gain_dict[set_repr(control)] = control_gain(dataset, control, weighted, leakage)

    # convert to dataframe
    df = pd.Series(gain_dict, name='Gain').to_frame()
    df.index.name = 'Control'

    return df


def gain_all(dataset: Dataset, controls: list[frozenset[str]], leakage: tuple[float, float]) -> pd.DataFrame:
    # compute the gains
    scores_unweighted = gain(dataset, False, controls, leakage)
    scores_weighted = gain(dataset, True, controls, leakage)

    # concatenate the results
    scores = pd.concat([scores_unweighted, scores_weighted], axis=1)
    scores.columns = ['Unweighted Gain', 'Weighted Gain']

    return scores
