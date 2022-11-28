# %%
import pandas as pd
import numpy as np
from plotnine import *
from warnings import filterwarnings
ignore = filterwarnings('ignore')

# %% [markdown]
# # Pre-post anlysis

# %% [markdown]
# ## Florida

# %%
# Read in the data
df = pd.read_parquet('./death_pop.parquet')
df.head()

# %%
# calculate the overdose death per capita
df["death_per_capita"] = df["Deaths"] / df["population"]
df["state"] = df["County"].str.split(", ").str[1]
df.head()

# %%
# add binary of whether the state is before or after 2010 (policy change) 
df_fl = df[df["state"] == "FL"]
df_fl.loc[:,"Policy Change"] = df_fl["year"] > 2010
df_fl.loc[:,"Years from Policy Change"] = df_fl["year"] - 2010

# %%
treated_success = df_fl[df_fl["Policy Change"]]
g = (
    ggplot(treated_success, aes(x="Years from Policy Change", y="death_per_capita"))
    
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
#g.save("fl_prepost_successful.pdf")
print(g)

# %% [markdown]
# From the output, we can see that slope is positive before the policy change and converted to negative after the policy change. Hence, the overdeath per capita increases every year before the policy change and started to decrease after the policy became effective. Hence, we may conclude that the policy effectively restrict the overdose death.

# %% [markdown]
# ## Texas

# %%
df_tx = df[df["state"] == "TX"]
df_tx.head()

# %%
df_tx.loc[:,"Policy Change"] = df_tx.loc[:,"year"] > 2007
df_tx.loc[:,"Years from Policy Change"] = df_tx.loc[:,"year"] - 2007

# %%
treated_success = df_tx[df_tx["Policy Change"]]
g = (
    ggplot(treated_success, aes(x="Years from Policy Change", y="death_per_capita"))
    
    + geom_smooth(
        method="lm",
        data=df_tx[df_tx["Years from Policy Change"] < 0],
    )
    + geom_smooth(
        method="lm",
        data=treated_success[treated_success["Years from Policy Change"] >= 0],
    )
    + geom_vline(xintercept=0, linetype="dashed")
    + geom_text(x=-0.9, y=0.21
                , label="Policy Change", color="black")
    + labs(title="Pre-Post Model Graph, Policy Intervention")
)
#g.save("tx_prepost_successful.pdf")
print(g)

# %% [markdown]
# In the left part of the chart, the slope is sharp which means the overdose per capita increased quickly year by year in Texas before 2007. However, after the policy became effecive in 2007, the overdose death started to decrease annually. Therefore, we may conclude that the policy restricted the overdose death per capita.

# %% [markdown]
# ## Washington

# %%
df_wa = df[df["state"] == "WA"]
df_wa.head()

# %%
df_wa.loc[:,"Policy Change"] = df_wa["year"] > 2012
df_wa.loc[:,"Years from Policy Change"] = df_wa["year"] - 2012

# %%
treated_success = df_wa[df_wa["Policy Change"]]
g = (
    ggplot(treated_success, aes(x="Years from Policy Change", y="death_per_capita"))
    
    + geom_smooth(
        method="lm",
        data=df_wa[df_wa["Years from Policy Change"] < 0],
    )
    + geom_smooth(
        method="lm",
        data=treated_success[treated_success["Years from Policy Change"] >= 0],
    )
    + geom_vline(xintercept=0, linetype="dashed")
    + geom_text(x=-0.9, y=0.000135
                , label="Policy Change", color="black")
    + labs(title="Pre-Post Model Graph, Policy Intervention")
)
#g.save("wa_prepost_successful.pdf")
print(g)

# %% [markdown]
# From the output, we can see that the overdeath rate increased even more sharply after the policy became effective. Based on this output, we may conclude that the policy doesn't have significant effect on the control of the situation of overdose death. However, this may relates to the some other issues. We then do the diff-diff analysis to fugure out the potenial reasons

# %% [markdown]
# # Diff-Diff Analysis

# %%
# Select the states that we want to use as control group
florida_compare = df[df["state"].isin(["GA", "NC", "SC"])]
florida_compare["Policy Change"] = florida_compare["year"] > 2010
florida_compare["Years from Policy Change"] = florida_compare["year"] - 2010
florida_compare["Compare"] = "Control Group"
df_fl["Compare"] = "Florida"

# %%
success_model = df_fl[["Policy Change","Years from Policy Change","death_per_capita","Compare"]].copy()

g = (
    ggplot(
        success_model,
        aes(x="Years from Policy Change", y="death_per_capita", color="Compare"),
    )
    + geom_smooth(
        method="lm", data=success_model[success_model["Years from Policy Change"] < 0]
    )
    + geom_smooth(
        method="lm", data=success_model[success_model["Years from Policy Change"] >= 0]
    )
    + geom_smooth(
        method="lm", data=florida_compare[florida_compare ["Years from Policy Change"] < 0]
    )
    + geom_smooth(
        method="lm", data=florida_compare[florida_compare["Years from Policy Change"] >= 0]
    )
    + geom_vline(xintercept=0, linetype="dashed")
    + geom_text(x=-0.7, y=7, label="Policy Change", color="black")
    + labs(
        title="Diff-in-Diff Model Graph, Effective Policy Intervention",
        color="Counties in State with Policy Change",
    )
    + theme(legend_position="bottom")
)
print(g)

# %% [markdown]
# From the output, we can see the slope overdose death rate over year keeps positive after policy change year, but the slope of red line which represents the overdose deaath in Florida decreased to begative afer 2010. Hence, we may conclude that the policy plays important role in restricting the overdose death

# %% [markdown]
# ## Texas

# %%
# Select the states that we want to use as control group
texas_compare = df[df["state"].isin(["AR", "OK", "NM"])]
texas_compare["Policy Change"] = texas_compare["year"] > 2007
texas_compare["Years from Policy Change"] = texas_compare["year"] - 2007
texas_compare["Compare"] = "Control Group"
df_tx["Compare"] = "Texas"

# %%
success_model = df_tx[["Policy Change","Years from Policy Change","death_per_capita","Compare"]].copy()

g = (
    ggplot(
        success_model,
        aes(x="Years from Policy Change", y="death_per_capita", color="Compare"),
    )
    + geom_smooth(
        method="lm", data=success_model[success_model["Years from Policy Change"] < 0]
    )
    + geom_smooth(
        method="lm", data=success_model[success_model["Years from Policy Change"] >= 0]
    )
    + geom_smooth(
        method="lm", data=texas_compare[texas_compare ["Years from Policy Change"] <= 0]
    )
    + geom_smooth(
        method="lm", data=texas_compare[texas_compare["Years from Policy Change"] >= 0]
    )
    + geom_vline(xintercept=0, linetype="dashed")
    + geom_text(x=-0.7, y=0.3, label="Policy Change", color="black")
    + labs(
        title="Diff-in-Diff Model Graph, Effective Policy Intervention",
        color="Counties in State with Policy Change",
    )
    + theme(legend_position="bottom")
)
print(g)

# %% [markdown]
# From the output, the green line which indicates the over death rate of states in control group is still positive after policy change. However, the red line which represents the overdose death per capita in Texas decreased a slightly negative after 2007. Hence, based on the output, we may conclude that the policy in Texas restricts the overdeath.

# %% [markdown]
# ## Washington

# %%
# Select the states that we want to use as control group
wa_compare = df[df["state"].isin(["OR", "ID", "MT"])]
wa_compare["Policy Change"] = wa_compare["year"] > 2012
wa_compare["Years from Policy Change"] = wa_compare["year"] - 2012
wa_compare["Compare"] = "Control Group"
df_wa["Compare"] = "Washington"

# %%
success_model = df_wa[["Policy Change","Years from Policy Change","death_per_capita","Compare"]].copy()

g = (
    ggplot(
        success_model,
        aes(x="Years from Policy Change", y="death_per_capita", color="Compare"),
    )
    + geom_smooth(
        method="lm", data=success_model[success_model["Years from Policy Change"] < 0]
    )
    + geom_smooth(
        method="lm", data=success_model[success_model["Years from Policy Change"] >= 0]
    )
    + geom_smooth(
        method="lm", data=wa_compare[wa_compare["Years from Policy Change"] <= 0]
    )
    + geom_smooth(
        method="lm", data=wa_compare[wa_compare["Years from Policy Change"] >= 0]
    )
    + geom_vline(xintercept=0, linetype="dashed")
    + geom_text(x=-0.5, y=0.3, label="Policy Change", color="black")
    + labs(
        title="Diff-in-Diff Model Graph, Effective Policy Intervention",
        color="Counties in State with Policy Change",
    )
    + theme(legend_position="bottom")
)
print(g)

# %% [markdown]
# From the output, we can see that two lines follow similar pattern for WA and states in control group. Hence, we may conclude hat the policy is not significantly significant in WA.

# %%



