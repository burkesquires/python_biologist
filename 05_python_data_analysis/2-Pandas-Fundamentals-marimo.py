import marimo

__generated_with = "0.16.5"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Pandas Fundamentals""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ---

    - This presentation is part of the [__Python Progrmming for Scientists Series__](https://github.com/burkesquires/python_biologist)
    - Source: Adapted from [Chris Fonnesbeck's](https://github.com/fonnesbeck) [Advanced Statistical Computing](https://github.com/fonnesbeck/Bios8366) course at Vanderbilt University.

    ---
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    __Topics__:
    - Manipulating Indicies
    - Indexing and Selection
    - Operations
    - Sorting and Ranking
    - Hairarchical Indexing
    - Missing Data
    - Data Summarization
    ---
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    This section introduces the new user to the key functionality of Pandas that is required to use the software effectively.

    For some variety, we will leave our digestive tract bacteria behind and employ some baseball data.
    """
    )
    return


@app.cell
def _():
    import pandas as pd
    pd.set_option('display.max_rows', 10)
    baseball = pd.read_csv("data/baseball.csv", index_col='id')
    return baseball, pd


@app.cell
def _(baseball):
    baseball
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Notice that we specified the `id` column as the index, since it appears to be a unique identifier. We could try to create a unique index ourselves by combining `player` and `year`:""")
    return


@app.cell
def _(baseball):
    player_id = baseball.player + baseball.year.astype(str)
    baseball_newind = baseball.copy()
    baseball_newind.index = player_id
    baseball_newind
    return (baseball_newind,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""This looks okay, but let's check:""")
    return


@app.cell
def _(baseball_newind):
    baseball_newind.index.is_unique
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""So, indices need not be unique. Our choice is not unique because some players change teams within years.""")
    return


@app.cell
def _(baseball_newind, pd):
    pd.Series(baseball_newind.index).value_counts()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""The most important consequence of a non-unique index is that indexing by label will return multiple values for some labels:""")
    return


@app.cell
def _(baseball_newind):
    baseball_newind.loc['wickmbo012007']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We will learn more about indexing below.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We can create a truly unique index by combining `player`, `team` and `year`:""")
    return


@app.cell
def _(baseball):
    player_unique = baseball.player + baseball.team + baseball.year.astype(str)
    baseball_newind_1 = baseball.copy()
    baseball_newind_1.index = player_unique
    # baseball_newind_1.head()
    baseball_newind_1
    return (baseball_newind_1,)


@app.cell
def _(baseball_newind_1):
    baseball_newind_1.index.is_unique
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We can create meaningful indices more easily using a hierarchical index; for now, we will stick with the numeric `id` field as our index.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Manipulating indices

    **Reindexing** allows users to manipulate the data labels in a DataFrame. It forces a DataFrame to conform to the new index, and optionally, fill in missing data if requested.

    A simple use of `reindex` is to alter the order of the rows:
    """
    )
    return


@app.cell
def _(baseball):
    baseball.reindex(baseball.index[::-1]).head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Notice that the `id` index is not sequential. Say we wanted to populate the table with every `id` value. We could specify and index that is a sequence from the first to the last `id` numbers in the database, and Pandas would fill in the missing data with `NaN` values:""")
    return


@app.cell
def _(baseball):
    id_range = range(baseball.index.values.min(), baseball.index.values.max())
    baseball.reindex(id_range).head()
    return (id_range,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Missing values can be filled as desired, either with selected values, or by rule:""")
    return


app._unparsable_cell(
    r"""
    baseball.reindex?
    """,
    name="_"
)


@app.cell
def _(baseball, id_range):
    baseball.reindex(id_range, method='ffill').head()
    return


@app.cell
def _(baseball, id_range):
    baseball.reindex(id_range, fill_value='charliebrown', columns=['player']).head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Keep in mind that `reindex` does not work if we pass a non-unique index series.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We can remove rows or columns via the `drop` method:""")
    return


@app.cell
def _(baseball):
    baseball.shape
    return


@app.cell
def _(baseball):
    baseball.drop([89525, 89526])
    return


@app.cell
def _(baseball):
    baseball.drop(['ibb','hbp'], axis=1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Indexing and Selection

    Indexing works analogously to indexing in NumPy arrays, except we can use the labels in the `Index` object to extract values in addition to arrays of integers.
    """
    )
    return


