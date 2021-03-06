
# coding: utf-8

# ## test excel report export creator

# In[1]:

import pandas as pd
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell


# In[2]:

# read in test data
# TODO: replace with queryset from django
raw_df = pd.read_csv("test.csv")

raw_df


# In[3]:

# clean up data types
df = raw_df.copy()
df.punch_time_in = pd.to_datetime(df.punch_time_in)
df.punch_time_out = pd.to_datetime(df.punch_time_out)

print df.dtypes
df


# In[4]:

# create new columns
df['volunteer_name'] = df.last_name + ", " + df.first_name
df['month'] = df['punch_time_in'].dt.month
df['year'] = df['punch_time_in'].dt.year

df


# In[5]:

grouped = df.groupby(['year','month','volunteer_name'])
volunteer = grouped.agg({'punch_time_in' : 'count', 'session_time_hours' : 'sum'})
volunteer.columns = ['Volunteer Sessions', 'Total Hours']

volunteer


# In[6]:

volunteer_month = volunteer['Total Hours'].unstack(['year','month'])

volunteer_month


# In[7]:

grouped = df.groupby(['task_name'])
task = grouped.agg({'punch_time_in' : 'count', 'session_time_hours' : 'sum'})
task.columns = ['Volunteer Sessions', 'Total Hours']

task


# In[8]:

grouped = df.groupby(['year','month'])
month = grouped.agg({'punch_time_in' : 'count', 'session_time_hours' : 'sum'})
month.columns = ['Volunteer Sessions', 'Total Hours']

month


# In[9]:

grouped = df.groupby(['year','month','task_name'])
task_month = grouped.agg({'session_time_hours' : 'sum'})
task_month.columns = ['Total Hours']
task_month = task_month.unstack(['year','month'])

task_month


# In[10]:

grouped = df.groupby(['year','month','volunteer_name', 'task_name'])
volunteer_task = grouped.agg({'punch_time_in' : 'count', 'session_time_hours' : 'sum'})
volunteer_task.columns = ['Volunteer Sessions', 'Total Hours']
volunteer_task


# ### Excel Writer

# In[12]:

#####################
#### prints to excel
#####################

writer = pd.ExcelWriter("recoverycafe_volunteer_report.xlsx", engine='xlsxwriter')

# set title format
workbook  = writer.book
title = workbook.add_format()
title.set_font_size(20)
title.set_bold()


#
### summary sheet
#

sheet = 'SUMMARY'

# write tables
month.to_excel(writer, sheet_name=sheet, startrow=3)
task.to_excel(writer, sheet_name=sheet, startrow=3, startcol=5)
task_month.to_excel(writer, sheet_name=sheet, startrow=3, startcol=9)

# set width for columns
worksheet = writer.sheets[sheet]
worksheet.set_column("C:D",18)
worksheet.set_column("F:F",44)
worksheet.set_column("G:H",18)
worksheet.set_column("J:J",44)

# write titles
worksheet.write('A2', 'Totals by Month', title)
worksheet.write('F2', 'Totals by Task', title)
worksheet.write('J2', 'Hours by Task & Month', title)




#
### volunteer sheet
#

sheet = 'Volunteers'

# write tables
volunteer.to_excel(writer, sheet_name=sheet, startrow=3)
volunteer_task.to_excel(writer, sheet_name=sheet, startrow=3, startcol=6)

# set width for columns
worksheet = writer.sheets[sheet]
worksheet.set_column("C:C",44)
worksheet.set_column("D:E",18)
worksheet.set_column("K:L",18)
worksheet.set_column("I:J",44)

# write titles
worksheet.write('A2', 'Volunteers by Month', title)
worksheet.write('G2', 'Volunteers by Task & Month', title)



#
### volunteer by month sheet
#

sheet = 'Volunteers by Month'

# write table
volunteer_month.to_excel(writer, sheet_name=sheet, startrow=3)

# set width for columns
worksheet = writer.sheets[sheet]
worksheet.set_column("A:A",44)

# write titles
worksheet.write('A2', 'Volunteers by Month', title)



#
### raw table sheet
#

sheet = '-- raw data --'

# write table
raw_df.ix[:,1:].to_excel(writer, sheet_name=sheet)

# set width for columns
worksheet = writer.sheets[sheet]
worksheet.set_column("B:Z",22)



#
### write excel file
#

writer.save()

