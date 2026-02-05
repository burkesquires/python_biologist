import marimo

__generated_with = "0.19.7"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # An Introduction to Seaborn
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **`Seaborn`** is a library for making statistical graphics in Python. It builds on top of [`matplotlib`](https://matplotlib.org/) and integrates closely with [`pandas`](https://pandas.pydata.org/) data structures.

    Seaborn helps you explore and understand your data. Its plotting functions operate on dataframes and arrays containing whole datasets and internally perform the necessary semantic mapping and statistical aggregation to produce informative plots. Its dataset-oriented, declarative API lets you focus on what the different elements of your plots mean, rather than on the details of how to draw them.

    Here's an example of what seaborn can do:
    """)
    return


@app.cell
def _():
    # Import seaborn
    import seaborn as sns

    # Apply the default theme
    sns.set_theme()

    # Load an example dataset
    tips = sns.load_dataset("tips")

    # Create a visualization
    sns.relplot(
        data=tips,
        x="total_bill", y="tip", col="time",
        hue="smoker", style="smoker", size="size",
    );
    return (sns,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A few things have happened here. Let's go through them one by one:
    """)
    return


@app.cell
def _():
    # Cell tags: hide-output
    # Import seaborn

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Seaborn is the only library we need to import for this simple example. By convention, it is imported with the shorthand `sns`.

    Behind the scenes, seaborn uses matplotlib to draw its plots. For interactive work, it's recommended to use a Jupyter/IPython interface in `matplotlib mode <https://ipython.readthedocs.io/en/stable/interactive/plotting.html>`_, or else you'll have to call :func:`matplotlib.pyplot.show` when you want to see the plot.
    """)
    return


@app.cell
def _(sns):
    # Cell tags: hide-output
    # Apply the default theme
    sns.set_theme()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This uses the matplotlib rcParam system and will affect how all matplotlib plots look, even if you don't make them with seaborn. Beyond the default theme, there are :doc:`several other options </tutorial/aesthetics>`, and you can independently control the style and scaling of the plot to quickly translate your work between presentation contexts (e.g., making a version of your figure that will have readable fonts when projected during a talk). If you like the matplotlib defaults or prefer a different theme, you can skip this step and still use the seaborn plotting functions.
    """)
    return


@app.cell
def _(sns):
    # Cell tags: hide-output
    # Load an example dataset
    tips_1 = sns.load_dataset('tips')
    return (tips_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Most code in the docs will use the :func:`load_dataset` function to get quick access to an example dataset. There's nothing special about these datasets: they are just pandas dataframes, and we could have loaded them with :func:`pandas.read_csv` or built them by hand. Most of the examples in the documentation will specify data using pandas dataframes, but seaborn is very flexible about the :doc:`data structures </tutorial/data_structure>` that it accepts.
    """)
    return


@app.cell
def _(sns, tips_1):
    # Cell tags: hide-output
    # Create a visualization
    sns.relplot(data=tips_1, x='total_bill', y='tip', col='time', hue='smoker', style='smoker', size='size')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This plot shows the relationship between five variables in the tips dataset using a single call to the seaborn function :func:`relplot`. Notice how we provided only the names of the variables and their roles in the plot. Unlike when using matplotlib directly, it wasn't necessary to specify attributes of the plot elements in terms of the color values or marker codes. Behind the scenes, seaborn handled the translation from values in the dataframe to arguments that matplotlib understands. This declarative approach lets you stay focused on the questions that you want to answer, rather than on the details of how to control matplotlib.

    .. _intro_api_abstraction:

    A high-level API for statistical graphics
    -----------------------------------------

    There is no universally best way to visualize data. Different questions are best answered by different plots. Seaborn makes it easy to switch between different visual representations by using a consistent dataset-oriented API.

    The function :func:`relplot` is named that way because it is designed to visualize many different statistical *relationships*. While scatter plots are often effective, relationships where one variable represents a measure of time are better represented by a line. The :func:`relplot` function has a convenient ``kind`` parameter that lets you easily switch to this alternate representation:
    """)
    return


