""" Number of tuples """
n_samples = 200_000

""" Number of runs for each experiment (to ensure stability) """
n_runs = 5

""" Number of clusters """
n_bins = 10

""" Leakage parameter (lambda_open, lambda_blocked) """
leakage = (0.6, 0.4)

""" Find conditioning attribute set using data-driven algorithm """
data_driven = False

""" Preference attribute set based decorrelation """
complete_decorrelation = False

""" Infer causal graph from the data """
infer_graph = False

""" Skip inference of causal graph and best control sets """
skip_inference = False

""" Choose baseline if gain <= 0 """
skip_gain_le_zero = False

""" Experiment type to run (enable only one line below) """
# experiment_type = 'Synthetic (Z != P)'
# experiment_type = 'Synthetic (Z = P)'
# experiment_type = 'Real (Z != P)'
# experiment_type = 'Real (Z = P)'
