#!/usr/bin/env bash

# Basics: build-essential, git, java, etc
apt-get -yy install build-essential git default-jre default-jdk

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
cd ../..

# imatch
gsutil cp gs://linksight/imatch/test/imatch-full-latest.jar imatch.jar

# run imatch
mkdir testing  # temporary, will remove soon but needed for testing right now
java -jar -Djava.library.path=/usr/local/lib/ imatch.jar
