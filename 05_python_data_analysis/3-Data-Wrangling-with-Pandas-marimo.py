import marimo

__generated_with = "0.16.5"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Data Wrangling with Pandas""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ---

    - This presentation is part of the [__Python Progrmming for Scientists Series__](https://github.com/burkesquires/python_biologist).
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
    - Data / Time Data Handling
    - Merging and Joining Dataframes
    - Concatenation
    - Reshaping Dataframes
    - Pivoting
    - Method Chaining
    - Pipes
    - Data Transformation
    - Categorical Data
    - Data Aggregation and GroupBy
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""---""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Now that we have been exposed to the basic functionality of Pandas, lets explore some more advanced features that will be useful when addressing more complex data management tasks.

    As most statisticians/data analysts will admit, often the lion's share of the time spent implementing an analysis is devoted to preparing the data itself, rather than to coding or running a particular model that uses the data. This is where Pandas and  Python's standard library are beneficial, providing high-level, flexible, and efficient tools for manipulating your data as needed.
    """
    )
    return


app._unparsable_cell(
    r"""
    pip install xlrd
    """,
    name="_"
)


@app.cell
def _():
    # '%matplotlib inline' command supported automatically in marimo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_context('notebook')
    return np, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Date/Time data handling

    Date and time data are inherently problematic. There are an unequal number of days in every month, an unequal number of days in a year (due to leap years), and time zones that vary over space. Yet information about time is essential in many analyses, particularly in the case of time series analysis.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""The `datetime` built-in library handles temporal information down to the nanosecond.""")
    return


@app.cell
def _():
    from datetime import datetime
    return (datetime,)


@app.cell
def _(datetime):
    now = datetime.now()
    now
    return (now,)


@app.cell
def _(now):
    now.day
    return


@app.cell
def _(now):
    now.weekday()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""In addition to `datetime` there are simpler objects for date and time information only, respectively.""")
    return


@app.cell
def _():
    from datetime import date, time
    return date, time


@app.cell
def _(time):
    time(3, 24)
    return


@app.cell
def _(date):
    date(1970, 9, 3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Having a custom data type for dates and times is convenient because we can perform operations on them easily. For example, we may want to calculate the difference between two times:""")
    return


@app.cell
def _(datetime, now):
    my_age = now - datetime(1970, 9, 3)
    my_age
    return (my_age,)


@app.cell
def _(my_age):
    my_age.days/365
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    In this section, we will manipulate data collected from ocean-going vessels on the eastern seaboard. Vessel operations are monitored using the Automatic Identification System (AIS), a safety at sea navigation technology which vessels are required to maintain and that uses transponders to transmit very high frequency (VHF) radio signals containing static information including ship name, call sign, and country of origin, as well as dynamic information unique to a particular voyage such as vessel location, heading, and speed.

    The International Maritime Organization’s (IMO) International Convention for the Safety of Life at Sea requires functioning AIS capabilities on all vessels 300 gross tons or greater and the US Coast Guard requires AIS on nearly all vessels sailing in U.S. waters. The Coast Guard has established a national network of AIS receivers that provides coverage of nearly all U.S. waters. AIS signals are transmitted several times each minute and the network is capable of handling thousands of reports per minute and updates as often as every two seconds. Therefore, a typical voyage in our study might include the transmission of hundreds or thousands of AIS encoded signals. This provides a rich source of spatial data that includes both spatial and temporal information.

    For our purposes, we will use summarized data that describes the transit of a given vessel through a particular administrative area. The data includes the start and end time of the transit segment, as well as information about the speed of the vessel, how far it travelled, etc.
    """
    )
    return


@app.cell
def _(pd):
    segments = pd.read_csv("data/AIS/transit_segments.csv")
    segments
    return (segments,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""For example, we might be interested in the distribution of transit lengths, so we can plot them as a histogram:""")
    return


@app.cell
def _(segments):
    segments.seg_length.hist(bins=500)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Though most of the transits appear to be short, there are a few longer distances that make the plot difficult to read. This is where a transformation is useful:""")
    return


@app.cell
def _(np, segments):
    segments.seg_length.apply(np.log).hist(bins=500)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We can see that although there are date/time fields in the dataset, they are not in any specialized format, such as `datetime`.""")
    return


@app.cell
def _(segments):
    segments.st_time.dtype
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Our first order of business will be to convert these data to `datetime`. The `strptime` method parses a string representation of a date and/or time field, according to the expected format of this information.""")
    return


@app.cell
def _(datetime, segments):
    datetime.strptime(segments.st_time.loc[0], '%m/%d/%y %H:%M')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""The `dateutil` package includes a parser that attempts to detect the format of the date strings, and convert them automatically.""")
    return


@app.cell
def _():
    from dateutil.parser import parse
    return (parse,)


@app.cell
def _(parse, segments):
    parse(segments.st_time.loc[0])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We can convert all the dates in a particular column by using the `apply` method.""")
    return


@app.cell
def _(datetime, segments):
    segments.st_time.apply(lambda d: datetime.strptime(d, '%m/%d/%y %H:%M'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""As a convenience, Pandas has a `to_datetime` method that will parse and convert an entire Series of formatted strings into `datetime` objects.""")
    return


