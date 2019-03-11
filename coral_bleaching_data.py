
# coding: utf-8

# In[ ]:

'''This code will open a .csv file that contains the coral bleaching data.  The data format is: each row is a different report on 
a different location.  The columns are ID #, Region, Subregion, Country, Location, Lat, Lon, Month, Year, Depth, Severity_Code, and 
Bleaching_Severity.
The severity_code works as follows:
-1 = severity unknown
0 = no bleaching
1 = low bleaching
2 = medium bleaching
3 = high bleaching
We want to read the file line by line and for each line, add it to a dictionary of dictionaries.
The outer dictionary keys will be ID #, and dictionary for each region will contain dictionaries with keys of the other columns'''

'''Outputs from this data:
1. tally of each type of bleaching severity for each broad region
2. tally of each type of bleaching severity for subregions, do this for countries too?
3. bar plots or some type of plot showing bleaching severity by region
4. dictionary of severity of coral bleaching for each year
5. beginning of plot of coral bleaching severity versus year'''


# In[4]:

#had to change csv file encoding to utf-8 because when I converted the excel file to .csv, it could no longer be 
#read by ASCII - here's the page that told me how to convert: https://superuser.com/questions/151981/converting-the-encoding-of-a-text-file-mac-os-x

import csv
import matplotlib.pyplot as plt
import matplotlib.axes as axes
get_ipython().magic('matplotlib inline')

#Open the bleaching data .csv file and format the data in a dictionary with the outer key as the ID number and the inner keys the data for each line (i.e. region, year, bleaching severity)
bleaching_dict = {}
with open('CoralBleaching_utf8.csv', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)    
    for row in csv_reader:
        inner_dict = {}
        ID = row[0]
        inner_dict['region'] = row[1]
        inner_dict['subregion'] = row[2]
        inner_dict['country'] = row[3]
        inner_dict['location'] = row[4]
        inner_dict['lat'] = row[5]
        inner_dict['lon'] = row[6]
        inner_dict['month'] = row[7]
        inner_dict['year'] = row[8]
        inner_dict['depth'] = row[9]
        inner_dict['severity_code'] = row[10]
        inner_dict['bleaching_severity'] = row[11]
        bleaching_dict[ID] = inner_dict


def list_of_values(bleaching_dict, heading): 
    '''Creates a list of all possible values for a particular heading (i.e. regions, subregions)'''
    values_list = []
    for row in bleaching_dict:
        if bleaching_dict[row][heading] not in values_list:
            values_list.append(bleaching_dict[row][heading])  
    return values_list


regions_list = list_of_values(bleaching_dict, 'region')
subregions_list = list_of_values(bleaching_dict, 'subregion')



# In[8]:

print(regions_list)


# In[7]:

#Creating dictionaries with number of counts of each coral bleaching severity type
def bleaching_counts_dict(bleaching_dict, values_list):
    '''Creates 4 dictionaries, one for each of the bleaching severity options, with the strings in values_list as the keys for each of the lists '''
    no_bleaching_dict = {}
    low_bleaching_dict = {}
    mod_bleaching_dict = {}
    high_bleaching_dict = {}
    for value in values_list:
        no_count = 0
        low_count = 0
        mod_count = 0
        high_count = 0
        for row in bleaching_dict:
            if bleaching_dict[row][value] == value:
                code = bleaching_dict[row]['severity_code']
                if code == '0':
                    no_count += 1
                elif code == '1':
                    low_count += 1
                elif code == '2':
                    mod_count += 1
                elif code == '3':
                    high_count += 1
        no_bleaching_dict[value] = no_count
        low_bleaching_dict[value] = low_count
        mod_bleaching_dict[value] = mod_count
        high_bleaching_dict[value] = high_count
    return no_bleaching_dict, low_bleaching_dict, mod_bleaching_dict, high_bleaching_dict
         

regions_count_dict = bleaching_counts_dict(bleaching_dict, regions_list)
subsregions_count_dict = bleaching_counts_dict(bleaching_dict, subregions_list)


# In[ ]:

