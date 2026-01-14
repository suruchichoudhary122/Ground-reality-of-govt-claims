import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Policy Gap Analyzer", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-title {text-align: center; color: #1f77b4; font-size: 2.5rem; margin-bottom: 1rem;}
    .metric-box {background: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center;}
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<p class="main-title">🔍 Policy-Practice Gap Detection</p>', unsafe_allow_html=True)
    
    # Load data
    try:
        df = pd.read_csv("pairs_with_predictions.csv")
    except:
        st.error("❌ Run your notebook first to generate predictions")
        return
    
    # Sidebar filters
    st.sidebar.header("🎛️ Controls")
    selected_labels = st.sidebar.multiselect("Filter Predictions", 
                                           options=sorted(df['predicted_label'].unique()),
                                           default=sorted(df['predicted_label'].unique()))
    min_confidence = st.sidebar.slider("Min Confidence", 0.0, 1.0, 0.0, 0.1)
    
    # Apply filters
    df_filtered = df[df['predicted_label'].isin(selected_labels)]
    df_filtered = df_filtered[df_filtered['confidence'] >= min_confidence]
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total", len(df_filtered))
    with col2: st.metric("✅ Fulfilled", (df_filtered['predicted_label'] == 'Fulfilled').sum())
    with col3: st.metric("❌ Unfulfilled", (df_filtered['predicted_label'] == 'Unfulfilled').sum())
    with col4: st.metric("🎯 Avg Confidence", f"{df_filtered['confidence'].mean():.2f}")
    
    # Visualizations
    col1, col2 = st.columns(2)
    with col1:
        fig_pie = px.pie(df_filtered, names='predicted_label', title='Prediction Distribution')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        fig_box = px.box(df_filtered, x='predicted_label', y='confidence', 
                        color='predicted_label', title='Confidence Analysis')
        st.plotly_chart(fig_box, use_container_width=True)
    
    # Data Explorer
    st.subheader("📋 Detailed Analysis")
    st.dataframe(df_filtered[['claim_text', 'report_text', 'predicted_label', 'confidence']], 
                use_container_width=True, height=300)

if __name__ == "__main__":
    main()