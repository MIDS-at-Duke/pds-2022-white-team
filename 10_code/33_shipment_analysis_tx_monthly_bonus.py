# Bonus Part
import pandas as pd
import numpy as np
from plotnine import *
from warnings import filterwarnings
import os

# Set working directory as location of current file to use relative paths further on
dir = os.path.dirname(os.path.abspath(__file__))

ignore = filterwarnings("ignore")

# Import data
df = pd.read_parquet(
    os.path.join(dir, "../20_intermediate_files/ship_pop_monthly.parquet")
)
df.head()
df_month = df[df["BUYER_STATE"].isin(["TX", "MS", "MT", "CT"])].loc[
    :, ["year", "month", "BUYER_COUNTY", "BUYER_STATE", "population"]
]

# calculate the opioid per capita - we don't have the data for monthly population, so we just use the yearly one
df_month["opioid_per_capita"] = df["opioid_converted_grams"] / df["population"]
df_month.head()
df_month.loc[:, "Months from Policy Change"] = (
    (df_month["year"] - 2007) * 12 + df_month["month"] - 1
)
df_month.loc[:, "Policy Change"] = df_month["Months from Policy Change"] > 0
df_month.head()
## Pre-Post
dftx = df_month[df_month["BUYER_STATE"] == "TX"]
treated_success = dftx[dftx["Policy Change"]]
g_pp = (
    ggplot(treated_success, aes(x="Months from Policy Change", y="opioid_per_capita"))
    + geom_smooth(
        method="lm",
        data=dftx[dftx["Months from Policy Change"] < 0],
    )
    + geom_smooth(
        method="lm",
        data=treated_success[treated_success["Months from Policy Change"] >= 0],
    )
    + geom_vline(xintercept=0, linetype="dashed")
    + geom_text(x=0, y=0.35, label="Policy Change", color="black")
    + labs(
        y="Monthly opioid per Capita", title="Pre-Post Model Graph, Policy Intervention"
    )
)
print(g_pp)
# In the left part of the chart the slope is sharper than the right's, which means the opioid converted amount per caipita increased year by year in Texas before January 2007. After the policy became effecive in January 2007, the trend is still increasing, but the gradient is smaller in the right part. Therefore, we may conclude that the policy restricted the opioid converted amount.

g_pp.save(
    os.path.join(
        dir, "../30_results/Bonus_Results/texas_opioid_shipment_prepost_monthly.png"
    )
)

## DID
# Select the states that we want to use as control group
texas_compare = df_month[df_month["BUYER_STATE"].isin(["MS", "MT", "CT"])]
texas_compare["Compare"] = "Control Group"
dftx["Compare"] = "Texas"
# texas_compare['BUYER_STATE'].unique()
# texas_compare.head()
# dftx.head()
success_model = dftx[
    ["Policy Change", "Months from Policy Change", "opioid_per_capita", "Compare"]
].copy()

g_did = (
    ggplot(
        success_model,
        aes(x="Months from Policy Change", y="opioid_per_capita", color="Compare"),
    )
    + geom_smooth(
        method="lm", data=success_model[success_model["Months from Policy Change"] < 0]
    )
    + geom_smooth(
        method="lm", data=success_model[success_model["Months from Policy Change"] >= 0]
    )
    + geom_smooth(
        method="lm", data=texas_compare[texas_compare["Months from Policy Change"] < 0]
    )
    + geom_smooth(
        method="lm", data=texas_compare[texas_compare["Months from Policy Change"] >= 0]
    )
    + geom_vline(xintercept=0, linetype="dashed")
    + geom_text(x=0, y=0.35, label="Policy Change", color="black")
    + labs(
        y="Monthly opioid per Capita",
        title="Diff-in-Diff Model Graph, Policy Intervention",
        color="Counties in State with Policy Change",
    )
    + theme(legend_position="right")
)
print(g_did)

g_did.save(
    os.path.join(
        dir, "../30_results/Bonus_Results/texas_opioid_shipment_diffdiff_monthly.png"
    )
)
