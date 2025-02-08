# README.md

---

## **Restaurant wise Delivery point**

This Streamlit-based application visualizes the relationship between restaurants and their delivery networks. It allows users to filter data by zone and restaurant, calculates distances using the Haversine formula, and provides an interactive map visualization of restaurant-to-delivery connections. Additionally, it offers insights into daily order trends and average delivery statistics.

---

### **Prerequisites for Running the Code**

Before running this application, ensure you have the following prerequisites installed:

1. **Python Environment**: Python 3.8 or higher is required.
2. **Required Libraries**:
   - Install the necessary libraries using `pip`:
     ```bash
     pip install streamlit pandas numpy plotly
     ```
   - If you encounter any issues with specific versions, consider creating a virtual environment:
     ```bash
     python -m venv env
     source env/bin/activate  # On Windows: env\Scripts\activate
     pip install -r requirements.txt
     ```
3. **Input Data Files**:
   - The application relies on two CSV files:
     - `restaurants_lat_long.csv`: Contains restaurant details, including latitude, longitude, and zone information.
     - `order_data.csv`: Contains order details, including delivery coordinates, order IDs, and dates.
   - Ensure these files are placed in the same directory as the script or provide the correct file paths in the code.

4. **Streamlit Framework**:
   - To run the application, use the following command:
     ```bash
     streamlit run app.py
     ```
   - Re**place `app.py` with the name of your Python script if it differs.

---
**Step- 1: Need to filter zone**

![Alt text](images\1.png?raw=true "Title")

**Step- 2: Need to filter Restturants under selected zone**

![Alt text](images\2.png?raw=true "Title")

**Step- 3: Map View**

![Alt text](images\3.png?raw=true "Title")

green circle resembles the delivery points. On hover this will show Order number, Order Date & Distance from restaurants.

**Step- 4: Daily Order Trendline View**

![Alt text](images\4.png?raw=true "Title")

### **Main Features of the Code**

1. **Interactive Filtering**:
   - Users can filter data by selecting a specific zone and restaurant from dropdown menus in the sidebar.
   - A "Show Relation" button triggers the visualization process based on the selected filters.
    ```
        zones = sorted(df["ZoneName"].unique())
        zone_options = ["Select Zone"] + zones
        selected_zone = st.sidebar.selectbox("Select Zone Name", options=zone_options)
    ```

2. **Distance Calculation**:
   - The Haversine formula is implemented in a vectorized manner using NumPy for efficient computation of distances between restaurant locations and delivery points.

3. **Interactive Map Visualization**:
   - Built using Plotly's `Scattermap`, the map displays:
     - Restaurant locations (marked with star icons).
     - Delivery points (marked with circle icons).
     - Connection lines between restaurants and delivery points.
   - Hover interactions provide detailed information about restaurants, orders, and computed distances.

4. **Daily Order Trends**:
   - The application analyzes order data to compute:
     - Average daily order deliveries.
     - Daily order trends displayed as a line chart.

5. **Responsive Layout**:
   - The interface is designed to adapt to different screen sizes, with the map occupying 80% of the screen width and summary statistics displayed in the remaining space.

---

### **What This Application Does**

The primary purpose of this application is to provide a comprehensive visualization of the relationship between restaurants and their delivery networks. Specifically:

- **Zone and Restaurant Filtering**:
  - Users can explore data for specific zones and restaurants, enabling targeted analysis.
  
- **Geospatial Visualization**:
  - The map highlights the spatial distribution of delivery points relative to the selected restaurant, helping identify patterns such as delivery density and proximity.

- **Distance Insights**:
  - By calculating the distance between restaurants and delivery points, the application provides valuable insights into logistics and operational efficiency.

- **Order Trend Analysis**:
  - The application summarizes daily order trends, offering actionable insights for demand forecasting and resource allocation.

---

### **Unique Approaches and Technical Highlights**

1. **Vectorized Haversine Distance Calculation**:
   - Instead of using iterative loops, the Haversine formula is applied in a vectorized manner using NumPy. This approach significantly improves performance, especially for large datasets.

2. **Efficient Data Loading with Caching**:
   - The `@st.cache_data` decorator ensures that data loading and preprocessing are performed only once, reducing redundant computations and improving application responsiveness.

3. **Dynamic Map Centering**:
   - The map dynamically centers on the selected restaurant's location, ensuring optimal visibility of delivery points and connection lines.

4. **Custom Hover Templates**:
   - Plotly's hover templates are customized to display relevant information, such as restaurant names, order IDs, delivery dates, and computed distances, enhancing user experience.

5. **Separation of Concerns**:
   - The code is modular, with distinct sections for data loading, filtering, distance calculation, and visualization. This structure promotes readability, maintainability, and scalability.

6. **OpenStreetMap Integration**:
   - The map uses OpenStreetMap as the base layer, providing a familiar and visually appealing geographic context.

7. **Error Handling**:
   - The application gracefully handles edge cases, such as missing data or invalid filters, by displaying appropriate warnings or fallback messages.

---

### **Potential Enhancements**

While the current implementation is robust, there are several opportunities for enhancement:

1. **Advanced Filtering Options**:
   - Add filters for date ranges, order statuses, or delivery times to enable more granular analysis.

2. **Cluster Analysis**:
   - Implement clustering algorithms (e.g., DBSCAN) to identify high-density delivery areas and optimize routing strategies.

3. **Export Functionality**:
   - Allow users to export filtered data, visualizations, or summary statistics in formats like CSV or PDF.

4. **Real-Time Data Integration**:
   - Integrate real-time data streams for dynamic updates, enabling live monitoring of delivery operations.

5. **Mobile Optimization**:
   - Further optimize the layout for mobile devices to improve accessibility.

---

### **Conclusion**

This application serves as a powerful tool for analyzing and visualizing restaurant delivery networks. Its combination of geospatial visualization, distance computation, and trend analysis provides valuable insights for optimizing logistics and improving customer satisfaction. By leveraging modern libraries like Streamlit and Plotly, the application delivers an intuitive and interactive user experience while maintaining high performance and scalability.

For questions or feedback, please contact.