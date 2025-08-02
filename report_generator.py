# enhanced_report_script.py (with charts, trends, and email simulated)

import requests
import feedparser
from datetime import datetime
import matplotlib.pyplot as plt
import os
from pytrends.request import TrendReq

# --- Section 1: Travel News (RSS) ---
rss_url = "https://www.breakingtravelnews.com/rss/"
feed = feedparser.parse(rss_url)
travel_news = "".join([f"<p><a href='{entry.link}'>{entry.title}</a></p>" for entry in feed.entries[:3]])

# --- Section 2: Airline & Travel Promos (manual for now) ---
promos = {
    "HK Express": "HK$78 flash sale till Aug 5",
    "Cathay": "Asia Miles summer boost – double miles till Aug 10",
    "Klook": "Get HK$100 off activities with code SUMMER100",
}
promo_html = "".join([f"<p><b>{k}</b>: {v}</p>" for k, v in promos.items()])

# --- Section 3: Insurance Campaigns (manual for now) ---
campaigns = {
    "AXA": "10% off travel insurance till Aug 15",
    "Bowtie": "Free airport lounge access with annual plan",
}
insurance_html = "".join([f"<p><b>{k}</b>: {v}</p>" for k, v in campaigns.items()])

# --- Section 4: Google Trends (HK) ---
pytrends = TrendReq(hl='zh-HK', tz=480)
try:
    trending_searches = pytrends.trending_searches(pn='hong_kong').head(5)
    trends_html = "<ul>" + "".join([f"<li>{kw}</li>" for kw in trending_searches[0]]) + "</ul>"
except Exception:
    trends_html = "<p>Google Trends unavailable.</p>"

# --- Section 5: LIHKG Posts (simulated) ---
lihkg_html = """
<ul>
  <li>【旅遊】下月日本第一手特價</li>
  <li>【機票】HK Express 真的有 $78?</li>
  <li>【高輟】要買保險請問有推薦嗎</li>
</ul>
"""

# --- Section 6: Weather ---
try:
    weather = requests.get("https://wttr.in/Hong+Kong?format=3").text
except Exception:
    weather = "Unable to retrieve weather."
weather_html = f"<p>{weather}</p>"

# --- Section 7: Marketing Suggestion ---
suggestion = "<p>推動旅遊保險主打“特價機票”兼帶日本元素。可同LIHKG buzz作一方向push</p>"

# --- Section 8: Chart Generation ---
x = ["HK Express", "Cathay", "Trip.com", "Expedia"]
y = [320, 290, 180, 210]
plt.figure(figsize=(6, 4))
plt.bar(x, y)
plt.title("Mention Count by Platform")
plt.ylabel("Buzz Count")
plt.tight_layout()
plt.savefig("chart.png")

# --- Compose HTML ---
html_content = f"""
<!DOCTYPE html>
<html>
<head><meta charset='UTF-8'><title>Zurich Daily Travel Report</title></head>
<body>
<h1>Zurich Daily Travel Report</h1>
<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

<h2>1. Travel News</h2>{travel_news}
<h2>2. Promos</h2>{promo_html}
<h2>3. Insurance Campaigns</h2>{insurance_html}
<h2>4. Google Trends (HK)</h2>{trends_html}
<h2>5. LIHKG Hot Posts</h2>{lihkg_html}
<h2>6. Weather</h2>{weather_html}
<h2>7. Marketing Suggestion</h2>{suggestion}
<h2>8. Buzz Chart</h2><img src="chart.png" width="600"/>
</body>
</html>
"""

# --- Write HTML ---
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Report saved to index.html")

# --- Email sending placeholder ---
print("Simulated email send to cathyshing12@gmail.com")
# Real email logic will be added after Gmail App Password setup.
