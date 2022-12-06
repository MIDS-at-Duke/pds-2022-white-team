# %%
import pandas as pd
import numpy as np

# %%
death = pd.read_parquet(
    "/Users/liuxiaoquan/Documents/GitHub/pds-2022-white-team/10_code/death_pop.parquet"
)
death["death_per_capita"] = (death["Deaths"] / death["population"]) * 100000
death["state"] = death["County"].str.split(", ").str[1]
death.head()

# %%
states_FL = ["FL", "GA", "NC", "SC"]
states_TX = ["TX", "OK", "AR", "NM"]
states_WA = ["WA", "OR", "ID", "MT"]


# %%
df_FL = death[death["state"].isin(states_FL)]
df_FL.head()


# %%
df_TX = death[death["state"].isin(states_TX)]
df_TX.head()

# %%
df_WA = death[death["state"].isin(states_WA)]
df_WA.head()

# %%
df_FL_pre = df_FL[df_FL["Year"] < 2010]
df_FL_post = df_FL[df_FL["Year"] >= 2010]

df_TX_pre = df_TX[df_TX["Year"] < 2007]
df_TX_post = df_TX[df_TX["Year"] >= 2007]

df_WA_pre = df_WA[df_WA["Year"] < 2011]
df_WA_post = df_WA[df_WA["Year"] >= 2011]

# %% [markdown]
# ## Florida and control groups

# %%
pre_FL = df_FL_pre.loc[df_FL_pre["state"] == "FL"]["death_per_capita"].describe()
pre_FL_x = df_FL_pre.loc[df_FL_pre["state"] != "FL"]["death_per_capita"].describe()

# %%
pre_FL

# %%
pre_FL_x

# %%
post_FL = df_FL_post.loc[df_FL_post["state"] == "FL"]["death_per_capita"].describe()
post_FL_x = df_FL_post.loc[df_FL_post["state"] != "FL"]["death_per_capita"].describe()

# %%
post_FL

# %%
post_FL_x

# %% [markdown]
# ## Texas and control groups

# %%
pre_TX = df_TX_pre.loc[df_TX_pre["state"] == "TX"]["death_per_capita"].describe()
pre_TX_x = df_TX_pre.loc[df_TX_pre["state"] != "TX"]["death_per_capita"].describe()
pre_TX

# %%
pre_TX_x

# %%
post_TX = df_TX_post.loc[df_TX_post["state"] == "TX"]["death_per_capita"].describe()
post_TX_x = df_TX_post.loc[df_TX_post["state"] != "TX"]["death_per_capita"].describe()
post_TX

# %%
post_TX_x

# %% [markdown]
# ## Washington and control groups

# %%
pre_WA = df_WA_pre.loc[df_WA_pre["state"] == "WA"]["death_per_capita"].describe()
pre_WA_x = df_WA_pre.loc[df_WA_pre["state"] != "WA"]["death_per_capita"].describe()
pre_WA

# %%
pre_WA_x

# %%
post_WA = df_WA_post.loc[df_WA_post["state"] == "WA"]["death_per_capita"].describe()
post_WA_x = df_WA_post.loc[df_WA_post["state"] != "WA"]["death_per_capita"].describe()
post_WA

# %%
post_WA_x

# %%
