##########################################################
############ IMPORT DRUG MORTALITY DATA ##################
##########################################################

# Source: https://www.dropbox.com/s/kad4dwebr88l3ud/US_VitalStatistics.zip?dl=0

import pandas as pd

# Create empty data frame
vital_stat = pd.DataFrame([])

# Loop over each file and concatenate all raw data to one data frame
for year in range(2003, 2016):

    # Data downloaded from Dropbox folder provided by Nick
    url = (
        "C:/Users/fabi3/Documents/PythonExercises/opioid_project/source_data/drug_overdose_mortality_US_vital_statistic/Underlying Cause of Death, "
        + str(year)
        + ".txt"
    )
    vital_stat_year = pd.read_csv(url, delimiter="\t")
    vital_stat = pd.concat([vital_stat, vital_stat_year])


## Notes column just cointains info about data download

# Drop all observations which contain information in Notes column
vital_stat = vital_stat.loc[vital_stat["Notes"].isnull(), :]

# Drop notes column
vital_stat = vital_stat.drop("Notes", axis=1)

# Check cases which have missing data
vital_stat.loc[vital_stat["Deaths"] == "Missing", "County"].value_counts()

# The 5 counties with missing data are located in Alaska and Virgina, both states are not used in our analysis
# Thus, we drop these observation
vital_stat = vital_stat.loc[vital_stat["Deaths"] != "Missing", :]

# Convert to numeric data type
vital_stat["Deaths"] = vital_stat["Deaths"].astype("float64")


# Check which drug/alcohol induced causes exist
vital_stat["Drug/Alcohol Induced Cause"].value_counts()

drug_death_causes = [
    "Drug poisonings (overdose) Unintentional (X40-X44)",
    "Drug poisonings (overdose) Suicide (X60-X64)",
    "Drug poisonings (overdose) Undetermined (Y10-Y14)",
    "All other drug-induced causes",
    "Drug poisonings (overdose) Homicide (X85)",
]

# Keep only drug related death causes
vital_stat_drug = vital_stat.loc[
    vital_stat["Drug/Alcohol Induced Cause"].isin(drug_death_causes), :
]

# Keep only relevant columns
vital_stat_drug = vital_stat_drug.loc[:, ["County", "County Code", "Year", "Deaths"]]

# Group by county and year
grouped_vital_stat_drug = vital_stat_drug.groupby(
    ["County Code", "Year", "County"], as_index=False
).sum()

# Check if group by was successful by testing if are there any duplicates left?
assert not grouped_vital_stat_drug.duplicated(["County Code", "Year"]).any()

# Adjust FIPS codes so that they always have 5 digits (first convert to string, then add 0 in front if FIPS code only has 4 digits)
grouped_vital_stat_drug["County Code"] = (
    grouped_vital_stat_drug["County Code"].astype("int64").astype("string")
)
grouped_vital_stat_drug.loc[
    grouped_vital_stat_drug["County Code"].str.len() == 4, "County Code"
] = ("0" + grouped_vital_stat_drug["County Code"])

# Save as parquet file
grouped_vital_stat_drug.to_parquet(
    "C:/Users/fabi3/Documents/PythonExercises/opioid_project/pds-2022-white-team/20_intermediate_files/drug_overdosis_death.parquet",
    engine="fastparquet",
)
