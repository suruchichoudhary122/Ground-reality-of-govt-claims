import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Policy Gap Analyzer", layout="wide")

# ---------- CUSTOM STYLING ----------
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #004C97;
        font-size: 2.7rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
    }
    .metric-box {
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-size: 1.2rem;
    }
    .fulfilled { background: #2ca02c; }
    .unfulfilled { background: #d62728; }
    .neutral { background: #ff7f0e; }
</style>
""", unsafe_allow_html=True)

# ---------- MAIN APP ----------
def main():
    st.markdown('<p class="main-title">🔍 AI-Powered Policy–Practice Gap Analyzer</p>', unsafe_allow_html=True)
    st.write("Use this dashboard to visualize how government claims align (or conflict) with ground reports using an NLI model.")

    # ---------- LOAD DATA ----------
    try:
        df = pd.read_csv("pairs_with_predictions.csv")
    except FileNotFoundError:
        st.error("❌ Missing file: `pairs_with_predictions.csv`. Run your detection script first.")
        return

    # ---------- SIDEBAR FILTERS ----------
    st.sidebar.header("🎛️ Controls")
    selected_labels = st.sidebar.multiselect(
        "Filter by Prediction", 
        options=sorted(df['predicted_label'].unique()),
        default=sorted(df['predicted_label'].unique())
    )
    min_confidence = st.sidebar.slider("Minimum Confidence", 0.0, 1.0, 0.3, 0.05)

    # ---------- APPLY FILTERS ----------
    df_filtered = df[
        (df['predicted_label'].isin(selected_labels)) &
        (df['confidence'] >= min_confidence)
    ]

    # ---------- METRICS ----------
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-box neutral'>Total<br><b>{len(df_filtered)}</b></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-box fulfilled'>Fulfilled<br><b>{(df_filtered['predicted_label'] == 'Fulfilled').sum()}</b></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-box unfulfilled'>Unfulfilled<br><b>{(df_filtered['predicted_label'] == 'Unfulfilled').sum()}</b></div>", unsafe_allow_html=True)
    with col4:
        avg_conf = df_filtered['confidence'].mean() if len(df_filtered) > 0 else 0
        st.markdown(f"<div class='metric-box neutral'>Avg Confidence<br><b>{avg_conf:.2f}</b></div>", unsafe_allow_html=True)

    st.markdown("---")

    # ---------- VISUALS ----------
    col1, col2 = st.columns(2)
    with col1:
        fig_pie = px.pie(
            df_filtered, 
            names='predicted_label', 
            title="Prediction Distribution",
            color='predicted_label',
            color_discrete_map={'Fulfilled': '#2ca02c', 'Unfulfilled': '#d62728', 'Neutral / Unclear': '#ff7f0e'}
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        fig_bar = px.bar(
            df_filtered,
            x='predicted_label',
            y='confidence',
            color='predicted_label',
            title="Confidence per Prediction",
            color_discrete_map={'Fulfilled': '#2ca02c', 'Unfulfilled': '#d62728', 'Neutral / Unclear': '#ff7f0e'}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # ---------- DETAILED TABLE ----------
    st.markdown("### 📋 Detailed Results")
    styled_df = df_filtered[['claim_text', 'report_text', 'predicted_label', 'confidence']].copy()
    st.dataframe(styled_df, use_container_width=True, height=400)

    st.markdown("---")
    st.info("✅ Tip: Adjust filters from the sidebar to explore specific confidence levels or outcome categories.")

# ---------- ENTRY POINT ----------
if __name__ == "__main__":
    main()
