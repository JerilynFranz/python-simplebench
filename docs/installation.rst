=================
Installation
=================

.. _simplebench-installation:

**Minimum Requirements**

- Python 3.10 or later
- pip

**Via PyPI**

This is the recommended way to install SimpleBench.

.. code-block:: shell
  :caption: Installing using pip
  :name: install-using-pip

    python3 -m pip install simplebench

**From source**

If you have downloaded the source code, you can install it directly.

.. code-block:: shell
  :caption: Installing from source
  :name: install-from-source

    git clone https://github.com/JerilynFranz/python-simplebench
    cd python-simplebench
    python3 -m pip install .

**For Development**

This project uses `uv <https://github.com/astral-sh/uv>`_, a fast, modern
Python package installer, for managing development environments.

The following commands will first install `uv`, then use it to create a local
virtual environment and install all necessary dependencies.

.. code-block:: shell
  :caption: Setup a development environment
  :name: setup-development-environment

    git clone https://github.com/JerilynFranz/python-simplebench
    cd python-simplebench

    # 1. Install uv into your user environment
    python3 -m pip install uv

    # 2. Use uv to create a .venv and install all dependencies
    uv sync --all-extras

    # 3. Activate the new environment
    source .venv/bin/activate