@app.cell
def _(baseball_newind_1):
    # Sample Series object
    hits = baseball_newind_1.h
    hits
    return (hits,)


@app.cell
def _(hits):
    # Numpy-style indexing
    hits[:3]
    return


@app.cell
def _(hits):
    # Indexing by label
    hits[['womacto01CHN2006','schilcu01BOS2006']]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We can also slice with data labels, since they have an intrinsic order within the Index:""")
    return


@app.cell
def _(hits):
    hits['womacto01CHN2006':'gonzalu01ARI2006']
    return


@app.cell
def _(hits):
    hits['womacto01CHN2006':'gonzalu01ARI2006'] = 5
    hits
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""In a `DataFrame` we can slice along either or both axes:""")
    return


@app.cell
def _(baseball_newind_1):
    baseball_newind_1[['h', 'ab']]
    return


@app.cell
def _(baseball_newind_1):
    baseball_newind_1[baseball_newind_1.ab > 500]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""For a more concise (and readable) syntax, we can use the new `query` method to perform selection on a `DataFrame`. Instead of having to type the fully-specified column, we can simply pass a string that describes what to select. The query above is then simply:""")
    return


@app.cell
def _(baseball_newind_1):
    baseball_newind_1.query('ab > 500')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""The `DataFrame.index` and `DataFrame.columns` are placed in the query namespace by default. If you want to refer to a variable in the current namespace, you can prefix the variable with `@`:""")
    return


@app.cell
def _():
    min_ab = 450
    return


@app.cell
def _(baseball_newind_1):
    baseball_newind_1.query('ab > @min_ab')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""The indexing field `loc` allows us to select subsets of rows and columns in an intuitive way:""")
    return


@app.cell
def _(baseball_newind_1):
    baseball_newind_1.loc['gonzalu01ARI2006', ['h', 'X2b', 'X3b', 'hr']]
    return


@app.cell
def _(baseball_newind_1):
    baseball_newind_1.loc[:'myersmi01NYA2006', 'hr']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    In addition to using `loc` to select rows and columns by **label**, pandas also allows indexing by **position** using the `iloc` attribute.

    So, we can query rows and columns by absolute position, rather than by name:
    """
    )
    return


@app.cell
def _(baseball_newind_1):
    baseball_newind_1.iloc[:5, 5:8]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Exercise

    You can use the `isin` method query a DataFrame based upon a list of values as follows:

        data['phylum'].isin(['Firmacutes', 'Bacteroidetes'])

    Use `isin` to find all players that played for the Los Angeles Dodgers (LAN) or the San Francisco Giants (SFN). How many records contain these values?
    """
    )
    return


@app.cell
def _():
    # Write your answer here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Operations

    `DataFrame` and `Series` objects allow for several operations to take place either on a single object, or between two or more objects.

    For example, we can perform arithmetic on the elements of two objects, such as combining baseball statistics across years. First, let's (artificially) construct two Series, consisting of home runs hit in years 2006 and 2007, respectively:
    """
    )
    return


@app.cell
def _(baseball):
    hr2006 = baseball.loc[baseball.year==2006, 'hr']
    hr2006.index = baseball.player[baseball.year==2006]

    hr2007 = baseball.loc[baseball.year==2007, 'hr']
    hr2007.index = baseball.player[baseball.year==2007]
    return hr2006, hr2007


@app.cell
def _(hr2007):
    hr2007
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Now, let's add them together, in hopes of getting 2-year home run totals:""")
    return


@app.cell
def _(hr2006, hr2007):
    hr_total = hr2006 + hr2007
    hr_total
    return (hr_total,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Pandas' data alignment places `NaN` values for labels that do not overlap in the two Series. In fact, there are only 6 players that occur in both years.""")
    return


@app.cell
def _(hr_total):
    hr_total[hr_total.notnull()]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""While we do want the operation to honor the data labels in this way, we probably do not want the missing values to be filled with `NaN`. We can use the `add` method to calculate player home run totals by using the `fill_value` argument to insert a zero for home runs where labels do not overlap:""")
    return


@app.cell
def _(hr2006, hr2007):
    hr2007.add(hr2006, fill_value=0)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Operations can also be **broadcast** between rows or columns.

    For example, if we subtract the maximum number of home runs hit from the `hr` column, we get how many fewer than the maximum were hit by each player:
    """
    )
    return


