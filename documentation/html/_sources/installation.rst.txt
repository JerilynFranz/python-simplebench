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
  :caption: Default install using pip (without graphs support)
  :name: install-using-pip

    python -m pip install simplebench

.. code-block:: shell
  :caption: Install using pip with graphs support
  :name: install-using-pip-with-graphs

    python -m pip install simplebench[graphs]

.. note::
   Please be aware that the ``[graphs]`` extra will install several large
   third-party libraries (such as Matplotlib, Pandas, and Seaborn),
   increasing the total installation size by over 200 MB.

.. code-block:: shell
  :caption: Install using pip with all optional features (currently only graphs)
  :name: install-using-pip-with-all-extras

    python -m pip install simplebench[all]

**From source**

If you have downloaded the source code, you can install it directly.

.. code-block:: shell
  :caption: Installing from source
  :name: install-from-source

    git clone https://github.com/JerilynFranz/python-simplebench
    cd python-simplebench
    python -m pip install .[all]

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

    # 1. Install uv into your user environment (if not already installed)
    python -m pip install uv --user --break-system-packages

    # 2. Use uv to create a .venv and install all dependencies
    uv sync --all-extras

    # 3. Activate the new environment
    source .venv/bin/activate
