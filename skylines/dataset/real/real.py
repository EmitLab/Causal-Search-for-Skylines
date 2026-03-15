import json
import os.path
from pathlib import Path

import numpy as np
import pandas as pd

from skylines import infer_graph, skip_inference
from skylines.common.state import get_state
from skylines.common.utils import format_num, safe_str
from skylines.dataset import Dataset, Dominance


class RealDataset(Dataset):

    def __init__(self,
                 file_name: str,
                 control: list[str],
                 preference: list[str],
                 effect: dict[str, dict[str, float]],
                 dominance: dict[str, Dominance] = None,
                 infer_controls: dict[str, Dominance] = None,
                 masked_nodes: list[str] = None,
                 masked_edges: list[tuple[str, str]] = None,
                 infer_graph: bool = infer_graph,
                 size: int = 10000,
                 seed: int = 42,
                 provided: bool = False,
                 actual_name: str = None):

        self.file_name = file_name
        self.provided = provided

        super().__init__(control=control,
                         preference=preference,
                         dominance=dominance,
                         effect=effect,
                         infer_controls=infer_controls,
                         masked_nodes=masked_nodes,
                         masked_edges=masked_edges,
                         infer_graph=infer_graph,
                         size=size,
                         seed=seed)


        if not skip_inference and self.infer_controls is not None:
            dataset: Dataset = RealDataset(file_name=self.file_name,
                                           control=self.control,
                                           preference=self.preference,
                                           effect=self.effect,
                                           dominance=self.infer_controls,
                                           infer_controls=None,
                                           masked_nodes=self.masked_nodes,
                                           masked_edges=self.masked_edges,
                                           infer_graph=infer_graph,
                                           size=self.size,
                                           seed=self.seed,
                                           provided=self.provided,
                                           actual_name=self.name)

            from skylines.common.heuristic import best_controls
            self.constant_controls = best_controls(dataset)

        self._data = self._load()

        if not skip_inference and self.infer_graph:
            self._graph = None
            self._masked_graph = None
            if actual_name is None:
                actual_name = self.name
            with open(f'graphs/{actual_name}.json', 'r') as f:
                self.effect = json.load(f)

    @property
    def data(self) -> pd.DataFrame:
        return self._data

    def _load(self) -> pd.DataFrame:
        if self.provided:
            # load dataframe
            file_path = os.path.join(Path(__file__).parent.resolve(), 'data', self.file_name, f'{self.file_name}_{format_num(self.size)}_{self.seed}.csv')
            df = pd.read_csv(file_path)
            df.columns = [safe_str(col) for col in df.columns]
            df = df[self.variates]

            # force convert to numeric
            df = df.apply(pd.to_numeric, errors='coerce')

        else:
            # load dataframe
            file_path = os.path.join(Path(__file__).parent.resolve(), 'data', self.file_name, f'{self.file_name}.csv')
            df = pd.read_csv(file_path)
            df.columns = [safe_str(col) for col in df.columns]
            df = df[self.variates]

            # force convert to numeric
            df = df.apply(pd.to_numeric, errors='coerce')

            # set the seed
            np.random.seed(self.seed)

            # generate synthetic samples
            post_df = df.sample(n=self.size, replace=True).reset_index(drop=True)

            for column in df.columns:
                # generate gaussian noise
                noise = np.random.normal(loc=0,
                                         scale=df[column].std() / 6,
                                         size=self.size)
                post_df[column] += noise

                # constraint for non-negative columns
                if df[column].min() == 0:
                    index = ~post_df[column].isna()
                    post_df.loc[index, column] = post_df.loc[index, column].mask(post_df.loc[index, column] < 0, 0)

                # constraint for integer columns
                if df[column].apply(lambda x: x.is_integer() | np.isnan(x)).all():
                    post_df[column] = np.round(post_df[column])

            df = post_df

        # fill NaNs
        df = df.fillna(df.max() + df.std())

        # store the data
        # file_path = get_state().get_file('data', f'{self.name}.csv')
        # df.to_csv(file_path)

        return df
