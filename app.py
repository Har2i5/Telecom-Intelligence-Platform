import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib


# PAGE CONFIG

st.set_page_config(page_title="Telecom Intelligence Platform", layout="wide")

st.title("📡 Telecom Reliability & Incident Intelligence Platform")

st.markdown("""
Understand **where failures happen**, **what causes the most damage**, and **what to prioritize**.
""")


# LOAD DATA

@st.cache_data
def load_data():
    df = pd.read_csv("telecommunications-equipment-failure-logs.csv")
    df['failure_datetime'] = pd.to_datetime(df['failure_datetime'], errors='coerce')
    return df

df = load_data()

# LOAD MODEL

pipeline = joblib.load("telecom_failure_model.pkl")

# FILTERS

st.sidebar.header("🔍 Filter Data")

countries = st.sidebar.multiselect(
    "Country",
    sorted(df['location_country'].dropna().unique())
)

equipment = st.sidebar.multiselect(
    "Equipment Type",
    sorted(df['equipment_type'].dropna().unique())
)

failure_types = st.sidebar.multiselect(
    "Failure Type",
    sorted(df['failure_type'].dropna().unique())
)

df_filtered = df.copy()

if countries:
    df_filtered = df_filtered[df_filtered['location_country'].isin(countries)]

if equipment:
    df_filtered = df_filtered[df_filtered['equipment_type'].isin(equipment)]

if failure_types:
    df_filtered = df_filtered[df_filtered['failure_type'].isin(failure_types)]

# KPIs

st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

total_failures = len(df_filtered)
total_customers = df_filtered['affected_customers_count'].sum()
median_impact = df_filtered['affected_customers_count'].median()

col1.metric("Total Failures", total_failures)
col2.metric("Total Customers Impacted", int(total_customers))
col3.metric("Typical Impact (Median)", int(median_impact) if total_failures else 0)

if total_failures > 0:
    st.info(f"""
    📌 Most failures affect around **{int(median_impact)} customers**, 
    but a few incidents cause significantly larger disruptions.
    """)

st.markdown("---")


# TABS

tab0, tab1, tab2, tab3, tab4 = st.tabs([
    "🌍 Global Overview",
    "📊 What Fails?",
    "📈 Impact Analysis",
    "⚠️ Risk Ranking",
    "🤖 ML Prediction"
])


# 🌍 GLOBAL (FIXED)

with tab0:

    st.subheader("🌍 Where Failures Occur Most")

    if df_filtered.empty:
        st.warning("No data available for selected filters.")
    else:
        # Bar chart (FILTERED)
        country_counts = df_filtered['location_country'].value_counts().reset_index()
        country_counts.columns = ['location_country', 'failures']

        fig1 = px.bar(
            country_counts.head(10),
            x='location_country',
            y='failures',
            text='failures'
        )
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("🌍 Global Failure Distribution")

        # Map (FILTERED)
        map_df = df_filtered.groupby('location_country').agg({
            'failure_id': 'count',
            'affected_customers_count': 'sum',
            'recovery_duration_minutes': 'mean'
        }).reset_index()

        map_df.columns = [
            'location_country',
            'failures',
            'total_impact',
            'avg_recovery'
        ]

        if not map_df.empty:
            map_df['failures_log'] = np.log1p(map_df['failures'])

            fig_map = px.choropleth(
                map_df,
                locations="location_country",
                locationmode="country names",
                color="failures_log",
                color_continuous_scale=[
                    "#fff5f0",
                    "#fcbba1",
                    "#fb6a4a",
                    "#cb181d",
                    "#67000d"
                ],
                hover_name="location_country",
                hover_data={
                    "failures": True,
                    "total_impact": ":,",
                    "avg_recovery": ":.1f",
                    "failures_log": False
                }
            )

            fig_map.update_layout(
                geo=dict(
                    showframe=False,
                    showcoastlines=True,
                    coastlinecolor="gray",
                    projection_type="natural earth"
                ),
                margin=dict(l=0, r=0, t=10, b=0)
            )

            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.warning("No map data available.")


# 📊 WHAT FAILS

