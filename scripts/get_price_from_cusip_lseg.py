import os
from dotenv import load_dotenv
import refinitiv.dataplatform as rd

load_dotenv()
api_key = os.getenv("APP_KEY")
rdp_login = os.getenv("RDP_LOGIN")
rdp_password = os.getenv("RDP_PASSWORD")
# Load CSV File
# rd.open_session()  # For LSEG Workspace users
session = rd.open_platform_session(
    api_key,
rd.GrantPassword(username = rdp_login, password = rdp_password)
)

# Example CUSIP-9 (Apple Inc.)
# cusip = "037833100"
# cusip = '31986N102'
# cusip = '770706109'
# cusip = '90131G107'
# cusip = '003687209'
# cusip = '004308102'
# cusip = '000973107'
# cusip = '006847107'
# cusip = '31865x106'
# cusip = '006855100'
cusip = '004308102'

isin_lookup = rd.get_data(
        fields=["TR.ISINCode"],  # Specify the field you want
        universe=[cusip]  # Ensure 'universe' is a list containing CUSIP
    )

# Extract ISIN
isin = isin_lookup.iloc[0, 1]  # Get ISIN value
print(f"ISIN for CUSIP {cusip}: {isin}")

# Define date range
start_date = "1950-01-01"
end_date = "2024-10-01"

# Fetch historical stock price data

name_data = rd.get_data(fields=["TR.CompanyName"], universe=[isin])
print(name_data)
historical_data = rd.get_data(
            fields=["TR.PriceCloseDate", "TR.PriceClose", "TR.PriceOpen", "TR.PriceHigh", "TR.PriceLow", "TR.Volume"],
            universe=[isin],  # Universe should be a list with ISIN
            parameters={"SDate": start_date, "EDate": end_date}  # Parameters with date range
        )
historical_data = historical_data.drop_duplicates(subset="TR.PriceCloseDate", keep="first").dropna() #???
print(historical_data)

rd.close_session()
