# CTF PWN/RE Agent Workspace
# Extends pwntools/pwntools:stable with radare2, pwndbg, and tooling
# Target: Intel x86_64 Linux (runs natively on Intel Mac Docker)

FROM pwntools/pwntools:stable

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    HOME=/home/icecream

USER root

# Install base packages
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      curl wget ca-certificates \
      git \
      gdb gdbserver \
      tmux \
      python3-dev python3-venv python3-pip python3-setuptools \
      libc6-dbg file neovim xclip \
      ruby-full \
      build-essential cmake pkg-config \
      libssl-dev libffi-dev \
      libglib2.0-dev libcairo2-dev \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install radare2 (latest stable release)
RUN wget -qO /tmp/radare2.deb \
    "https://github.com/radareorg/radare2/releases/download/5.9.6/radare2_5.9.6_amd64.deb" \
 && dpkg -i /tmp/radare2.deb || apt-get install -f -y --no-install-recommends \
 && rm /tmp/radare2.deb

# Install r2ghidra-dec plugin for pseudo-C decompilation
RUN r2pm -U && r2pm -ci r2ghidra-dec || true

# Install pwndbg (packaged build)
RUN curl -qsL 'https://install.pwndbg.re' | sh -s -- -t pwndbg-gdb

# Install additional Python tools (break-system-packages OK in container)
RUN pip3 install --no-cache-dir --break-system-packages \
      ropgadget

# Install seccomp-tools (Ruby gem)
RUN gem install --no-document seccomp-tools

# Install one_gadget
RUN gem install --no-document one_gadget

# Ensure pwntools is latest (break-system-packages OK in container)
RUN pip3 install --upgrade --break-system-packages pwntools

# Create non-root user
RUN useradd -ms /bin/bash icecream \
 && echo "icecream ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \
 && mkdir -p /home/icecream/.config/tmux \
 && chown -R icecream:icecream /home/icecream

# Copy helper scripts
COPY skel.py /usr/local/bin/skel
RUN chmod +x /usr/local/bin/skel

# Copy tmux config
COPY tmux.conf /home/icecream/.config/tmux/tmux.conf
RUN chown icecream:icecream /home/icecream/.config/tmux/tmux.conf

# Set GDB alias
ENV GDB=/usr/local/bin/pwndbg

USER icecream
WORKDIR /workspace

# Default shell
CMD ["/bin/bash"]
