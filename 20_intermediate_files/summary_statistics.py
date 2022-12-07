import pandas as pd
import numpy as np

# Define state where policy was implemented and corresponding control states
states_FL_death = ["FL", "NC", "TN", "IA"]
states_FL_opioid = ["FL", "TN", "WV", "NV"]
states_TX_death = ["TX", "WV", "OR", "ID"]
states_TX_opioid = ["TX", "MS", "MT", "CT"]
states_WA_death = ["WA", "KS", "NJ", "OR"]
states_WA_opioid = ["WA", "IL", "WI", "RI"]


### Overdose deaths

death = pd.read_parquet(
    "C:/Users/fabi3/Documents/PythonExercises/opioid_project/pds-2022-white-team/20_intermediate_files/death_pop.parquet"
)
death["death_per_capita"] = (death["Deaths"] / death["population"]) * 100000
death["state"] = death["County"].str.split(", ").str[1]
death.head()

df_FL = death[death["state"].isin(states_FL_death)]
df_TX = death[death["state"].isin(states_TX_death)]
df_WA = death[death["state"].isin(states_WA_death)]


df_FL_pre = df_FL[df_FL["Year"] < 2010]
df_FL_post = df_FL[df_FL["Year"] >= 2010]

df_TX_pre = df_TX[df_TX["Year"] < 2007]
df_TX_post = df_TX[df_TX["Year"] >= 2007]

df_WA_pre = df_WA[df_WA["Year"] < 2011]
df_WA_post = df_WA[df_WA["Year"] >= 2011]

# Florida and control groups
pre_FL = df_FL_pre.loc[df_FL_pre["state"] == "FL"]["death_per_capita"].describe()
pre_FL_x = df_FL_pre.loc[df_FL_pre["state"] != "FL"]["death_per_capita"].describe()
post_FL = df_FL_post.loc[df_FL_post["state"] == "FL"]["death_per_capita"].describe()
post_FL_x = df_FL_post.loc[df_FL_post["state"] != "FL"]["death_per_capita"].describe()


# Texas and control groups
pre_TX = df_TX_pre.loc[df_TX_pre["state"] == "TX"]["death_per_capita"].describe()
pre_TX_x = df_TX_pre.loc[df_TX_pre["state"] != "TX"]["death_per_capita"].describe()
post_TX = df_TX_post.loc[df_TX_post["state"] == "TX"]["death_per_capita"].describe()
post_TX_x = df_TX_post.loc[df_TX_post["state"] != "TX"]["death_per_capita"].describe()


# Washington and control groups
pre_WA = df_WA_pre.loc[df_WA_pre["state"] == "WA"]["death_per_capita"].describe()
pre_WA_x = df_WA_pre.loc[df_WA_pre["state"] != "WA"]["death_per_capita"].describe()
post_WA = df_WA_post.loc[df_WA_post["state"] == "WA"]["death_per_capita"].describe()
post_WA_x = df_WA_post.loc[df_WA_post["state"] != "WA"]["death_per_capita"].describe()


death_summary_stat_dict = {
    "State": [
        "Florida",
        "Florida",
        "Control group (NC, TN, IA)",
        "Control group (NC, TN, IA)",
        "Texas",
        "Texas",
        "Control group (WV, OR, ID)",
        "Control group (WV, OR, ID)",
        "Washington",
        "Washington",
        "Control group (KS, NJ, OR)",
        "Control group (KS, NJ, OR)",
    ],
    "Year of Policy Implementation": [
        2010,
        2010,
        2010,
        2010,
        2007,
        2007,
        2007,
        2007,
        2012,
        2012,
        2012,
        2012,
    ],
    "Statistics": [
        "Before",
        "After",
        "Before",
        "After",
        "Before",
        "After",
        "Before",
        "After",
        "Before",
        "After",
        "Before",
        "After",
    ],
    "Mean": [
        pre_FL["mean"],
        post_FL["mean"],
        pre_FL_x["mean"],
        post_FL_x["mean"],
        pre_TX["mean"],
        post_TX["mean"],
        pre_TX_x["mean"],
        post_TX_x["mean"],
        pre_WA["mean"],
        post_WA["mean"],
        pre_WA_x["mean"],
        post_WA_x["mean"],
    ],
    "Std. Dev.": [
        pre_FL["std"],
        post_FL["std"],
        pre_FL_x["std"],
        post_FL_x["std"],
        pre_TX["std"],
        post_TX["std"],
        pre_TX_x["std"],
        post_TX_x["std"],
        pre_WA["std"],
        post_WA["std"],
        pre_WA_x["std"],
        post_WA_x["std"],
    ],
    "Min.": [
        pre_FL["min"],
        post_FL["min"],
        pre_FL_x["min"],
        post_FL_x["min"],
        pre_TX["min"],
        post_TX["min"],
        pre_TX_x["min"],
        post_TX_x["min"],
        pre_WA["min"],
        post_WA["min"],
        pre_WA_x["min"],
        post_WA_x["min"],
    ],
    "Max.": [
        pre_FL["max"],
        post_FL["max"],
        pre_FL_x["max"],
        post_FL_x["max"],
        pre_TX["max"],
        post_TX["max"],
        pre_TX_x["max"],
        post_TX_x["max"],
        pre_WA["max"],
        post_WA["max"],
        pre_WA_x["max"],
        post_WA_x["max"],
    ],
}

