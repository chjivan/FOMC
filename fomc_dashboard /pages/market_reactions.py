import streamlit as st
from datetime import datetime, timedelta
import plotly.express as px
import pandas as pd

# ----------------------------------------
# Configuration Variables
FOMC_TARGET_DATE = datetime(2024, 12, 18).date()

# Economic Projections
economic_projections = {
    "Year": ["2024 Q4", "2025 Q4", "2026 Q4"],
    "Rate Cuts (%)": [4.25, 3.6, 3.1],
    "GDP Growth (%)": [2.4, 2.0, 2.0],
    "Unemployment (%)": [4.2, 4.4, 4.4],
    "Core PCE Inflation (%)": [2.8, 2.2, 2.2],
}

# ----------------------------------------
# Functions

def display_countdown(target_date):
    """Display a countdown to the FOMC meeting date."""
    today = datetime.now().date()
    remaining_days = (target_date - today).days
    if remaining_days > 0:
        return f"{remaining_days} Days Remaining"
    elif remaining_days == 0:
        return "🚨 FOMC Meeting Today!"
    return "FOMC Meeting Completed"

def market_reactions_section():
    """Display market reactions to the Nov 6-7 FOMC meeting recap."""
    st.subheader("📊 Market Reactions: Nov 6-7 FOMC Recap")

    # Recap text
    st.markdown("""
    - **Recap**: At the November 6-7, 2024 FOMC meeting, the Federal Reserve cut the federal funds rate from **4.75%** to **4.50%**.  
    - Markets reacted positively, pricing in expectations of improved liquidity and economic stability.
    """)

    # Market data
    market_data = {
        "Date": ["2024-11-04", "2024-11-05", "2024-11-06", "2024-11-07"],
        "S&P 500": [5712.69, 5782.76, 5929.04, 5973.10],
        "Dow Jones": [41794.60, 42221.88, 43729.93, 43729.34],
        "NASDAQ": [18179.98, 18439.17, 18983.47, 19269.46],
    }
    df = pd.DataFrame(market_data)
    df["Date"] = pd.to_datetime(df["Date"]).dt.date  # Format date without time

    # Display table
    st.write("### Market Reaction Data")
    st.table(df.set_index("Date"))

    # Line chart visualization
    st.write("### Market Performance")
    fig = px.line(
        df,
        x="Date",
        y=["S&P 500", "Dow Jones", "NASDAQ"],
        title="Market Indices Performance During Nov 6-7 FOMC Recap",
        labels={"value": "Index Value", "variable": "Market Index"},
        markers=True
    )
    st.plotly_chart(fig)

    # Key Insights
    st.markdown("""
    **Key Insights**:
    - **S&P 500**: Rose by **4.6%**, indicating strong investor confidence.
    - **Dow Jones**: Increased by **4.6%**, reflecting optimism in broader markets.
    - **NASDAQ**: Surged **5.9%**, led by tech sector resilience.
    """)

def forward_guidance_section():
    """Interactive FOMC economic projections."""
    st.subheader("🔮 Forward Guidance: Rate Cuts and Economic Trends")
    st.write("The following projections summarize FOMC expectations for the economy:")

    # Display projections table
    df_projections = pd.DataFrame(economic_projections)
    st.table(df_projections)

    # Line chart visualization
    fig = px.line(
        df_projections,
        x="Year",
        y=["Rate Cuts (%)", "GDP Growth (%)", "Unemployment (%)", "Core PCE Inflation (%)"],
        title="FOMC Projections: Rates, GDP, Inflation, and Unemployment",
        labels={"value": "Percentage (%)", "variable": "Projection"},
        markers=True
    )
    st.plotly_chart(fig)

def fed_analysis_insights():
    """Summarize insights for the upcoming FOMC meeting."""
    st.subheader("📝 Key Insights: December 18, 2024 FOMC Meeting")
    st.markdown("""
    - **Expected Decision**: A **25bps rate cut** to **4.25%-4.50%** range.
    - **Economic Factors**:
        - **GDP Growth**: Stronger-than-expected at **2.4%** for 2024.
        - **Unemployment**: Expected to decline to **4.2%** by Q4 2024.
        - **Inflation**: Core PCE projected at **2.8%** in 2024.
    - **Forward Guidance**:
        - Gradual policy adjustments are expected to balance inflation risks and economic activity.
    """)

    st.info("🔍 **Focus Point**: Watch for Powell's remarks on balancing rate cuts with inflation expectations.")

# ----------------------------------------
# Streamlit App Layout
def main():
    """Render the Streamlit FOMC Insights app."""
    st.set_page_config(page_title="FOMC Insights and Countdown", page_icon="📊", layout="wide")

    # Title and countdown
    st.title("⏳ FOMC Countdown & Insights")
    st.markdown("## Countdown to Next FOMC Meeting")
    countdown = display_countdown(FOMC_TARGET_DATE)
    st.markdown(f"<h2 style='text-align: center; color: #FF5733;'>{countdown}</h2>", unsafe_allow_html=True)

    # Separator
    st.markdown("---")

    # Market Reactions Recap Section
    market_reactions_section()

    # Separator
    st.markdown("---")

    # Forward Guidance Section
    forward_guidance_section()

    # Separator
    st.markdown("---")

    # Key Insights Section
    fed_analysis_insights()

# ----------------------------------------
# Run App
if __name__ == "__main__":
    main()
