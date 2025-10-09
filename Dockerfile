# Use the pwntools/pwntools:stable image as the base image
FROM pwntools/pwntools:stable

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    HOME=/home/icecream

USER root

# Install required packages in a single layer (slim + cleanup)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      curl wget ca-certificates \
      git \
      gdb gdbserver \
      tmux \
      python3-dev python3-venv python3-pip python3-setuptools \
      libc6-dbg file neovim xclip \
      ruby-full \
 && gem install --no-document one_gadget \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Add helper script
COPY skel.py /usr/local/bin/skel
RUN chmod +x /usr/local/bin/skel

# Create non-root user and prepare home config
RUN useradd -ms /bin/bash icecream \
 && echo "icecream ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \
 && mkdir -p /home/icecream/.config/tmux \
 && chown -R icecream:icecream /home/icecream

# Copy tmux config and ensure ownership
COPY tmux.conf /home/icecream/.config/tmux/tmux.conf
RUN chown icecream:icecream /home/icecream/.config/tmux/tmux.conf

# Install pwndbg packaged build (per new docs) - installs pwndbg-gdb
RUN curl -qsL 'https://install.pwndbg.re' | sh -s -- -t pwndbg-gdb

# (optional) if you prefer `gdb` to launch pwndbg by default, uncomment:
#RUN ln -sf "$(command -v pwndbg-gdb)" /usr/local/bin/gdb || true
ENV GDB=/usr/local/bin/pwndbg

USER icecream
WORKDIR /home/icecream/pwn

# Start a shell by default
CMD ["/bin/bash"]

