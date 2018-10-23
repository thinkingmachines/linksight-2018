#!/usr/bin/env bash

# libzmq (from https://github.com/zeromq/libzmq)
echo "deb http://download.opensuse.org/repositories/network:/messaging:/zeromq:/release-stable/Debian_9.0/ ./" >> /etc/apt/sources.list
wget https://download.opensuse.org/repositories/network:/messaging:/zeromq:/release-stable/Debian_9.0/Release.key -O- | sudo apt-key add
apt-get -yy install libzmq3-dev

# jzmq
apt-get -yy install pkg-config libtool autoconf automake
git clone https://github.com/zeromq/jzmq.git
cd jzmq/jzmq-jni/
./autogen.sh
./configure
make
make install
