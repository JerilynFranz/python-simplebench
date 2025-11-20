=================
Installation
=================

.. _simplebench-installation:


.. toctree::
   :maxdepth: 3

.. index::


**Via PyPI**

.. code-block:: shell
  :caption: Installing using pip
  :name: install-using-pip

    pip3 install simplebench

**From source**

.. code-block:: shell
  :caption: Installing from source
  :name: install-from-source

    git clone https://github.com/JerilynFranz/python-simplebench
    cd python-simplebench
    pip3 install .

**For Development**

.. code-block:: shell
  :caption: Setup a development environment
  :name: setup-development-environment

    git clone https://github.com/JerilynFranz/python-simplebench
    cd python-simplebench
    pip3 install uv
    uv sync
    source .venv/bin/activate
