# %%
import pandas as pd
import numpy as np
import difflib
from difflib import SequenceMatcher


# %% [markdown]
# ## merge ship data and population data

# %%
##########################################################
######### ADD FIPS CODE TO OPIOID DATA ###################
##########################################################


import numpy as np
import pandas as pd

# Import aggregated drug data set
# opioid_data = pd.read_csv(
#    "C:/Users/fabi3/Documents/PythonExercises/opioid_project/drug_data_woFIPS.csv"
# )

opioid_data = pd.read_parquet("/Users/a563186832/Documents/GitHub/pds-2022-white-team/20_intermediate_files/opioid_data_woFIPS.parquet", engine="fastparquet")

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
    opioid_data["BUYER_COUNTY"] = opioid_data["BUYER_COUNTY"].str.replace(
        key, value, regex=True
    )


# 3 cases must be solved manually
opioid_data.loc[
    (opioid_data["BUYER_COUNTY"] == "BRISTOL") & (opioid_data["BUYER_STATE"] == "VA"),
    "BUYER_COUNTY",
] = "BRISTOLCITY"
opioid_data.loc[
    (opioid_data["BUYER_COUNTY"] == "RADFORD") & (opioid_data["BUYER_STATE"] == "VA"),
    "BUYER_COUNTY",
] = "RADFORDCITY"
opioid_data.loc[
    (opioid_data["BUYER_COUNTY"] == "SALEM") & (opioid_data["BUYER_STATE"] == "VA"),
    "BUYER_COUNTY",
] = "SALEMCITY"
# Add missing FIPS code for 1 US territory and 1 freely associated state which are part of the opioid data ste
fips.loc[len(fips.index)] = [np.nan, "PALAU", "PW"]
fips.loc[len(fips.index)] = [np.nan, "NORTHERNMARIANA", "MP"]


# Merge FIPS data with opioid data
merge = pd.merge(
    opioid_data,
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
assert merge["_merge"].value_counts()[0] == len(opioid_data)


# %% [markdown]
# since the assert didn't break out, hence, we can conclude that our data is perfectly merged

# %%
# then we check whether our data covered all years
merge.year.unique()

# %% [markdown]
# From the output, we covered all needed data to analyze the Washington Policy

# %%
merge = merge.drop(columns=["CountyName", "StateName", "_merge"])
merge.head()

# %% [markdown]
# ## merge shipment data with fips

# %%
# 
df_pop = pd.read_parquet("/Users/a563186832/Documents/GitHub/pds-2022-white-team/20_intermediate_files/county_population.parquet", engine="fastparquet")
df_ship_pop = pd.merge(merge,df_pop,how="left",left_on=["FIPS","year"],right_on=["FIPS","year"],validate="m:1",indicator=True)

# %%
# Check whether some state has no FIPS code
df_ship_pop[df_ship_pop["_merge"]=="left_only"].BUYER_STATE.unique()

# %% [markdown]
# From the output, only PR is missing with FIPS. PR is Puerto Rico which is a  Caribbean island and unincorporated U.S. territory and is not influencial in our analysis. So, we can safely drop those missing observations

# %%
df_ship_pop = df_ship_pop.drop(columns=["_merge"])
df_ship_pop.to_csv("./ship_pop.csv",index=False)
df_ship_pop.to_parquet("./ship_pop.parquet",engine="fastparquet")

# %% [markdown]
# ## merge overdose death data with population data

# %%
# load death data
df_death= pd.read_parquet("/Users/a563186832/Documents/GitHub/pds-2022-white-team/20_intermediate_files/drug_overdosis_death.parquet", engine="fastparquet")
df_death.head()

# %%
# merge with fips data

df_death_pop = pd.merge(df_death,df_pop,how="left",left_on=["County Code","Year"],right_on=["FIPS","year"],validate="m:1",indicator=True)

# %%
df_death_pop[df_death_pop["_merge"]=="left_only"].County.unique()

# %% [markdown]
# From the output, we can see the counties which have no population data come from AK and VA. According to the instruction, we can safely ignore the Alaska area. Then we wento deal with the counties from VA

# %% [markdown]
# From Google, we found the FIPS for Bedford city, VA is 51515 and Clifton Forge city, VA is 51560

# %%
df_pop[(df_pop.FIPS==51515) | (df_pop.FIPS==51560)]

# %% [markdown]
# We found that the FIPS 51515 and 51560 are missing. Since we don't include the VA in our analysis (it is not a target nor in control group). Hence, we may safely drop it.

# %%
# drop left only
df_death_pop = df_death_pop.loc[df_death_pop._merge=="both",:]
# drop merge column
df_death_pop = df_death_pop.drop(columns=["_merge"])
# write into parquet
df_death_pop.to_parquet("./death_pop.parquet",engine="fastparquet")
# write into csv
df_death_pop.to_csv("./death_pop.csv",index=False)

# %%



