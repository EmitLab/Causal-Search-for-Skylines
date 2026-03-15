import networkx as nx

from castle.algorithms import Notears
from castle.common import Tensor
import numpy as np


class NotearsStrict(Notears):

    def __init__(self, lambda1=0.1, 
                 loss_type='l2', 
                 max_iter=100, 
                 h_tol=1e-8, 
                 rho_max=1e+16, 
                 w_threshold=0.3):
        super().__init__(lambda1=lambda1,
                         loss_type=loss_type,
                         max_iter=max_iter,
                         h_tol=h_tol,
                         rho_max=rho_max,
                         w_threshold=w_threshold)

    def learn(self, data, columns=None, **kwargs):
        """
        Set up and run the Notears algorithm.

        Parameters
        ----------
        data: castle.Tensor or numpy.ndarray
            The castle.Tensor or numpy.ndarray format data you want to learn.
        columns : Index or array-like
            Column labels to use for resulting tensor. Will default to
            RangeIndex (0, 1, 2, ..., n) if no column labels are provided.
        """
        X = Tensor(data, columns=columns)

        W_est = self.notears_linear(X, lambda1=self.lambda1, 
                                    loss_type=self.loss_type, 
                                    max_iter=self.max_iter, 
                                    h_tol=self.h_tol, 
                                    rho_max=self.rho_max)
        W_est = self._break_cycles(W_est)
        causal_matrix = (abs(W_est) > self.w_threshold).astype(int)
        self.weight_causal_matrix = Tensor(W_est,
                                           index=X.columns,
                                           columns=X.columns)
        self.causal_matrix = Tensor(causal_matrix, index=X.columns,
                                    columns=X.columns)
        
    @staticmethod
    def _order_from_weights(W):
        """
        Deterministic node ordering that maximizes forward NOTEARS weight.
        """
        d = W.shape[0]
        nodes = list(range(d))
        order = []

        score = np.abs(W) - np.abs(W.T)

        while nodes:
            # net outgoing preference
            net = {i: sum(score[i, j] for j in nodes if j != i) for i in nodes}

            # pick node with maximum net score (tie-break by index)
            v = max(net.items(), key=lambda x: (x[1], -x[0]))[0]

            order.append(v)
            nodes.remove(v)

        return order
    
    @staticmethod
    def _dag_from_order(W, order):
        """
        Remove edges inconsistent with a given node ordering.
        """
        pos = {v: i for i, v in enumerate(order)}
        W_dag = W.copy()

        for i in range(W.shape[0]):
            for j in range(W.shape[1]):
                if W_dag[i, j] != 0 and pos[i] > pos[j]:
                    W_dag[i, j] = 0.0

        return W_dag
    
    @staticmethod
    def _break_cycles(W):
        order = NotearsStrict._order_from_weights(W)
        return NotearsStrict._dag_from_order(W, order)
