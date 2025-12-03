import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import base64
from io import BytesIO

st.set_page_config(page_title="The Hacker News — Top 1 Dashboard", layout="wide")

# -----------------------------
# Helper / sample data
# -----------------------------

# Sample monthly ratings (1..5) for the Hacker News
monthly_ratings = pd.DataFrame({
    "month": pd.date_range(start="2024-01-01", periods=12, freq='M').strftime('%b %Y'),
    "rating": [3.8, 4.0, 4.2, 4.1, 4.3, 4.4, 4.5, 4.6, 4.4, 4.3, 4.2, 4.4],
})

# Sample articles per month
articles_per_month = pd.DataFrame({
    "month": monthly_ratings['month'],
    "articles": [28, 34, 30, 27, 40, 45, 42, 50, 48, 44, 39, 36],
})

# Sample sentiment trend (percent positive)
sentiment = pd.DataFrame({
    "month": monthly_ratings['month'],
    "positive_pct": [55, 57, 60, 58, 62, 64, 66, 68, 65, 63, 61, 64],
})

# Sample India state "intensity" data (for choropleth-like map)
state_data = pd.DataFrame([
    {"state":"Delhi","lat":28.6139,"lon":77.2090,"value":85},
    {"state":"Maharashtra","lat":19.7515,"lon":75.7139,"value":70},
    {"state":"Karnataka","lat":15.3173,"lon":75.7139,"value":50},
    {"state":"Tamil Nadu","lat":11.1271,"lon":78.6569,"value":40},
    {"state":"Telangana","lat":17.3850,"lon":78.4867,"value":60},
    {"state":"West Bengal","lat":22.9868,"lon":87.8550,"value":30},
    {"state":"Gujarat","lat":22.2587,"lon":71.1924,"value":35},
    {"state":"Uttar Pradesh","lat":26.8467,"lon":80.9462,"value":45},
])

# Sample top-3 news cards
news_cards = [
    {
        "title":"Google Patches 107 Android Flaws, Including Two Framework Bugs Exploited in the Wild",
        "summary":"Google released monthly security updates including fixes for two vulnerabilities exploited in the wild.",
        "image":"https://i.ibb.co/3mY2Q6p/android-vuln.jpg",
        "url":"https://thehackernews.com/2025/12/google-patches-107-android-flaws.html"
    },
    {
        "title":"India Orders Phone Makers to Pre-Install Government App to Tackle Telecom Fraud",
        "summary":"India's ministry ordered manufacturers to preload a cybersecurity app on new phones.",
        "image":"https://i.ibb.co/tc0QK7W/india-phone.jpg",
        "url":"https://thehackernews.com/2025/12/india-orders-phone-makers-pre-install-app.html"
    },
    {
        "title":"Enhance Microsoft Intune to Optimize Endpoint Management",
        "summary":"New recommendations to improve endpoint management and reduce attack surface.",
        "image":"https://i.ibb.co/7bX7s0m/intune.jpg",
        "url":"https://thehackernews.com/2025/11/enhance-microsoft-intune.html"
    }
]

st.markdown("""
<style>
.header {
  background: linear-gradient(90deg,#1e3a8a,#3b82f6);
  padding: 18px 20px;
  border-radius: 8px;
  color: white;
}
.header h1 { margin: 0; }
.header p { margin: 2px 0 0 0; opacity: 0.9 }
.card { border-radius: 10px; padding: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header"><h1>The Hacker News — Top #1 Dashboard</h1><p>Focused view: monthly ratings, article trends, sentiment & India map</p></div>', unsafe_allow_html=True)
st.write('')

col1, col2, col3 = st.columns([1,1,1])

with col1:
    st.markdown("### Monthly Rating Trend")
    fig1 = px.line(monthly_ratings, x='month', y='rating', markers=True)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("### Articles per Month")
    fig2 = px.bar(articles_per_month, x='month', y='articles')
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    st.markdown("### Sentiment (Positive %)")
    fig3 = px.line(sentiment, x='month', y='positive_pct', markers=True)
    st.plotly_chart(fig3, use_container_width=True)

left, right = st.columns([2,1])

with left:
    st.markdown("### Top headlines — The Hacker News")
    card_cols = st.columns(3)
    for i, card in enumerate(news_cards):
        c = card_cols[i]
        with c:
            st.markdown(f"<div class='card'> <img src=\"{card['image']}\" style='width:100%;height:140px;object-fit:cover;border-radius:6px'/> </div>", unsafe_allow_html=True)
            st.markdown(f"**[{card['title']}]({card['url']})**")
            st.write(card['summary'])

with right:
    st.markdown("### India — Cyber Report Intensity")
    fig_map = go.Figure()
    fig_map.add_trace(go.Scattergeo(
        lon = state_data['lon'],
        lat = state_data['lat'],
        text = state_data['state'] + ': ' + state_data['value'].astype(str),
        marker = dict(
            size = state_data['value'] / 3 + 8,
            color = state_data['value'],
            colorscale = 'Reds',
            colorbar=dict(title='Intensity')
        ),
        hoverinfo='text'
    ))
    fig_map.update_geos(fitbounds="locations", visible=False, showcountries=True)
    fig_map.update_layout(margin=dict(l=0,r=0,t=10,b=0), geo=dict(scope='asia', lataxis_range=[6,38], lonaxis_range=[68,98]))
    st.plotly_chart(fig_map, use_container_width=True)

