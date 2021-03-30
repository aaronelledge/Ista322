#!/usr/bin/env python
# coding: utf-8

# # ISTA 322 Homework 1
# 
# Welcome to your first homework!  This one is focused on just practicing some of the exercises covered in the last coding lesson.  There are also some more open-ended questions with elements that I didn't demonstrate in that lesson... they're structurally similar, but you might need to google a thing or two to figure out the correction function.  
# 
# You need to add your own code blocks to answer any of the coding questions.  Also, at the end of some sections I have a 'questions' section.  Add a text cell right below and enter your answers. 

# ## Loading and Importing
# 
# First thing you need to do is load up your packages and then bring in the data.  
# 
# This dataset contains daily values for Amazon's stock.  This includes opening, closing, high price, low price, and also the amount of stock traded. 

# In[2]:


import pandas as pd
# also import matplotlib.pyplot and numpy with the proper aliases
import numpy as np
import matplotlib.pyplot as plt


# In[3]:


# Bring in your data. You just need to run this cell.
price = pd.read_csv("https://docs.google.com/spreadsheets/d/1z6br9DCz3v9MmPSBfGm7zy9-B-JQuKk71uh9SM0-NPw/gviz/tq?tqx=out:csv")


# ## Exploring the whole dataset
# 
# Now make some code cells to explore the whole dataset.  I want you to do the following:
# 
# - Get the number of rows and columns
# - Get the datatypes of each column
# - Look at the first five rows
# - Look at the last five rows
# - Look at summary statistics

# In[4]:


price.shape
# The dimensions are 5852 rows, and 7 columns


# In[5]:


price.dtypes
# Datatypes of each column


# In[6]:


price.head()
# Outputs the first 5 rows of data


# In[7]:


price.head(5852)
# Outputs the last 5 rows of data


# In[7]:


price.describe()
#Summary of the statistics


# ### Questions
# 
# - How many rows are in this dataset?
# - Do any datatypes need to be converted?
# - What was the mean and all time high opening stock price?

# In[ ]:


# The dataset contains 5852 rows
# Yes, the date column needs to be converted
#  The mean and all time high opening stock price is 


# ## Making some columns
# 
# Here we need to make a couple new columns.
# 
# - First, turn that date column into an actual date object.  
# - Also make a new column called 'up_binom' if the stock price increased for that day

# In[8]:


price['Date']
pd.to_datetime(price['Date'])
price['Date']= pd.to_datetime(price['Date'])
price.dtypes
# Date column turned into an actual date object


# In[11]:


price['Date']
price['Date'] = pd.to_datetime(price['Date'])
price.dtypes

price.head
np.where(price['Close'] >= 0, 1, 0)

price['up_binom'] = np.where(price['Close'] >= price['Open'], 1, 0)
print(price['up_binom'])

# Column creating column up_binom 


# In[ ]:





# ### Using the columns - Making a plot
# 
# Let's use those columns we just made to make a plot
# 
# - First, explore your new column.  What is the starting date, ending date, and total time from beginning to end?  You'll need three lines of code to do this
# - Next, make a plot of the closing price over the whole timeframe of the dataset
# - Hint - you might need to google how to make a line plot!

# In[110]:


plt.plot(price['Date'],
price['Close'])
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.show()


# ### Using the columns - How rich could I be?  
# 
# Word problem time.  When I was 13 I save up $2000 from mowing lawns and bought a bicycle.  This was honestly right around the start of this dataset (May 15, 1997).  Let's say instead of buying that bike I put all that money into Amazon stock.  How much would that stock be worth on the very last day of this dataset?
# 
# 
# 
# 

# In[113]:


# I'm going to make your life easier and set the date column you created as the index.
# This will make searching and extracting the values much easier
(2000/price['Close'].iloc[0])*(price['Close'].iloc[-1])

# Stock would be worth 3214999.7165956963 on the last day of the dataset


# ###Questions
# 
# How big of a mistake did I make in dollars by not buying Amazon stock?

# ## JSON
# 
# The last part of the assignment will have you working with some basic JSON data.  The URL links to a JSON file with stats on every episode of the TV show Silicon Valley
# 

# In[74]:


# First just run this to import the data
import requests
url = 'http://api.tvmaze.com/singlesearch/shows?q=silicon-valley&embed=episodes'
sv_json_obj = requests.get(url)
sv_json = sv_json_obj.json()


# ### Viewing your JSON
# 
# Now just to look at what's in the JSON a bit
# 
# - Make a code cell that just calls the JSON we named above. 
# - Also run the .keys() function on the object.

# In[68]:


sv_json = sv_json_obj.json()
type(sv_json)
sv_json
# Calling JSON

sv_json.keys()

# Returns a list of dict_keys


# ### Questions
# 
# Based on these responses, what keys are present in the JSON.  More importantly, are there any keys that don't get returned by .keys()?

# In[ ]:


# Keys present in JSON id', 'url', 'name', 'type', 'language', 'genres', 'status', 'runtime', 'premiered', 'officialSite', 'schedule', 'rating',
# 'weight', 'network', 'webChannel', 'externals', 'image', 'summary', 'updated', '_links', '_embedded

#The key does not get returned airtime, airstamp, and airdate


# ### Looking at overall show info
# 
# They keys it's returning are related to the overall show info.  Can you do the following? 
# 
# - Get the day the show premiered
# - Get the summary of the show
# - Get the name of the network the show aired on 

# In[114]:


sv_json['premiered']
# Ouputs the day the show preiered


# In[115]:


sv_json['summary']
# Outputs the summary 


# In[116]:


sv_json['network']
# Outputs the name of the network the show aired on


# ### Info from individual episodes
# 
# To wrap up I want you to pull just some info from individual episodes. To access them we can use the '_embedded' key first.  Please do the following
# 
# - Get the title of the 7th episode entry from the start
# - Get the summary of the 3rd episode entry from the start
# - Get the original image URL from the 4 entry from the start

# In[92]:


# First, you can see the structure after moving down a level into '_embedded'
sv_json['_embedded']


# In[107]:


sv_json['_embedded']['episodes'][6]
# Outputs the title of the 7th episode, 'Proof of Concept'


# In[108]:


sv_json['_embedded']['episodes'][2]['summary']
#Outputs the summary for the 3rd episode


# In[109]:


sv_json['_embedded']['episodes'][3]['image']
#Outputs the image URL for the 4th entry


# In[ ]:




