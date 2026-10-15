#!/usr/bin/env bash
set -euo pipefail

# MODE selects which experiment scripts to run:
#   benchmark - skyline computation experiments, then summarize (default)
#   gain      - gain computation experiments
#   graph     - only build the NO-TEARS inferred causal graph cache
#   all       - benchmark, summarize, then gain
MODE="${MODE:-benchmark}"

# Pre-flight: validate the configuration in skylines/__init__.py
python - <<'EOF'
import sys

try:
    import skylines
except Exception as e:
    sys.exit(f'Failed to import skylines/__init__.py: {e}')

valid = ['Synthetic (Z != P)', 'Synthetic (Z = P)', 'Real (Z != P)', 'Real (Z = P)']
experiment_type = getattr(skylines, 'experiment_type', None)
if experiment_type not in valid:
    sys.exit('Invalid experiment_type in skylines/__init__.py: uncomment exactly one of\n  '
             + '\n  '.join(repr(v) for v in valid))

print('=== Experiment configuration ===')
for key in ['experiment_type', 'n_samples', 'n_runs', 'n_bins', 'leakage', 'data_driven',
            'complete_decorrelation', 'infer_graph', 'skip_inference', 'skip_gain_le_zero']:
    print(f'{key:24s} = {getattr(skylines, key, None)!r}')
print('================================')
EOF

run() {
    echo ">>> python -m $1"
    python -m "$1"
}

# The NO-TEARS graph cache must exist before running with infer_graph = True
INFER_GRAPH=$(python -c 'import skylines; print(skylines.infer_graph)')
if [[ "$MODE" != "graph" && "$INFER_GRAPH" == "True" ]] && [[ -z "$(ls -A graphs 2>/dev/null)" ]]; then
    echo "infer_graph = True and graphs/ is empty: building causal graph cache first"
    run skylines.experiment.core.graph
fi

case "$MODE" in
    benchmark)
        run skylines.experiment.core.benchmark
        run skylines.experiment.core.summarize
        ;;
    gain)
        run skylines.experiment.core.gain
        ;;
    graph)
        run skylines.experiment.core.graph
        ;;
    all)
        run skylines.experiment.core.benchmark
        run skylines.experiment.core.summarize
        run skylines.experiment.core.gain
        ;;
    *)
        echo "Unknown MODE '$MODE' (expected: benchmark, gain, graph, all)" >&2
        exit 1
        ;;
esac
