import pandas as pd

# Load the saved CSV file
file_path = "./data/lopucki_data.csv"
df = pd.read_csv(file_path)

# Select only the required columns
columns_to_display = ["NameCorp", "Cusip6", "Cusip9"]  # Adjust if column names differ
df = df[columns_to_display]

# Set Pandas options to display all rows and columns without truncation
pd.set_option("display.max_rows", None)  # Show all rows
pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.width", 1000)  # Prevent line breaks
pd.set_option("display.colheader_justify", "left")  # Better alignment

# Display full DataFrame in terminal
print(df)
df.to_csv('data/lopucki_data_cusip.csv')