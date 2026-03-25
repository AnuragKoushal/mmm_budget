from pymc_marketing.mmm import MMM
import pymc as pm
from config import TARGET_COL, ADSTOCK_LAG


def train_mmm(df, channel_cols):

    model_config = {
        "intercept": pm.Normal.dist(mu=0, sigma=1),
        "beta_channel": pm.HalfNormal.dist(sigma=1),
        "sigma": pm.HalfNormal.dist(sigma=1),
    }

    mmm = MMM(
        date_column="date",
        target_column=TARGET_COL,
        channel_columns=channel_cols,
        adstock_max_lag=ADSTOCK_LAG,
        model_config=model_config,
    )

    idata = mmm.fit(df)

    return mmm, idata