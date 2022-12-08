##########################################################
############## IMPORT POPULATION DATA ####################
##########################################################

# Sources:
# - 2000-2009: https://www2.census.gov/programs-surveys/popest/datasets/2000-2009/counties/totals/
# - 2010-2019: https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/

import pandas as pd

pop_all = pd.DataFrame([])

# Loop over two files which are similarly formatted and contain data for one decade each
for n in [2009, 2019]:

    pop = pd.read_csv(
        "C:/Users/fabi3/Documents/PythonExercises/opioid_project/source_data/co-est"
        + str(n)
        + "-alldata.csv",
        encoding="ISO-8859-1",
    )

    # Only keep county population data
    pop = pop[pop["SUMLEV"] == 50]

    # Convert FIPS state code in common two-digit format
    pop["STATE"] = pop["STATE"].astype("string")
    pop.loc[pop["STATE"].str.len() == 1, "STATE"] = "0" + pop["STATE"]

    # Convert FIPS county code in common three-digit format
    pop["COUNTY"] = pop["COUNTY"].astype("string")
    pop.loc[pop["COUNTY"].str.len() == 1, "COUNTY"] = "00" + pop["COUNTY"]
    pop.loc[pop["COUNTY"].str.len() == 2, "COUNTY"] = "0" + pop["COUNTY"]

    # Generate five-digit FIPS code by appending county code to state code
    pop["FIPS"] = pop["STATE"] + pop["COUNTY"]
    assert not (pop["STATE"].str.len() == 5).any()

    # Only keep relevant variables and create list with value variables for reshape
    vars = ["FIPS"]
    value_vars = []
    for i in range(n - 9, n + 1):
        value_vars.append("POPESTIMATE" + str(i))
        vars.append("POPESTIMATE" + str(i))
    pop = pop[vars]

    # Reshape from wide to long
    pop_long = pd.melt(
        pop,
        id_vars="FIPS",
        value_vars=value_vars,
        var_name="year",
        value_name="population",
    )

    # Correctly format year variable
    pop_long["year"] = pop_long["year"].str[-4:].astype("int64")

    pop_all = pd.concat([pop_all, pop_long])


# Check if reshaping and concatenating  was successful by testing if are there any duplicates left
assert not pop_all.duplicated(["FIPS", "year"]).any()


# Export to Parquet format
pop_all.to_parquet(
    "C:/Users/fabi3/Documents/PythonExercises/opioid_project/pds-2022-white-team/20_intermediate_files/county_population.parquet",
    engine="fastparquet",
)
