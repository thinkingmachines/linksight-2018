#!/usr/bin/env bash

# Install zmq
#   - From https://software.opensuse.org/download.html?project=network%3Amessaging%3Azeromq%3Arelease-stable&package=libzmq3-dev
wget -nv https://download.opensuse.org/repositories/network:messaging:zeromq:release-stable/Debian_9.0/Release.key -O Release.key
apt-key add - < Release.key
apt-get update

echo 'deb http://download.opensuse.org/repositories/network:/messaging:/zeromq:/release-stable/Debian_9.0/ /' > /etc/apt/sources.list.d/network:messaging:zeromq:release-stable.list
apt-get update
apt-get -yy  install libzmq3-dev


# Install jzmq
apt-get -yy install pkg-config libtool autoconf automake
git clone https://github.com/zeromq/jzmq.git
cd jzmq/jzmq-jni/
./autogen.sh
./configure
make
make install
