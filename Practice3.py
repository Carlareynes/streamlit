import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Airbnb Analysis - Carla Reynes")

@st.cache_data
def load_data():
    return pd.read_csv("airbnb.csv")

df = load_data()

# ---- SIDEBAR ----
st.sidebar.header("Filter Options")
neighborhood = st.sidebar.multiselect("Select neighborhood", df["neighbourhood"].dropna().unique(), default=df["neighbourhood"].dropna().unique())
listing_type = st.sidebar.multiselect("Select room type", df["room_type"].dropna().unique(), default=df["room_type"].dropna().unique())

filtered_data = df[(df["neighbourhood"].isin(neighborhood)) & (df["room_type"].isin(listing_type))]

# ---- TABS ----
tab1, tab2 = st.tabs(["Airbnb's Overview", "Prices & Reviews from Clients"])

# ---- TAB 1: Airbnb's Overview ----
with tab1:
    st.subheader("This year's top hosts in Madrid")

    # 🔹 Display Top Hosts
    df_host = df.groupby(["host_id", "host_name"]).size().reset_index(name="listings_count")
    df_host_sorted = df_host.sort_values(by="listings_count", ascending=False).head(10)
    st.dataframe(df_host_sorted)

    # 🔹 Select and Visualize Top Hosts
    host_selection = st.selectbox("How many hosts do you want to visualize?", [5, 10, 20, 50])
    top_hosts = df_host.sort_values(by="listings_count", ascending=False).head(host_selection)
    fig1 = px.bar(top_hosts, x="host_name", y="listings_count", title="Top Hosts with Most Listings")
    st.plotly_chart(fig1)

    # 🔹 Minimum Nights by Room Type
    if "minimum_nights" in df.columns:
        fig2 = px.box(filtered_data, x="room_type", y="minimum_nights", title="Minimum Nights by Airbnb's Room Types")
        st.plotly_chart(fig2)
    else:
        st.warning("Column 'minimum_nights' not found in dataset.")

    # 🔹 Top Reviewed Listings per Month by Neighborhood
    if "reviews_per_month" in df.columns:
        top_reviews = df.groupby(["neighbourhood", "room_type"])["reviews_per_month"].sum().reset_index()
        fig3 = px.bar(top_reviews, x="neighbourhood", y="reviews_per_month", color="room_type",
                      title="Top Reviewed Listings per Month by Neighborhood")
        st.plotly_chart(fig3)
    else:
        st.warning("Column 'reviews_per_month' not found in dataset.")

# ---- TAB 2: Prices & Reviews from Clients ----
with tab2:
    st.subheader("Price & Reviews Analysis")

    # 🔹 Price by Listing Type
    if "price" in df.columns:
        fig4 = px.box(filtered_data, x="room_type", y="price", title="Price Distribution by Listing Type")
        st.plotly_chart(fig4)
    else:
        st.warning("Column 'price' not found in dataset.")

    # 🔹 Reviews vs. Price Relationship
    if "number_of_reviews" in df.columns and "price" in df.columns:
        fig5 = px.scatter(filtered_data, x="number_of_reviews", y="price", color="room_type", opacity=0.6, title="Reviews vs Price")
        st.plotly_chart(fig5)
    else:
        st.warning("Columns 'number_of_reviews' or 'price' not found in dataset.")

# ---- Price Recommendation Simulator (Optional) ----
st.sidebar.subheader("Price Recommendation Simulator")
user_neighborhood = st.sidebar.selectbox("Select Neighborhood", df["neighbourhood"].dropna().unique())
user_listing_type = st.sidebar.selectbox("Select Listing Type", df["room_type"].dropna().unique())
user_people = st.sidebar.slider("Number of People", min_value=1, max_value=10, value=2)

if "price" in df.columns:
    price_recommendation = df[(df["neighbourhood"] == user_neighborhood) & 
                              (df["room_type"] == user_listing_type)]["price"].median()

    if not pd.isna(price_recommendation):
        st.sidebar.write(f"Recommended Price: **${price_recommendation:.2f} per night**")
    else:
        st.sidebar.write("No sufficient data to recommend a price.")
else:
    st.sidebar.write("Column 'price' not found in dataset.")