death_summary_stat_df = pd.DataFrame(death_summary_stat_dict)

s = death_summary_stat_df.style
s.format(precision=2)
s.to_latex()


### Opioid shipment

opioid = pd.read_parquet(
    "C:/Users/fabi3/Documents/PythonExercises/opioid_project/pds-2022-white-team/20_intermediate_files/ship_pop.parquet"
)
opioid["opioid_per_capita"] = opioid["opioid_converted_grams"] / opioid["population"]


df_FL = opioid[opioid["BUYER_STATE"].isin(states_FL_opioid)]
df_TX = opioid[opioid["BUYER_STATE"].isin(states_TX_opioid)]
df_WA = opioid[opioid["BUYER_STATE"].isin(states_WA_opioid)]

df_FL_pre = df_FL[df_FL["year"] < 2010]
df_FL_post = df_FL[df_FL["year"] >= 2010]

df_TX_pre = df_TX[df_TX["year"] < 2007]
df_TX_post = df_TX[df_TX["year"] >= 2007]

df_WA_pre = df_WA[df_WA["year"] < 2011]
df_WA_post = df_WA[df_WA["year"] >= 2011]

# Florida and control groups
pre_FL = df_FL_pre.loc[df_FL_pre["BUYER_STATE"] == "FL"]["opioid_per_capita"].describe()
pre_FL_x = df_FL_pre.loc[df_FL_pre["BUYER_STATE"] != "FL"][
    "opioid_per_capita"
].describe()
post_FL = df_FL_post.loc[df_FL_post["BUYER_STATE"] == "FL"][
    "opioid_per_capita"
].describe()
post_FL_x = df_FL_post.loc[df_FL_post["BUYER_STATE"] != "FL"][
    "opioid_per_capita"
].describe()

# Washington and control groups
pre_WA = df_WA_pre.loc[df_WA_pre["BUYER_STATE"] == "WA"]["opioid_per_capita"].describe()
pre_WA_x = df_WA_pre.loc[df_WA_pre["BUYER_STATE"] != "WA"][
    "opioid_per_capita"
].describe()
post_WA = df_WA_post.loc[df_WA_post["BUYER_STATE"] == "WA"][
    "opioid_per_capita"
].describe()
post_WA_x = df_WA_post.loc[df_WA_post["BUYER_STATE"] != "WA"][
    "opioid_per_capita"
].describe()

opioid_summary_stat_dict = {
    "State": [
        "Florida",
        "Florida",
        "Control group (TN, WV, NV)",
        "Control group (TN, WV, NV)",
        "Washington",
        "Washington",
        "Control group (IL, WI, RI)",
        "Control group (IL, WI, RI)",
    ],
    "Year of Policy Implementation": [2010, 2010, 2010, 2010, 2012, 2012, 2012, 2012],
    "Statistics": [
        "Before",
        "After",
        "Before",
        "After",
        "Before",
        "After",
        "Before",
        "After",
    ],
    "Mean": [
        pre_FL["mean"],
        post_FL["mean"],
        pre_FL_x["mean"],
        post_FL_x["mean"],
        pre_WA["mean"],
        post_WA["mean"],
        pre_WA_x["mean"],
        post_WA_x["mean"],
    ],
    "Std. Dev.": [
        pre_FL["std"],
        post_FL["std"],
        pre_FL_x["std"],
        post_FL_x["std"],
        pre_WA["std"],
        post_WA["std"],
        pre_WA_x["std"],
        post_WA_x["std"],
    ],
    "Min.": [
        pre_FL["min"],
        post_FL["min"],
        pre_FL_x["min"],
        post_FL_x["min"],
        pre_WA["min"],
        post_WA["min"],
        pre_WA_x["min"],
        post_WA_x["min"],
    ],
    "Max.": [
        pre_FL["max"],
        post_FL["max"],
        pre_FL_x["max"],
        post_FL_x["max"],
        pre_WA["max"],
        post_WA["max"],
        pre_WA_x["max"],
        post_WA_x["max"],
    ],
}

opioid_summary_stat_df = pd.DataFrame(opioid_summary_stat_dict)

s = opioid_summary_stat_df.style
s.format(precision=2)
s.to_latex()
