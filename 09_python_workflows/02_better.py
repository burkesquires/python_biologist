#!/usr/bin/env python
# coding: utf-8

# # Better Python Workflow

# ---

# In[1]:


data_file = 'data/gapminder_five_year_dirty.txt'


# # conda install pandas

# In[2]:


import pandas as pd
get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


import logging

# create logger with 'spam_application'
logger = logging.getLogger('better_workflow')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('better_workflow.log')
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


# In[4]:


logging.info("Reading Data into pandas")
df_original = pd.read_csv(data_file, sep='\t')


# In[5]:


logging.debug(df_original.info())


# In[6]:


logging.debug(df_original.region.unique())


# In[7]:


logging.debug('Replace: Africa_Congo, Dem. Rep., Africa_Democratic Republic of the Congo, Africa_Congo, Rep. with Africa_Congo, Democratic Republic')
df_original.region.replace('Africa_Congo, Dem. Rep.', 'Africa_Congo, Democratic Republic')
df_original.region.replace('Africa_Democratic Republic of the Congo', 'Africa_Congo, Democratic Republic')
df_original.region.replace('Africa_Congo, Rep.', 'Africa_Congo, Democratic Republic')
df_original.region.replace('Asia_china', 'Asia_China')
df_original.region.replace('Americas_Colombia    ', 'Americas_Colombia')


# In[8]:


df_original['year'].describe()


# In[9]:


df_original.year.hist()


# In[ ]:




