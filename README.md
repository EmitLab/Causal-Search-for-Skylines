# Causal Search for Skylines (CSS): Causally-Informed Selective Data De-Correlation

This repository contains the implementation of Causal Search for Skylines (CSS), as described in our SIGMOD 2026 paper.

## File Structure

All paths below are relative to `skylines/`.

- `__init__.py`: Experiment configuration.
- `dataset/`: Dataset definitions, including causal graphs, preference attribute sets, dominance criteria, and data-generation scripts. `synthetic/` contains synthetic datasets; `real/` contains real-world datasets and augmentation scripts. `real/data/` holds the raw, unaugmented CSV files, with tuples as rows and variables as columns.
- `heuristic/`: Heuristics for finding the best conditioning set: `algorithm0.py` (`ddSkyline`), `algorithm4.py` (`gnSkyline`), and `algorithm4_leaky.py` (`lnSkyline`).
- `skyline/`: Naive and causal implementations of Block Nested Loop (`bnl/`), Sort-Filter-Skyline (`sfs/`), Sort and Limit Skyline (`salsa/`), Divide and Conquer (`dnc/`), and Branch and Bound Skyline (`bbs/`).
- `experiment/core/`: Experiment scripts. `benchmark.py` generates dataset instances and runs skyline experiments; `summarize.py` aggregates the results; `gain.py` compares the time required by the three conditioning-set heuristics.
- `common/`: Shared code, including experiment definitions in `constants/`, K-Means in `kmeans/`, and utility methods in `utils/`.

In experiment outputs, `Gain 0` refers to `ddSkyline`, `Gain 4` to `gnSkyline`, and `Leaky Gain 4` to `lnSkyline`. The leakage parameters in `skylines/__init__.py` apply to `lnSkyline`.

## Causal Graphs

Datasets are defined in `skylines/dataset/`. A typical definition is:

    class XY_C_1(SyntheticDataset):

        def __init__(self,
                    dominance: dict[str, Dominance] = None,
                    size: int = 10000,
                    seed: int = 42):
            super().__init__(control=['C'],
                            preference=['X', 'Y'],
                            effect={'X': {'C':  1},
                                    'Y': {'C': -1}},
                            dominance=dominance,
                            infer_controls={
                                'X': Dominance.MAX,
                                'Y': Dominance.MAX
                            },
                            size=size,
                            seed=seed)

The `effect` map encodes the causal graph as a weighted directed adjacency map: variate `C` affects `X` with causal strength `+1` and `Y` with causal strength `-1`. The corresponding directed acyclic graph (DAG) is:

![graph.svg](./graph.svg)

## Requirements

The experiments were run with Python 3.12.7 in a conda environment.

> [!TIP]
> If using Docker, skip the steps below. Docker sets up the environment automatically.

Install [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install), then create and activate the `skyline` environment:

    conda env create -f environment.yml
    conda activate skyline

## Experiment Lifecycle

### Setup

Prepare the environment as described above and select a preset using the [experiment setup instructions](#experiment-setup). Check that the active `experiment_type` and parameter values match the intended experiment. If `infer_graph = True`, generate the required NOTEARS graph cache first; Docker does this automatically when the cache is empty.

### Execution

Run `benchmark.py`, followed immediately by `summarize.py`, for skyline experiments; run `gain.py` for gain computation experiments. Check the terminal for exceptions and confirm that the output contains results for every configured dataset, dominance setting, and repetition, plus the summary workbook after summarization. A run directory alone does not indicate successful completion.

### Cleanup

Results are retained in `out/<timestamp>/<sample-size>/` (`results/out/` on the host when using Docker). Finish each run and its summarization before starting another: benchmark, gain, and graph runs update `timestamp.txt`, which selects the run to summarize. Timestamps have minute precision, so start successive runs in different minutes and verify that their output directories differ. Previous outputs need not be deleted. The `graphs/` cache persists across runs; regenerate the required files when newly inferred graphs are needed.

## Experiment Setup

The `configs/` folder contains presets for the following experiments:

| Experiment             | Settings varied                                                | Location                                   |
| ---------------------- | -------------------------------------------------------------- | ------------------------------------------ |
| Method comparison      | ddSky, gnSky, lnSky, and preference de-correlation             | `configs/200K/`                          |
| Dataset size           | 50K, 100K, 200K, and 400K tuples                               | `configs/{size}/`                        |
| Leakage                | (0.6, 0.4), (0.7, 0.3), (0.8, 0.2), (0.9, 0.1), and (1.0, 0.0) | `configs/200K/lnSky {leakage}/`          |
| Cluster count          | 2–20 clusters                                                 | `configs/200K/clusters/{count}/`         |
| Causal graph inference | lnSky with NOTEARS-inferred causal graphs                      | `configs/200K/lnSky (0.6, 0.4) NOTEARS/` |

Presets cover synthetic and real-world datasets. Method comparisons and NOTEARS experiments include both `Z = P` and `Z != P`; the dataset-size, leakage, and cluster-count sweeps use `Z != P`, with convenience duplicates retained at shared settings. All presets use five runs.

Unless varied, experiments use 200K tuples and 10 clusters. The dataset-size, cluster-count, and NOTEARS experiments use lnSky with leakage (0.6, 0.4).

For example, `configs/200K/ddSky/real (Z != P).py` configures skyline computation with ddSky on real-world datasets with `Z != P`, 200K tuples, 10 clusters, and five runs. Each preset begins with a short description of its setup.

Copy the selected preset to `skylines/__init__.py`, then follow the manual or Docker instructions below.

## Running Manually

### Run skyline computation experiments

These experiments compare non-causal and causal skyline algorithms, recording dominance checks and execution time. Run the benchmark, then summarize its results:

    python -m skylines.experiment.core.benchmark
    python -m skylines.experiment.core.summarize

### Run gain computation experiments

These experiments measure the time required by the proposed heuristics to find a conditioning attribute set:

    python -m skylines.experiment.core.gain

### Generate inferred causal graphs using NOTEARS

For manual runs with `infer_graph = True`, build the causal-graph cache using NOTEARS before running the experiment:

    python -m skylines.experiment.core.graph

## Running with Docker

The Docker image sets up the `skyline` conda environment from `environment.yml` and runs the experiment configured in `skylines/__init__.py`. This file is mounted at runtime, so changing the preset does not require a rebuild.

> [!NOTE]
> The Docker image requires an x86 (`linux/amd64`) platform.

### Build the image

    docker compose build

### Run the experiment

    docker compose run --rm css

Use the `MODE` variable to select what to run:

- `benchmark` (default): skyline computation experiments, followed by `summarize`
- `gain`: gain computation experiments
- `graph`: build the NOTEARS inferred causal graph cache
- `all`: `benchmark`, `summarize`, then `gain`

For example:

    MODE=gain docker compose run --rm css

The `benchmark` and `all` modes run summarization immediately after the benchmark, as required by the [experiment lifecycle](#experiment-lifecycle). If `infer_graph = True` and the graph cache is empty, Docker builds it before the experiment.

The number of BLAS/OpenMP threads defaults to 64 (as in `openblas.sh`) and can be changed with `N_THREADS`, e.g. `N_THREADS=32 docker compose run --rm css`.

All outputs (`out/`, `graphs/`, `timestamp.txt`) are written to `./results` on the host.

## Reproducing the Paper Figures

The `figures/` folder contains Excel workbooks with experimental results, summary calculations, and charts for Figures 9–17 in the paper. Each figure directory contains separate workbooks for synthetic and real-world datasets.

The following table maps each figure to its configurations. Paths are relative to `configs/`.

| Figure | Experiment | Configurations | `Z != P` | `Z = P` |
|---|---|---|:---:|:---:|
| 9 | Mean Execution Time | `200K/pref decor/`<br>`200K/ddSky/`<br>`200K/gnSky/`<br>`200K/lnSky (0.6, 0.4)/` | ✓ | ✓ |
| 10 | Mean Gain Computation Time | `200K/lnSky (0.6, 0.4)/` | ✓ | ✓ |
| 11 | Median % Reduction in Execution Time (expected gain > 0) | Same as Figure 9 | ✓ | - |
| 12 | Median % Reduction in Execution Time (expected gain > 0) | Same as Figure 9 | - | ✓ |
| 13 | Median % Reduction in Execution Time (expected gain ≤ 0) | Same as Figure 9 | ✓ | ✓ |
| 14 | Median % Reduction in Execution Time for Different Numbers of Tuples | `{50K,100K,200K,400K}/lnSky (0.6, 0.4)/` | ✓ | - |
| 15 | Median % Reduction in Execution Time for Different Leakage Parameters | `200K/lnSky (1.0, 0.0)/`<br>`200K/lnSky (0.9, 0.1)/`<br>`200K/lnSky (0.8, 0.2)/`<br>`200K/lnSky (0.7, 0.3)/`<br>`200K/lnSky (0.6, 0.4)/` | ✓ | - |
| 16 | Median % Reduction in Execution Time for Different Numbers of De-correlation Clusters | `200K/clusters/{2–20}/lnSky (0.6, 0.4)/` | ✓ | - |
| 17 | Mean Execution Time with Provided and Inferred Causal Graphs | `200K/lnSky (0.6, 0.4)/`<br>`200K/lnSky (0.6, 0.4) NOTEARS/` | ✓ | ✓ |

### Running the experiments

For each configuration listed above, select the synthetic and real-world preset files with the indicated `Z != P` or `Z = P` setting. Run them using the manual or Docker instructions above.

For Figure 10, run the gain-computation script. It computes timings for ddSky, gnSky, and all four lnSky leakage pairs in one execution; the paper plots ddSky, gnSky, and lnSky `(0.6, 0.4)`.

For all other figures, run the skyline benchmark followed by summarization. The NOTEARS configuration in Figure 17 also requires the graph-cache setup described above.

The method-comparison results can be reused across Figures 9, 11, 12, and 13. Positive-gain and negative-gain cases are selected within the Excel workbooks rather than through separate configurations.

### Using the Excel workbooks

Open the synthetic or real-world workbook in the corresponding `figures/Figure N/` directory. Figure 10 contains a `Gain` worksheet. The other workbooks contain a `Summary` worksheet and supporting worksheets organized by method, number of tuples, leakage parameters, number of clusters, or causal-graph source.

The workbooks also include results beyond the paper's execution-time plots, such as dominance checks.

## Citation

If you use this work, please cite our paper:

**Causal Search for Skylines (CSS): Causally-Informed Selective Data De-Correlation**
Pratanu Mandal, Abhinav Gorantla, K. Selçuk Candan, Maria Luisa Sapino
*Accepted to SIGMOD 2026 · [https://dl.acm.org/doi/10.1145/3802026](https://dl.acm.org/doi/10.1145/3802026)*

```bibtex
@article{10.1145/3802026,
author = {Mandal, Pratanu and Gorantla, Abhinav and Candan, K. Sel\c{c}uk and Sapino, Maria Luisa},
title = {Causal Search for Skylines (CSS): Causally-Informed Selective Data De-Correlation},
year = {2026},
issue_date = {June 2026},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
volume = {4},
number = {3},
url = {https://doi.org/10.1145/3802026},
doi = {10.1145/3802026},
journal = {Proc. ACM Manag. Data},
month = may,
articleno = {149},
numpages = {27}
}
```
