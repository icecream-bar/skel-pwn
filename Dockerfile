# Use the pwntools/pwntools:stable image as the base image
FROM pwntools/pwntools:stable

# Install gdb, pwndbg, and tmux
USER root
RUN apt-get update -y
RUN apt-get install gdb tmux git gdbserver python3-dev python3-venv python3-pip python3-setuptools libglib2.0-dev libc6-dbg file neovim tmux -y
RUN apt-get install ruby-full -y
RUN gem install one_gadget
COPY skel.py /usr/bin/

# Define a non-root user for running the container
RUN useradd -ms /bin/bash icecream && \
  echo "icecream ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER icecream

# Set up a home directory for the non-root user
ENV HOME /home/icecream

# Set the working directory to /home/pwntools/exploits
WORKDIR /home/icecream/

# Clone and set up pwndbg
RUN git clone https://github.com/pwndbg/pwndbg
WORKDIR /home/icecream/pwndbg/
RUN git config --global --add safe.directory /home/icecream/pwndbg
RUN git config --global --add safe.directory /home/icecream/pwndbg/gdb-pt-dump
USER root
RUN ./setup.sh

USER icecream
WORKDIR /home/icecream/

# Start a shell by default when the container is run
CMD ["/bin/bash"]