@app.cell
def _(pd, segments):
    pd.to_datetime(segments.st_time[:10])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Pandas also has a custom NA value for missing datetime objects, `NaT`.""")
    return


@app.cell
def _(pd):
    pd.to_datetime([None])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Also, if `to_datetime()` has problems parsing any particular date/time format, you can pass the spec in using the `format=` argument.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""The `read_*` functions now have an optional `parse_dates` argument that try to convert any columns passed to it into `datetime` format upon import:""")
    return


@app.cell
def _(pd):
    segments_1 = pd.read_csv('data/AIS/transit_segments.csv', parse_dates=['st_time', 'end_time'])
    return (segments_1,)


@app.cell
def _(segments_1):
    segments_1.dtypes
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Columns of the `datetime` type have an **accessor** to easily extract properties of the data type. This will return a `Series`, with the same row index as the `DataFrame`. For example:""")
    return


@app.cell
def _(segments_1):
    segments_1.st_time.dt.month.head()
    return


@app.cell
def _(segments_1):
    segments_1.st_time.dt.hour.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""This can be used to easily filter rows by particular temporal attributes:""")
    return


@app.cell
def _(segments_1):
    segments_1[segments_1.st_time.dt.month == 2].head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""In addition, time zone information can be applied:""")
    return


@app.cell
def _(segments_1):
    segments_1.st_time.dt.tz_localize('UTC').head()
    return


@app.cell
def _(segments_1):
    segments_1.st_time.dt.tz_localize('UTC').dt.tz_convert('US/Eastern').head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Composing DateTime columns

    Often data will include temporal information that is not expressed as a date or time. For example, the year, month, day, hour, etc. will occupy their own columns. These can be composed into a `datetime64` column using`to_datetime`.

    Let's simulate some temperature data to see how this works:
    """
    )
    return


@app.cell
def _(np, pd):
    from itertools import product

    years = range(2000, 2018)
    months = range(1, 13)
    days = range(1, 29)
    hours = range(24)

    temp_df = pd.DataFrame(list(product(years, months, days, hours)), 
                             columns=['year', 'month', 'day', 'hour'])

    dtemp = np.random.normal(size=temp_df.shape[0])
    temp_df['temperature'] = 75 + dtemp
    return (temp_df,)


@app.cell
def _(temp_df):
    temp_df.head()
    return


@app.cell
def _(pd, temp_df):
    temp_df.index = pd.to_datetime(temp_df[['year', 'month', 'day', 'hour']])
    temp_df.head()
    return


@app.cell
def _(temp_df):
    temp_df.index
    return


@app.cell
def _(temp_df):
    temp_df.temperature.plot()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Merging and joining DataFrame objects""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Now that we have the vessel transit information as we need it, we may want a little more information regarding the vessels themselves. In the `data/AIS` folder there is a second table that contains information about each of the ships that traveled the segments in the `segments` table.""")
    return


@app.cell
def _(pd):
    vessels = pd.read_csv("data/AIS/vessel_information.csv", index_col='mmsi')
    vessels.head()
    return (vessels,)


@app.cell
def _(vessels):
    [v for v in vessels.type.unique() if v.find('/')==-1]
    return


@app.cell
def _(vessels):
    vessels.type.value_counts()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    The challenge, however, is that several ships have travelled multiple segments, so there is not a one-to-one relationship between the rows of the two tables. The table of vessel information has a *one-to-many* relationship with the segments.

    In Pandas, we can combine tables according to the value of one or more *keys* that are used to identify rows, much like an index. Using a trivial example:
    """
    )
    return


@app.cell
def _(np, pd):
    df1 = pd.DataFrame(dict(id=range(4), age=np.random.randint(18, 31, size=4)))
    df2 = pd.DataFrame(dict(id=list(range(3))+list(range(3)), 
                            score=np.random.random(size=6)))

    df1
    return df1, df2


@app.cell
def _(df2):
    df2
    return


@app.cell
def _(df1, df2, pd):
    pd.merge(df1, df2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Notice that without any information about which column to use as a key, Pandas did the right thing and used the `id` column in both tables. Unless specified otherwise, `merge` will used any common column names as keys for merging the tables.

    Notice also that `id=3` from `df1` was omitted from the merged table. This is because, by default, `merge` performs an **inner join** on the tables, meaning that the merged table represents an intersection of the two tables.
    """
    )
    return


@app.cell
def _(df1, df2, pd):
    pd.merge(df1, df2, how='outer')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""The **outer join** above yields the union of the two tables, so all rows are represented, with missing values inserted as appropriate. One can also perform **right** and **left** joins to include all rows of the right or left table (*i.e.* first or second argument to `merge`), but not necessarily the other.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Looking at the two datasets that we wish to merge:""")
    return


@app.cell
def _(segments_1):
    segments_1.head(1)
    return


