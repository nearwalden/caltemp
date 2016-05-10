# Routines to create, analyze and plot different calendard models of temperature

import math
# we'll want pandas to structure the datasets
import pandas as p
# use numpy to do vector work
import numpy as np

# plotting routines
# import mapplotlib as plt

# months in order
months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
          'september', 'october', 'november', 'december']

# months and how many days in them (except feb)
# be careful with this, no guarantee of order
days_month = {'january': 31,
              'february': 28,
              'march': 31,
              'april': 30,
              'may': 31,
              'june': 30,
              'july': 31,
              'august': 31,
              'september': 30,
              'october': 31,
              'november': 30,
              'december': 31
              }

minutes_day = 1440
minutes_solar_year = 525969

# returns true if year is a leap-year
def is_leap_year (year):
    if (year % 4) != 0:
        return False
    elif (year % 400) == 0:
        return True
    elif (year % 100) == 0:
        return False
    else:
        return True

# returns the number of days in a month for a given year
def days_in_month (mo, year):
    # if not feb, just lookup the result above
    if mo != 'february':
        return days_month[mo]
    # if leap year, return 29
    elif is_leap_year(year):
        return days_month['february'] + 1;
    else:
        return days_month['february']

# returns an array of minutes_solar_year with a temp per minute
# value is a sinusouid around mean_temp

century_temp = {"year": 1950,
                "january": 12.0,
                "february": 12.1,
                "march": 12.7,
                "april": 13.7,
                "may": 14.8,
                "june": 15.5,
                "july": 15.8,
                "august": 15.6,
                "september": 15.0,
                "october": 14.0,
                "november": 12.9,
                "december": 12.2}

century_max_temp = 15.8
century_min_temp = 12.0
century_simple_mean_temp = (century_max_temp + century_min_temp)/2
# 3 months, 15 days offset to put bottom in middle of january
offset_minutes = 153092

def temp_array():
    res = []
    for i in range(0, minutes_solar_year):
        res.append(century_simple_mean_temp + (century_max_temp - century_simple_mean_temp) * math.sin(2 * math.pi * (i - offset_minutes)/minutes_solar_year))
    return res

# given a dictionary of year data including the year, calculates the mean for the year
def year_mean(year_data):
    year = year_data['year']
    total_days = 0
    total_temp = 0
    for month in months:
        data = year_data[month]
        days = days_in_month(month, year)
        # multiply average temp by days, add to total
        total_temp = total_temp + data * days
        # sum up days
        total_days = total_days + days
    return total_temp/total_days


# print out a non-leap year (1999) starting at beginning of temp_array
def print_temp_array():
    # make an np.array from temp_array()
    temp = np.array(temp_array())
    # keeping track of where we are
    start_minute = 0
    # year to use (1999)
    year = 1999
    # iterate through teh months
    for month in months:
        days = days_in_month(month, year)
        minutes = minutes_day * days
        mean_temp = temp[start_minute:start_minute + minutes].mean()
        print month + ":  " + str(mean_temp)
        start_minute = start_minute + minutes
    print "\nMean for year:  " + str(temp[0:start_minute].mean())
    # need to fix this, not really right
    print "20th Century mean: " + str(year_mean(1950, century_temp))


def model (start_year, years):
    temp = np.array(temp_array())
    start_minute = 0
    res = []
    for year in range(start_year, start_year + years):
        year_res = {"year": year}
        for month in months:
            days = days_in_month(month, year)
            minutes = minutes_day * days
            # check if cross solar year
            if start_minute + minutes < minutes_solar_year:
                # within solar year
                mean_temp = temp[start_minute:start_minute + minutes].mean()
                start_minute = start_minute + minutes
            else:
                # crosses solar years
                # compute minutes in this year v. next
                this_year = minutes_solar_year - start_minute
                next_year = minutes - this_year
                # connect the pieces and take the mean
                mean_temp = np.append(temp[start_minute:minutes_solar_year], temp[0: next_year]).mean()
                start_minute = next_year
            # save the vaule for the month
            year_res[month] = mean_temp
        year_res['year_avg'] = year_mean(year_res)
        # add the year record to the result array
        res.append(year_res)
    df = p.DataFrame(res)
    df.to_csv('model_' + str(start_year) + "_" + str(years) + ".csv")
    print "complete"













