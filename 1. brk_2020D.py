import pandas as pd
import numpy as np

# 1. Read data
brk_data = pd.read_csv('data/brk_20D.csv')

# Convert to DataFrame
dt = pd.DataFrame(brk_data)
dt.loc[0:4]

# 2. Rename columns to lowercase
dt.columns = dt.columns.str.lower()  # Change column names to lowercase
dt.rename(columns={'value (x$1000)': 'value'}, inplace=True)

# 3. Select relevant columns
dt = dt[['security', 'ticker', 'shares', 'value']]

# 4. Display first few rows for verification
print(dt.loc[0:4])  # Display first 5 rows

# 5. Check for missing values
print(dt.isna().sum())

# Replace 'Nan' with np.nan and check for missing values again
dt.replace('Nan', np.nan, inplace=True)
print(dt.isna().sum())
print(dt[dt['ticker'].isna()])  # Display rows with missing Ticker values

# 6. Convert data types for 'shares' and 'value'
dt['shares'] = dt['shares'].str.replace(',', '').astype(float)
dt['value'] = dt['value'].str.replace(',', '').str.replace('$', '', regex=False).astype(float)
print(dt.dtypes)

# 7. Remove duplicates based on 'ticker'
dt = dt[~dt['ticker'].duplicated()]
print(dt)

# 8. Calculate additional columns: price and portfolio percentage
dt['price'] = (dt['value'] * 1000) / dt['shares']
dt['port'] = (dt['value'] / dt['value'].sum()) * 100

# Round the calculated values
dt['price'] = dt['price'].round(1)
dt['port'] = dt['port'].round(1)

# 9. Sort data by portfolio percentage
dt = dt.sort_values(by='port', ascending=False)

# 10. Print relevant columns and rows
print(dt[['security', 'port']].head(5))  # Print top 5 securities by portfolio percentage
print(dt.loc[0:4, 'security':'port'])  # Print more detailed information about top 5

# 11. Save the cleaned dataset
dt.to_csv('clean_data/new_brk_21D.csv', index=False)

# 12. Read the newly created file (optional verification step)
new_data = pd.read_csv('clean_data/new_brk_21D.csv')
print(new_data.head())  # Display top rows of the newly created dataset
