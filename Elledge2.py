#!/usr/bin/env python
# coding: utf-8

# #HW3 - SQL
#  
# This homework has you working with a new database of information on ticket sales for various types of events.  Your job will be to do some initial exploring and then demonstrate your ability to do all the different types of SQL queries we learned over the last two week.  You'll also need to make one function that'll make looking at the tables easier. 
#  
# These questions are written in the way someone would ask them to you.  In other words, I'm using 'plain english' questions vs. ones where I'm very explicit in terms of what columns and tables to use.  Your exploring of the database and functions to ease that process will come in handy here!  
#  
# Also, I made the database using a set of data from Amazon. You can read more about what each table contains here: https://docs.aws.amazon.com/redshift/latest/dg/c_sampledb.html.  

# ## Libraries and import functions

# First bring the libraries we'll need!

# In[3]:


import psycopg2 
import pandas as pd


# Now bring in all our functions we used in the lessons!  

# In[4]:


# Make our connection/cursor function 

def get_conn_cur(): # define function name and arguments (there aren't any)
  # Make a connection
  conn = psycopg2.connect(
    host="ticket-sales-db.cnt7cm8tgir1.us-west-1.rds.amazonaws.com",
    database="sales_db",
    user="postgres",
    password="ISTA322SALESDB",
    port='5432')
  
  cur = conn.cursor()   # Make a cursor after

  return(conn, cur)   # Return both the connection and the cursor

# Same run_query function
def run_query(query_string):

  conn, cur = get_conn_cur() # get connection and cursor

  cur.execute(query_string) # executing string as before

  my_data = cur.fetchall() # fetch query data as before

  # here we're extracting the 0th element for each item in cur.description
  colnames = [desc[0] for desc in cur.description]

  cur.close() # close
  conn.close() # close

  return(colnames, my_data) # return column names AND data

# Column name function for checking out what's in a table
def get_column_names(table_name): # arguement of table_name
  conn, cur = get_conn_cur() # get connection and cursor

  # Now select column names while inserting the table name into the WERE
  column_name_query =  """SELECT column_name FROM information_schema.columns
       WHERE table_name = '%s' """ %table_name

  cur.execute(column_name_query) # exectue
  my_data = cur.fetchall() # store

  cur.close() # close
  conn.close() # close

  return(my_data) # return

# Check table_names
def get_table_names():
  conn, cur = get_conn_cur() # get connection and cursor

  # query to get table names
  table_name_query = """SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public' """

  cur.execute(table_name_query) # execute
  my_data = cur.fetchall() # fetch results

  cur.close() #close cursor
  conn.close() # close connection

  return(my_data) # return your fetched results


# ## Make a SQL head function - 1 point
# 
# Make function to get the pandas equivalent of `.head()`
# 
# This function should be called `sql_head` and take a single argument of `table_name` where you specify the table name you want the head information from.  It should return the column names along with the first five rows of the table along.  
# 
# High-five if you return a pandas dataframe with this information so it displays nicely:)

# In[5]:


# make sql_head function
def sql_head(table_name):
    conn, cur = get_conn_cur()
    table_name_query = """SELECT * FROM %s LIMIT 5"""% table_name
    cur.execute(table_name_query)
    my_data = cur.fetchall()
    return(my_data)
    


# In[6]:


# Check that it works!
sql_head(table_name = 'event')


# ## Explore and SELECT - 1 point
# 
# Let's start this homework with some basic queries to get a look at what's in the various tables.  I want you to do the following.
# 
# * Use your get_table_names() function to see what tables are in the database.
# * Use your get_column_names() to get the column names of each of the tables.  **Do this all within a single cell to keep it neat**.
# * Make and run a query that selects all columns from the event table.  Only return the first 5 rows.
# * Use the `sql_head()` function you created to get the first five rows of the sales table.

# In[231]:


# Getting table names
get_table_names()


# In[232]:


# Getting column names
print(get_column_names('users'))
print(get_column_names('category'))
print(get_column_names('date'))
print(get_column_names('listing'))
print(get_column_names('venue'))
print(get_column_names('event'))
print(get_column_names('sales'))


# In[233]:


# Could also just use a list comprehension vs a bunch of print statements :)
names = get_table_names()
[get_column_names(table_name= x) for x in names]


# In[234]:


# Query on events
sq = """SELECT * FROM event LIMIT 5"""
run_query(sq)


# In[235]:


# Use sql_head to get the head of sales
sql_head('sales')


# ## WHERE - 2 points
# 
# Now let's do a bit of filtering with WHERE.  Write and run queries to get the following results.  LIMIT all returns to first five rows. 
# 
# * Get venues with >= 10000 seats from the venues table
# * Get venues in Arizona
# * Get users who have a first name that starts with H
# * Get just email addresses of users who gave a .edu email address
# 
# 
# 

