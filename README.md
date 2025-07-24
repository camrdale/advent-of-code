# Advent of Code

My work on the [Advent of Code](https://adventofcode.com/) puzzles.

## Python

Some of the solutions rely on a faster Python with multi-threading (GIL disabled), that is not yet available in a stable release. These are the steps to build Python locally with support for disabling the GIL.

Install the needed build dependencies:

```
sudo apt build-dep python3
sudo apt install build-essential gdb lcov libbz2-dev libffi-dev \
libgdbm-compat-dev libgdbm-dev liblzma-dev libncurses5-dev libncursesw5-dev \
libreadline6-dev libreadline-dev libsqlite3-dev libssl-dev lzma lzma-dev \
pkg-config python3-dev tk-dev uuid-dev xvfb zlib1g-dev
```

Download the appropriate version of the "Gzipped source tarball" from the
[Python download page](https://www.python.org/downloads/source/).
The current latest version is `3.14.0rc1`.

Extract the archive:

```
tar -xvf Python-3.14.0rc1.tgz
```

Change into the new directory and build and install Python locally:

```
./configure --enable-optimizations --disable-gil
make
make test
sudo make altinstall
```

In the top level directory of this repo, create a new virtual environment
using the locally built Python:

```
python3.14 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

To guarantee the GIL is disabled, run the code like this:

```
.venv/bin/python -Xgil=0 ./main.py
```
