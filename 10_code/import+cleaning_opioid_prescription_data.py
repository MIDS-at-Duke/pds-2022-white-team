##########################################################
############ IMPORT OPIOID DRUG DATA #####################
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

# Use read_csv with appropriate separator to chunk the huge file and only import required columns
opioid_data_chunk = pd.read_csv(
    "C:/Users/fabi3/Documents/PythonExercises/opioid_project/source_data/arcos_all_washpost.tsv",
    chunksize=2_000_000,
    iterator=True,
    usecols=cols,
    sep="\t",
)

# Create empty data frame to put chunks in it
opioid_data = pd.DataFrame([])

# Loop over different chunks, make some modifications, and decrease number of observations by aggregating observations on the county-year level
for chunk in opioid_data_chunk:

    # Extract year from TRANSACTION_DATE column (year is stored in the last 4 digits)
    chunk["year"] = chunk["TRANSACTION_DATE"] % 10_000

    # Convert weights to common unit based on morphine equivalent
    chunk["opioid_converted_grams"] = (
        chunk["MME_Conversion_Factor"] * chunk["CALC_BASE_WT_IN_GM"]
    )

    # Subset to relevant variables
    chunk = chunk[["year", "BUYER_COUNTY", "BUYER_STATE", "opioid_converted_grams"]]

    # Aggregate opioid data by year and county (+ corresponding state)
    chunk = chunk.groupby(["year", "BUYER_COUNTY", "BUYER_STATE"], as_index=False).sum()

    # Concatenate with previous chunks
    opioid_data = pd.concat([opioid_data, chunk])


# Use group by again to group again by year and county (+ corresponding state) over the different chunks
opioid_data_final = opioid_data.groupby(
    ["year", "BUYER_COUNTY", "BUYER_STATE"], as_index=False
).sum()


# Test if groupby was successful and that there is actually only one row per year-county (state) combination
assert not opioid_data_final.duplicated(["year", "BUYER_COUNTY", "BUYER_STATE"]).any()

# Save intermediate dataset in paquet format
opioid_data.to_parquet(
    "C:/Users/fabi3/Documents/PythonExercises/opioid_project/pds-2022-white-team/20_intermediate_files/opioid_data_woFIPS.parquet",
    engine="fastparquet",
)
