from collections import defaultdict
import logging
import warnings
import pandas as pd
import networkx as nx

from skylines.common.causal.notears import NotearsStrict
from skylines.common.utils import scale_variance


logging.disable(logging.INFO)
warnings.simplefilter("ignore", FutureWarning)


# def break_cycles(dag):
#     dag = dag.copy()

#     while not nx.is_directed_acyclic_graph(dag):
#         cycle = next(nx.simple_cycles(dag))
#         edges_in_cycle = [(cycle[i], cycle[(i + 1) % len(cycle)]) for i in range(len(cycle))]

#         # compute "impact" of removing each edge: number of reachable pairs it disconnects
#         impacts = {}
#         for u, v in edges_in_cycle:
#             dag_tmp = dag.copy()
#             dag_tmp.remove_edge(u, v)
            
#             # number of reachable pairs
#             reachable = sum(len(nx.descendants(dag_tmp, n)) for n in dag_tmp.nodes)
#             impacts[(u, v)] = reachable

#         # remove edge that maximizes reachable pairs (i.e., minimal impact)
#         edge_to_remove = max(impacts, key=impacts.get)
#         dag.remove_edge(*edge_to_remove)

#     return dag


def learn_dag(df: pd.DataFrame):
    vars = list(df.columns)

    # variance normalization
    df = scale_variance(df)
    
    # discover DAG
    model = NotearsStrict()
    model.learn(df)

    # adjacency matrix
    adj = model.causal_matrix * model.weight_causal_matrix

    # convert to a directed graph
    dag = nx.from_numpy_array(adj, create_using=nx.DiGraph)
    dag = nx.relabel_nodes(dag, {idx: col for idx, col in enumerate(vars)})

    # convert to dict of dicts form
    effect = defaultdict(dict)
    for (src, snk, strength) in dag.edges(data="weight"):
        effect[snk][src] = strength
    
    return dict(effect)
