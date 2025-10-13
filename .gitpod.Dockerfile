FROM gitpod/workspace-full:latest

RUN sudo apt-get update && \
    sudo apt-get install -y golang && \
    sudo rm -rf /var/lib/apt/lists/*
