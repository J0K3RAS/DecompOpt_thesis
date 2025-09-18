FROM ubuntu:24.04
RUN apt-get update \
    && apt-get install -y curl git openbabel3
RUN mkdir -p /home/root/DecompOpt/output
WORKDIR /home/root/DecompOpt
RUN git clone -b main https://github.com/J0K3RAS/DecompOpt_thesis .
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && ~/.local/bin/uv python install cpython-3.12.9-linux-x86_64-gnu \
    && ~/.local/bin/uv lock  \
    && ~/.local/bin/uv sync