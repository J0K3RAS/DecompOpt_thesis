FROM ubuntu:24.04
RUN apt-get update \
    && apt-get install -y curl git git-lfs libopenbabel-dev swig build-essential \
    && ln -s /usr/include/openbabel3 /usr/local/include
RUN mkdir -p /home/root/DecompOpt
WORKDIR /home/root/DecompOpt
RUN git clone -b main https://github.com/J0K3RAS/DecompOpt_thesis . \
    && git lfs pull \
    && chmod +x scripts/run/sample_compose.sh \
    && mkdir output
WORKDIR /home/root/DecompOpt/data
RUN tar -xf crossdocked_v1.1_rmsd1.0_processed_full_similarity.tar.xz
WORKDIR /home/root/DecompOpt
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && ln -s /root/.local/bin/uv /usr/local/bin \
    && uv python install cpython-3.12.9-linux-x86_64-gnu \
    && uv sync \
    && uv pip install torch_sparse -f https://data.pyg.org/whl/torch-2.7.1+cpu.html \
    && uv pip install torch_scatter -f https://data.pyg.org/whl/torch-2.7.1+cpu.html \
    && uv pip install torch_cluster -f https://data.pyg.org/whl/torch-2.7.1+cpu.html