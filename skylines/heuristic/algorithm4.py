import networkx as nx
import pandas as pd

from skylines.common.utils import set_repr
from skylines.dataset import Dataset


def has_blocked_endpoints(path: list[str], controls: frozenset) -> bool:
    return path[0] in controls or path[-1] in controls


def has_blocked_mediator(graph: nx.DiGraph, path: list[str], controls: frozenset) -> bool:
    for i in range(1, len(path) - 1):
        if path[i] in controls and (
                (graph.has_edge(path[i - 1], path[i]) and graph.has_edge(path[i], path[i + 1])) or
                (graph.has_edge(path[i], path[i - 1]) and graph.has_edge(path[i + 1], path[i]))):
            return True
    return False


def has_blocked_fork(graph: nx.DiGraph, path: list[str], controls: frozenset) -> bool:
    for i in range(1, len(path) - 1):
        if path[i] in controls and graph.has_edge(path[i], path[i - 1]) and graph.has_edge(path[i], path[i + 1]):
            return True
    return False


def count_colliders(graph: nx.DiGraph, path: list[int], controls: frozenset) -> (int, int):
    unblocked = 0
    blocked = 0

    for i in range(1, len(path) - 1):
        if graph.has_edge(path[i - 1], path[i]) and graph.has_edge(path[i + 1], path[i]):
            # collider is in controls
            if path[i] in controls:
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


def path_weight(dataset: Dataset, graph: nx.Graph, path: list[str], unblocked: int) -> float:
    weight = (-1) ** unblocked

    if dataset.dominance[path[0]] != dataset.dominance[path[-1]]:
        weight *= -1

    for i in range(len(path) - 1):
        edge_weight = graph.get_edge_data(path[i], path[i + 1])['weight']
        weight *= edge_weight

    return weight


def count_open_paths(dataset: Dataset, controls: frozenset, source: any, target: any, weighted: bool) -> (float, float):
    # convert to undirected graph
    graph = dataset.masked_graph
    undirected = graph.to_undirected()

    # find all paths between source and target
    paths = nx.all_simple_paths(undirected, source, target)

    # count positive and negative open paths
    positive = 0
    negative = 0

    for path in paths:
        # get number of unblocked and blocked colliders
        unblocked, blocked = count_colliders(graph, path, controls)

        # ignore path if it contains a blocked collider, mediator, or fork
        if blocked > 0 or has_blocked_mediator(graph, path, controls) or has_blocked_fork(graph, path, controls) or has_blocked_endpoints(path, controls):
            continue

        # compute the path weight
        weight = path_weight(dataset, undirected, path, unblocked)

        # positive path
        if weight > 0:
            positive += weight if weighted else 1

        # negative path
        elif weight < 0:
            negative += weight if weighted else -1

    return positive, negative


def control_gain(dataset: Dataset, controls: frozenset, weighted: bool) -> float:
    overall_gain = 0

    for i in range(len(dataset.preference) - 1):
        for j in range(i + 1, len(dataset.preference)):
            # count open paths before conditioning
            positive, negative = count_open_paths(dataset,
                                                  frozenset(),  # unconditioned
                                                  dataset.preference[i],  # source
                                                  dataset.preference[j],  # sink
                                                  weighted)

            # count open paths after conditioning
            positive_control, negative_control = count_open_paths(dataset,
                                                                  controls,  # conditioned
                                                                  dataset.preference[i],  # source
                                                                  dataset.preference[j],  # sink
                                                                  weighted)

            # compute impact
            imp_positive = positive_control - positive
            imp_negative = -(negative_control - negative)

            # compute gain
            overall_gain += imp_positive - imp_negative

    return overall_gain


def gain(dataset: Dataset, weighted: bool, controls: list[frozenset[str]]) -> pd.DataFrame:
    # compute the gains
    gain_dict = {}
    for control in controls:
        gain_dict[set_repr(control)] = control_gain(dataset, control, weighted)

    # convert to dataframe
    df = pd.Series(gain_dict, name='Gain').to_frame()
    df.index.name = 'Control'

    return df


def gain_all(dataset: Dataset, controls: list[frozenset[str]]) -> pd.DataFrame:
    # compute the gains
    scores_unweighted = gain(dataset, False, controls)
    scores_weighted = gain(dataset, True, controls)

    # concatenate the results
    scores = pd.concat([scores_unweighted, scores_weighted], axis=1)
    scores.columns = ['Unweighted Gain', 'Weighted Gain']

    return scores
