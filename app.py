import streamlit as st
# import app as st - do not include
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
from io import BytesIO
import base64
import requests

st.title("Property / Area Search")


UK_AREAS = [
    "Anywhere in the UK",

    "Aberdeen",
    "Aberdeenshire",
    "Anglesey",
    "Angus",
    "Antrim and Newtownabbey",
    "Ards and North Down",
    "Argyll and Bute",
    "Armagh City, Banbridge and Craigavon",

    "Bangor",
    "Barnet",
    "Bath",
    "Bedfordshire",
    "Belfast",
    "Berkshire",
    "Bexley",
    "Birmingham",
    "Blackburn",
    "Blackpool",
    "Blaenau Gwent",
    "Bolton",
    "Bournemouth",
    "Bracknell Forest",
    "Bradford",
    "Brent",
    "Bridgend",
    "Bristol",
    "Bromley",
    "Buckinghamshire",
    "Bury",

    "Caerphilly",
    "Cambridgeshire",
    "Cambridge",
    "Camden",
    "Cardiff",
    "Carmarthenshire",
    "Causeway Coast and Glens",
    "Ceredigion",
    "Cheshire",
    "Chelmsford",
    "Cheltenham",
    "Chester",
    "Clackmannanshire",
    "Colchester",
    "Conwy",
    "Cornwall",
    "Coventry",
    "Croydon",
    "Cumbria",

    "Darlington",
    "Denbighshire",
    "Derby",
    "Derbyshire",
    "Derry",
    "Devon",
    "Doncaster",
    "Dorset",
    "Dudley",
    "Dumfries and Galloway",
    "Dundee",
    "Durham",

    "Ealing",
    "East Ayrshire",
    "East Dunbartonshire",
    "East Lothian",
    "East Midlands",
    "East of England",
    "East Renfrewshire",
    "East Sussex",
    "Edinburgh",
    "Enfield",
    "England",
    "Essex",
    "Exeter",

    "Falkirk",
    "Fermanagh and Omagh",
    "Fife",
    "Flintshire",

    "Gateshead",
    "Glasgow",
    "Gloucester",
    "Gloucestershire",
    "Greater London",
    "Greater Manchester",
    "Greenwich",
    "Gwynedd",

    "Hackney",
    "Halifax",
    "Hammersmith and Fulham",
    "Hampshire",
    "Haringey",
    "Harrow",
    "Hartlepool",
    "Havering",
    "Hereford",
    "Herefordshire",
    "Hertfordshire",
    "Highland",
    "Hillingdon",
    "Hounslow",
    "Hove",
    "Huddersfield",

    "Inverness",
    "Ipswich",
    "Isle of Wight",
    "Islington",

    "Kensington and Chelsea",
    "Kent",
    "Kingston upon Thames",

    "Lambeth",
    "Lancashire",
    "Leeds",
    "Leicester",
    "Leicestershire",
    "Lewisham",
    "Lincolnshire",
    "Lisburn",
    "Liverpool",
    "London",
    "Luton",

    "Manchester",
    "Medway",
    "Merseyside",
    "Merthyr Tydfil",
    "Midlothian",
    "Milton Keynes",
    "Monmouthshire",
    "Moray",
    "Merton",
    "Middlesbrough",

    "Na h-Eileanan Siar",
    "Neath Port Talbot",
    "Newcastle upon Tyne",
    "Newham",
    "Newport",
    "Newry",
    "Norfolk",
    "North Ayrshire",
    "North East England",
    "North Lanarkshire",
    "North Northamptonshire",
    "North Somerset",
    "North Tyneside",
    "North West England",
    "North Yorkshire",
    "Northamptonshire",
    "Northumberland",
    "Northern Ireland",
    "Nottingham",
    "Nottinghamshire",
    "Norwich",

    "Oldham",
    "Orkney Islands",
    "Oxfordshire",

    "Pembrokeshire",
    "Perth",
    "Peterborough",
    "Plymouth",
    "Poole",
    "Portsmouth",
    "Powys",
    "Preston",

    "Reading",
    "Redbridge",
    "Renfrewshire",
    "Rhondda Cynon Taf",
    "Richmond upon Thames",
    "Rochdale",
    "Rutland",

    "Salford",
    "Scarborough",
    "Scotland",
    "Scottish Borders",
    "Sefton",
    "Sheffield",
    "Shetland Islands",
    "Shropshire",
    "Slough",
    "Solihull",
    "Somerset",
    "South Ayrshire",
    "South East England",
    "South Gloucestershire",
    "South Lanarkshire",
    "South Shields",
    "South Tyneside",
    "South West England",
    "Southampton",
    "Southend-on-Sea",
    "Southwark",
    "St Helens",
    "Staffordshire",
    "Stirling",
    "Stockport",
    "Stoke-on-Trent",
    "Suffolk",
    "Sunderland",
    "Surrey",
    "Sutton",
    "Swansea",
    "Swindon",

    "Telford",
    "Thurrock",
    "Torfaen",
    "Torquay",
    "Tower Hamlets",
    "Trafford",
    "Tyne and Wear",

    "Vale of Glamorgan",
    "Wakefield",
    "Wales",
    "Waltham Forest",
    "Wandsworth",
    "Warrington",
    "Warwickshire",
    "West Dunbartonshire",
    "West Lothian",
    "West Midlands",
    "West Sussex",
    "Westminster",
    "Wigan",
    "Wiltshire",
    "Wokingham",
    "Wolverhampton",
    "Worcester",
    "Worcestershire",
    "Wrexham",

    "York",
    "Yorkshire and the Humber"
]


def mock_search(area: str, query: str):
    """
    Restreaplace this with your real backend/API call.
    Must return a list (or dataframe) of results.
    """
    # Example fake results
    q = query.strip().lower()
    base = [
        {"address":"yes"},
    ]
    if not q:
        return base
    return [r for r in base if q in r["address"].lower()]

st.set_page_config(page_title="UK Area Search", layout="wide")

# --- Sidebar search panel ---
with st.sidebar:
    st.header("Search")
    area = st.selectbox("Choose an area", UK_AREAS, index=0)
    query = st.text_input("Search", placeholder="e.g. postcode, street, ward...")
    submitted = st.button("Search", use_container_width=True)

# --- Session state to keep results ---
if "results" not in st.session_state:
    st.session_state.results = []
if "last_search" not in st.session_state:
    st.session_state.last_search = {"area": None, "query": None}

# --- Trigger search ---
if submitted:
    results = mock_search(area, query)
    st.session_state.results = results
    st.session_state.last_search = {"area": area, "query": query}

# --- Main content area: show results ---
last = st.session_state.last_search
if last["area"] is None:
    st.info("Select an area, and a postcode/street/ward to search within that area. when you select this, make sure it is correct e.g, SS0 0BW")
else:
    st.subheader(f"Results for {last['area']} — query: {last['query']!r}")

    results = st.session_state.results
    if not results:
        st.warning("No results found.")
    else:
        # Simple card-style display
        for r in results:
            with st.container(border=True):
                st.write(f"**{r['address']}**")
                st.caption(f"Area: {r['area']} | Sustainability score: {r['score']}")

        # If you want a dataframe instead:
        # import pandas as pd
        # st.dataframe(pd.DataFrame(results), use_container_width=True)