@app.cell
def _(baseball):
    baseball['hr diff'] = baseball.hr - baseball.hr.max()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Or, looking at things row-wise, we can see how a particular player compares with the rest of the group with respect to important statistics""")
    return


@app.cell
def _(baseball):
    baseball.loc[89521, "player"]
    return


@app.cell
def _(baseball):
    stats = baseball[['h','X2b', 'X3b', 'hr']]
    diff = stats - stats.loc[89521]
    diff[:10]
    return (stats,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We can also apply functions to each column or row of a `DataFrame`""")
    return


@app.cell
def _(stats):
    import numpy as np

    stats.apply(np.median)
    return (np,)


@app.function
def range_calc(x):
    return x.max() - x.min()


@app.cell
def _(stats):
    stat_range = lambda x: x.max() - x.min()
    stats.apply(stat_range)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Lets use apply to calculate a meaningful baseball statistics, slugging percentage:

    $$SLG = \frac{1B + (2 \times 2B) + (3 \times 3B) + (4 \times HR)}{AB}$$

    And just for fun, we will format the resulting estimate.
    """
    )
    return


@app.cell
def _(baseball):
    def slugging(x): 
        bases = x['h']-x['X2b']-x['X3b']-x['hr'] + 2*x['X2b'] + 3*x['X3b'] + 4*x['hr']
        ab = x['ab']+1e-6

        return bases/ab

    baseball.apply(slugging, axis=1).round(3)
    return


@app.cell
def _(baseball):
    baseball.to_csv("baseball.csv")
    return


@app.cell
def _(baseball):
    help(baseball.to_csv)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Sorting and Ranking

    Pandas objects include methods for re-ordering data.
    """
    )
    return


@app.cell
def _(baseball_newind_1):
    baseball_newind_1.sort_index().head()
    return


@app.cell
def _(baseball_newind_1):
    baseball_newind_1.sort_index(ascending=False).head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Try sorting the **columns** instead of the rows, in ascending order:""")
    return


@app.cell
def _(baseball_newind_1):
    baseball_newind_1.sort_index(axis=1).head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We can also use `sort_values` to sort a `Series` by value, rather than by label.""")
    return


@app.cell
def _(baseball):
    baseball.hr.sort_values()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""For a `DataFrame`, we can sort according to the values of one or more columns using the `by` argument of `sort_values`:""")
    return


@app.cell
def _(baseball):
    baseball[['player','sb','cs']].sort_values(ascending=[False,True], 
                                               by=['sb', 'cs']).head(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""**Ranking** does not re-arrange data, but instead returns an index that ranks each value relative to others in the Series.""")
    return


@app.cell
def _(baseball):
    baseball.hr.rank()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Ties are assigned the mean value of the tied ranks, which may result in decimal values.""")
    return


@app.cell
def _(pd):
    pd.Series([100,100]).rank()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Alternatively, you can break ties via one of several methods, such as by the order in which they occur in the dataset:""")
    return


@app.cell
def _(baseball):
    baseball.hr.rank(method='first')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Calling the `DataFrame`'s `rank` method results in the ranks of all columns:""")
    return


@app.cell
def _(baseball):
    baseball.rank(ascending=False).head()
    return


@app.cell
def _(baseball):
    baseball[['r','h','hr']].rank(ascending=False).head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Exercise

    Calculate **on base percentage** for each player, and return the ordered series of estimates.

    $$OBP = \frac{H + BB + HBP}{AB + BB + HBP + SF}$$
    """
    )
    return


@app.cell
def _():
    # Write your answer here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Hierarchical indexing

    In the baseball example, I was forced to combine 3 fields to obtain a unique index that was not simply an integer value. A more elegant way to have done this would be to create a hierarchical index from the three fields.
    """
    )
    return


@app.cell
def _(baseball):
    baseball_h = baseball.set_index(['year', 'team', 'player'])
    baseball_h.head(10)
    return (baseball_h,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""This index is a `MultiIndex` object that consists of a sequence of tuples, the elements of which is some combination of the three columns used to create the index. Where there are multiple repeated values, Pandas does not print the repeats, making it easy to identify groups of values.""")
    return


@app.cell
def _(baseball_h):
    baseball_h.index[:10]
    return


@app.cell
def _(baseball_h):
    baseball_h.index.is_unique
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Try using this hierarchical index to retrieve Julio Franco (`francju01`), who played for the Atlanta Braves (`ATL`) in 2007:""")
    return


