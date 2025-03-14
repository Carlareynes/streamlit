import streamlit as st
import pandas as pd
import plotly.express as px

# ---- Load Data ----
st.title("Airbnb Analysis - Carla Reynes")  # Replace with your actual name

@st.cache_data
def load_data():
    return pd.read_csv("airbnb.csv")  # Ensure the file is in the same directory

df = load_data()

# ---- SIDEBAR ----
st.sidebar.header("Filter Options")
neighborhood = st.sidebar.multiselect("Select Neighborhood", df["neighbourhood"].dropna().unique(), default=df["neighbourhood"].dropna().unique())
listing_type = st.sidebar.multiselect("Select Listing Type", df["room_type"].dropna().unique(), default=df["room_type"].dropna().unique())

# Apply Filters
filtered_data = df[(df["neighbourhood"].isin(neighborhood)) & (df["room_type"].isin(listing_type))]

# ---- TABS ----
tab1, tab2 = st.tabs(["Listings Overview", "Price & Reviews"])

# ---- TAB 1: Listings Overview ----
with tab1:
    st.subheader("Top Hosts in Madrid")

    # Grouping and Sorting Hosts
    df_host = df.groupby(["host_id", "host_name"]).size().reset_index(name="listings_count")
    df_host_sorted = df_host.sort_values(by="listings_count", ascending=False).head(10)
    st.dataframe(df_host_sorted)

    # Visualizing Top Hosts
    host_selection = st.selectbox("How many hosts do you want to visualize?", [5, 10, 20, 50])
    top_hosts = df_host.sort_values(by="listings_count", ascending=False).head(host_selection)
    fig1 = px.bar(top_hosts, x="host_name", y="listings_count", title="Top Hosts with Most Listings")
    st.plotly_chart(fig1)

    # Relationship between listing type and minimum nights
    if "minimum_nights" in df.columns:
        fig2 = px.box(filtered_data, x="room_type", y="minimum_nights", title="Minimum Nights by Listing Type")
        st.plotly_chart(fig2)
    else:
        st.warning("Column 'minimum_nights' not found in dataset.")

# ---- TAB 2: Price & Reviews ----
with tab2:
    st.subheader("Price & Reviews Analysis")

    # Exploring price by listing type
    if "price" in df.columns:
        fig3 = px.box(filtered_data, x="room_type", y="price", title="Price Distribution by Listing Type")
        st.plotly_chart(fig3)
    else:
        st.warning("Column 'price' not found in dataset.")

    # Relationship between number of reviews and price
    if "number_of_reviews" in df.columns and "price" in df.columns:
        fig4 = px.scatter(filtered_data, x="number_of_reviews", y="price", color="room_type", opacity=0.6, title="Reviews vs Price")
        st.plotly_chart(fig4)
    else:
        st.warning("Columns 'number_of_reviews' or 'price' not found in dataset.")

# ---- Optional: Price Recommendation Simulator ----
st.sidebar.subheader("Price Recommendation Simulator")
user_neighborhood = st.sidebar.selectbox("Select Neighborhood", df["neighbourhood"].dropna().unique())
user_listing_type = st.sidebar.selectbox("Select Listing Type", df["room_type"].dropna().unique())
user_people = st.sidebar.slider("Number of People", min_value=1, max_value=10, value=2)

# Suggest price based on median values
if "price" in df.columns:
    price_recommendation = df[(df["neighbourhood"] == user_neighborhood) & 
                              (df["room_type"] == user_listing_type)]["price"].median()

    if not pd.isna(price_recommendation):
        st.sidebar.write(f"Recommended Price: **${price_recommendation:.2f} per night**")
    else:
        st.sidebar.write("No sufficient data to recommend a price.")
else:
    st.sidebar.write("Column 'price' not found in dataset.")

# ---- DEPLOYMENT INSTRUCTIONS ----
# To run locally: streamlit run your_script.py
# To deploy: Push to GitHub and connect to Streamlit Cloud

