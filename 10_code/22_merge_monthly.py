# Merge monthly opioid shipment data with population data
import pandas as pd
import numpy as np
import os

# Set working directory as location of current file to use relative paths further on
dir = os.path.dirname(os.path.abspath(__file__))

### Step 1: Add FIPS code to opioid data
opioid_data_monthly = pd.read_parquet(
    os.path.join(dir, "../20_intermediate_files/opioid_data_woFIPS_monthly.parquet")
)

# Import FIPS data from US census
url_fips = "https://www2.census.gov/geo/docs/reference/codes/files/national_county.txt"
fips = pd.read_csv(
    url_fips,
    names=["StateName", "FIPS_State", "FIPS_County", "CountyName", "E"],
    dtype="string",
)

# Create 5-digit county FIPS code by adding state and county FIPS codes
fips["FIPS"] = fips["FIPS_State"] + fips["FIPS_County"]

# Only keep relevant columns
fips = fips[["FIPS", "CountyName", "StateName"]]

# Harmonize county names in both data sets so that merging works properly
fips["CountyName"] = fips["CountyName"].str.upper()

char_to_replace_fips = {
    ".": "",
    " MUNICIPIO": "",
    "-": "",
    "'": "",
    " COUNTY": "",
    " PARISH": "",
    " CITY AND BOROUGH": "",
    " BOROUGH": "",
    " CENSUS AREA": "",
    " MUNICIPALITY": "",
    " ISLANDS": "",
    " ISLAND": "",
    " ": "",
}

char_to_replace_opioid = {
    "SAINT ": "ST ",
    "SAINTE ": "STE ",
    "-": "",
    " ISLANDS": "",
    " ISLAND": "",
    " ": "",
}

for key, value in char_to_replace_fips.items():
    fips["CountyName"] = fips["CountyName"].str.replace(key, value, regex=True)

for key, value in char_to_replace_opioid.items():
    opioid_data_monthly["BUYER_COUNTY"] = opioid_data_monthly[
        "BUYER_COUNTY"
    ].str.replace(key, value, regex=True)


# 3 cases must be solved manually
opioid_data_monthly.loc[
    (opioid_data_monthly["BUYER_COUNTY"] == "BRISTOL")
    & (opioid_data_monthly["BUYER_STATE"] == "VA"),
    "BUYER_COUNTY",
] = "BRISTOLCITY"
opioid_data_monthly.loc[
    (opioid_data_monthly["BUYER_COUNTY"] == "RADFORD")
    & (opioid_data_monthly["BUYER_STATE"] == "VA"),
    "BUYER_COUNTY",
] = "RADFORDCITY"
opioid_data_monthly.loc[
    (opioid_data_monthly["BUYER_COUNTY"] == "SALEM")
    & (opioid_data_monthly["BUYER_STATE"] == "VA"),
    "BUYER_COUNTY",
] = "SALEMCITY"
# Add missing FIPS code for 1 US territory and 1 freely associated state which are part of the opioid data ste
fips.loc[len(fips.index)] = [np.nan, "PALAU", "PW"]
fips.loc[len(fips.index)] = [np.nan, "NORTHERNMARIANA", "MP"]


# Merge FIPS data with opioid data
merge = pd.merge(
    opioid_data_monthly,
    fips,
    how="left",
    left_on=["BUYER_COUNTY", "BUYER_STATE"],
    right_on=["CountyName", "StateName"],
    validate="m:1",
    indicator=True,
)

# Check if merge was successful for all county
merge["_merge"].value_counts()

# Run test to check if merge was succesful
assert merge["_merge"].value_counts()[0] == len(opioid_data_monthly)

merge = merge.drop(columns="_merge")

# Step 2: merge with population data
df_pop = pd.read_parquet(
    os.path.join(dir, "../20_intermediate_files/county_population.parquet")
)
df_ship_pop_monthly = pd.merge(
    merge,
    df_pop,
    how="left",
    left_on=["FIPS", "year"],
    right_on=["FIPS", "year"],
    validate="m:1",
    indicator=True,
)
df_ship_pop_monthly["_merge"].value_counts()

# Check whether some state has no FIPS code (it is only Puerto Rico -> no problem)
df_ship_pop_monthly[df_ship_pop_monthly["_merge"] == "left_only"].BUYER_STATE.unique()

# Drop merge columns
df_ship_pop_monthly = df_ship_pop_monthly.drop(columns=["_merge"])

# Save file
df_ship_pop_monthly.to_parquet(
    os.path.join(dir, "../20_intermediate_files/ship_pop_monthly.parquet")
)
