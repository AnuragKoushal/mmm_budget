import pandas as pd


def generate_multi_period_scenario(df, scenario_dict, periods=3):
    scenario_df = df.copy()

    for i in range(1, periods + 1):
        row = scenario_df.iloc[-1].copy()

        for ch, mult in scenario_dict.items():
            if ch in row:
                row[ch] *= mult

        row["date"] = row["date"] + pd.DateOffset(months=i)
        scenario_df = pd.concat([scenario_df, pd.DataFrame([row])])

    return scenario_df


def simulate_scenario(mmm, df):
    return mmm.predict(df)