@app.cell
def _(vessels):
    vessels.head(1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""we see that there is a `mmsi` value (a vessel identifier) in each table, but it is used as an index for the `vessels` table. In this case, we have to specify to join on the index for this table, and on the `mmsi` column for the other.""")
    return


@app.cell
def _(pd, segments_1, vessels):
    segments_merged = pd.merge(vessels, segments_1, left_index=True, right_on='mmsi')
    return (segments_merged,)


@app.cell
def _(segments_merged):
    segments_merged.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    In this case, the default inner join is suitable; we are not interested in observations from either table that do not have corresponding entries in the other.

    Notice that `mmsi` field that was an index on the `vessels` table is no longer an index on the merged table.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Here, we used the `merge` function to perform the merge; we could also have used the `merge` *method* for either of the tables:""")
    return


@app.cell
def _(segments_1, vessels):
    vessels.merge(segments_1, left_index=True, right_on='mmsi').head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Occasionally, there will be fields with the same in both tables that we do not wish to use to join the tables; they may contain different information, despite having the same name. In this case, Pandas will by default append suffixes `_x` and `_y` to the columns to uniquely identify them.""")
    return


@app.cell
def _(pd, segments_1, vessels):
    segments_1['type'] = 'foo'
    pd.merge(vessels, segments_1, left_index=True, right_on='mmsi').head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""This behavior can be overridden by specifying a `suffixes` argument, containing a list of the suffixes to be used for the columns of the left and right columns, respectively.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Concatenation

    A common data manipulation is appending rows or columns to a dataset that already conform to the dimensions of the exsiting rows or colums, respectively. In NumPy, this is done either with `concatenate` or the convenience "functions" `c_` and `r_`:
    """
    )
    return


@app.cell
def _(np):
    np.concatenate([np.random.random(5), np.random.random(5)])
    return


@app.cell
def _(np):
    np.r_[np.random.random(5), np.random.random(5)]
    return


@app.cell
def _(np):
    np.c_[np.random.random(5), np.random.random(5)]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""> Notice that `c_` and `r_` are not really functions at all, since it is performing some sort of indexing operation, rather than being called. They are actually *class instances*, but they are here behaving mostly like functions. Don't think about this too hard; just know that they are there.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    This operation is also called *binding* or *stacking*.

    With Pandas' indexed data structures, there are additional considerations as the overlap in index values between two data structures affects how they are concatenate.

    Lets import two microbiome datasets, each consisting of counts of microorganiams from a particular patient. We will use the first column of each dataset as the index.
    """
    )
    return


@app.cell
def _(pd):
    mb1 = pd.read_excel('data/microbiome/MID1.xls', 'Sheet 1', index_col=0, header=None)
    mb2 = pd.read_excel('data/microbiome/MID2.xls', 'Sheet 1', index_col=0, header=None)
    mb1.shape, mb2.shape
    return mb1, mb2


@app.cell
def _(mb1):
    mb1.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Let's give the index and columns meaningful labels:""")
    return


@app.cell
def _(mb1, mb2):
    mb1.columns = mb2.columns = ['Count']
    return


@app.cell
def _(mb1, mb2):
    mb1.index.name = mb2.index.name = 'Taxon'
    return


@app.cell
def _(mb1):
    mb1.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    The index of these data is the unique biological classification of each organism, beginning with *domain*, *phylum*, *class*, and for some organisms, going all the way down to the genus level.

    ![classification](http://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Biological_classification_L_Pengo_vflip.svg/150px-Biological_classification_L_Pengo_vflip.svg.png)
    """
    )
    return


@app.cell
def _(mb1):
    mb1.index[:3]
    return


@app.cell
def _(mb1):
    mb1.index.is_unique
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""If we concatenate along `axis=0` (the default), we will obtain another data frame with the the rows concatenated:""")
    return


@app.cell
def _(mb1, mb2, pd):
    pd.concat([mb1, mb2], axis=0).shape
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""However, the index is no longer unique, due to overlap between the two DataFrames.""")
    return


@app.cell
def _(mb1, mb2, pd):
    pd.concat([mb1, mb2], axis=0).index.is_unique
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Concatenating along `axis=1` will concatenate column-wise, but respecting the indices of the two DataFrames.""")
    return


@app.cell
def _(mb1, mb2, pd):
    pd.concat([mb1, mb2], axis=1).shape
    return


@app.cell
def _(mb1, mb2, pd):
    pd.concat([mb1, mb2], axis=1).head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""If we are only interested in taxa that are included in both DataFrames, we can specify a `join=inner` argument.""")
    return


@app.cell
def _(mb1, mb2, pd):
    pd.concat([mb1, mb2], axis=1, join='inner').head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""If we wanted to use the second table to *fill values* absent from the first table, we could use `combine_first`.""")
    return


@app.cell
def _(mb1, mb2):
    mb1.combine_first(mb2).head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We can also create a hierarchical index based on keys identifying the original tables.""")
    return


@app.cell
def _(mb1, mb2, pd):
    pd.concat([mb1, mb2], keys=['patient1', 'patient2']).head()
    return


@app.cell
def _(mb1, mb2, pd):
    pd.concat([mb1, mb2], keys=['patient1', 'patient2']).index.is_unique
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Alternatively, you can pass keys to the concatenation by supplying the DataFrames (or Series) as a dict, resulting in a "wide" format table.""")
    return


@app.cell
def _(mb1, mb2, pd):
    pd.concat(dict(patient1=mb1, patient2=mb2), axis=1).head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""If you want `concat` to work like `numpy.concatanate`, you may provide the `ignore_index=True` argument.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Exercise

    In the *data/microbiome* subdirectory, there are 9 spreadsheets of microbiome data that was acquired from high-throughput RNA sequencing procedures, along with a 10th file that describes the content of each. Write code that imports each of the data spreadsheets and combines them into a single `DataFrame`, adding the identifying information from the metadata spreadsheet as columns in the combined `DataFrame`.
    """
    )
    return


@app.cell
def _():
    # Write solution here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Reshaping DataFrame objects

    In the context of a single DataFrame, we are often interested in re-arranging the layout of our data.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    This dataset is from Table 6.9 of [Statistical Methods for the Analysis of Repeated Measurements](http://www.amazon.com/Statistical-Methods-Analysis-Repeated-Measurements/dp/0387953701) by Charles S. Davis, pp. 161-163 (Springer, 2002). These data are from a multicenter, randomized controlled trial of botulinum toxin type B (BotB) in patients with cervical dystonia from nine U.S. sites.

    * Randomized to placebo (N=36), 5000 units of BotB (N=36), 10,000 units of BotB (N=37)
    * Response variable: total score on Toronto Western Spasmodic Torticollis Rating Scale (TWSTRS), measuring severity, pain, and disability of cervical dystonia (high scores mean more impairment)
    * TWSTRS measured at baseline (week 0) and weeks 2, 4, 8, 12, 16 after treatment began
    """
    )
    return


@app.cell
def _(pd):
    cdystonia = pd.read_csv("data/cdystonia.csv", index_col=None)
    cdystonia.head()
    return (cdystonia,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""This dataset includes repeated measurements of the same individuals (longitudinal data). Its possible to present such information in (at least) two ways: showing each repeated measurement in their own row, or in multiple columns representing multiple measurements.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""The `stack` method rotates the data frame so that columns are represented in rows:""")
    return


@app.cell
def _(cdystonia):
    stacked = cdystonia.stack()
    stacked
    return (stacked,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""To complement this, `unstack` pivots from rows back to columns.""")
    return


@app.cell
def _(stacked):
    stacked.unstack().head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""For this dataset, it makes sense to create a hierarchical index based on the patient and observation:""")
    return


@app.cell
def _(cdystonia):
    cdystonia2 = cdystonia.set_index(['patient','obs'])
    cdystonia2.head()
    return (cdystonia2,)


@app.cell
def _(cdystonia2):
    cdystonia2.index.is_unique
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""If we want to transform this data so that repeated measurements are in columns, we can `unstack` the `twstrs` measurements according to `obs`.""")
    return


@app.cell
def _(cdystonia2):
    twstrs_wide = cdystonia2['twstrs'].unstack('obs')
    twstrs_wide.head()
    return (twstrs_wide,)


@app.cell
def _(cdystonia, twstrs_wide):
    cdystonia_wide = (cdystonia[['patient','site','id','treat','age','sex']]
                      .drop_duplicates()
                      .merge(twstrs_wide, right_index=True, left_on='patient', how='inner')
                      .head())
    cdystonia_wide
    return (cdystonia_wide,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""A slightly cleaner way of doing this is to set the patient-level information as an index before unstacking:""")
    return


@app.cell
def _(cdystonia):
    (cdystonia.set_index(['patient','site','id','treat','age','sex','week'])['twstrs']
         .unstack('week').head())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    To convert our "wide" format back to long, we can use the `melt` function, appropriately parameterized. This function is useful for `DataFrame`s where one
    or more columns are identifier variables (`id_vars`), with the remaining columns being measured variables (`value_vars`). The measured variables are "unpivoted" to
    the row axis, leaving just two non-identifier columns, a *variable* and its corresponding *value*, which can both be renamed using optional arguments.
    """
    )
    return


@app.cell
def _(cdystonia_wide, pd):
    pd.melt(cdystonia_wide, id_vars=['patient','site','id','treat','age','sex'], 
            var_name='obs', value_name='twsters').head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    This illustrates the two formats for longitudinal data: **long** and **wide** formats. Its typically better to store data in long format because additional data can be included as additional rows in the database, while wide format requires that the entire database schema be altered by adding columns to every row as data are collected.

    The preferable format for analysis depends entirely on what is planned for the data, so it is imporant to be able to move easily between them.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Pivoting

    The `pivot` method allows a DataFrame to be transformed easily between long and wide formats in the same way as a pivot table is created in a spreadsheet. It takes three arguments: `index`, `columns` and `values`, corresponding to the DataFrame index (the row headers), columns and cell values, respectively.

    For example, we may want the `twstrs` variable (the response variable) in wide format according to patient, as we saw with the unstacking method above:
    """
    )
    return


@app.cell
def _(cdystonia):
    cdystonia.pivot(index='patient', columns='obs', values='twstrs').head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""If we omit the `values` argument, we get a `DataFrame` with hierarchical columns, just as when we applied `unstack` to the hierarchically-indexed table:""")
    return


@app.cell
def _():
    # cdystonia.pivot('patient', 'obs')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""A related method, `pivot_table`, creates a spreadsheet-like table with a hierarchical index, and allows the values of the table to be populated using an arbitrary aggregation function.""")
    return


