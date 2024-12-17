import streamlit as st
import pandas as pd
import plotly.express as px

# Load Real Historical Interest Rate Data
def load_interest_rate_data():
    """
    Load real historical Fed Funds Rate data.
    """
    data = {
        "Date": [
            "2024-11-07", "2024-09-18", "2024-07-31", "2024-06-12", "2024-05-01",
            "2024-03-20", "2024-01-31", "2023-12-13", "2023-11-01", "2023-09-20",
            "2023-07-26", "2023-06-14", "2023-05-03", "2023-03-22", "2023-02-01",
            "2022-12-14", "2022-11-02", "2022-09-21", "2022-07-27", "2022-06-15",
            "2022-05-04", "2022-03-16", "2020-11-05"
        ],
        "Fed Funds Rate": [
            4.50, 4.75, 5.25, 5.25, 5.25, 5.25, 5.25, 5.25, 5.25, 5.25,
            5.25, 5.00, 5.00, 4.75, 4.50, 4.25, 3.75, 3.00, 2.25, 1.50,
            0.75, 0.25, 0.00
        ],
    }
    df = pd.DataFrame(data)
    df["Date"] = pd.to_datetime(df["Date"])  # Ensure Date column is in datetime format
    return df

# Main App Render Function
def render():
    """Render the Interest Rate Trends page."""
    st.title("📉 Historical Interest Rate Trends")
    st.markdown("""
    Visualize **real historical Fed Funds Rate** data over a selected time range.  
    Use the interactive chart below to analyze trends and key policy changes.
    """)

    # Load Data
    df = load_interest_rate_data()

    # Date Range Selection - Above the Chart
    st.subheader("📅 Select Date Range")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", df["Date"].min())
    with col2:
        end_date = st.date_input("End Date", df["Date"].max())

    # Error handling for invalid date range
    if start_date > end_date:
        st.error("Start date must be before or equal to the end date.")
        st.stop()

    # Filter Data Based on User Selection
    filtered_df = df[(df["Date"] >= pd.to_datetime(start_date)) &
                     (df["Date"] <= pd.to_datetime(end_date))]

    # Plotly Visualization
    st.subheader("📊 Federal Funds Rate Over Selected Time Range")
    fig = px.line(
        filtered_df,
        x="Date",
        y="Fed Funds Rate",
        title="Federal Funds Rate Trends",
        labels={"Fed Funds Rate": "Interest Rate (%)", "Date": "Date"},
        markers=True,
        template="plotly_white",
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=6))
    st.plotly_chart(fig, use_container_width=True)

    # Insights Section
    st.subheader("📌 Key Insights")
    st.markdown("""
    - Explore how the Federal Funds Rate has evolved in response to economic conditions.  
    - Analyze periods of rate hikes or cuts during events like the **COVID-19 Pandemic** or **high inflation periods**.
    - Recent data indicates how the Fed is managing rates to stabilize the economy.
    """)

    st.info("""
    💡 **Tip**: Compare specific time ranges to understand rate changes' impact on borrowing, mortgages, and financial markets.
    """)

# Main Execution
if __name__ == "__main__":
    st.set_page_config(page_title="Historical Interest Rates", page_icon="📉", layout="wide")
    render()
