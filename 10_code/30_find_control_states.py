import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# Goal of this file: Find control states by finding the states which have the most similiar trend before the policy change was implemented

#############################
###  Opioid shipment data ###
#############################

opioid = pd.read_parquet(
    "C:/Users/fabi3/Documents/PythonExercises/opioid_project/pds-2022-white-team/20_intermediate_files/ship_pop.parquet"
)
opioid["opioid_per_capita"] = opioid["opioid_converted_grams"] / opioid["population"]

# Drop Puerto Rico as no data available
opioid = opioid.loc[opioid["BUYER_STATE"] != "PR", :]
states = opioid["BUYER_STATE"].unique()


### Policy change Florida 2010

# Define year of policy implementation
opioid.loc[:, "policy_change_FL"] = opioid["year"] > 2010
opioid.loc[:, "years_from_policy_change_FL"] = opioid["year"] - 2010

# Calculate for each state the linear trend before the policy was implemented and store it in a dictionary
slopes_fl_opioid = {}
for i in states:
    opioid_subset = opioid.loc[
        (opioid["BUYER_STATE"] == i) & (opioid["years_from_policy_change_FL"] < 0), :
    ]
    model = smf.ols("opioid_per_capita ~ years_from_policy_change_FL", opioid_subset)
    fit = model.fit()
    slopes_fl_opioid[i] = fit.params[1]

# Convert dictionary to data frame
slopes_fl_opioid_df = (
    pd.DataFrame.from_dict(slopes_fl_opioid, orient="index", columns=["slope"])
    .reset_index()
    .sort_values(by="slope")
)

# Extract slope for Florida
fl_slope_opioid = slopes_fl_opioid_df.loc[
    slopes_fl_opioid_df["index"] == "FL", "slope"
].reset_index()["slope"][0]

# Calculate difference between Florida's slope and the slope of other states
slopes_fl_opioid_df["diff_fl"] = np.abs(slopes_fl_opioid_df["slope"] - fl_slope_opioid)

# Sort and store five most similiar states in list
slopes_fl_opioid_df = slopes_fl_opioid_df.sort_values(by="diff_fl")
comp_states_fl_opioid = list(slopes_fl_opioid_df["index"][1:6])


### Policy change Washington 2012
opioid.loc[:, "policy_change_WA"] = opioid["year"] > 2012
opioid.loc[:, "years_from_policy_change_WA"] = opioid["year"] - 2012

slopes_wa_opioid = {}
for i in states:
    opioid_subset = opioid.loc[
        (opioid["BUYER_STATE"] == i) & (opioid["years_from_policy_change_WA"] < 0), :
    ]
    model = smf.ols("opioid_per_capita ~ years_from_policy_change_WA", opioid_subset)
    fit = model.fit()
    slopes_wa_opioid[i] = fit.params[1]

slopes_wa_opioid_df = (
    pd.DataFrame.from_dict(slopes_wa_opioid, orient="index", columns=["slope"])
    .reset_index()
    .sort_values(by="slope")
)

wa_slope_opioid = slopes_wa_opioid_df.loc[
    slopes_wa_opioid_df["index"] == "WA", "slope"
].reset_index()["slope"][0]
slopes_wa_opioid_df["diff_wa"] = np.abs(slopes_wa_opioid_df["slope"] - wa_slope_opioid)
slopes_wa_opioid_df = slopes_wa_opioid_df.sort_values(by="diff_wa")
comp_states_wa_opioid = list(slopes_wa_opioid_df["index"][1:6])


### Policy change Texas 2007 (use monthly data)
opioid_monthly = pd.read_parquet(
    "C:/Users/fabi3/Documents/PythonExercises/opioid_project/ship_pop_monthly.parquet"
)
opioid_monthly["opioid_per_capita"] = (
    opioid_monthly["opioid_converted_grams"] / opioid_monthly["population"]
)

# Drop Puerto Rico as no data available
opioid_monthly = opioid_monthly.loc[opioid_monthly["BUYER_STATE"] != "PR", :]

opioid_monthly.loc[:, "months_from_policy_change_TX"] = (
    (opioid_monthly["year"] - 2007) * 12 + opioid_monthly["month"] - 1
)
opioid_monthly.loc[:, "policy_change_TX"] = (
    opioid_monthly["months_from_policy_change_TX"] > 0
)

slopes_tx_opioid = {}
for i in states:
    opioid_monthly_subset = opioid_monthly.loc[
        (opioid_monthly["BUYER_STATE"] == i)
        & (opioid_monthly["months_from_policy_change_TX"] < 0),
        :,
    ]
    model = smf.ols(
        "opioid_per_capita ~ months_from_policy_change_TX", opioid_monthly_subset
    )
    fit = model.fit()
    slopes_tx_opioid[i] = fit.params[1]

slopes_tx_opioid_df = (
    pd.DataFrame.from_dict(slopes_tx_opioid, orient="index", columns=["slope"])
    .reset_index()
    .sort_values(by="slope")
)