@app.cell
def _(cdystonia):
    cdystonia.pivot_table(index=['site', 'treat'], columns='week', values='twstrs', 
                          aggfunc=max).head(20)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""For a simple cross-tabulation of group frequencies, the `crosstab` function (not a method) aggregates counts of data according to factors in rows and columns. The factors may be hierarchical if desired.""")
    return


@app.cell
def _(cdystonia, pd):
    pd.crosstab(cdystonia.sex, cdystonia.site)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Method chaining

    In the DataFrame reshaping section above, you probably noticed how several methods were strung together to produce a wide format table:
    """
    )
    return


@app.cell
def _(cdystonia, twstrs_wide):
    (cdystonia[['patient','site','id','treat','age','sex']] 
                      .drop_duplicates() 
                      .merge(twstrs_wide, right_index=True, left_on='patient', how='inner') 
                      .head())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    This approach of seqentially calling methods is called **method chaining**, and despite the fact that it creates very long lines of code that must be properly justified, it allows for the writing of rather concise and readable code.

    Method chaining is possible because of the pandas convention of returning copies of the results of operations, rather than in-place operations. This allows methods from the returned object to be immediately called, as needed, rather than assigning the output to a variable that might not otherwise be used.

    For example, without method chaining we would have done the following:
    """
    )
    return


@app.cell
def _(cdystonia, twstrs_wide):
    cdystonia_subset = cdystonia[['patient','site','id','treat','age','sex']]
    cdystonia_complete = cdystonia_subset.drop_duplicates()
    cdystonia_merged = cdystonia_complete.merge(twstrs_wide, right_index=True, left_on='patient', how='inner')
    cdystonia_merged.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""This necessitates the creation of a slew of intermediate variables that we really don't need.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Method chaining (properly used) can make for more readable code for data processing. Typioally, a series of function calls end up being nested within each other, resulting in the code's "story" being told in reverse. As an analogy, I will use an actual story (this is taken from [Jeff Allen's example](http://trestletech.com/wp-content/uploads/2015/07/dplyr.pdf) in the context of R programming.

    Consider the nursery rhyme "Jack and Jill":

    > Jack and Jill went up the hill
    > To fetch a pail of water
    > Jack fell down and broke his crown,
    > And Jill came tumbling after

    Implementing the actions of this rhyme in code as a series of function calls results in the following:

    ```python
    tumble_after(broke(
        fell_down(
            fetch(went_up(jack_jill, "hill"), "water"), jack),
            "crown"),
        "jill"
    )
    ```

    notice that the beginning of the story end up in the middle, and reading the code necessitates working your way out out from the middle, keeping track of arguments and the function within which the current function is nested.

    With method chaining, you end up with a more linear story:

    ```python
    (jack_jill.went_up("hill")
            .fetch("water")
            .fell_down("jack")
            .broke("crown")
            .tumble_after("jill"))
    ```
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Let's transform another dataset using method chaining. The `measles.csv` file contains de-identified cases of measles from an outbreak in Sao Paulo, Brazil in 1997. The file contains rows of individual records:""")
    return


@app.cell
def _(pd):
    measles = pd.read_csv("data/measles.csv", index_col=0, encoding='latin-1', parse_dates=['ONSET'])
    measles.head()
    return (measles,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    The goal is to summarize this data by age groups and bi-weekly period, so that we can see how the outbreak affected different ages over the course of the outbreak.

    The best approach is to build up the chain incrementally. We can begin by generating the age groups (using `cut`) and grouping by age group and the date (`ONSET`):
    """
    )
    return


@app.cell
def _(measles, pd):
    pd.cut(measles.YEAR_AGE, [0,5,10,15,20,25,30,35,40,100], right=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""What we then want is the number of occurences in each combination, which we can obtain by checking the `size` of each grouping:""")
    return


@app.cell
def _(measles, pd):
    (measles.assign(AGE_GROUP=pd.cut(measles.YEAR_AGE, [0,5,10,15,20,25,30,35,40,100], right=False))
                            .groupby(['ONSET', 'AGE_GROUP'])
                            .size()).head(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""This results in a hierarchically-indexed `Series`, which we can pivot into a `DataFrame` by simply unstacking:""")
    return


@app.cell
def _(measles, pd):
    (measles.assign(AGE_GROUP=pd.cut(measles.YEAR_AGE, [0,5,10,15,20,25,30,35,40,100], right=False))
                            .groupby(['ONSET', 'AGE_GROUP'])
                            .size()
                            .unstack()).head(5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Now, fill replace the missing values with zeros:""")
    return


@app.cell
def _(measles, pd):
    (measles.assign(AGE_GROUP=pd.cut(measles.YEAR_AGE, [0,5,10,15,20,25,30,35,40,100], right=False))
                            .groupby(['ONSET', 'AGE_GROUP'])
                            .size()
                            .unstack()
                            .fillna(0)).head(5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Finally, we want the counts in 2-week intervals, rather than as irregularly-reported days, which yields our the table of interest:""")
    return


@app.cell
def _(measles, pd):
    case_counts_2w = (measles.assign(AGE_GROUP=pd.cut(measles.YEAR_AGE, [0,5,10,15,20,25,30,35,40,100], right=False))
                            .groupby(['ONSET', 'AGE_GROUP'])
                            .size()
                            .unstack()
                            .fillna(0)
                            .resample('2W')
                            .sum())

    case_counts_2w
    return (case_counts_2w,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""From this, it is easy to create meaningful plots and conduct analyses:""")
    return


