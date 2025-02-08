import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go


# -----------------------
# Data Loading with Cache
# -----------------------
@st.cache_data
def load_data():
    restaurants = pd.read_csv("restaurants_lat_long.csv").dropna(axis=1, how="all")
    orders = pd.read_csv("order_data.csv").dropna(axis=1, how="all")
    merged_df = pd.merge(
        orders, restaurants, left_on="BranchId", right_on="id", how="inner"
    )
    return merged_df


df = load_data()

st.title("Restaurant wise Delivery Points")

# -----------------------------
# Sidebar: Zone and Restaurant Filters
# -----------------------------
zones = sorted(df["ZoneName"].unique())
zone_options = ["Select Zone"] + zones
selected_zone = st.sidebar.selectbox("Select Zone Name", options=zone_options)

if selected_zone != "Select Zone":
    df_zone = df[df["ZoneName"] == selected_zone]
    restaurants_in_zone = sorted(df_zone["primaryrestautantname"].unique())
    restaurant_options = ["Select Restaurant"] + restaurants_in_zone
    selected_restaurant = st.sidebar.selectbox(
        "Select Restaurant", options=restaurant_options
    )
else:
    selected_restaurant = None


if (selected_zone != "Select Zone") and (
    selected_restaurant and selected_restaurant != "Select Restaurant"
):
    if st.sidebar.button("Show Relation"):
        # ----------------------------
        # Filter Data Based on Selections
        # ----------------------------
        filtered_df = df[
            (df["ZoneName"] == selected_zone)
            & (df["primaryrestautantname"] == selected_restaurant)
        ]
        if filtered_df.empty:
            st.warning("No data available for the selected filters.")
        else:
            # -------------------------------------------
            # Vectorized Haversine Distance Calculation
            # -------------------------------------------
            def haversine_vectorized(lat1, lon1, lat2, lon2):
                R = 6371.0  # Earth radius in km
                lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
                dlat = lat2 - lat1
                dlon = lon2 - lon1
                a = (
                    np.sin(dlat / 2) ** 2
                    + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
                )
                c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
                return R * c

            filtered_df = filtered_df.copy()  # Avoid SettingWithCopyWarning
            filtered_df["distance_km"] = haversine_vectorized(
                filtered_df["Latitude"],
                filtered_df["Longitude"],
                filtered_df["DeliveryLat"],
                filtered_df["DeliveryLong"],
            ).round(2)

            # -------------------------------------------
            # Prepare Data for Map Visualization
            # -------------------------------------------
            # Restaurant data: location and name.
            restaurant_data = filtered_df[
                ["Latitude", "Longitude", "Name", "ZoneName"]
            ].rename(
                columns={
                    "Latitude": "lat",
                    "Longitude": "lon",
                    "Name": "restaurant_name",
                }
            )

            # Delivery data: includes order id, order date, and computed distance.
            delivery_data = filtered_df[
                ["DeliveryLat", "DeliveryLong", "OrderId", "order_date", "distance_km"]
            ].rename(
                columns={
                    "DeliveryLat": "lat",
                    "DeliveryLong": "lon",
                    "OrderId": "order_id",
                }
            )

            # Build a single trace for connection lines
            edge_lat = []
            edge_lon = []
            for _, row in filtered_df.iterrows():
                edge_lat.extend([row["Latitude"], row["DeliveryLat"], None])
                edge_lon.extend([row["Longitude"], row["DeliveryLong"], None])
            edge_trace = go.Scattermap(
                lat=edge_lat,
                lon=edge_lon,
                mode="lines",
                line=dict(width=2, color="gray"),
                hoverinfo="none",
                showlegend=False,
            )

            # -------------------------
            # Create the Map Figure using Scattermap
            # -------------------------
            fig = go.Figure()

            # Add connection lines
            fig.add_trace(edge_trace)

            # Restaurant Marker (star icon with restaurant name on hover)
            fig.add_trace(
                go.Scattermap(
                    lat=restaurant_data["lat"],
                    lon=restaurant_data["lon"],
                    mode="markers",
                    marker=dict(symbol="star", size=14, color="blue"),
                    text=restaurant_data["restaurant_name"],
                    hovertemplate="<b>Restaurant:</b> %{text}<extra></extra>",
                    name="Restaurant",
                )
            )

            # Delivery Marker (circle marker with order details on hover)
            fig.add_trace(
                go.Scattermap(
                    lat=delivery_data["lat"],
                    lon=delivery_data["lon"],
                    mode="markers",
                    marker=dict(symbol="circle", size=10, color="green"),
                    text=delivery_data["order_id"],
                    customdata=np.stack(
                        (
                            delivery_data["order_date"].astype(str),
                            delivery_data["distance_km"].astype(str),
                        ),
                        axis=-1,
                    ),
                    hovertemplate=(
                        "<b>Order ID:</b> %{text}<br>"
                        + "<b>Date:</b> %{customdata[0]}<br>"
                        + "<b>Distance:</b> %{customdata[1]} km<extra></extra>"
                    ),
                    name="Delivery",
                )
            )


            # Center the map on the restaurant's location
            center_lat = restaurant_data["lat"].mean()
            center_lon = restaurant_data["lon"].mean()

            # Update layout using the new 'map' property with an open-street-map style
            fig.update_layout(
                map=dict(
                    style="open-street-map",
                    center=dict(lat=center_lat, lon=center_lon),
                    zoom=12,
                ),
                margin={"r": 0, "t": 30, "l": 0, "b": 0},
                height=800,
                title="Restaurant and Delivery Network",
            )

            # -------------------------
            # Display Map in 80% of the Screen Width
            # -------------------------
            
            st.plotly_chart(fig, use_container_width=True)

            # -------------------------------------------------
            # Restaurant Summary & Daily Order Trends Summary
            # -------------------------------------------------
            # Convert order_date to datetime and group by date
            filtered_df["order_date"] = pd.to_datetime(
                filtered_df["order_date"], errors="coerce"
            )
            daily_orders = (
                filtered_df.groupby(filtered_df["order_date"].dt.date)
                .size()
                .reset_index(name="orders")
            )
            avg_daily_orders = (
                daily_orders["orders"].mean() if not daily_orders.empty else 0
            )

            st.subheader("Restaurant Summary")
            st.write(f"**Average Daily Order Delivery:** {avg_daily_orders:.2f}")

            # Create a line chart for daily order trends using Plotly
            line_fig = go.Figure()
            line_fig.add_trace(
                go.Scatter(
                    x=daily_orders["order_date"],
                    y=daily_orders["orders"],
                    mode="lines+markers",
                    name="Daily Orders",
                )
            )
            line_fig.update_layout(
                title="Daily Order Trends",
                xaxis_title="Date",
                yaxis_title="Number of Orders",
                margin={"r": 0, "t": 30, "l": 0, "b": 0},
            )
            st.plotly_chart(line_fig, use_container_width=True)