import pandas as pd
from config import DATE_COL, TARGET_COL, SPEND_COL, CHANNEL_COL


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    df["date"] = pd.to_datetime(df[DATE_COL])

    agg_df = (
        df.groupby(["date", CHANNEL_COL])
        .agg({
            SPEND_COL: "sum",
            TARGET_COL: "sum"
        })
        .reset_index()
    )

    pivot_spend = agg_df.pivot(
        index="date",
        columns=CHANNEL_COL,
        values=SPEND_COL
    ).fillna(0)

    target = agg_df.groupby("date")[TARGET_COL].sum()

    model_df = pivot_spend.copy()
    model_df[TARGET_COL] = target

    return model_df.reset_index()