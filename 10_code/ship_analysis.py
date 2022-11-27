# %%
import pandas as pd
import numpy as np
from plotnine import *
from warnings import filterwarnings
ignore = filterwarnings('ignore')

# %% [markdown]
# # Pre-Post Analysis

# %% [markdown]
# ## Florida 

# %%
# Read in the data
df = pd.read_parquet('./ship_pop.parquet')
df.head()

# %%
# calculate the opioide per capita
df["opioid_per_capita"] = df["opioid_converted_grams"] / df["population"]
df.head()

# %%
# add binary of whether the state is before or after 2010 (policy change) 
df_fl = df[df["BUYER_STATE"] == "FL"]
df_fl.loc[:,"Policy Change"] = df_fl["year"] > 2010
df_fl.loc[:,"Years from Policy Change"] = df_fl["year"] - 2010

# %% [markdown]
# # Pre-Post

# %%
treated_success = df_fl[df_fl["Policy Change"]]
g = (
    ggplot(treated_success, aes(x="Years from Policy Change", y="opioid_per_capita"))
    
    + geom_smooth(
        method="lm",
        data=df_fl[df_fl["Years from Policy Change"] < 0],
        se=False,
    )
    + geom_smooth(
        method="lm",
        data=treated_success[treated_success["Years from Policy Change"] >= 0],
        se=False,
    )
    + geom_vline(xintercept=0, linetype="dashed")
    + geom_text(x=-0.7, y=0.5, label="Policy Change", color="black")
    + labs(title="Pre-Post Model Graph, Policy Intervention")
)
#g.save("images/prepost_successful.pdf")
print(g)

# %% [markdown]
# From the output of the graph, we can see the slope of regression model of opioid convert amount per capita is positive before the policy became effective, but changed to negative after the date the policy became effect. This means that the convert amoungt per capita increased year by year before the policy change and started to decrease annually after the policy effective date. Therefore, we may conclude that The policy is effective in Florida according to pre-post analysis.

# %% [markdown]
# ## Texas

# %%
df_tx = df[df["BUYER_STATE"] == "TX"]
df_tx.head()

# %%
df_tx.loc[:,"Policy Change"] = df_tx.loc[:,"year"] > 2008
df_tx.loc[:,"Years from Policy Change"] = df_tx.loc[:,"year"] - 2008

# %%
treated_success = df_tx[df_tx["Policy Change"]]
g = (
    ggplot(treated_success, aes(x="Years from Policy Change", y="opioid_per_capita"))
    
    + geom_smooth(
        method="lm",
        data=df_tx[df_tx["Years from Policy Change"] < 0],
        se=False,
    )
    + geom_smooth(
        method="lm",
        data=treated_success[treated_success["Years from Policy Change"] >= 0],
        se=False,
    )
    + geom_vline(xintercept=0, linetype="dashed")
    + geom_text(x=-0.9, y=0.21
                , label="Policy Change", color="black")
    + labs(title="Pre-Post Model Graph, Policy Intervention")
)
#g.save("images/prepost_successful.pdf")
print(g)

# %% [markdown]
# From the output graph, we can see the slope of opioid converted amount per capita are positive for both before and after policy change. However, the gradient decreased after year 2008 when the policy went to effective. Therefore, we concluded that the policy restricts the opioid in Texas. But the effect might be less obvious than Florida. 

# %% [markdown]
# ### Washington

# %%
df_wa = df[df["BUYER_STATE"] == "WA"]
df_wa.head()

# %%
df_wa.loc[:,"Policy Change"] = df_wa["year"] > 2012
df_wa.loc[:,"Years from Policy Change"] = df_wa["year"] - 2012

# %%
treated_success = df_wa[df_wa["Policy Change"]]
g = (
    ggplot(treated_success, aes(x="Years from Policy Change", y="opioid_per_capita"))
    
    + geom_smooth(
        method="lm",
        data=df_wa[df_wa["Years from Policy Change"] < 0],
        se=False,
    )
    + geom_smooth(
        method="lm",
        data=treated_success[treated_success["Years from Policy Change"] >= 0],
        se=False,
    )
    + geom_vline(xintercept=0, linetype="dashed")
    + geom_text(x=-0.9, y=0.21
                , label="Policy Change", color="black")
    + labs(title="Pre-Post Model Graph, Policy Intervention")
)
#g.save("images/prepost_successful.pdf")
print(g)

# %% [markdown]
# From the output, we can find that the slope of opioid conveted amount is positive before the date of policy being effective and became negative after 2012 in which year the policy became effective. Even though the gradient indicates that the decreasing speed is not high, but the overall trend is totally different from the previous years. Hence, we conclude that the policy has positive influence on the opioid converted amount restriction.

# %% [markdown]
# ## Diff-in-Diff

# %% [markdown]
# ### Florida

# %%
# Select the states that we want to use as control group
florida_compare = df[df["BUYER_STATE"].isin(["GA", "NC", "SC"])]
florida_compare["Policy Change"] = florida_compare["year"] > 2010
florida_compare["Years from Policy Change"] = florida_compare["year"] - 2010
florida_compare["Compare"] = "Control Group"
df_fl["Compare"] = "Florida"

# %% [markdown]
# We selected Georgia, North Corarlina, and South Carolina since those three states are close to Florida and have similar weather

# %%
success_model = df_fl[["Policy Change","Years from Policy Change","opioid_per_capita","Compare"]].copy()

g = (
    ggplot(
        success_model,
        aes(x="Years from Policy Change", y="opioid_per_capita", color="Compare"),
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
# From the output, we can see that the slope of control groups is still positive but the slope oof Florida opioid convert amount annual increase decreased to negative. Therefore, we may conclude that the decrease of the opioid per caipta in Florida after 2010 is because of the policy which means the policy is effective.

# %% [markdown]
# ## Texas

# %%
# Select the states that we want to use as control group
texas_compare = df[df["BUYER_STATE"].isin(["AR", "OK", "NM"])]
texas_compare["Policy Change"] = texas_compare["year"] > 2007
texas_compare["Years from Policy Change"] = texas_compare["year"] - 2007
texas_compare["Compare"] = "Control Group"
df_tx["Compare"] = "Texas"

# %%
success_model = df_tx[["Policy Change","Years from Policy Change","opioid_per_capita","Compare"]].copy()

g = (
    ggplot(
        success_model,
        aes(x="Years from Policy Change", y="opioid_per_capita", color="Compare"),
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
# From the output, we can conclude that even though the slope of opioid converted amount per caipita is still positive, but value of gradient is smaller. Also, compare to control grou, the second derivative is negative for Texas, but positive for the control group. Hence, we may conclude that the policy restrict the opioid converted amount.

# %% [markdown]
# ## Washington

# %%
# Select the states that we want to use as control group
wa_compare = df[df["BUYER_STATE"].isin(["OR", "ID", "MT"])]
wa_compare["Policy Change"] = wa_compare["year"] > 2012
wa_compare["Years from Policy Change"] = wa_compare["year"] - 2012
wa_compare["Compare"] = "Control Group"
df_wa["Compare"] = "Washington"

# %%
success_model = df_wa[["Policy Change","Years from Policy Change","opioid_per_capita","Compare"]].copy()

g = (
    ggplot(
        success_model,
        aes(x="Years from Policy Change", y="opioid_per_capita", color="Compare"),
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
# From the output, we can see the gradient change is similar for Washington and neiboughood states. Hence, we cannot conclude the policy is the only factor which deceased the opioid convert amount per capita.


