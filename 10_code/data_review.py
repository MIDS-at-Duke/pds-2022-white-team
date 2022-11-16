import pandas as pd

# Review county population data set
df_cp = pd.read_parquet("/county_population.parquet")
df_cp.head()

# Review FIPS code (the key to merge)
df_fips = pd.read_parquet("./fips.parquet")
df_fips["CountyName"] = df_fips["CountyName"].str.replace(" County", "")
df_fips["CountyName"] = df_fips["CountyName"].str.lower()
df_fips

# Review opioid data
df_od = pd.read_parquet("./opioid_data_woFIPS.parquet")
df_od.head()

# Review drug overdosis death data
df_dod = pd.read_parquet("./drug_overdosis_death.parquet")
df_dod.rename(columns={"County Code": "FIPS", "Year": "year"}, inplace=True)
df_dod["year"] = df_dod["year"].astype(int)
df_dod.head()

# From the ouput, we can see use County code as key to merge.
# The opioid data has no county fips data, hence the first step is to merge od data with fips dataset.


# Generate County code for opioid data

# generate key for od data
df_od["county_key"] = df_od["BUYER_COUNTY"].str.lower() + ", " + df_od["BUYER_STATE"]
df_fips["county_key"] = df_fips["CountyName"] + ", " + df_fips["StateName"]
# generate key for fips data
df_od_fips = pd.merge(
    df_fips, df_od, left_on="county_key", right_on="county_key", how="right"
)
# filter columns
df_od_fips = df_od_fips[
    ["FIPS", "year", "CountyName", "StateName", "opioid_converted_grams"]
]
# show the results
df_od_fips.head()


# Merge with County Population data by FIPS and year
df_od_fips_pop = pd.merge(df_od_fips, df_cp, on=["FIPS", "year"], how="left")
df_od_fips_pop.head()


# Merge with overdose death data with FIPS and year
master = pd.merge(df_od_fips_pop, df_dod, on=["FIPS", "year"], how="left")
master.head()


# drop Nan and manage column names
master = master.dropna()
master = master[
    ["FIPS", "year", "County", "opioid_converted_grams", "population", "Deaths"]
]
master.head()

# store values in parquet file and csv file
master.to_parquet("./master.parquet")
master.to_csv("./master.csv")

master.year.unique()
