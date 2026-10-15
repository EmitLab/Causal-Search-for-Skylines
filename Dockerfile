FROM --platform=linux/amd64 continuumio/miniconda3:latest

# Non-interactive acceptance of the Anaconda ToS for the `defaults` channel
# (required by recent conda releases; ignored by older ones)
ENV CONDA_PLUGINS_AUTO_ACCEPT_TOS=yes

# Build the `skyline` conda environment first so code changes don't invalidate this layer
COPY environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml && conda clean -afy

# Use the `skyline` environment by default (equivalent of `conda activate skyline`)
ENV PATH=/opt/conda/envs/skyline/bin:$PATH

# Thread settings from openblas.sh (override at runtime if needed)
ENV OPENBLAS_NUM_THREADS=64 \
    BLIS_NUM_THREADS=64 \
    OMP_NUM_THREADS=64 \
    MKL_NUM_THREADS=64 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

COPY . /app
RUN chmod +x /app/docker/entrypoint.sh

# The experiment code writes out/, graphs/ and timestamp.txt relative to the
# working directory, so run from a dedicated directory that gets mounted as a volume
WORKDIR /results

ENTRYPOINT ["/app/docker/entrypoint.sh"]
