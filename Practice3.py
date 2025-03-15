import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Airbnb's rental Analysis - Carla Reynes")

@st.cache_data
def load_data():
    return pd.read_csv("airbnb.csv")

df = load_data()

# ---- SIDEBAR ----
st.sidebar.header("Filter Options")
neighborhood = st.sidebar.multiselect("Select neighbourhood", df["neighbourhood"].dropna().unique(), default=df["neighbourhood"].dropna().unique())
listing_type = st.sidebar.multiselect("Select room type", df["room_type"].dropna().unique(), default=df["room_type"].dropna().unique())

filtered_data = df[(df["neighbourhood"].isin(neighborhood)) & (df["room_type"].isin(listing_type))]

# ---- TABS ----
tab1, tab2 = st.tabs(["Airbnb's Overview", "Prices & Reviews from clients"])

# ---- TAB 1: Airbnb Listings Overview ----
with tab1:
    st.subheader("Most Reviewed Airbnb's in Madrid")

    # 🔹 Top Reviewed Airbnb Listings
    if "number_of_reviews" in df.columns:
        top_listings = df.sort_values(by="number_of_reviews", ascending=False).head(10)
        st.dataframe(top_listings[["name", "neighbourhood", "room_type", "price", "number_of_reviews"]])
        
        fig1 = px.bar(top_listings, x="name", y="number_of_reviews", color="neighbourhood",
                      title="Top 10 Most Reviewed Airbnb rentals")
        st.plotly_chart(fig1)
    else:
        st.warning("Column 'number_of_reviews' not found in dataset.")

    # 🔹 Minimum Nights by Listing Type
    if "minimum_nights" in df.columns:
        fig2 = px.box(filtered_data, x="room_type", y="minimum_nights", title="Minimum nights by Airbnb renting type")
        st.plotly_chart(fig2)
    else:
        st.warning("Column 'minimum_nights' not found in dataset.")

    # 🔹 Corrected Graph: Apartments with the Highest Reviews Per Month, Broken Down by Neighborhood
    if "reviews_per_month" in df.columns:
        top_reviews = df.groupby(["neighbourhood", "room_type"])["reviews_per_month"].sum().reset_index()
        fig3 = px.bar(top_reviews, x="neighbourhood", y="reviews_per_month", color="room_type",
                      title="Most reviewed Airbnb rentings per month by each neighborhood")
        st.plotly_chart(fig3)
    else:
        st.warning("Column 'reviews_per_month' not found in dataset.")

# ---- TAB 2: Prices & Reviews ----
with tab2:
    st.subheader("Prices and Reviews Analysis")

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
st.sidebar.subheader("Prices Recommendation for each renting type")
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