@app.cell
def _(case_counts_2w):
    case_counts_2w.plot(cmap='magma');
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Pipes

    The one shortcoming of method chaining is that it requires all of the functionality that you need for data processing to be implemented somewhere as methods. Occasionally, we need to do custom manipulations on our data, which can be either awkward or impossible using DataFrame methods alone.

    The pandas `pipe` DataFrame method allows users to apply a function to a DataFrame, as if it were a method. The lone restriction on the function is that it must return the modified DataFrame as its return value.

    For example, let's say we wanted, rather than counts of measles cases from the dataset above, **proportions** of cases in each period. For this, we need a function that sums the total cases for each period, and then divides each row by that total. Here is such a function:
    """
    )
    return


@app.function
def to_proportions(df, axis=1):
    row_totals = df.sum(axis)
    return df.div(row_totals, True - axis)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We can then use the `pipe` method in our chain, with the function as its argument:""")
    return


@app.cell
def _(measles, pd):
    case_prop_2w = (measles.assign(AGE_GROUP=pd.cut(measles.YEAR_AGE, [0,5,10,15,20,25,30,35,40,100], right=False))
                            .groupby(['ONSET', 'AGE_GROUP'])
                            .size()
                            .unstack()
                            .fillna(0)
                            .resample('2W')
                            .sum()
                            .pipe(to_proportions))

    case_prop_2w
    return (case_prop_2w,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    If there are secondary arguments to the function, they can be passed after the function name.

    Note that this transformation results in a very different plot that tells a different story!
    """
    )
    return


@app.cell
def _(case_prop_2w):
    case_prop_2w.plot(cmap='magma');
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Data transformation

    There are a slew of additional operations for DataFrames that we would collectively refer to as "transformations" which include tasks such as removing duplicate values, replacing values, and grouping values.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Dealing with duplicates

    We can easily identify and remove duplicate values from `DataFrame` objects. For example, say we want to removed ships from our `vessels` dataset that have the same name:
    """
    )
    return


@app.cell
def _(vessels):
    vessels.duplicated(subset='names')
    return


@app.cell
def _(vessels):
    vessels.drop_duplicates(['names'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Value replacement

    Frequently, we get data columns that are encoded as strings that we wish to represent numerically for the purposes of including it in a quantitative analysis. For example, consider the treatment variable in the cervical dystonia dataset:
    """
    )
    return


@app.cell
def _(cdystonia):
    cdystonia.treat.value_counts()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""A logical way to specify these numerically is to change them to integer values, perhaps using "Placebo" as a baseline value. If we create a dict with the original values as keys and the replacements as values, we can pass it to the `map` method to implement the changes.""")
    return


@app.cell
def _():
    treatment_map = {'Placebo': 0, '5000U': 1, '10000U': 2}
    return (treatment_map,)


@app.cell
def _(cdystonia, treatment_map):
    cdystonia['treatment'] = cdystonia.treat.map(treatment_map)
    cdystonia.treatment
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Alternately, if we simply want to replace particular values in a `Series` or `DataFrame`, we can use the `replace` method.

    An example where replacement is useful is dealing with zeros in certain transformations. For example, if we try to take the log of a set of values:
    """
    )
    return


@app.cell
def _(pd):
    vals = pd.Series([float(i)**10 for i in range(10)])
    vals
    return (vals,)


@app.cell
def _(np, vals):
    np.log(vals)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""In such situations, we can replace the zero with a value so small that it makes no difference to the ensuing analysis. We can do this with `replace`.""")
    return


@app.cell
def _(np, vals):
    vals_1 = vals.replace(0, 1e-06)
    np.log(vals_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We can also perform the same replacement that we used `map` for with `replace`:""")
    return


@app.cell
def _(cdystonia2):
    cdystonia2.treat.replace({'Placebo': 0, '5000U': 1, '10000U': 2})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Inidcator variables

    For some statistical analyses (*e.g.* regression models or analyses of variance), categorical or group variables need to be converted into columns of indicators--zeros and ones--to create a so-called **design matrix**. The Pandas function `get_dummies` (indicator variables are also known as *dummy variables*) makes this transformation straightforward.

    Let's consider the DataFrame containing the ships corresponding to the transit segments on the eastern seaboard. The `type` variable denotes the class of vessel; we can create a matrix of indicators for this. For simplicity, lets filter out the 5 most common types of ships:
    """
    )
    return


@app.cell
def _(vessels):
    top5 = vessels.type.isin(vessels.type.value_counts().index[:5])
    top5.head(10)
    return (top5,)


@app.cell
def _(top5, vessels):
    vessels5 = vessels[top5]
    return (vessels5,)


@app.cell
def _(pd, vessels5):
    pd.get_dummies(vessels5.type).head(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Categorical Data

    Pandas provides a convenient `dtype` for reprsenting categorical (factor) data, called `category`.

    For example, the `treat` column in the cervical dystonia dataset represents three treatment levels in a clinical trial, and is imported by default as an `object` type, since it is a mixture of string characters.
    """
    )
    return


@app.cell
def _(cdystonia):
    cdystonia.treat.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We can convert this to a `category` type either by the `Categorical` constructor, or casting the column using `astype`:""")
    return


