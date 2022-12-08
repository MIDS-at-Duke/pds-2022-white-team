##########################################################
############ IMPORT OPIOID DRUG DATA #####################
################# MONTHLY DATA ###########################
##########################################################

# Source: https://www.washingtonpost.com/national/2019/07/18/how-download-use-dea-pain-pills-database/?arc404=true

import pandas as pd

# Create list with variables which are required in the analysis to only import them
cols = [
    "BUYER_COUNTY",
    "BUYER_STATE",
    "TRANSACTION_DATE",
    "MME_Conversion_Factor",
    "CALC_BASE_WT_IN_GM",
]

# Unfortunately, all data types must be set to string in the beginning to avoid a warning
# This will be changed after the flawed rows which contain variable names are dropped
dtypes = {
    "BUYER_COUNTY": str,
    "BUYER_STATE": str,
    "TRANSACTION_DATE": str,
    "MME_Conversion_Factor": str,
    "CALC_BASE_WT_IN_GM": str,
}

# Use read_csv to chunk the huge file and only import required columns
opioid_data_chunk = pd.read_csv(
    "C:/Users/fabi3/Documents/PythonExercises/opioid_project/source_data/national_shipment_data.csv",
    chunksize=2_000_000,
    iterator=True,
    usecols=cols,
    dtype=dtypes,
)

# Create empty data frame to put chunks in it
opioid_data = pd.DataFrame([])

# Loop over different chunks, make some modifications, and decrease number of observations by aggregating observations on the county-year level
for chunk in opioid_data_chunk:

    # Extract month and year from transaction date
    chunk["month"] = chunk["TRANSACTION_DATE"].str[0:2]
    chunk["year"] = chunk["TRANSACTION_DATE"].str[-4:]

    # Probably caused by the manual concatenating to include data from 2013 - 2014, some rows have have string entries so that the option errors = "coerce" is requried
    # Convert columns to numeric data
    chunk["month"] = pd.to_numeric(chunk["month"], errors="coerce")

    chunk["year"] = pd.to_numeric(chunk["year"], errors="coerce")

    chunk["MME_Conversion_Factor"] = pd.to_numeric(
        chunk["MME_Conversion_Factor"], errors="coerce"
    )
    chunk["CALC_BASE_WT_IN_GM"] = pd.to_numeric(
        chunk["CALC_BASE_WT_IN_GM"], errors="coerce"
    )

    # Convert weights to common unit based on morphine equivalent
    chunk["opioid_converted_grams"] = (
        chunk["MME_Conversion_Factor"] * chunk["CALC_BASE_WT_IN_GM"]
    )

    # Subset to relevant variables
    chunk = chunk[
        ["year", "month", "BUYER_COUNTY", "BUYER_STATE", "opioid_converted_grams"]
    ]

    # Aggregate opioid data by year-month and county (+ corresponding state)
    chunk = chunk.groupby(
        ["year", "month", "BUYER_COUNTY", "BUYER_STATE"], as_index=False
    ).sum()

    # Concatenate with previous chunks
    opioid_data = pd.concat([opioid_data, chunk])


# Use group by again to group again by year-month and county (+ corresponding state) over the different chunks
opioid_data_final = opioid_data.groupby(
    ["year", "month", "BUYER_COUNTY", "BUYER_STATE"], as_index=False
).sum()


# Test if groupby was successful and that there is actually only one row per year-month-county (state) combination
assert not opioid_data_final.duplicated(
    ["year", "month", "BUYER_COUNTY", "BUYER_STATE"]
).any()

# Save intermediate dataset in paquet format
opioid_data_final.to_parquet(
    "C:/Users/fabi3/Documents/PythonExercises/opioid_project/pds-2022-white-team/20_intermediate_files/opioid_data_woFIPS_monthly.parquet",
    engine="fastparquet",
)