#plot the counts for each region and subregion as bar plots
#first make lists of just the values of low, mod, and high bleaching for each region that corresponds
#to the regions_list order
no_height = []
for region in regions_list:
    for key in no_bleaching_dict:
        if key == region:
            #print('True')
            no_height.append(no_bleaching_dict[key])

low_height = []
for region in regions_list:
    for key in low_bleaching_dict:
        if key == region:
            #print('True')
            low_height.append(low_bleaching_dict[key])


mod_height = []
for region in regions_list:
    for key in mod_bleaching_dict:
        if key == region:
            #print('True')
            mod_height.append(mod_bleaching_dict[key])

high_height = []
for region in regions_list:
    for key in high_bleaching_dict:
        if key == region:
            #print('True')
            high_height.append(high_bleaching_dict[key])

#bar plot of regions
x = list(range(1, len(regions_list) * 10 + 1, 10))
x_mod = list(range(2, len(regions_list) * 10 + 2, 10))
x_high = list(range(3, len(regions_list) * 10 + 3, 10))
x_no = list(range(4, len(regions_list) * 10 + 4, 10))
low = plt.bar(x, low_height, width = .8)
mod = plt.bar(x_mod, mod_height, width = .8)
high = plt.bar(x_high, high_height, width = .8)
none = plt.bar(x_no, no_height, width = .8)
plt.xticks(x, regions_list, fontsize = '5', fontstretch = '100')
plt.legend((low[0], mod[0], high[0], none[0]), ('low bleaching', 'mod bleaching', 'high bleaching', 'no bleaching') , fontsize = '10')
plt.ylabel('Number of bleaching events', fontsize = '10')
plt.show()


#bleaching events over time
bleaching_eachyear_dict = {}


#This could probably be a function
#change year to whatever other parameter you are interested in and you get a dictionary of dictionaries with that parameter
for region in regions_list:
    dict_of_years = {}
    for row in bleaching_dict:
        #print(bleaching_dict[row]['region'])
        
        if bleaching_dict[row]['region'] == region:
            code = bleaching_dict[row]['severity_code']
           
            year = bleaching_dict[row]['year']            
            if year in dict_of_years:
                if code == '0':
                    previous_value = dict_of_years[year].get('none', 0)
                    dict_of_years[year]['none'] = previous_value + 1                
                if code == '1': 
                    previous_value = dict_of_years[year].get('low', 0)
                    dict_of_years[year]['low'] = previous_value + 1                               
                if code == '2':
                    previous_value = dict_of_years[year].get('mod', 0)
                    dict_of_years[year]['mod'] = previous_value + 1                                
                if code == '3':
                    previous_value = dict_of_years[year].get('high',0)
                    dict_of_years[year]['high'] = previous_value + 1                
            else:
                if code == '0':    
                    dict_of_years[year] = {}
                    dict_of_years[year]['none'] = 1
                if code == '1':
                    dict_of_years[year] = {}
                    dict_of_years[year]['low'] = 1
                if code == '2':
                    dict_of_years[year] = {}
                    dict_of_years[year]['mod'] = 1
                if code == '3':
                    dict_of_years[year] = {}
                    dict_of_years[year]['high'] = 1
    bleaching_eachyear_dict[region] = dict_of_years
print(bleaching_eachyear_dict)


#plotting number of each type of severity over time for each region
year_am_list = []
low_am_list = []
mod_am_list = []
high_am_list = []
none_am_list = []
for year in bleaching_eachyear_dict['Americas']:
    year_am_list.append(year)
    low_am_list.append(bleaching_eachyear_dict['Americas'][year].get('low', 0))
    mod_am_list.append(bleaching_eachyear_dict['Americas'][year].get('mod', 0))
    high_am_list.append(bleaching_eachyear_dict['Americas'][year].get('high', 0))
    none_am_list.append(bleaching_eachyear_dict['Americas'][year].get('none', 0))
        
low = plt.plot(year_am_list, low_am_list, 'bo')
mod = plt.plot(year_am_list, mod_am_list, 'mo')
high = plt.plot(year_am_list, high_am_list, 'ro')
none = plt.plot(year_am_list, none_am_list, 'go')
plt.legend(('low bleaching', 'mod bleaching', 'high bleaching', 'no bleaching'))
plt.show()

