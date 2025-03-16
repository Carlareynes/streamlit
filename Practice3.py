import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Airbnb's rental analysis - Carla Reynes")
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
                      title="Top 10 most reviewed Airbnb rentals")
        st.plotly_chart(fig1)
    else:
        st.warning("Column 'number_of_reviews' not found in dataset.")
    
    if "minimum_nights" in df.columns:
        fig2 = px.box(filtered_data, x="room_type", y="minimum_nights", title="Minimum nights by room type")
        st.plotly_chart(fig2)
    else:
        st.warning("Column 'minimum_nights' not found in dataset.")
    
    if "reviews_per_month" in df.columns:
        top_reviews = df.groupby(["neighbourhood", "room_type"])["reviews_per_month"].sum().reset_index()
        fig3 = px.bar(top_reviews, x="neighbourhood", y="reviews_per_month", color="room_type",
                      title="Most reviewed Airbnb rentals per month by neighborhood")
        st.plotly_chart(fig3)
    else:
        st.warning("Column 'reviews_per_month' not found in dataset.")

with tab2:
    st.subheader("Prices and Reviews Analysis")
    if "price" in df.columns:
        fig4 = px.box(filtered_data, x="room_type", y="price", title="Price distribution by rental type")
        st.plotly_chart(fig4)
    else:
        st.warning("Column 'price' not found in dataset.")
    
    if "number_of_reviews" in df.columns and "price" in df.columns:
        fig5 = px.scatter(filtered_data, x="number_of_reviews", y="price", color="room_type", opacity=0.6, title="Reviews vs Price")
        st.plotly_chart(fig5)
    else:
        st.warning("Columns 'number_of_reviews' or 'price' not found in dataset.")
with tab3:
    st.subheader("Top hosts and price distribution")
    st.subheader("Top hosts in Madrid")
    df_host = df.groupby(["host_name"]).size().reset_index(name="listings_count")
    df_host_sorted = df_host.sort_values(by="listings_count", ascending=False).head(10)
    st.dataframe(df_host_sorted)
    #select the number of hosts
    host_selection = st.selectbox("How many hosts do you want to visualize?", [5, 10, 20, 50])
    st.dataframe(df_host.sort_values(by="listings_count", ascending=False).head(host_selection))
    #visualize them
    fig_host = px.bar(df_host.sort_values(by="listings_count", ascending=False).head(host_selection),
                      x="host_name", y="listings_count", title="Top hosts with most Airbnbs")
    st.plotly_chart(fig_host)
    #price distribution per neightbourhood
    st.subheader("Price distribution per neighbourhood")
    df_filtered = df[["neighbourhood_group", "neighbourhood", "price"]].dropna()
    neighbourhood_selection = st.multiselect("Please select one or more neighbourhoods", 
                                             df_filtered["neighbourhood_group"].unique(), 
                                             default=df_filtered["neighbourhood_group"].unique())

    df_filtered = df_filtered[df_filtered["neighbourhood_group"].isin(neighbourhood_selection)]
    df_filtered = df_filtered[df_filtered["price"] < 500]  

    fig_price = px.box(df_filtered, x="neighbourhood", y="price", title="price distribution by neighbourhood ")
    st.plotly_chart(fig_price)
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