# In[4]:


# Get big venues... so those with >= than 10000 seats
sq = """ SELECT * FROM venue
            WHERE venue_seats >= '10000' LIMIT 5;"""
run_query(sq)


# In[5]:


# Get venues in AZ
sq = """ SELECT * FROM venue
        WHERE venue_state = 'AZ'LIMIT 5;"""
run_query(sq)


# In[6]:


# Get user names of who have names starting with 'H'
sq = """SELECT first_name as name FROM users
        WHERE first_name LIKE 'H%' LIMIT 5;"""
run_query(sq)


# In[7]:


# Get all .edu email addresses... just the email addresses
sq = """ SELECT email FROM users
        WHERE email LIKE '%.edu%' LIMIT 5;"""
run_query(sq)


# ## GROUP BY and HAVING - 2 points
#  
# Time to practice some GROUP BY and HAVING operations.  Please write and run queries that do the following:
#  
# GROUP BY application
# * Find the top five venues that hosted the most events.  Alias the count of events as 'events_hosted'.  Also return the venue ID
# * Get the number of events hosted in each month.  You'll need to use `date_part()` in your select to select just the months.  Alias this as 'month' and then the count of the number of events hosted as 'events_hosted'. 
# * Get the top five sellers who made the most commission.  Alias their total commission made as 'total_com'.  Also get their average commission made and alias as 'avg_com'.  Be sure to also display the seller_id.  
#  
# HAVING application
# * Using the same query as the last one, instead of getting the top five sellers get all sellers who have made a total commission greater than 4000.
# * Using the same query as the first groupby, instead of returning the top five venues, return just the ID's of venues that have had greater than 60 events. 

# In[8]:


# Which venue_id hosted the most events?  
sq = """SELECT event.venue_id, COUNT(event.venue_id) AS events_hosted 
    FROM event GROUP BY event.venue_id 
    ORDER BY events_hosted DESC LIMIT 5"""

run_query(sq)


# In[9]:


# Get the number of events hosted each month
sq ="""SELECT date_part('month', start_time) AS month, COUNT(event.start_time) AS events_hosted FROM event GROUP BY month""" 
run_query(sq)


# In[11]:


# Get the top five sellers who made the most commission.  Also display their ID and their average commission
sq = """SELECT SUM(sales.commission) 
        AS total_com, seller_id, AVG(sales.commission) AS avg_com 
        FROM sales GROUP BY seller_id ORDER BY total_com DESC LIMIT 5"""
run_query(sq)


# In[12]:


# Get the seller id, total commission made, and average commision made for sellers who have made more than $4000
sq = """SELECT seller_id, SUM(sales.commission) 
    AS total_com, AVG(sales.commission) AS avg_com 
    FROM sales GROUP BY seller_id HAVING SUM(sales.commission) > 4000"""
run_query(sq)


# In[13]:


# Get the ids of venues that have hosted over 60 events. Return just the venue_id
sq = """SELECT venue_id FROM event 
        GROUP BY event.venue_id HAVING COUNT(event.venue_id)>60"""

run_query(sq)


# ## JOIN - 2 points
#  
# Time for some joins.  You've probably noticed by now that there is at least one relational key in each table, but some have more.  For example, sales has a unique sale id, listing id, seller id, buyer id, date id.  This allows you to link each sale to relevant information in other tables.  
#  
# Please write queries to do the following items:
#  
# * Join information of users to each sale made.  
# * Join information about each venue to each event. 

# In[14]:


# Join user information to sales to each user
sq = """SELECT * FROM sales LEFT JOIN users 
ON sales.buyer_id = users.user_id"""

run_query(sq)


# In[15]:


# For each event attach the venue information
sq = """SELECT * FROM event LEFT JOIN venue 
        ON event.venue_id = venue.venue_id"""

run_query(sq)


# ## Subqueries - 2 points
# 
# To wrap up let's do several subqueries. Please do the following:
# 
# * Get all purchases made by users of live in Arizona
# * Get event information for all events that took place in a venue where the venue name ends with 'Stadium'. 
# * Get event information for all events where the total ticket sales were greater than $50,000.  

# In[280]:


# Get all purchases from users who live in Arizona
sq = """SELECT * FROM sales, venue WHERE venue.venue_state = 'AZ'"""
run_query(sq)


# In[ ]:


# Get event information for all events that took place in a venue where the name ended in 'Stadium'
sq = """SELECT * FROM venue WHERE venue_name LIKE '%Stadium'"""
run_query(sq)


# In[16]:


# Get event information where the total sales for that event were greater than 50000
sq = """SELECT event_id FROM sales GROUP BY sales.event_id 
        HAVING SUM(sales.price_paid*sales.qty_sold) > 50000""" 
run_query(sq)


# In[ ]:





# In[ ]:




