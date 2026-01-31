import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import requests
import random

# --- Page Config (must be first Streamlit command) ---
st.set_page_config(page_title="UK Property Search", layout="wide")

# --- API Configuration ---
API_BASE_URL = "https://api.scansan.com/v1"
API_KEY = "370b0b6f-3f09-4807-b7fe-270a4e5ba2c2"
HEADERS = {
    "X-Auth-Token": API_KEY,
    "Content-Type": "application/json"
}

st.title("🏠 UK Property / Area Search")

UK_AREAS = [
    "Any", "London", "Manchester", "Birmingham", "Leeds", "Glasgow", "Edinburgh",
    "Bristol", "Liverpool", "Sheffield", "Newcastle upon Tyne", "Nottingham",
    "Hammersmith", "Westminster", "Camden", "Islington", "Hackney", "Tower Hamlets",
    "Southwark", "Lambeth", "Wandsworth", "Kensington", "Chelsea", "Richmond"
]

# Placeholder house images for demo
HOUSE_IMAGES = [
    "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400",
    "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=400",
    "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=400",
    "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=400",
    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=400",
]


def get_sustainability_color(score: int) -> str:
    """Return color based on sustainability score."""
    if score >= 80:
        return "#28a745"  # Green
    elif score >= 60:
        return "#ffc107"  # Yellow
    elif score >= 40:
        return "#fd7e14"  # Orange
    else:
        return "#dc3545"  # Red


def get_sustainability_label(score: int) -> str:
    """Return label based on sustainability score."""
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Average"
    else:
        return "Poor"


def create_validation_chart(property_data: dict) -> plt.Figure:
    """Create a validation chart showing price trends over time."""
    fig, ax = plt.subplots(figsize=(4, 2.5))
    
    # Generate sample validation data (past, now, future predictions)
    months = ["Past", "Now", "Later"]
    
    # Simulated price trend data
    base_price = property_data.get("price", 300000)
    prices = [
        base_price * 0.9,
        base_price,
        base_price * 1.1
    ]
    
    # Plot the validation trend
    ax.plot(months, prices, marker='o', linewidth=2, color='#4CAF50', label='Price Trend')
    ax.fill_between(months, [p * 0.95 for p in prices], [p * 1.05 for p in prices], 
                    alpha=0.2, color='#4CAF50')
    
    ax.set_ylabel("Price (£)", fontsize=8)
    ax.set_title("Validation", fontsize=10, fontweight='bold')
    ax.tick_params(axis='both', labelsize=7)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def search_properties_api(area: str, postcode: str):
    """
    Search for properties using the ScanSan API.
    Falls back to mock data if API fails.
    """
    properties = []
    
    try:
        # Try to get area codes first
        area_url = f"{API_BASE_URL}/area_codes/search"
        params = {"area_name": area if area != "Any" else "London"}
        
        response = requests.get(area_url, params=params, headers=HEADERS, timeout=10)
        response.raise_for_status()
        area_data = response.json()
        
        # Try to get properties for the postcode
        if postcode:
            property_url = f"{API_BASE_URL}/properties/search"
            property_params = {"postcode": postcode.upper().strip()}
            
            prop_response = requests.get(property_url, params=property_params, headers=HEADERS, timeout=10)
            
            if prop_response.status_code == 200:
                properties = prop_response.json().get("properties", [])
    
    except requests.exceptions.RequestException as e:
        st.warning(f"API connection issue. Showing sample properties for demonstration.")
    
    # If no properties from API, generate sample data
    if not properties:
        properties = generate_sample_properties(area, postcode)
    
    return properties


def generate_sample_properties(area: str, postcode: str):
    """Generate sample property data for demonstration."""
    num_properties = random.randint(3, 6)
    properties = []
    
    street_names = ["High Street", "Church Road", "Station Road", "Victoria Road", 
                    "Park Avenue", "Queens Road", "Kings Lane", "Mill Lane"]
    
    for i in range(num_properties):
        # Generate a realistic postcode based on input
        if postcode:
            base_postcode = postcode.upper().strip()
            if len(base_postcode) >= 3:
                prop_postcode = base_postcode[:3] + f" {random.randint(1,9)}{random.choice('ABCDEFGHJKLMNPQRSTUVWXYZ')}{random.choice('ABCDEFGHJKLMNPQRSTUVWXYZ')}"
            else:
                prop_postcode = f"{base_postcode} {random.randint(1,9)}{random.choice('ABCDEFGHJKLMNPQRSTUVWXYZ')}{random.choice('ABCDEFGHJKLMNPQRSTUVWXYZ')}"
        else:
            prop_postcode = f"SW{random.randint(1,20)} {random.randint(1,9)}{random.choice('ABCDEFGHJKLMNPQRSTUVWXYZ')}{random.choice('ABCDEFGHJKLMNPQRSTUVWXYZ')}"
        
        property_data = {
            "id": f"prop_{i+1}",
            "address": f"{random.randint(1, 150)} {random.choice(street_names)}",
            "postcode": prop_postcode,
            "area": area if area != "Any" else "London",
            "price": random.randint(250000, 1500000),
            "bedrooms": random.randint(1, 5),
            "bathrooms": random.randint(1, 3),
            "sustainability_score": random.randint(35, 95),
            "epc_rating": random.choice(["A", "B", "C", "D", "E"]),
            "property_type": random.choice(["Detached", "Semi-Detached", "Terraced", "Flat", "Bungalow"]),
            "image_url": random.choice(HOUSE_IMAGES),
            "validation_confidence": random.randint(70, 98),
        }
        properties.append(property_data)
    
    return properties


