import pandas as pd
import plotly.express as px
import streamlit as st
import os

# Set up the page configuration
st.set_page_config(
    page_title="FOMC SEP Projections and Library",
    page_icon="📊",
    layout="wide"
)

# Function to render the SEP Projections
def render_projections():
    """Render the SEP Projections Page."""
    st.title("📊 FOMC Projections: Understanding the Importance of Voting")
    st.markdown("""
    The **Federal Open Market Committee (FOMC)** sets monetary policy by voting on key interest rate decisions.  
    These votes are critical because they determine the **federal funds rate**, impacting **inflation control**, **employment growth**, and **economic stability**.

    ### Why FOMC Votes Matter:
    - **Consensus Building**: The FOMC's voting decisions reflect the collective economic outlook of top policymakers.
    - **Market Impact**: Financial markets closely follow voting outcomes to anticipate changes in interest rates and economic growth.
    - **Projections Guide Policy**: Each vote contributes to the **Summary of Economic Projections (SEP)**, providing insights into where interest rates are likely headed.

    ### Explore SEP Projections
    Use the interactive chart below to see how FOMC participants project interest rate ranges over the coming years.  
    These projections reflect the balance of risks between controlling inflation and fostering employment.
    """)

    # Data preparation
    data = {
        "Rate (%)": [
            "2-2.25", "2.25-2.5", "2.5-2.75", "2.75-3", "3.0-3.25", "3.25-3.5",
            "3.5-3.75", "3.75-4", "4-4.25", "4.25-4.5", "4.5-4.75", "4.75-5",
            "5.25-5.5", "5.5-5.75", "5.75-6"
        ],
        "2024": [0, 0, 0, 0, 0, 0, 0, 0, 1, 9, 7, 2, 0, 0, 0],
        "2025": [0, 0, 0, 0, 2, 6, 6, 3, 1, 1, 0, 0, 0, 0, 0],
        "2026": [0, 1, 3, 6, 2, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0],
        "2027": [0, 2, 3, 5, 2, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0],
    }

    # Convert data to DataFrame and reshape it
    df = pd.DataFrame(data)
    df_melted = df.melt(id_vars=["Rate (%)"], var_name="Year", value_name="Count")

    # User selection for year
    st.subheader("🔍 Explore Projections by Year")
    selected_year = st.selectbox("📅 **Select a Year:**", options=["2024", "2025", "2026", "2027"])

    # Filter data for the selected year
    filtered_data = df_melted[(df_melted["Year"] == selected_year) & (df_melted["Count"] > 0)]

    # Show a warning if no data is available
    if filtered_data.empty:
        st.warning(f"No projections available for {selected_year}.")
        return

    # Bar chart visualization
    fig = px.bar(
        filtered_data,
        x="Rate (%)",
        y="Count",
        title=f"📈 Federal Funds Rate Projections for {selected_year}",
        labels={"Count": "Number of Participants", "Rate (%)": "Rate Range (%)"},
        color="Rate (%)",
        color_discrete_sequence=px.colors.sequential.Blues,
    )
    fig.update_layout(
        xaxis_title="Rate Range (%)",
        yaxis_title="Number of Participants",
        template="plotly_white",
        font=dict(size=14),
        title_x=0.5,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Insights Section
    st.subheader("📌 Key Takeaways")
    st.markdown(f"""
    - **Voting Dynamics**: FOMC members' votes reflect their confidence in the economic outlook, balancing inflationary risks with growth potential.
    - **Projections in {selected_year}**:
        - Higher rates signal a stronger commitment to inflation control.
        - Lower rates indicate concerns about economic slowdown or employment risks.
    - **Market Relevance**: Projections influence stock and bond market movements, shaping trading strategies and long-term investments.
    """)
    st.info("💡 These insights help you align your financial decisions with FOMC policy expectations.")

# Function to render the SEP Library
def render_library():
    """Render the SEP Library Page."""
    st.title("📚 FOMC SEP Files Library")
    st.markdown("""
    Access historical and recent **Summary of Economic Projections (SEP)** files to delve deeper into the Federal Reserve's outlook on key economic indicators.  
    These files are essential for understanding the Fed's approach to inflation, employment, and overall economic stability.
    """)

    # FOMC meeting dates and corresponding SEP file names
    fomc_meetings = [
        {"Date": "January 31, 2023", "File Name": "fomcprojtabl20230131.pdf"},
        {"Date": "March 22, 2023", "File Name": "fomcprojtabl20230322.pdf"},
        {"Date": "June 14, 2023", "File Name": "fomcprojtabl20230614.pdf"},
        {"Date": "September 20, 2023", "File Name": "fomcprojtabl20230920.pdf"},
        {"Date": "December 13, 2023", "File Name": "fomcprojtabl20231213.pdf"},
        {"Date": "March 20, 2024", "File Name": "fomcprojtabl20240320.pdf"},
        {"Date": "June 19, 2024", "File Name": "fomcprojtabl20240619.pdf"},
        {"Date": "September 18, 2024", "File Name": "fomcprojtabl20240918.pdf"},
        {"Date": "December 11, 2024", "File Name": "fomcprojtabl20241211.pdf"},
    ]

    # Base URL for SEP files
    base_url = "https://www.federalreserve.gov/monetarypolicy/files/"

    # Create a DataFrame
    df = pd.DataFrame(fomc_meetings)
    df["Download Link"] = df["File Name"].apply(lambda x: base_url + x)

    # Selection Box
    st.subheader("📥 Download SEP Files by Meeting Date")
    selected_date = st.selectbox("Select a Meeting Date:", ["Select a date"] + list(df["Date"]))

    if selected_date != "Select a date":
        # Filter the selected row
        selected_row = df[df["Date"] == selected_date]
        selected_file = selected_row["File Name"].values[0]
        selected_link = selected_row["Download Link"].values[0]

        # Show the selected file details
        st.write(f"**Selected Meeting Date:** {selected_date}")
        st.write(f"**File Name:** {selected_file}")
        st.markdown(f"[Click here to download the file]({selected_link})", unsafe_allow_html=True)

        # Display the full table
        st.subheader("📋 Full List of Available SEP Files")
        st.dataframe(df[["Date", "File Name", "Download Link"]], use_container_width=True)
    else:
        st.info("Please select a date to view details and access the full table.")

# Render the combined app
def main():
    st.sidebar.title("📋 Navigation")
    option = st.sidebar.radio(
        "Choose a feature:",
        ["SEP Projections", "SEP Library"]
    )

    if option == "SEP Projections":
        render_projections()
    elif option == "SEP Library":
        render_library()

if __name__ == "__main__":
    main()