@app.cell
def _(sns):
    dots = sns.load_dataset("dots")
    sns.relplot(
        data=dots, kind="line",
        x="time", y="firing_rate", col="align",
        hue="choice", size="coherence", style="choice",
        facet_kws=dict(sharex=False),
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice how the ``size`` and ``style`` parameters are used in both the scatter and line plots, but they affect the two visualizations differently: changing the marker area and symbol in the scatter plot vs the line width and dashing in the line plot. We did not need to keep those details in mind, letting us focus on the overall structure of the plot and the information we want it to convey.

    .. _intro_stat_estimation:

    Statistical estimation
    ~~~~~~~~~~~~~~~~~~~~~~

    Often, we are interested in the *average* value of one variable as a function of other variables. Many seaborn functions will automatically perform the statistical estimation that is necessary to answer these questions:
    """)
    return


@app.cell
def _(sns):
    fmri = sns.load_dataset("fmri")
    sns.relplot(
        data=fmri, kind="line",
        x="timepoint", y="signal", col="region",
        hue="event", style="event",
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    When statistical values are estimated, seaborn will use bootstrapping to compute confidence intervals and draw error bars representing the uncertainty of the estimate.

    Statistical estimation in seaborn goes beyond descriptive statistics. For example, it is possible to enhance a scatterplot by including a linear regression model (and its uncertainty) using :func:`lmplot`:
    """)
    return


@app.cell
def _(sns, tips_1):
    sns.lmplot(data=tips_1, x='total_bill', y='tip', col='time', hue='smoker')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    .. _intro_distributions:


    Distributional representations
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Statistical analyses require knowledge about the distribution of variables in your dataset. The seaborn function :func:`displot` supports several approaches to visualizing distributions. These include classic techniques like histograms and computationally-intensive approaches like kernel density estimation:
    """)
    return


@app.cell
def _(sns, tips_1):
    sns.displot(data=tips_1, x='total_bill', col='time', kde=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Seaborn also tries to promote techniques that are powerful but less familiar, such as calculating and plotting the empirical cumulative distribution function of the data:
    """)
    return


@app.cell
def _(sns, tips_1):
    sns.displot(data=tips_1, kind='ecdf', x='total_bill', col='time', hue='smoker', rug=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    .. _intro_categorical:

    Plots for categorical data
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Several specialized plot types in seaborn are oriented towards visualizing categorical data. They can be accessed through :func:`catplot`. These plots offer different levels of granularity. At the finest level, you may wish to see every observation by drawing a "swarm" plot: a scatter plot that adjusts the positions of the points along the categorical axis so that they don't overlap:
    """)
    return


@app.cell
def _(sns, tips_1):
    sns.catplot(data=tips_1, kind='swarm', x='day', y='total_bill', hue='smoker')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Alternately, you could use kernel density estimation to represent the underlying distribution that the points are sampled from:
    """)
    return


@app.cell
def _(sns, tips_1):
    sns.catplot(data=tips_1, kind='violin', x='day', y='total_bill', hue='smoker', split=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Or you could show only the mean value and its confidence interval within each nested category:
    """)
    return


@app.cell
def _(sns, tips_1):
    sns.catplot(data=tips_1, kind='bar', x='day', y='total_bill', hue='smoker')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    .. _intro_dataset_funcs:

    Multivariate views on complex datasets
    --------------------------------------

    Some seaborn functions combine multiple kinds of plots to quickly give informative summaries of a dataset. One, :func:`jointplot`, focuses on a single relationship. It plots the joint distribution between two variables along with each variable's marginal distribution:
    """)
    return


@app.cell
def _(sns):
    penguins = sns.load_dataset("penguins")
    sns.jointplot(data=penguins, x="flipper_length_mm", y="bill_length_mm", hue="species")
    return (penguins,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The other, :func:`pairplot`, takes a broader view: it shows joint and marginal distributions for all pairwise relationships and for each variable, respectively:
    """)
    return


@app.cell
def _(penguins, sns):
    sns.pairplot(data=penguins, hue="species")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    .. _intro_figure_classes:

    Lower-level tools for building figures
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    These tools work by combining :doc:`axes-level </tutorial/function_overview>` plotting functions with objects that manage the layout of the figure, linking the structure of a dataset to a :doc:`grid of axes </tutorial/axis_grids>`. Both elements are part of the public API, and you can use them directly to create complex figures with only a few more lines of code:
    """)
    return