tx_slope_opioid = slopes_tx_opioid_df.loc[
    slopes_tx_opioid_df["index"] == "TX", "slope"
].reset_index()["slope"][0]
slopes_tx_opioid_df["diff_tx"] = np.abs(slopes_tx_opioid_df["slope"] - tx_slope_opioid)
slopes_tx_opioid_df = slopes_tx_opioid_df.sort_values(by="diff_tx")
comp_states_tx_opioid = list(slopes_tx_opioid_df["index"][1:6])

#############################
######  Mortality data ######
#############################

death = pd.read_parquet(
    "C:/Users/fabi3/Documents/PythonExercises/opioid_project/pds-2022-white-team/10_code/death_pop.parquet"
)

death["death_per_capita"] = death["Deaths"] / death["population"]
death["state"] = death["County"].str.split(", ").str[1]

### Policy change Florida 2010

death.loc[:, "policy_change_FL"] = death["year"] > 2010
death.loc[:, "years_from_policy_change_FL"] = death["year"] - 2010

# Get list of states to loop over which have at least one observation prior to policy change
state_count = (
    death.loc[death["years_from_policy_change_FL"] < 0, :]
    .groupby("state")
    .count()
    .reset_index()
)
states_fl_death = state_count.loc[state_count["Year"] > 1, "state"].unique()

slopes_fl_death = {}
for i in states_fl_death:
    death_subset = death.loc[
        (death["state"] == i) & (death["years_from_policy_change_FL"] < 0), :
    ]
    model = smf.ols("death_per_capita ~ years_from_policy_change_FL", death_subset)
    fit = model.fit()
    slopes_fl_death[i] = fit.params[1]

slopes_fl_death_df = (
    pd.DataFrame.from_dict(slopes_fl_death, orient="index", columns=["slope"])
    .reset_index()
    .sort_values(by="slope")
)

fl_slope_death = slopes_fl_death_df.loc[
    slopes_fl_death_df["index"] == "FL", "slope"
].reset_index()["slope"][0]
slopes_fl_death_df["diff_fl"] = np.abs(slopes_fl_death_df["slope"] - fl_slope_death)
slopes_fl_death_df = slopes_fl_death_df.sort_values(by="diff_fl")
comp_states_fl_death = list(slopes_fl_death_df["index"][1:6])


### Policy change Texas 2007

death.loc[:, "policy_change_TX"] = death["year"] > 2007
death.loc[:, "years_from_policy_change_TX"] = death["year"] - 2007

# Get list of states to loop over which have at least one observation prior to policy change
state_count = (
    death.loc[death["years_from_policy_change_TX"] < 0, :]
    .groupby("state")
    .count()
    .reset_index()
)
states_tx_death = state_count.loc[state_count["Year"] > 1, "state"].unique()


slopes_tx_death = {}
for i in states_tx_death:
    death_subset = death.loc[
        (death["state"] == i) & (death["years_from_policy_change_TX"] < 0), :
    ]
    model = smf.ols("death_per_capita ~ years_from_policy_change_TX", death_subset)
    fit = model.fit()
    slopes_tx_death[i] = fit.params[1]

slopes_tx_death_df = (
    pd.DataFrame.from_dict(slopes_tx_death, orient="index", columns=["slope"])
    .reset_index()
    .sort_values(by="slope")
)

tx_slope_death = slopes_tx_death_df.loc[
    slopes_tx_death_df["index"] == "TX", "slope"
].reset_index()["slope"][0]
slopes_tx_death_df["diff_tx"] = np.abs(slopes_tx_death_df["slope"] - tx_slope_death)
slopes_tx_death_df = slopes_tx_death_df.sort_values(by="diff_tx")
comp_states_tx_death = list(slopes_tx_death_df["index"][1:6])


### Policy change Washington 2012
death.loc[:, "policy_change_WA"] = death["year"] > 2012
death.loc[:, "years_from_policy_change_WA"] = death["year"] - 2012

# Get list of states to loop over which have at least one observation prior to policy change
state_count = (
    death.loc[death["years_from_policy_change_WA"] < 0, :]
    .groupby("state")
    .count()
    .reset_index()
)
states_wa_death = state_count.loc[state_count["Year"] > 1, "state"].unique()

slopes_wa_death = {}
for i in states_wa_death:
    death_subset = death.loc[
        (death["state"] == i) & (death["years_from_policy_change_WA"] < 0), :
    ]
    model = smf.ols("death_per_capita ~ years_from_policy_change_WA", death_subset)
    fit = model.fit()
    slopes_wa_death[i] = fit.params[1]

slopes_wa_death_df = (
    pd.DataFrame.from_dict(slopes_wa_death, orient="index", columns=["slope"])
    .reset_index()
    .sort_values(by="slope")
)

wa_slope_death = slopes_wa_death_df.loc[
    slopes_wa_death_df["index"] == "WA", "slope"
].reset_index()["slope"][0]
slopes_wa_death_df["diff_wa"] = np.abs(slopes_wa_death_df["slope"] - wa_slope_death)
slopes_wa_death_df = slopes_wa_death_df.sort_values(by="diff_wa")
comp_states_wa_death = list(slopes_wa_death_df["index"][1:6])
