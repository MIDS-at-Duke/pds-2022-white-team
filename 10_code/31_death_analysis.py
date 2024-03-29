import pandas as pd
import numpy as np
from plotnine import *
from warnings import filterwarnings
import os

ignore = filterwarnings("ignore")

# Set working directory as location of current file to use relative paths further on
dir = os.path.dirname(os.path.abspath(__file__))

### Pre-post anlysis

## Florida

# Read in the data
df = pd.read_parquet(os.path.join(dir, "../20_intermediate_files/death_pop.parquet"))
df.head()

# Dalculate the overdose death per capita
df["Overdose deaths per 100,000 people"] = df["Deaths"] / df["population"] * 100000
df["state"] = df["County"].str.split(", ").str[1]

df.head()

# add binary of whether the state is before or after 2010 (policy change)
df_fl = df[df["state"] == "FL"]
df_fl.loc[:, "Policy Change"] = df_fl["year"] > 2010
df_fl.loc[:, "Years from Policy Change"] = df_fl["year"] - 2010

treated_success = df_fl[df_fl["Policy Change"]]
g = (
    ggplot(
        treated_success,
        aes(x="Years from Policy Change", y="Overdose deaths per 100,000 people"),
    )
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
        dir, "../30_results/General_Results/florida_overdose_death_prepost.png"
    )
)
print(g)

# From the output, we can see that slope is positive before the policy change and converted to negative after the policy change. Hence, the overdeath per capita increases every year before the policy change and started to decrease after the policy became effective. Hence, we may conclude that the policy effectively restrict the overdose death.


## Texas

df_tx = df[df["state"] == "TX"]
df_tx.head()

df_tx.loc[:, "Policy Change"] = df_tx.loc[:, "year"] > 2007
df_tx.loc[:, "Years from Policy Change"] = df_tx.loc[:, "year"] - 2007