with tab1:

    st.subheader("⚙️ What Equipment Fails Most?")

    freq = df_filtered['equipment_type'].value_counts().reset_index()
    freq.columns = ['equipment_type', 'failures']

    fig2 = px.bar(freq, x='equipment_type', y='failures', text='failures')
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("⚠️ Failure Types Distribution")

    ft = df_filtered['failure_type'].value_counts().reset_index()
    ft.columns = ['failure_type', 'count']

    fig3 = px.bar(ft, x='failure_type', y='count', text='count')
    st.plotly_chart(fig3, use_container_width=True)


# 📈 IMPACT ANALYSIS

with tab2:

    st.subheader("👥 Total Customer Impact by Equipment")

    total_impact = df_filtered.groupby('equipment_type')['affected_customers_count'].sum().reset_index()

    fig4 = px.bar(
        total_impact,
        x='equipment_type',
        y='affected_customers_count',
        text='affected_customers_count'
    )

    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("📊 Distribution of Impact")

    fig5 = px.histogram(
        df_filtered,
        x='affected_customers_count',
        nbins=30
    )

    st.plotly_chart(fig5, use_container_width=True)

# ⚠️ RISK RANKING

with tab3:

    st.subheader("⚠️ What Should Be Prioritized?")

    risk_by = st.selectbox("Rank By", ["Country", "Equipment"])

    group_col = 'location_country' if risk_by == "Country" else 'equipment_type'

    if df_filtered.empty:
        st.warning("No data available.")
    else:
        risk_df = df_filtered.groupby(group_col).agg({
            'failure_id': 'count',
            'affected_customers_count': 'sum',
            'recovery_duration_minutes': 'mean'
        }).reset_index()

        risk_df.columns = [
            group_col,
            'failures',
            'total_impact',
            'avg_recovery'
        ]

        risk_df['risk_score'] = (
            (risk_df['failures'] / risk_df['failures'].max()) * 0.4 +
            (risk_df['total_impact'] / risk_df['total_impact'].max()) * 0.4 +
            (risk_df['avg_recovery'] / risk_df['avg_recovery'].max()) * 0.2
        )

        risk_df = risk_df.sort_values(by='risk_score', ascending=False)

        fig6 = px.bar(
            risk_df.head(10),
            x=group_col,
            y='risk_score',
            color='risk_score',
            text='risk_score'
        )

        st.plotly_chart(fig6, use_container_width=True)
        st.dataframe(risk_df.head(10), use_container_width=True)

# 🤖 ML

with tab4:

    st.subheader("🔮 Predict Failure Severity")

    col1, col2 = st.columns(2)

    equipment_input = col1.selectbox("Equipment Type", df['equipment_type'].unique())
    failure_input = col1.selectbox("Failure Type", df['failure_type'].unique())
    country_input = col2.selectbox("Country", df['location_country'].unique())
    provider_input = col2.selectbox("Provider", df['provider_id'].unique())
    detected_input = col1.selectbox("Detected By", df['detected_by'].unique())
    customers_input = col2.number_input("Affected Customers", min_value=0, value=100)

    if st.button("Predict Severity"):

        input_df = pd.DataFrame({
            'equipment_type': [equipment_input],
            'failure_type': [failure_input],
            'location_country': [country_input],
            'provider_id': [provider_input],
            'detected_by': [detected_input],
            'affected_customers_count': [customers_input]
        })

        pred = pipeline.predict(input_df)[0]

        severity_map = {
            0: "🟢 Warning",
            1: "🟡 Minor",
            2: "🟠 Major",
            3: "🔴 Critical"
        }

        st.success(f"Prediction: {severity_map[pred]}")

        if pred >= 2:
            st.warning("⚠️ High severity — act immediately.")
        else:
            st.info("ℹ️ Monitor the situation.")

    st.markdown("---")

    st.subheader("📂 Batch Prediction")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        batch_df = pd.read_csv(uploaded_file)

        required_cols = [
            'equipment_type','failure_type','location_country',
            'provider_id','detected_by','affected_customers_count'
        ]

        if not all(col in batch_df.columns for col in required_cols):
            st.error("Missing required columns")
        else:
            preds = pipeline.predict(batch_df)

            batch_df['Predicted Severity'] = preds

            st.dataframe(batch_df)

            st.bar_chart(batch_df['Predicted Severity'].value_counts())

            csv = batch_df.to_csv(index=False).encode('utf-8')

            st.download_button(
                "Download Results",
                data=csv,
                file_name="predictions.csv"
            )