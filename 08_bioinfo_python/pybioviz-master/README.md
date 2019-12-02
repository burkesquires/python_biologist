[![PyPI version shields.io](https://img.shields.io/pypi/v/pybioviz.svg)](https://pypi.python.org/pypi/pybioviz/)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Documentation Status](https://readthedocs.org/projects/pybioviz/badge/?version=latest)](https://pybioviz.readthedocs.io/en/latest/?badge=latest)

# pybioviz

<img align="right" src=img/logo.svg width=150px>

Bioinformatics visualization tools with PyViz Panel and Bokeh.
The objective is to have a set of plots and dashboards that can be re-used inside Jupyter notebooks as part of bioinformatic workflows or deployed as local web apps.

Current tools include:

* sequence alignment viewer
* genome feature viewer
* bam alignment viewer

<img src=https://github.com/dmnfarrell/pybioviz/raw/master/doc/source/sequence_align_plot.png width=600px>

### Installation

```
pip install pybioviz
```

If using JupyterLab:
```
jupyter labextension install @bokeh/jupyter_bokeh
jupyter labextension install @pyviz/jupyterlab_pyviz
```

### See the [documentation](https://pybioviz.readthedocs.io) for usage.

### Links

* https://panel.pyviz.org/
* https://docs.bokeh.org/en/latest/