treated_success = df_tx[df_tx["Policy Change"]]
g = (
    ggplot(
        treated_success,
        aes(x="Years from Policy Change", y="Overdose deaths per 100,000 people"),
    )
    + geom_smooth(
        method="lm",
        data=df_tx[df_tx["Years from Policy Change"] < 0],
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
    os.path.join(dir, "../30_results/General_Results/texas_overdose_death_prepost.png")
)
print(g)

# In the left part of the chart, the slope is sharp which means the overdose per capita increased quickly year by year in Texas before 2007. However, after the policy became effecive in 2007, the overdose death started to decrease annually. Therefore, we may conclude that the policy restricted the overdose death per capita.

## Washington
df_wa = df[df["state"] == "WA"]
df_wa.head()

df_wa.loc[:, "Policy Change"] = df_wa["year"] > 2012
df_wa.loc[:, "Years from Policy Change"] = df_wa["year"] - 2012

treated_success = df_wa[df_wa["Policy Change"]]
g = (
    ggplot(
        treated_success,
        aes(x="Years from Policy Change", y="Overdose deaths per 100,000 people"),
    )
    + geom_smooth(
        method="lm",
        data=df_wa[df_wa["Years from Policy Change"] < 0],
    )
    + geom_smooth(
        method="lm",
        data=treated_success[treated_success["Years from Policy Change"] >= 0],
    )
    + geom_vline(xintercept=0, linetype="dashed")
    + geom_text(x=-0.9, y=0.000135, label="Policy Change", color="black")
    + labs(title="Pre-Post Model Graph, Policy Intervention")
)
g.save(
    os.path.join(
        dir,
        "../30_results/General_Results/washington_overdose_death_prepost.png",
    )
)
print(g)

# From the output, we can see that the overdeath rate increased even more sharply after the policy became effective. Based on this output, we may conclude that the policy doesn't have significant effect on the control of the situation of overdose death. However, this may relates to the some other issues. We then do the diff-diff analysis to fugure out the potenial reasons

### Diff-in-Diff Analysis

# Select the states that we want to use as control group
florida_compare = df[df["state"].isin(["NC", "TN", "IA"])]
florida_compare["Policy Change"] = florida_compare["year"] > 2010
florida_compare["Years from Policy Change"] = florida_compare["year"] - 2010
florida_compare["Compare"] = "Control Group"
df_fl["Compare"] = "Florida"

success_model = df_fl[
    [
        "Policy Change",
        "Years from Policy Change",
        "Overdose deaths per 100,000 people",
        "Compare",
    ]
].copy()

g = (
    ggplot(
        success_model,
        aes(
            x="Years from Policy Change",
            y="Overdose deaths per 100,000 people",
            color="Compare",
        ),
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

g.save(
    os.path.join(
        dir, "../30_results/General_Results/florida_overdose_death_diffdiff.png"
    )
)
print(g)

# From the output, we can see the slope overdose death rate over year keeps positive after policy change year, but the slope of red line which represents the overdose deaath in Florida decreased to begative afer 2010. Hence, we may conclude that the policy plays important role in restricting the overdose death

## Texas

# Select the states that we want to use as control group
texas_compare = df[df["state"].isin(["WV", "OR", "ID"])]
texas_compare["Policy Change"] = texas_compare["year"] > 2007
texas_compare["Years from Policy Change"] = texas_compare["year"] - 2007
texas_compare["Compare"] = "Control Group"
df_tx["Compare"] = "Texas"

success_model = df_tx[
    [
        "Policy Change",
        "Years from Policy Change",
        "Overdose deaths per 100,000 people",
        "Compare",
    ]
].copy()

g = (
    ggplot(
        success_model,
        aes(
            x="Years from Policy Change",
            y="Overdose deaths per 100,000 people",
            color="Compare",
        ),
    )
    + geom_smooth(
        method="lm", data=success_model[success_model["Years from Policy Change"] < 0]
    )
    + geom_smooth(
        method="lm", data=success_model[success_model["Years from Policy Change"] >= 0]
    )
    + geom_smooth(
        method="lm", data=texas_compare[texas_compare["Years from Policy Change"] < 0]
    )
    + geom_smooth(
        method="lm", data=texas_compare[texas_compare["Years from Policy Change"] >= 0]
    )
    + geom_vline(xintercept=0, linetype="dashed")
    + geom_text(x=-0.7, y=0.3, label="Policy Change", color="black")
    + labs(
        title="Diff-in-Diff Model Graph, Policy Intervention",
        color="Counties in State with Policy Change",
    )
    + theme(legend_position="right")
)
g.save(
    os.path.join(dir, "../30_results/General_Results/texas_overdose_death_diffdiff.png")
)
print(g)

# From the output, the green line which indicates the over death rate of states in control group is still positive after policy change. However, the red line which represents the overdose death per capita in Texas decreased a slightly negative after 2007. Hence, based on the output, we may conclude that the policy in Texas restricts the overdeath.

## Washington

# Select the states that we want to use as control group
wa_compare = df[df["state"].isin(["KS", "NJ", "OR"])]
wa_compare["Policy Change"] = wa_compare["year"] > 2012
wa_compare["Years from Policy Change"] = wa_compare["year"] - 2012
wa_compare["Compare"] = "Control Group"
df_wa["Compare"] = "Washington"

success_model = df_wa[
    [
        "Policy Change",
        "Years from Policy Change",
        "Overdose deaths per 100,000 people",
        "Compare",
    ]
].copy()

g = (
    ggplot(
        success_model,
        aes(
            x="Years from Policy Change",
            y="Overdose deaths per 100,000 people",
            color="Compare",
        ),
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
        dir,
        "../30_results/General_Results/washington_overdose_death_diffdiff.png",
    )
)
print(g)

# From the output, we can see that two lines follow similar pattern for WA and states in control group. Hence, we may conclude hat the policy is not significantly significant in WA.