@app.cell
def _(baseball_h):
    baseball_h.loc[(2007, 'ATL', 'francju01')]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Recall earlier we imported some microbiome data using two index columns. This created a 2-level hierarchical index:""")
    return


@app.cell
def _(pd):
    mb = pd.read_csv("data/microbiome.csv", index_col=['Taxon','Patient'])
    return (mb,)


@app.cell
def _(mb):
    mb.head(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""With a hierachical index, we can select subsets of the data based on a *partial* index:""")
    return


@app.cell
def _(mb):
    mb.loc['Proteobacteria']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Hierarchical indices can be created on either or both axes. Here is a trivial example:""")
    return


@app.cell
def _(np, pd):
    frame = pd.DataFrame(np.arange(12).reshape(( 4, 3)), 
                      index =[['a', 'a', 'b', 'b'], [1, 2, 1, 2]], 
                      columns =[['Ohio', 'Ohio', 'Colorado'], ['Green', 'Red', 'Green']])

    frame
    return (frame,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""If you want to get fancy, both the row and column indices themselves can be given names:""")
    return


@app.cell
def _(frame):
    frame.index.names = ['key1', 'key2']
    frame.columns.names = ['state', 'color']
    frame
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""With this, we can do all sorts of custom indexing:""")
    return


@app.cell
def _(frame):
    frame.loc['a', 'Ohio']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Try retrieving the value corresponding to `b2` in `Colorado`:""")
    return


@app.cell
def _():
    # Write your answer here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Additionally, the order of the set of indices in a hierarchical `MultiIndex` can be changed by swapping them pairwise:""")
    return


@app.cell
def _(mb):
    mb.swaplevel('Patient', 'Taxon').head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Data can also be sorted by any index level, using `sortlevel`:""")
    return


@app.cell
def _(mb):
    mb.sort_values(by='Patient')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Missing data

    The occurence of missing data is so prevalent that it pays to use tools like Pandas, which seamlessly integrates missing data handling so that it can be dealt with easily, and in the manner required by the analysis at hand.

    Missing data are represented in `Series` and `DataFrame` objects by the `NaN` floating point value. However, `None` is also treated as missing, since it is commonly used as such in other contexts (*e.g.* NumPy).
    """
    )
    return


@app.cell
def _(np, pd):
    foo = pd.Series([np.nan, -3, None, 'foobar'])
    foo
    return (foo,)


@app.cell
def _(foo):
    foo.isnull()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Missing values may be dropped or indexed out:""")
    return


@app.cell
def _(pd):
    test_scores = pd.read_csv('data/test_scores.csv', index_col=0, nrows=50)
    test_scores
    return (test_scores,)


@app.cell
def _(test_scores):
    test_scores.dropna()
    return


@app.cell
def _(test_scores):
    test_scores.isnull()
    return


@app.cell
def _(test_scores):
    test_scores[test_scores.notnull()]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""By default, `dropna` drops entire rows in which one or more values are missing.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""This can be overridden by passing the `how='all'` argument, which only drops a row when every field is a missing value.""")
    return


@app.cell
def _(test_scores):
    test_scores.dropna(how='all')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""This can be customized further by specifying how many values need to be present before a row is dropped via the `thresh` argument.""")
    return


@app.cell
def _(test_scores):
    test_scores.dropna(thresh=10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""This is typically used in time series applications, where there are repeated measurements that are incomplete for some subjects.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Exercise

    Try using the `axis` argument to drop columns with missing values:
    """
    )
    return


@app.cell
def _():
    # Write your answer here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Rather than omitting missing data from an analysis, in some cases it may be suitable to fill the missing value in, either with a default value (such as zero) or a value that is either imputed or carried forward/backward from similar data points. We can do this programmatically in Pandas with the `fillna` argument.""")
    return


@app.cell
def _(test_scores):
    test_scores.fillna(-999)
    return


