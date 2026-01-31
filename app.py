"""
Frontend module for UK Property Search application.
Streamlit UI that imports backend functions from main.py.
"""

import streamlit as st

# Import backend functions from main.py
from main import (
    search_properties, 
    get_uk_areas, 
    get_street_view_image_url, 
    is_full_postcode,
    sort_properties,
    validate_search_input
)

st.set_page_config(page_title="UK Property Search", layout="wide")

st.title("Property / Area Search")


def display_property_card(property_data: dict):
    """
    Display a single property card with image, current price, and future price.
    
    Parameters:
        property_data: Dictionary containing property information
            Expected keys (to be set by backend):
            - address: str
            - postcode: str (optional)
            - image_url: str (optional, will use Street View if not provided)
            - current_price: float/int (optional)
            - future_price: float/int (optional)
            - area: str (optional)
    """
    # Extract data with defaults for missing values
    address = property_data.get("address", "Address not available")
    postcode = property_data.get("postcode", "")
    area = property_data.get("area", "")
    
    # Image URL - use provided URL or generate Street View URL
    image_url = property_data.get("image_url")
    if not image_url:
        image_url = get_street_view_image_url(address, postcode)
    
    # Prices - will be set by backend, display placeholder if not available
    current_price = property_data.get("current_price")
    future_price = property_data.get("future_price")
    
    # Display the property card
    with st.container(border=True):
        # House Image
        st.image(
            image_url,
            use_container_width=True,
            caption=f"{address}" + (f", {postcode}" if postcode else "")
        )
        
        # Price information
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Current Price**")
            if current_price is not None:
                st.markdown(f"### £{current_price:,.0f}")
            else:
                st.markdown("### N/A")
        
        with col2:
            st.markdown("**Future Price**")
            if future_price is not None:
                st.markdown(f"### £{future_price:,.0f}")
                # Show price change indicator
                if current_price is not None:
                    change = future_price - current_price
                    change_pct = (change / current_price) * 100 if current_price > 0 else 0
                    if change >= 0:
                        st.caption(f"+£{change:,.0f} ({change_pct:+.1f}%)")
                    else:
                        st.caption(f"£{change:,.0f} ({change_pct:.1f}%)")
            else:
                st.markdown("### —")
                st.caption("Forecast pending")


def display_property_grid(properties: list, columns: int = 4):
    """
    Display properties in a grid layout.
    
    Parameters:
        properties: List of property dictionaries
        columns: Number of columns in the grid (default 4 as per sketch)
    """
    if not properties:
        st.info("No properties to display. Search for an area to see results.")
        return
    
    # Create grid rows
    for i in range(0, len(properties), columns):
        cols = st.columns(columns)
        for j, col in enumerate(cols):
            if i + j < len(properties):
                with col:
                    display_property_card(properties[i + j])



# Sidebar: Search Panel

with st.sidebar:
    st.header("Search")
    
    # Get areas from backend
    uk_areas = get_uk_areas()
    
    area = st.selectbox("Choose an area", uk_areas, index=0)
    query = st.text_input(
        "Search", 
        placeholder="e.g. Brixton, Aberdeen...",
        help="Enter a place/area name. For street search, use the fields below."
    )
    
    # Advanced search: Postcode District + Street
    with st.expander("Advanced: Search by Postcode District + Street"):
        st.caption("To search by street, provide BOTH the postcode district AND street name.")
        col_district, col_street = st.columns(2)
        with col_district:
            postcode_district = st.text_input(
                "Postcode District",
                placeholder="e.g. SW1A, NG8, SS0",
                help="The first part of a postcode (before the space)"
            )
        with col_street:
            street_name = st.text_input(
                "Street Name",
                placeholder="e.g. Downing Street, High Street",
                help="Street name within the postcode district"
            )
    
    submitted = st.button("Search", use_container_width=True, type="primary")



# Session State
if "results" not in st.session_state:
    st.session_state.results = []
if "last_search" not in st.session_state:
    st.session_state.last_search = {"area": None, "query": None}



# Search Trigger
if submitted:
    # Validate inputs using backend function
    error_message = validate_search_input(query, postcode_district, street_name)
    
    if error_message:
        st.error(error_message)
    else:
        with st.spinner("Searching properties..."):
            # Call backend search function with appropriate parameters
            results = search_properties(
                area=area, 
                query=query,
                postcode_district=postcode_district.strip() if postcode_district else "",
                street=street_name.strip() if street_name else ""
            )
            st.session_state.results = results
            st.session_state.last_search = {"area": area, "query": query or f"{postcode_district} {street_name}".strip()}


# Main Content: Display Results
last = st.session_state.last_search

# Initialize view state
if "current_view" not in st.session_state:
    st.session_state.current_view = "properties"  # Default to properties view

# Navigation tabs (clickable links)
tab_col1, tab_col2 = st.columns(2)

with tab_col1:
    if st.button("Individual Properties", use_container_width=True, 
                 type="primary" if st.session_state.current_view == "properties" else "secondary"):
        st.session_state.current_view = "properties"
        st.rerun()

with tab_col2:
    if st.button("Heatmap View", use_container_width=True,
                 type="primary" if st.session_state.current_view == "heatmap" else "secondary"):
        st.session_state.current_view = "heatmap"
        st.rerun()

st.divider()

# Show content based on selected view

if st.session_state.current_view == "properties":

    # Individual Properties View - Grid Layout (3 columns)
    st.subheader("Individual Properties")
    
    if last["area"] is None:
        st.info("Select an area to see property listings")
    else:
        results = st.session_state.results
        if results:
            # Sorting options
            sort_col1, sort_col2 = st.columns([3, 1])
            with sort_col1:
                st.success(f"Found {len(results)} properties in **{last['area']}**")
            with sort_col2:
                sort_option = st.selectbox(
                    "Sort by",
                    options=[
                        "Default",
                        "Current Price: Low to High",
                        "Current Price: High to Low",
                        "Future Price: Low to High",
                        "Future Price: High to Low"
                    ],
                    label_visibility="collapsed"
                )
            
            # Sort results based on selection (using backend function)
            sorted_results = sort_properties(results, sort_option)
            
            # Display properties in a 3-column grid
            columns_per_row = 3
            for row_start in range(0, len(sorted_results), columns_per_row):
                cols = st.columns(columns_per_row)
                for col_idx, col in enumerate(cols):
                    prop_idx = row_start + col_idx
                    if prop_idx < len(sorted_results):
                        prop = sorted_results[prop_idx]
                        address = prop.get("address", "Unknown")
                        postcode = prop.get("postcode", "")
                        current_price = prop.get("current_price")
                        future_price = prop.get("future_price")
                        
                        with col:
                            with st.container(border=True):
                                # House Image
                                image_url = prop.get("image_url")
                                if not image_url:
                                    image_url = get_street_view_image_url(address, postcode)
                                st.image(image_url, use_container_width=True)
                                
                                # Address
                                st.markdown(f"**{address}**")
                                if postcode:
                                    st.caption(postcode)
                                
                                # Price information
                                price_col1, price_col2 = st.columns(2)
                                with price_col1:
                                    st.caption("Current")
                                    if current_price:
                                        st.markdown(f"**£{current_price:,.0f}**")
                                    else:
                                        st.markdown("**N/A**")
                                with price_col2:
                                    st.caption("Future")
                                    if future_price:
                                        st.markdown(f"**£{future_price:,.0f}**")
                                    else:
                                        st.markdown("**—**")
                                
                                # View details button
                                if st.button("View Details", key=f"view_{prop_idx}", use_container_width=True):
                                    st.session_state.selected_property = prop_idx
        else:
            st.warning("No properties found. Try a different search.")

elif st.session_state.current_view == "heatmap":
    # Heatmap View
    st.subheader("Heatmap View")
    
    if last["area"] is None:
        st.info("Search for properties to see the heatmap here")
    else:
        st.caption(f"Showing results for: **{last['area']}** | Query: *{last['query'] or 'All'}*")
        
        results = st.session_state.results
        
        if results:
            st.success(f"Found {len(results)} properties")
            
            # Placeholder for heatmap - link to be added later
            st.info("Heatmap visualization coming soon...")
            
            # Placeholder container for future heatmap
            with st.container(border=True):
                st.markdown("""
                <div style="
                    height: 500px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                    flex-direction: column;
                ">
                    <span>Heatmap View</span>
                    <span style="font-size: 14px; font-weight: normal; margin-top: 10px;">Click to explore (coming soon)</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Button placeholder for future heatmap page link
                st.button("Open Full Heatmap", use_container_width=True, disabled=True,
                         help="Heatmap page coming soon")
        else:
            st.warning("No properties found. Try a different search.")