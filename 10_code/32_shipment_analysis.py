import pandas as pd
import numpy as np
import os
from plotnine import *
from warnings import filterwarnings

ignore = filterwarnings("ignore")

# Set working directory as location of current file to use relative paths further on
dir = os.path.dirname(os.path.abspath(__file__))

### Pre-Post Analysis

## Florida

# Read in the data
df = pd.read_parquet(os.path.join(dir, "../20_intermediate_files/ship_pop.parquet"))
df.head()

# calculate the opioids per capita
df["Opioid per capita"] = df["opioid_converted_grams"] / df["population"]
df.head()

# add binary of whether the state is before or after 2010 (policy change)
df_fl = df[df["BUYER_STATE"] == "FL"]
df_fl.loc[:, "Policy Change"] = df_fl["year"] > 2010
df_fl.loc[:, "Years from Policy Change"] = df_fl["year"] - 2010

treated_success = df_fl[df_fl["Policy Change"]]
g = (
    ggplot(treated_success, aes(x="Years from Policy Change", y="Opioid per capita"))
    + geom_smooth(
        method="lm",
        data=df_fl[df_fl["Years from Policy Change"] < 0],
    )
    + geom_smooth(
        method="lm",
        data=treated_success[treated_success["Years from Policy Change"] >= 0],
    )
    + geom_vline(xintercept=0, linetype="dashed")
    + geom_text(x=-0.7, y=0.5, label="Policy Change", color="black")
    + labs(title="Pre-Post Model Graph, Policy Intervention")
)
g.save(
    os.path.join(
        dir, "../30_results/General_Results/florida_opioid_shipment_prepost.png"
    )
)
print(g)

# From the output of the graph, we can see the slope of regression model of opioid convert amount per capita is positive before the policy became effective, but changed to negative after the date the policy became effect. This means that the convert amount per capita increased year by year before the policy change and started to decrease annually after the policy effective date. Therefore, we may conclude that The policy is effective in Florida according to pre-post analysis.

## Washington

df_wa = df[df["BUYER_STATE"] == "WA"]
df_wa.head()

df_wa.loc[:, "Policy Change"] = df_wa["year"] > 2012
df_wa.loc[:, "Years from Policy Change"] = df_wa["year"] - 2012


treated_success = df_wa[df_wa["Policy Change"]]
g = (
    ggplot(treated_success, aes(x="Years from Policy Change", y="Opioid per capita"))
    + geom_smooth(
        method="lm",
        data=df_wa[df_wa["Years from Policy Change"] < 0],
    )
    + geom_smooth(
        method="lm",
        data=treated_success[treated_success["Years from Policy Change"] >= 0],
    )
    + geom_vline(xintercept=0, linetype="dashed")
    + geom_text(x=-0.9, y=0.21, label="Policy Change", color="black")
    + labs(title="Pre-Post Model Graph, Policy Intervention")
)
g.save(
    os.path.join(
        dir, "../30_results/General_Results/washington_opioid_shipment_prepost.png"
    )
)
print(g)

# From the output, we can find that the slope of opioid conveted amount is positive before the date of policy being effective and became negative after 2012 in which year the policy became effective. Even though the gradient indicates that the decreasing speed is not high, but the overall trend is totally different from the previous years. Hence, we conclude that the policy has positive influence on the opioid converted amount restriction.

### Diff-in-Diff

## Florida

# Select the states that we want to use as control group
florida_compare = df[df["BUYER_STATE"].isin(["TN", "WV", "NV"])]
florida_compare["Policy Change"] = florida_compare["year"] > 2010
florida_compare["Years from Policy Change"] = florida_compare["year"] - 2010
florida_compare["Compare"] = "Control Group"
df_fl["Compare"] = "Florida"

# We selected TN, WV, and NV since those three states have similar trends before the policy change

success_model = df_fl[
    ["Policy Change", "Years from Policy Change", "Opioid per capita", "Compare"]
].copy()

g = (
    ggplot(
        success_model,
        aes(x="Years from Policy Change", y="Opioid per capita", color="Compare"),
    )
    + geom_smooth(
        method="lm", data=success_model[success_model["Years from Policy Change"] < 0]
    )
    + geom_smooth(
        method="lm", data=success_model[success_model["Years from Policy Change"] >= 0]
    )
    + geom_smooth(
        method="lm",
        data=florida_compare[florida_compare["Years from Policy Change"] < 0],
    )
    + geom_smooth(
        method="lm",
        data=florida_compare[florida_compare["Years from Policy Change"] >= 0],
    )
    + geom_vline(xintercept=0, linetype="dashed")
    + geom_text(x=-0.7, y=7, label="Policy Change", color="black")
    + labs(
        title="Diff-in-Diff Model Graph, Policy Intervention",
        color="Counties in State with Policy Change",
    )
    + theme(legend_position="right")
)

print(g)

g.save(
    os.path.join(
        dir, "../30_results/General_Results/florida_opioid_shipment_diffdiff.png"
    )
)

# From the output, we can see that the slope of control groups is still positive but the slope of Florida opioid convert amount annual increase decreased to negative. Therefore, we may conclude that the decrease of the opioid per caipta in Florida after 2010 is because of the policy which means the policy is effective.


## Washington

# Select the states that we want to use as control group
wa_compare = df[df["BUYER_STATE"].isin(["IL", "WI", "RI"])]
wa_compare["Policy Change"] = wa_compare["year"] > 2012
wa_compare["Years from Policy Change"] = wa_compare["year"] - 2012
wa_compare["Compare"] = "Control Group"
df_wa["Compare"] = "Washington"

success_model = df_wa[
    ["Policy Change", "Years from Policy Change", "Opioid per capita", "Compare"]
].copy()

g = (
    ggplot(
        success_model,
        aes(x="Years from Policy Change", y="Opioid per capita", color="Compare"),
    )
    + geom_smooth(
        method="lm", data=success_model[success_model["Years from Policy Change"] < 0]
    )
    + geom_smooth(
        method="lm", data=success_model[success_model["Years from Policy Change"] >= 0]
    )
    + geom_smooth(
        method="lm", data=wa_compare[wa_compare["Years from Policy Change"] < 0]
    )
    + geom_smooth(
        method="lm", data=wa_compare[wa_compare["Years from Policy Change"] >= 0]
    )
    + geom_vline(xintercept=0, linetype="dashed")
    + geom_text(x=-0.5, y=0.3, label="Policy Change", color="black")
    + labs(
        title="Diff-in-Diff Model Graph, Policy Intervention",
        color="Counties in State with Policy Change",
    )
    + theme(legend_position="right")
)

g.save(
    os.path.join(
        dir, "../30_results/General_Results/washington_opioid_shipment_diffdiff.png"
    )
)
print(g)

# From the output, we can see the gradient change is similar for Washington and neiboughood states. Hence, we cannot conclude the policy is the only factor which deceased the opioid convert amount per capita.