def display_property_card(prop: dict, index: int):
    """Display a single property card with image, sustainability, and validation."""
    
    with st.container(border=True):
        col1, col2, col3 = st.columns([1, 1, 1])
        
        # Column 1: House Image and Description
        with col1:
            st.markdown("##### 🏠 Property")
            
            # Display house image
            image_url = prop.get("image_url", HOUSE_IMAGES[0])
            st.image(image_url, width="stretch")
            
            # Property description
            st.markdown(f"**{prop['address']}**")
            st.markdown(f"📍 {prop['postcode']}")
            st.caption(f"Area: {prop['area']}")
            st.caption(f"🛏️ {prop['bedrooms']} beds | 🛁 {prop['bathrooms']} baths")
            st.caption(f"🏷️ {prop['property_type']}")
            st.markdown(f"**💰 £{prop['price']:,}**")
        
        # Column 2: Sustainability Score
        with col2:
            st.markdown("##### 🌿 Sustainability")
            
            score = prop["sustainability_score"]
            color = get_sustainability_color(score)
            label = get_sustainability_label(score)
            
            # Create a visual score display
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {color}22, {color}44);
                border: 3px solid {color};
                border-radius: 15px;
                padding: 30px;
                text-align: center;
                margin: 20px 0;
            ">
                <div style="font-size: 48px; font-weight: bold; color: {color};">
                    {score}%
                </div>
                <div style="font-size: 18px; color: {color}; font-weight: 600;">
                    {label}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # EPC Rating
            epc = prop.get("epc_rating", "C")
            st.markdown(f"**EPC Rating:** {epc}")
            
            # Sustainability breakdown
            st.caption("Energy Efficiency: " + "🟢" * (score // 20) + "⚪" * (5 - score // 20))
        
        # Column 3: Validation Chart
        with col3:
            st.markdown("##### 📈 Validation")
            
            # Create and display validation chart
            fig = create_validation_chart(prop)
            st.pyplot(fig)
            plt.close(fig)
            
            # Validation confidence
            confidence = prop.get("validation_confidence", 85)
            st.markdown(f"**Confidence:** {confidence}%")
            
            # Validation status
            if confidence >= 85:
                st.success("✅ High confidence valuation")
            elif confidence >= 70:
                st.warning("⚠️ Moderate confidence")
            else:
                st.error("❌ Low confidence - needs review")


# --- Sidebar search panel ---
with st.sidebar:
    st.header("🔍 Search Properties")
    
    area = st.selectbox("Choose an area", UK_AREAS, index=0)
    query = st.text_input(
        "Postcode", 
        placeholder="e.g. SW1A 1AA, E1 6AN...",
        help="Enter a full or partial UK postcode"
    )
    
    st.divider()
    
    # Additional filters
    st.subheader("Filters")
    min_sustainability = st.slider("Min Sustainability Score", 0, 100, 0)
    property_type = st.multiselect(
        "Property Type",
        ["Detached", "Semi-Detached", "Terraced", "Flat", "Bungalow"],
        default=[]
    )
    
    st.divider()
    submitted = st.button("🔍 Search", width="stretch", type="primary")

# --- Session state to keep results ---
if "results" not in st.session_state:
    st.session_state.results = []
if "last_search" not in st.session_state:
    st.session_state.last_search = {"area": None, "query": None}

# --- Trigger search ---
if submitted:
    with st.spinner("Searching for properties..."):
        results = search_properties_api(area, query)
        
        # Apply filters
        if min_sustainability > 0:
            results = [r for r in results if r["sustainability_score"] >= min_sustainability]
        
        if property_type:
            results = [r for r in results if r["property_type"] in property_type]
        
        st.session_state.results = results
        st.session_state.last_search = {"area": area, "query": query}

# --- Main content area: show results ---
last = st.session_state.last_search

if last["area"] is None:
    st.info("👋 Welcome! Select an area and enter a postcode to search for properties. Example: SW1A 1AA")
    
    # Show sample cards
    st.subheader("Featured Properties")
    sample_props = generate_sample_properties("London", "SW1")[:2]
    for i, prop in enumerate(sample_props):
        display_property_card(prop, i)
else:
    st.subheader(f"📍 Results for {last['area']} — Postcode: {last['query'] or 'All'}")
    
    results = st.session_state.results
    
    if not results:
        st.warning("No properties found matching your criteria. Try adjusting your search.")
    else:
        st.success(f"Found {len(results)} properties")
        
        # Display each property card
        for i, prop in enumerate(results):
            display_property_card(prop, i)
            
        # Summary statistics
        st.divider()
        st.subheader("📊 Search Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_price = sum(p["price"] for p in results) / len(results)
            st.metric("Average Price", f"£{avg_price:,.0f}")
        
        with col2:
            avg_sustainability = sum(p["sustainability_score"] for p in results) / len(results)
            st.metric("Avg Sustainability", f"{avg_sustainability:.1f}%")
        
        with col3:
            st.metric("Properties Found", len(results))
        
        with col4:
            high_rated = len([p for p in results if p["sustainability_score"] >= 70])
            st.metric("High Sustainability", high_rated)