@app.cell
def _(penguins, sns):
    _g = sns.PairGrid(penguins, hue='species', corner=True)
    _g.map_lower(sns.kdeplot, hue=None, levels=5, color='.2')
    _g.map_lower(sns.scatterplot, marker='+')
    _g.map_diag(sns.histplot, element='step', linewidth=0, kde=True)
    _g.add_legend(frameon=True)
    _g.legend.set_bbox_to_anchor((0.61, 0.6))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    .. _intro_defaults:

    Opinionated defaults and flexible customization
    -----------------------------------------------

    Seaborn creates complete graphics with a single function call: when possible, its functions will automatically add informative axis labels and legends that explain the semantic mappings in the plot.

    In many cases, seaborn will also choose default values for its parameters based on characteristics of the data. For example, the :doc:`color mappings </tutorial/color_palettes>` that we have seen so far used distinct hues (blue, orange, and sometimes green) to represent different levels of the categorical variables assigned to ``hue``. When mapping a numeric variable, some functions will switch to a continuous gradient:
    """)
    return


@app.cell
def _(penguins, sns):
    sns.relplot(
        data=penguins,
        x="bill_length_mm", y="bill_depth_mm", hue="body_mass_g"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    When you're ready to share or publish your work, you'll probably want to polish the figure beyond what the defaults achieve. Seaborn allows for several levels of customization. It defines multiple built-in :doc:`themes </tutorial/aesthetics>` that apply to all figures, its functions have standardized parameters that can modify the semantic mappings for each plot, and additional keyword arguments are passed down to the underlying matplotlib artists, allowing even more control. Once you've created a plot, its properties can be modified through both the seaborn API and by dropping down to the matplotlib layer for fine-grained tweaking:
    """)
    return


@app.cell
def _(penguins, sns):
    sns.set_theme(style='ticks', font_scale=1.25)
    _g = sns.relplot(data=penguins, x='bill_length_mm', y='bill_depth_mm', hue='body_mass_g', palette='crest', marker='x', s=100)
    _g.set_axis_labels('Bill length (mm)', 'Bill depth (mm)', labelpad=10)
    _g.legend.set_title('Body mass (g)')
    _g.figure.set_size_inches(6.5, 4.5)
    _g.ax.margins(0.15)
    _g.despine(trim=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Relationship to matplotlib
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Seaborn's integration with matplotlib allows you to use it across the many environments that matplotlib supports, including exploratory analysis in notebooks, real-time interaction in GUI applications, and archival output in a number of raster and vector formats.

    While you can be productive using only seaborn functions, full customization of your graphics will require some knowledge of matplotlib's concepts and API. One aspect of the learning curve for new users of seaborn will be knowing when dropping down to
    the matplotlib layer is necessary to achieve a particular customization. On the other hand, users coming from matplotlib will find that much of their knowledge transfers.

    Matplotlib has a comprehensive and powerful API; just about any attribute of the figure can be changed to your liking. A combination of seaborn's high-level interface and matplotlib's deep customizability will allow you both to quickly explore your data and to create graphics that can be tailored into a `publication quality <https://github.com/wagnerlabpapers/Waskom_PNAS_2017>`_ final product.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next steps
    ~~~~~~~~~~

    You have a few options for where to go next. You might first want to learn how to :doc:`install seaborn </installing>`. Once that's done, you can browse the :doc:`example gallery </examples/index>` to get a broader sense for what kind of graphics seaborn can produce. Or you can read through the rest of the :doc:`user guide and tutorial </tutorial>` for a deeper discussion of the different tools and what they are designed to accomplish. If you have a specific plot in mind and want to know how to make it, you could check out the :doc:`API reference </api>`, which documents each function's parameters and shows many examples to illustrate usage.
    """)
    return


if __name__ == "__main__":
    app.run()
