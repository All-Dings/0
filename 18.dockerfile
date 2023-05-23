# # Dockerfile for this Project

# ## Build and run Docker Image
# ```
# $ docker build -t mm -f 18.dockerfile .
# $ docker run -ti --rm mm bash
# ```

# # Define Base Image
FROM ubuntu:22.04

# # Working Directory for all Files
WORKDIR root

# # Copy Repitory Files to Docker Image
COPY . .

# # Resynchronize the Package Index
RUN apt-get update

# # Unminimize Ubuntu
RUN yes | unminimize

# # Install and configure Software

# ## Bash Shell

# ### Install Bash Completion
RUN apt-get install -y bash-completion

#
# ### Setup Configuration File (bashrc)
RUN rm -f .bashrc
RUN ln -s 14.bashrc .bashrc

# ## Manpages
#
RUN apt-get install -y man

# ## Python3
#
# ### Install Python-3 Base Package
RUN apt-get install -y python3

# ### Install pip Pyhton-Packet-Manager
RUN apt-get install -y pip

# ### Install Time-Zone-Support
RUN pip install pytz
RUN pip install tzlocal

# ## Git Version Control
#
# ### Install Git Base Package
RUN apt-get install -y git

# ### Install Large File Support (LFS)
RUN apt-get install -y git-lfs

# ### Setup .gitconfig
RUN ln -s 15.gitconfig .gitconfig

# ## Vim Editor
#
# ### Install vim Base Package
RUN apt-get install -y vim

# ## ImageMagic
#
RUN apt-get install -y imagemagick

# ### Setup Configuration File (vimrc)
RUN ln -s 13.vimrc .vimrc

# ## Kivy
#
# ### Install Kivy
Run pip3 install "kivy[base]" kivy_examples
# ### Install Buildozer
Run pip3 install --upgrade buildozer
# ### Install Cython
Run pip3 install --upgrade cython
# ### Java
Run apt-get install -y openjdk-8-jdk
# ### Unzip
Run apt-get install unzip
