import streamlit as st
import pandas as pd

from src.preprocessing import prepare_data
from src.model import train_mmm
from src.optimizer import run_optimization
from src.inference import (
    get_channel_contributions,
    plot_channel_contributions,
    plot_response_curves,
    plot_posterior_diagnostics,
    compute_marginal_roas
)
from src.constraints import build_constraints
from src.risk import summarize_with_uncertainty
from src.export import export_results
from src.scenario import generate_multi_period_scenario, simulate_scenario

from config import DATE_COL, TARGET_COL, SPEND_COL, CHANNEL_COL


st.set_page_config(page_title="MMM Decision Engine", layout="wide")

st.title("📊 Enterprise MMM Decision Engine")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Raw Data")
    st.dataframe(df.head())

    model_df = prepare_data(df)

    st.subheader("Transformed Data")
    st.dataframe(model_df.head())

    if st.button("🚀 Train Model"):

        channel_cols = [
            col for col in model_df.columns
            if col not in ["date", TARGET_COL]
        ]

        mmm, idata = train_mmm(model_df, channel_cols)

        st.success("Model trained!")

        # =====================
        # 📊 INFERENCE
        # =====================
        st.header("📊 Insights")

        contrib = get_channel_contributions(mmm)
        st.write(contrib.mean(dim=["chain", "draw"]))

        st.pyplot(plot_channel_contributions(contrib))
        st.pyplot(plot_response_curves(mmm))
        st.pyplot(plot_posterior_diagnostics(idata))

        st.subheader("Marginal ROAS (Proxy)")
        st.write(compute_marginal_roas(mmm))

        # =====================
        # 🔮 SCENARIO
        # =====================
        st.header("🔮 Scenario Planner")

        scenario_inputs = {}

        for ch in channel_cols:
            scenario_inputs[ch] = st.slider(ch, 0.0, 2.0, 1.0, 0.1)

        if st.button("Run Scenario"):
            scenario_df = generate_multi_period_scenario(
                model_df,
                scenario_inputs,
                periods=3
            )

            preds = simulate_scenario(mmm, scenario_df)
            summary = summarize_with_uncertainty(preds)

            st.write(summary)

        # =====================
        # 💰 OPTIMIZATION
        # =====================
        st.header("💰 Optimization")

        total_budget = st.number_input("Total Budget", value=100000)

        if st.button("Optimize Budget"):
            bounds = build_constraints(channel_cols)

            result = run_optimization(mmm, total_budget, bounds)

            st.write(result)
            st.bar_chart(result)

            preds = mmm.predict(model_df)
            summary = summarize_with_uncertainty(preds)

            st.subheader("Uncertainty")
            st.write(summary)

            export_results({
                "allocation": result,
                "uncertainty": summary
            })