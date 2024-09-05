import chardet
import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats

# Constants:
FILEPATH = 'RNAMonitoring_Public - Result Description - N1 Gene, Reported Value - N1 Gene (gc-l), Days Since.csv'

# Determine the encoding of the input file:
with open(FILEPATH, 'rb') as data:
    chardet_result = chardet.detect(data.read())

# Read the data:
df = pd.read_csv(FILEPATH, encoding=chardet_result['encoding'], sep='\t')

# Column names:
HEALTH_AREA = 'Health Area'
SITE_NAME = 'Site Name'
POPULATION = 'Population'
DATE = 'Date'
VALUE = 'Reported Value - N1 Gene (gc/l)'
VALUE_PER_1000 = 'Reported Value - N1 Gene per 1000 People (gc/l)'

# Column values:
SITE_NAMES = df[SITE_NAME].unique()
HEALTH_AREA_GGC = 'Greater Glasgow and Clyde'

# Outliers - number of standard deviations:
OUTLIER_STD_DEV = 3

# Check that each sample was taken on a different date:
for site_name in SITE_NAMES:
    assert df[df[SITE_NAME] == site_name][DATE].is_unique

# Remove outliers:
df = df[np.abs(stats.zscore(df[VALUE])) < OUTLIER_STD_DEV]

# Convert the date:
def parse_datetime(date):
    if not isinstance(date, datetime.datetime):
        month, day, year = map(int, date.split("/"))
        return datetime.datetime(year, month, day)
    else:
        return date
    
# Convert the population:
def parse_population(population):
    try:
        return float(population)
    except ValueError:
        return None

# Create a datetime index:
df[DATE] = pd.DatetimeIndex(df[DATE].map(parse_datetime))

# Add value per person:
df[VALUE_PER_1000] = df[VALUE] / (df[POPULATION].map(parse_population) / 1000)

series = df.groupby(SITE_NAME).apply(lambda df_sn: df_sn.set_index(DATE)[VALUE_PER_1000].plot())
series.plot()
