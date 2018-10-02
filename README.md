# imatch

## Installing

### Installing jzmq

1. Install [libzmq](https://github.com/zeromq/libzmq) on your system.
2. Follow the instructions [here](https://github.com/zeromq/jzmq) to install jzmq.
    - E.g. for Mac, you need:
    ```
    cd jzmq-jni/
    ./autogen.sh
    ./configure
    make
    make install
    ```
3. Add the jzmq lib to your java library path, by passing in the path to jzmq as a parameter.
    - E.g. for Mac:
    ```
    java -Djava.library.path=/usr/local/lib/ ...
    ```

#### Possible pitfalls

1. Make sure you have the latest `jzmq` version (`3.1.0` as of the time of writing)
