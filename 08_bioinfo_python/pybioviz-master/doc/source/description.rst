Description
===========

Bioinformatics visualization tools with PyViz Panel and Bokeh. The objective is to have a set of interactive plotting tools that can be re-used inside notebook dashboards as part of bioinformatic workflows or deployed as local web apps.

Current dashboards include:

* sequence alignment viewer
* genome feature viewer
* bam alignment viewer


Links
=====

* https://github.com/dmnfarrell/pybioviz
* https://panel.pyviz.org/

Citation
========

If you use this software in your work please cite the following article:

Farrell, D 2019

Installation
============

    pip install pybioviz

If using JupyterLab::

    jupyter labextension install @bokeh/jupyter_bokeh
    jupyter labextension install @pyviz/jupyterlab_pyviz

Dependencies
++++++++++++

* numpy
* pandas
* panel
* bokeh
* biopython
* pyfaidx
* pysam
* bcbio_gff