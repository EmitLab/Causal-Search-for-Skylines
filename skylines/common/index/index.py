import numpy as np
import pandas as pd

from skylines.common.state import get_state
from skylines.common.utils import set_repr
from skylines.dataset import Dataset


class Index:

    def __init__(self, dataset: Dataset, clusterby: frozenset, mode: str = 'r'):
        if mode not in ['r', 'w']:
            raise ValueError('mode must be either "r" or "w"')

        self.dataset = dataset
        self.clusterby = clusterby
        self.mode = mode

        self.index_file_path = get_state().get_file('index', f'{dataset.name}_{set_repr(clusterby)}.txt')
        self.skyline_file_path = get_state().get_file('skyline', f'{dataset.name}_{set_repr(clusterby)}.txt')
        # self.data_file_path = get_state().get_file('data', f'{dataset.name}.csv')

        if self.mode == 'r':
            # load the index
            self.index = []
            with open(self.index_file_path, 'r') as f:
                line = f.readline()
                while line:
                    self.index.append([int(s) for s in line.split()])
                    line = f.readline()

            # load the skyline
            skylines = []
            with open(self.skyline_file_path, 'r') as f:
                line = f.readline()
                while line:
                    skylines.append([int(s) for s in line.split()])
                    line = f.readline()
            self.skyline = skylines[0]
            self.group_skylines = skylines[1:]
            # self.skyline = []
            # self.group_skyline = skyline

            # load the data
            # self.data = pd.read_csv(self.data_file_path, index_col=0)
            self.data = dataset.data

    def index_size(self) -> list[int]:
        if self.mode == 'r':
            size_list = []
            for i in self.index:
                size_list.append(len(i))
            return size_list
        else:
            raise ValueError('Index is open in write mode')

    def group_skyline_sizes(self) -> list[int]:
        if self.mode == 'r':
            size_list = []
            for group_skyline in self.group_skylines:
                size_list.append(len(group_skyline))
            return size_list
        else:
            raise ValueError('Index is open in write mode')

    def corr(self) -> list[pd.DataFrame]:
        if self.mode == 'r':
            corr_list = []
            for i in self.index:
                corr_list.append(self.data.loc[i].corr())
            return corr_list
        else:
            raise ValueError('Index is open in write mode')

    def corr_preferences(self) -> list[pd.DataFrame]:
        if self.mode == 'r':
            corr_list = []
            for i in self.index:
                corr_list.append(self.data.loc[i][self.dataset.preference].corr())
            return corr_list
        else:
            raise ValueError('Index is open in write mode')

    def write_index(self, index: list[np.ndarray]):
        if self.mode == 'w':
            with open(self.index_file_path, 'w') as f:
                for i in index:
                    f.write(' '.join([str(e) for e in i]) + '\n')
        else:
            raise ValueError('Index is open in read mode')

    def write_skyline(self, skyline: np.ndarray, group_skylines: list[np.ndarray]):
        if self.mode == 'w':
            with open(self.skyline_file_path, 'w') as f:
                f.write(' '.join([str(e) for e in skyline]) + '\n')
                for group_skyline in group_skylines:
                    f.write(' '.join([str(e) for e in group_skyline]) + '\n')
        else:
            raise ValueError('Index is open in read mode')
