import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Airbnb's Rental Analysis - Carla Reynes")
df = pd.read_csv("airbnb.csv")

# Sidebar Filters
st.sidebar.header("Filter Options")
neighborhood = st.sidebar.multiselect("Select Neighbourhood", df["neighbourhood"].dropna().unique(), default=df["neighbourhood"].dropna().unique())
listing_type = st.sidebar.multiselect("Select Room Type", df["room_type"].dropna().unique(), default=df["room_type"].dropna().unique())

filtered_data = df[(df["neighbourhood"].isin(neighborhood)) & (df["room_type"].isin(listing_type))]

tab1, tab2, tab3 = st.tabs(["Airbnb's Overview", "Prices & Reviews", "Advanced Analysis"])

with tab1:
    st.subheader("Most Reviewed Airbnb's in Madrid")
    if "number_of_reviews" in df.columns:
        top_listings = df.sort_values(by="number_of_reviews", ascending=False).head(10)
        st.dataframe(top_listings[["name", "neighbourhood", "room_type", "price", "number_of_reviews"]])
        
        fig1 = px.bar(top_listings, x="name", y="number_of_reviews", color="neighbourhood",
                      title="Top 10 Most Reviewed Airbnb Rentals")
        st.plotly_chart(fig1)
    else:
        st.warning("Column 'number_of_reviews' not found in dataset.")
    
    if "minimum_nights" in df.columns:
        fig2 = px.box(filtered_data, x="room_type", y="minimum_nights", title="Minimum Nights by Listing Type")
        st.plotly_chart(fig2)
    else:
        st.warning("Column 'minimum_nights' not found in dataset.")
    
    if "reviews_per_month" in df.columns:
        top_reviews = df.groupby(["neighbourhood", "room_type"])["reviews_per_month"].sum().reset_index()
        fig3 = px.bar(top_reviews, x="neighbourhood", y="reviews_per_month", color="room_type",
                      title="Most Reviewed Airbnb Rentals per Month by Neighborhood")
        st.plotly_chart(fig3)
    else:
        st.warning("Column 'reviews_per_month' not found in dataset.")

with tab2:
    st.subheader("Prices and Reviews Analysis")
    if "price" in df.columns:
        fig4 = px.box(filtered_data, x="room_type", y="price", title="Price Distribution by Listing Type")
        st.plotly_chart(fig4)
    else:
        st.warning("Column 'price' not found in dataset.")
    
    if "number_of_reviews" in df.columns and "price" in df.columns:
        fig5 = px.scatter(filtered_data, x="number_of_reviews", y="price", color="room_type", opacity=0.6, title="Reviews vs Price")
        st.plotly_chart(fig5)
    else:
        st.warning("Columns 'number_of_reviews' or 'price' not found in dataset.")

# Price Recommendation based on selected filters
st.sidebar.subheader("Price Recommendation for Each Renting Type")
user_neighborhood = st.sidebar.selectbox("Select Neighborhood", df["neighbourhood"].dropna().unique())
user_listing_type = st.sidebar.selectbox("Select Listing Type", df["room_type"].dropna().unique())
user_people = st.sidebar.slider("Number of People", min_value=1, max_value=10, value=2)

# Define price adjustments based on number of guests
price_adjustments = {
    1: 0.9,  # 10% discount for solo travelers
    2: 1.0,  # Standard price
    3: 1.1,  # 10% increase for 3 guests
    4: 1.2,  # 20% increase for 4 guests
    5: 1.3,  # 30% increase for 5 guests
    6: 1.4,  # 40% increase for 6 guests
    7: 1.5,  # 50% increase for 7+ guests
    8: 1.6,
    9: 1.7,
    10: 1.8
}

if "price" in df.columns:
    filtered_price_data = df[(df["neighbourhood"] == user_neighborhood) & 
                              (df["room_type"] == user_listing_type)]
    
    if not filtered_price_data.empty:
        base_price = filtered_price_data["price"].median()
        adjusted_price = base_price * price_adjustments.get(user_people, 1.0)
        st.sidebar.write(f"Recommended Price: **${adjusted_price:.2f} per night**")
    else:
        st.sidebar.write("No sufficient data to recommend a price.")
else:
    st.sidebar.write("Column 'price' not found in dataset.")
