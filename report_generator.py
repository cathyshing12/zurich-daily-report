# Enhanced report_generator.py with external JSON content for promos

import requests
import feedparser
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime
from pytrends.request import TrendReq
import json
import os

# --- Travel News ---
feed = feedparser.parse("https://www.breakingtravelnews.com/rss/")
travel_news = "".join([f"<p><a href='{e.link}'>{e.title}</a></p>" for e in feed.entries[:5]])

# --- Airline Promos from JSON ---
try:
    with open("airline_promos.json", "r", encoding="utf-8") as f:
        airline_promos = json.load(f)
except:
    airline_promos = []

airline_html = "".join([f"<h3>{p['title']}</h3><p>{p['content']}</p>" for p in airline_promos])

# --- Insurance Campaigns from JSON ---
try:
    with open("insurance_campaigns.json", "r", encoding="utf-8") as f:
        insurance_promos = json.load(f)
except:
    insurance_promos = []

insurance_html = "".join([f"<h3>{p['title']}</h3><p>{p['content']}</p>" for p in insurance_promos])

# --- Google Trends ---
pytrends = TrendReq(hl='en-US', tz=480)
trend_keywords = []
trends_html = "<ul>"
try:
    pytrends.build_payload(["travel", "Japan", "Korea"], geo='HK', timeframe='now 7-d')
    interest = pytrends.related_queries()
    for kw, val in interest.items():
        top = val.get('top')
        if top is not None:
            for _, row in top.head(3).iterrows():
                trend_keywords.append(row['query'])
                trends_html += f"<li>{row['query']}</li>"
except Exception as e:
    trends_html += f"<li>Trends unavailable</li>"
trends_html += "</ul>"

# --- LIHKG Posts ---
lihkg_titles = []
lihkg_html = "<ul>"
try:
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get("https://lihkg.com/api_v2/thread/category/15?page=1", headers=headers)
    if res.status_code == 200:
        posts = res.json().get("response", {}).get("items", [])[:5]
        for post in posts:
            title = post['title']
            lihkg_titles.append(title)
            lihkg_html += f"<li>{title}</li>"
except:
    lihkg_html += "<li>LIHKG fetch failed</li>"
lihkg_html += "</ul>"

# --- Weather ---
try:
    weather = requests.get("https://wttr.in/Hong+Kong?format=3").text
except:
    weather = "Weather unavailable"
weather_html = f"<p>{weather}</p>"

# --- Dynamic Suggestion Engine ---
suggestion = "<p>推出7折旅遊保險優惠，搭配熱門目的地推廣</p>"
if any("日本" in kw or "Japan" in kw for kw in trend_keywords + lihkg_titles):
    suggestion = "<p>日本熱門話題推升，建議加推日本旅行保優惠</p>"
elif "紅雨" in weather:
    suggestion = "<p>紅雨警告，主打家居保險 + 財物保障</p>"

# --- Chart (static demo) ---
x = [p['title'][:10] for p in insurance_promos]
y = [20 + i*5 for i in range(len(x))]
plt.figure(figsize=(6, 4))
plt.bar(x, y, color='teal')
plt.title('Insurance Campaign Buzz')
plt.tight_layout()
plt.savefig('chart.png')

# --- Combine into HTML ---
html_content = f"""
<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Zurich Daily Report</title></head><body>
<h1>Zurich Daily Travel Report</h1>
<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
<h2>1. Travel News</h2>{travel_news}
<h2>2. Travel Promos</h2>{airline_html}
<h2>3. Insurance Campaigns</h2>{insurance_html}
<h2>4. Google Trends</h2>{trends_html}
<h2>5. LIHKG Posts</h2>{lihkg_html}
<h2>6. Weather</h2>{weather_html}
<h2>7. Suggestion</h2>{suggestion}
<h2>8. Insurance Buzz Chart</h2><img src='chart.png' width='600'/>
</body></html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Daily report generated: index.html")
