import numpy as np
import pandas as pd
import networkx as nx
from dowhy import CausalModel
from scipy.optimize import minimize

from skylines.dataset import *

import warnings
warnings.filterwarnings('ignore')

import logging
logging.disable(logging.CRITICAL)


def compute_CATE(data: pd.DataFrame, graph: nx.DiGraph, treatment: str, outcome: str):
    model = CausalModel(
        data=data,
        treatment=treatment,
        outcome=outcome,
        graph=graph
    )

    identified_estimand = model.identify_effect()

    estimate = model.estimate_effect(
        identified_estimand,
        method_name='backdoor.linear_regression',
        test_significance=True
    )

    return estimate.value


def total_effect(data: pd.DataFrame, graph: nx.DiGraph):
    effect = dict()
    for edge in graph.edges:
        effect[edge] = compute_CATE(data, graph, edge[0], edge[1])
    return effect


def direct_effect(data: pd.DataFrame, graph: nx.DiGraph):
    effect = total_effect(data, graph)

    def objective(strengths):
        strengths = {edge: strengths[i] for i, edge in enumerate(graph.edges)}
        error_sum = 0

        for (X, Y) in graph.edges:
            paths = nx.all_simple_paths(graph, X, Y)
            error = -effect[(X, Y)]

            for path in paths:
                prod = 1
                for i in range(len(path) - 1):
                    prod *= strengths[(path[i], path[i + 1])]
                error += prod

            error_sum += np.abs(error)

        return error_sum

    initial_guess = np.array([0] * len(graph.edges))
    result = minimize(objective, initial_guess, method='SLSQP')

    return {edge: result.x[i] for i, edge in enumerate(graph.edges)}