@app.cell
def _(cdystonia, pd):
    pd.Categorical(cdystonia.treat)
    return


@app.cell
def _(cdystonia):
    cdystonia['treat'] = cdystonia.treat.astype('category')
    return


@app.cell
def _(cdystonia):
    cdystonia.treat.describe()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""By default the Categorical type represents an unordered categorical.""")
    return


@app.cell
def _(cdystonia):
    cdystonia.treat.cat.categories
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""However, an ordering can be imposed. The order is lexical by default, but will assume the order of the listed categories to be the desired order.""")
    return


@app.cell
def _(cdystonia):
    cdystonia.treat = cdystonia.treat.cat.set_categories(
        ['Placebo', '5000U', '10000U'], rename=True
    )
    return


@app.cell
def _(cdystonia):
    cdystonia.treat.cat.as_ordered().head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""The important difference between the `category` type and the `object` type is that `category` is represented by an underlying array of integers, which is then mapped to character labels.""")
    return


@app.cell
def _(cdystonia):
    cdystonia.treat.cat.codes
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Notice that these are 8-bit integers, which are essentially single bytes of data, making memory usage lower.

    There is also a performance benefit. Consider an operation such as calculating the total segment lengths for each ship in the `segments` table (this is also a preview of pandas' `groupby` operation!):
    """
    )
    return


@app.cell
def _():
    # magic command not supported in marimo; please file an issue to add support
    # %time segments.groupby(segments.name).seg_length.sum().sort_values(ascending=False, inplace=False).head()
    return


@app.cell
def _(segments_1):
    segments_1['name'] = segments_1.name.astype('category')
    return


@app.cell
def _():
    # magic command not supported in marimo; please file an issue to add support
    # %time segments.groupby(segments.name).seg_length.sum().sort_values(ascending=False, inplace=False).head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Hence, we get a considerable speedup simply by using the appropriate `dtype` for our data.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Permutation and sampling

    For some data analysis tasks, such as simulation, we need to be able to randomly reorder our data, or draw random values from it. Calling NumPy's `permutation` function with the length of the sequence you want to permute generates an array with a permuted sequence of integers, which can be used to re-order the sequence.
    """
    )
    return


@app.cell
def _(np, segments_1):
    new_order = np.random.permutation(len(segments_1))
    new_order[:30]
    return (new_order,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Using this sequence as an argument to the `take` method results in a reordered DataFrame:""")
    return


@app.cell
def _(new_order, segments_1):
    segments_1.take(new_order).head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Compare this ordering with the original:""")
    return


@app.cell
def _(segments_1):
    segments_1.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""For random sampling, `DataFrame` and `Series` objects have a `sample` method that can be used to draw samples, with or without replacement:""")
    return


@app.cell
def _(vessels):
    vessels.sample(n=10)
    return


@app.cell
def _(vessels):
    vessels.sample(n=10, replace=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Data aggregation and GroupBy operations

    One of the most powerful features of Pandas is its **GroupBy** functionality. On occasion we may want to perform operations on *groups* of observations within a dataset. For exmaple:

    * **aggregation**, such as computing the sum of mean of each group, which involves applying a function to each group and returning the aggregated results
    * **slicing** the DataFrame into groups and then doing something with the resulting slices (*e.g.* plotting)
    * group-wise **transformation**, such as standardization/normalization
    """
    )
    return


@app.cell
def _(cdystonia):
    cdystonia_grouped = cdystonia.groupby(cdystonia.patient)
    return (cdystonia_grouped,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""This *grouped* dataset is hard to visualize""")
    return


@app.cell
def _(cdystonia_grouped):
    cdystonia_grouped
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""However, the grouping is only an intermediate step; for example, we may want to **iterate** over each of the patient groups:""")
    return


@app.cell
def _(cdystonia_grouped):
    for patient, group in cdystonia_grouped:
        print('patient', patient)
        print('group', group)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    A common data analysis procedure is the **split-apply-combine** operation, which groups subsets of data together, applies a function to each of the groups, then recombines them into a new data table.

    For example, we may want to aggregate our data with with some function.

    ![split-apply-combine](https://wesmckinney.com/book/images/pyda_0901.png)

    <div align="right">*(figure taken from "Python for Data Analysis", p.251)*</div>
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We can aggregate in Pandas using the `aggregate` (or `agg`, for short) method:""")
    return


@app.cell
def _(cdystonia, cdystonia_grouped, np):
    # cdystonia_grouped.agg(np.mean).head()
    numeric_cols = cdystonia.select_dtypes(include='number').columns
    cdystonia_grouped[numeric_cols].agg(np.mean).head()
    return (numeric_cols,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Notice that the `treat` and `sex` variables are not included in the aggregation. Since it does not make sense to aggregate non-string variables, these columns are simply ignored by the method.

    Some aggregation functions are so common that Pandas has a convenience method for them, such as `mean`:
    """
    )
    return


@app.cell
def _(cdystonia_grouped, numeric_cols):
    cdystonia_grouped[numeric_cols].mean().head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""The `add_prefix` and `add_suffix` methods can be used to give the columns of the resulting table labels that reflect the transformation:""")
    return


