import streamlit as st
import datetime
import requests
import platform
import socket
import networkx as nx
import matplotlib.pyplot as plt

# ------------------ CONTEXT DETECTION ------------------ #
def get_time_context():
    now = datetime.datetime.now()
    hour = now.hour
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 21:
        return "Evening"
    else:
        return "Night"

def get_location_context():
    try:
        res = requests.get("https://ipinfo.io").json()
        city = res.get("city", "Unknown")
        country = res.get("country", "Unknown")
        return city, country
    except:
        return "Unknown", "Unknown"

def get_device_context():
    return f"{platform.system()} - {platform.release()}"

def get_network_context():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except:
        return "Unavailable"

# ------------------ ONTOLOGY-LIKE KNOWLEDGE BASE ------------------ #
knowledge_base = [
    ("Student", "Morning", "📖 Review notes before class."),
    ("Student", "Night", "😴 Time to rest, tomorrow’s lectures await."),
    ("Professor", "Morning", "👩‍🏫 Prepare and deliver lectures."),
    ("Professor", "Night", "📊 Review submissions and plan classes."),
    ("Developer", "Morning", "⚡ Start coding sprints with fresh energy."),
    ("Developer", "Night", "🛠 Debug and commit code before sleeping."),
    ("Guest", "Any", "👋 Welcome! Explore context-aware computing.")
]

def query_ontology(role, time_ctx):
    for r, t, service in knowledge_base:
        if r == role and (t == time_ctx or t == "Any"):
            return service
    return "🤔 No defined service for this role/context."

# ------------------ TOURIST GUIDE CONTEXT ------------------ #
tourist_spots = {
    "Chennai": ["🏖 Marina Beach", "🛕 Kapaleeshwarar Temple", "🏰 Fort St. George"],
    "Bengaluru": ["🌳 Lalbagh Botanical Garden", "🏯 Bangalore Palace", "🛰 ISRO Museum"],
    "Delhi": ["🕌 India Gate", "🏛 Qutub Minar", "🏰 Red Fort"],
    "Mumbai": ["🌊 Marine Drive", "🎥 Bollywood Studio Tour", "🕍 Gateway of India"],
    "Unknown": ["🌍 Explore global tourist spots online!"]
}

def get_tourist_recommendations(city, time_ctx):
    spots = tourist_spots.get(city, tourist_spots["Unknown"])
    if time_ctx == "Morning":
        return f"🌅 Great time to explore outdoors in {city}!", spots[:2]
    elif time_ctx == "Evening":
        return f"🌆 Evening vibes in {city}! Perfect for sightseeing.", spots
    else:
        return f"🌙 In {city}? Night walks and cultural shows are best now.", spots[-2:]

# ------------------ APP UI ------------------ #
st.set_page_config(page_title="Context-Aware Smart Assistant", layout="wide")

st.title("🧠 Context-Aware Smart Workspace Assistant + Tourist Guide")

# Detect context
time_ctx = get_time_context()
city_ctx, country_ctx = get_location_context()
dev_ctx = get_device_context()
net_ctx = get_network_context()

# Role context
role_ctx = st.sidebar.selectbox("Select your role", ["Student", "Professor", "Developer", "Guest"])

# Display detected contexts
st.subheader("📌 Detected Contexts")
st.write(f"**Time Context:** {time_ctx}")
st.write(f"**Location Context:** {city_ctx}, {country_ctx}")
st.write(f"**Device Context:** {dev_ctx}")
st.write(f"**Network Context:** {net_ctx}")
st.write(f"**Role Context:** {role_ctx}")

# ------------------ CONTEXTUAL SERVICES ------------------ #
st.subheader("⚡ Context-Aware Services (Ontology-Driven)")
recommendation = query_ontology(role_ctx, time_ctx)
st.success(recommendation)

# Actuator example
if time_ctx == "Morning":
    st.markdown("<style>body {background-color:#FFFACD;}</style>", unsafe_allow_html=True)
elif time_ctx == "Night":
    st.markdown("<style>body {background-color:#2F4F4F; color:white;}</style>", unsafe_allow_html=True)

# ------------------ DEMO OF KNOWLEDGE BASE ------------------ #
with st.expander("📖 Show Ontology Knowledge Base"):
    st.table([{"Role": r, "Context": t, "Service": s} for r, t, s in knowledge_base])

# ------------------ VISUAL ONTOLOGY GRAPH ------------------ #
st.subheader("🕸 Ontology Graph: Role → Context → Service")
G = nx.DiGraph()
for role, context, service in knowledge_base:
    G.add_node(role, color="lightblue")
    G.add_node(context, color="lightgreen")
    G.add_node(service, color="lightyellow")
    G.add_edge(role, context)
    G.add_edge(context, service)

pos = nx.spring_layout(G, seed=42)
node_colors = [G.nodes[n].get("color", "lightgrey") for n in G.nodes]

plt.figure(figsize=(10, 6))
nx.draw(G, pos, with_labels=True, node_size=2500, node_color=node_colors, font_size=9, font_weight="bold", edge_color="gray")
st.pyplot(plt.gcf())

# ------------------ TOURIST GUIDE DEMO ------------------ #
st.subheader("🧳 Smart Tourist Guide (Cyberguide-Inspired)")
guide_msg, spots = get_tourist_recommendations(city_ctx, time_ctx)
st.info(guide_msg)
st.write("Recommended spots:")
for spot in spots:
    st.write(f"- {spot}")
