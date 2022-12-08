##########################################################
################## IMPORT FIPS  DATA #####################
##########################################################

# Source: https://www2.census.gov/geo/docs/reference/codes/files/national_county.txt

import pandas as pd

# Import txt file, add column names (based on https://www.census.gov/library/reference/code-lists/ansi.html),
# and set data type to string so that FIPS codes with 0 in the beginning are unchanged

fips = pd.read_csv(
    "C:/Users/fabi3/Documents/PythonExercises/opioid_project/source_data/FIPS_national_county.txt",
    names=["StateName", "FIPS_State", "FIPS_County", "CountyName", "FIPSClassCode"],
    dtype="string",
)

# Create 5-digit county FIPS code by adding state and county FIPS codes
fips["FIPS"] = fips["FIPS_State"] + fips["FIPS_County"]

# Only keep relevant columns
fips = fips[["FIPS", "CountyName", "StateName"]]

# Check if county name + state name combination is unique
assert not fips.duplicated(["CountyName", "StateName"]).any()


# Export to Parquet format
fips.to_parquet(
    "C:/Users/fabi3/Documents/PythonExercises/opioid_project/pds-2022-white-team/20_intermediate_files/fips.parquet",
    engine="fastparquet",
)