@app.cell
def _(cdystonia_grouped, numeric_cols):
    cdystonia_grouped[numeric_cols].mean().add_suffix('_mean').head()
    return


@app.cell
def _(cdystonia_grouped):
    # The median of the `twstrs` variable
    cdystonia_grouped['twstrs'].quantile(0.5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""If we wish, we can easily aggregate according to multiple keys:""")
    return


@app.cell
def _(cdystonia):
    # cdystonia.groupby(['week','site']).mean().head()
    numeric_cols_1 = cdystonia.select_dtypes(include=['number']).columns
    cdystonia.groupby(['week', 'site'])[numeric_cols_1].mean().head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Alternately, we can **transform** the data, using a function of our choice with the `transform` method:""")
    return


@app.cell
def _(cdystonia, cdystonia_grouped):
    #normalize = lambda x: (x - x.mean())/x.std()
    #cdystonia_grouped.transform(normalize).head()
    numeric_cols_2 = cdystonia.select_dtypes(include=['number']).columns
    normalize = lambda x: (x - x.mean()) / x.std()
    cdystonia_grouped[numeric_cols_2].transform(normalize).head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""It is easy to do column selection within `groupby` operations, if we are only interested split-apply-combine operations on a subset of columns:""")
    return


@app.cell
def _(cdystonia_grouped):
    cdystonia_grouped['twstrs'].mean().head()
    return


@app.cell
def _(cdystonia_grouped):
    # This gives the same result as a DataFrame
    cdystonia_grouped[['twstrs']].mean().head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""If you simply want to divide your DataFrame into chunks for later use, its easy to convert them into a dict so that they can be easily indexed out as needed:""")
    return


@app.cell
def _(cdystonia_grouped):
    chunks = dict(list(cdystonia_grouped))
    return (chunks,)


@app.cell
def _(chunks):
    chunks[4]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Its also possible to group by one or more levels of a hierarchical index. Recall `cdystonia2`, which we created with a hierarchical index:""")
    return


@app.cell
def _(cdystonia2):
    cdystonia2.head(10)
    return


@app.cell
def _(cdystonia2):
    cdystonia2.groupby(level='obs', axis=0)['twstrs'].mean()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Apply

    We can generalize the split-apply-combine methodology by using `apply` function. This allows us to invoke any function we wish on a grouped dataset and recombine them into a DataFrame.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""The function below takes a DataFrame and a column name, sorts by the column, and takes the `n` largest values of that column. We can use this with `apply` to return the largest values from every group in a DataFrame in a single call.""")
    return


@app.function
def top(df, column, n=5):
    return df.sort_values(by=column, ascending=False)[:n]


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""To see this in action, consider the vessel transit segments dataset (which we merged with the vessel information to yield `segments_merged`). Say we wanted to return the 3 longest segments travelled by each ship:""")
    return


@app.cell
def _(segments_merged):
    top3segments = segments_merged.groupby('mmsi').apply(top, column='seg_length', n=3)[['names', 'seg_length']]
    top3segments.head(15)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Notice that additional arguments for the applied function can be passed via `apply` after the function name. It assumes that the DataFrame is the first argument.""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Recall the microbiome data sets that we used previously for the concatenation example. Suppose that we wish to aggregate the data at a higher biological classification than genus. For example, we can identify samples down to *class*, which is the 3rd level of organization in each index.""")
    return


@app.cell
def _(mb1):
    mb1.index[:3]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Using the string methods `split` and `join` we can create an index that just uses the first three classifications: domain, phylum and class.""")
    return


@app.cell
def _(mb1):
    class_index = mb1.index.map(lambda x: ' '.join(x.split(' ')[:3]))
    return (class_index,)


@app.cell
def _(class_index, mb1):
    mb_class = mb1.copy()
    mb_class.index = class_index
    return (mb_class,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""However, since there are multiple taxonomic units with the same class, our index is no longer unique:""")
    return


@app.cell
def _(mb_class):
    mb_class.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""We can re-establish a unique index by summing all rows with the same class, using `groupby`:""")
    return


@app.cell
def _(mb_class):
    mb_class.groupby(level=0).sum().head(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Exercise

    Load the dataset in `titanic.xls`. It contains data on all the passengers that travelled on the Titanic.
    """
    )
    return


@app.cell
def _():
    from IPython.core.display import HTML
    HTML(filename='data/titanic.html')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Women and children first?

    1. Use the `groupby` method to calculate the proportion of passengers that survived by sex.
    2. Calculate the same proportion, but by class and sex.
    3. Create age categories: children (under 14 years), adolescents (14-20), adult (21-64), and senior(65+), and calculate survival proportions by age category, class and sex.
    """
    )
    return


@app.cell
def _():
    # Write your answer here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""---""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Clean Up""")
    return


@app.cell
def _():
    # Clean up files that were created above:
    import os
    if os.path.exists("baseball_pickle"): os.remove("baseball_pickle")
    if os.path.exists("mb.csv"): os.remove("mb.csv")
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