@app.cell
def _(test_scores):
    test_scores.fillna({'family_inv': 0, 'prev_disab': 1})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Notice that `fillna` by default returns a new object with the desired filling behavior, rather than changing the `Series` or  `DataFrame` in place (**in general, we like to do this, by the way!**).""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We can alter values in-place using `inplace=True`.""")
    return


@app.cell
def _(test_scores):
    test_scores.prev_disab.fillna(0, inplace=True)
    test_scores
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Missing values can also be interpolated, using any one of a variety of methods:""")
    return


@app.cell
def _(test_scores):
    test_scores.fillna(method='bfill')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Data summarization

    We often wish to summarize data in `Series` or `DataFrame` objects, so that they can more easily be understood or compared with similar data. The NumPy package contains several functions that are useful here, but several summarization or reduction methods are built into Pandas data structures.
    """
    )
    return


@app.cell
def _(baseball):
    baseball.sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Clearly, `sum` is more meaningful for some columns than others. For methods like `mean` for which application to string variables is not just meaningless, but impossible, these columns are automatically exculded:""")
    return


@app.cell
def _():
    # baseball.mean()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""The important difference between NumPy's functions and Pandas' methods is that the latter have built-in support for handling missing data.""")
    return


@app.cell
def _(test_scores):
    test_scores.mean()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Sometimes we may not want to ignore missing values, and allow the `nan` to propagate.""")
    return


@app.cell
def _(test_scores):
    test_scores.mean(skipna=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Passing `axis=1` will summarize over rows instead of columns, which only makes sense in certain situations.""")
    return


@app.cell
def _(baseball):
    extra_bases = baseball[['X2b','X3b','hr']].sum(axis=1)
    extra_bases.sort_values(ascending=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""A useful summarization that gives a quick snapshot of multiple statistics for a `Series` or `DataFrame` is `describe`:""")
    return


@app.cell
def _(baseball):
    baseball.describe()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""`describe` can detect non-numeric data and sometimes yield useful information about it.""")
    return


@app.cell
def _(baseball):
    baseball.player.describe()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    We can also calculate summary statistics *across* multiple columns, for example, correlation and covariance.

    $$cov(x,y) = \sum_i (x_i - \bar{x})(y_i - \bar{y})$$
    """
    )
    return


@app.cell
def _(baseball):
    baseball.hr.cov(baseball.X2b)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""$$corr(x,y) = \frac{cov(x,y)}{(n-1)s_x s_y} = \frac{\sum_i (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_i (x_i - \bar{x})^2 \sum_i (y_i - \bar{y})^2}}$$""")
    return


@app.cell
def _(baseball):
    baseball.hr.corr(baseball.X2b)
    return


@app.cell
def _(baseball):
    baseball.ab.corr(baseball.h)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Try running `corr` on the entire `baseball` DataFrame to see what is returned:""")
    return


@app.cell
def _():
    # Write answer here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""If we have a `DataFrame` with a hierarchical index (or indices), summary statistics can be applied with respect to any of the index levels:""")
    return


@app.cell
def _(mb):
    mb.head()
    return


@app.cell
def _(mb):
    mb.groupby(level='Taxon').sum()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Writing Data to Files

    As well as being able to read several data input formats, Pandas can also export data to a variety of storage formats. We will bring your attention to just a couple of these.
    """
    )
    return


@app.cell
def _(mb):
    mb.to_csv("mb.csv")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""The `to_csv` method writes a `DataFrame` to a comma-separated values (csv) file. You can specify custom delimiters (via `sep` argument), how missing values are written (via `na_rep` argument), whether the index is writen (via `index` argument), whether the header is included (via `header` argument), among other options.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""An efficient way of storing data to disk is in binary format. Pandas supports this using Python’s built-in pickle serialization.""")
    return


@app.cell
def _(baseball):
    baseball.to_pickle("baseball_pickle")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""The complement to `to_pickle` is the `read_pickle` function, which restores the pickle to a `DataFrame` or `Series`:""")
    return


@app.cell
def _(pd):
    pd.read_pickle("baseball_pickle")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""As Wes warns in his book, it is recommended that binary storage of data via pickle only be used as a temporary storage format, in situations where speed is relevant. This is because there is no guarantee that the pickle format will not change with future versions of Python.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ---
    ## References

    [Python for Data Analysis](http://shop.oreilly.com/product/0636920023784.do) Wes McKinney
    """
    )
    return


if __name__ == "__main__":
    app.run()
