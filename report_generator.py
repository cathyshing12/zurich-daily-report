# report_generator.py with real-time promo scraping, insurance JSON, and dynamic suggestions

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

# --- Travel Promos Scraping ---
def scrape_promos():
    promos = {}
    try:
        r = requests.get("https://www.hkexpress.com/en-hk/promotions/")
        soup = BeautifulSoup(r.text, 'html.parser')
        promos['HK Express'] = soup.select_one(".promo-heading, .promotion-title").get_text(strip=True)
    except: promos['HK Express'] = "(Failed to fetch)"
    try:
        r = requests.get("https://www.cathaypacific.com/cx/en_HK/offers.html")
        soup = BeautifulSoup(r.text, 'html.parser')
        item = soup.select_one(".offer-card__title")
        promos['Cathay'] = item.get_text(strip=True) if item else "(No offer)"
    except: promos['Cathay'] = "(Failed to fetch)"
    try:
        r = requests.get("https://www.klook.com/en-HK/deals/")
        soup = BeautifulSoup(r.text, 'html.parser')
        klook_text = soup.find("h2")
        promos['Klook'] = klook_text.get_text(strip=True) if klook_text else "(No deals)"
    except: promos['Klook'] = "(Failed to fetch)"
    try:
        r = requests.get("https://www.trip.com/deals/")
        soup = BeautifulSoup(r.text, 'html.parser')
        trip_title = soup.find("h2")
        promos['Trip.com'] = trip_title.get_text(strip=True) if trip_title else "(No deals)"
    except: promos['Trip.com'] = "(Failed to fetch)"
    return promos

promos = scrape_promos()
promo_html = "".join([f"<p><b>{k}</b>: {v}</p>" for k, v in promos.items()])

# --- Insurance Campaigns from JSON ---
try:
    with open("insurance_campaigns.json", "r", encoding="utf-8") as f:
        campaigns = json.load(f)
except:
    campaigns = {"Fallback": "Unable to load campaigns."}
insurance_html = "".join([f"<p><b>{k}</b>: {v}</p>" for k, v in campaigns.items()])

# --- Google Trends (HK) ---
pytrends = TrendReq(hl='en-US', tz=480)
trends_html, trend_keywords = "<ul>", []
try:
    trending = pytrends.trending_searches(pn='hong_kong').head(5)
    trend_keywords = list(trending[0])
    for kw in trend_keywords:
        trends_html += f"<li>{kw}</li>"
except: trends_html += "<li>Google Trends unavailable</li>"
trends_html += "</ul>"

# --- LIHKG Posts ---
lihkg_html, lihkg_titles = "<ul>", []
try:
    r = requests.get('https://lihkg.com/api_v2/thread/category/15?page=1')
    posts = r.json().get('response', {}).get('items', [])[:5]
    for post in posts:
        title = post['title']
        lihkg_titles.append(title)
        lihkg_html += f'<li>{title}</li>'
except: lihkg_html += "<li>LIHKG data not available</li>"
lihkg_html += "</ul>"

# --- Weather ---
try:
    weather = requests.get("https://wttr.in/Hong+Kong?format=3").text
except:
    weather = "Weather unavailable"
weather_html = f"<p>{weather}</p>"

# --- Marketing Suggestion (dynamic) ---
suggestion = "<p>推出7折旅遊保險優惠，搭配熱門目的地推廣</p>"
if any(kw for kw in trend_keywords + lihkg_titles if '日本' in kw or 'Japan' in kw):
    suggestion = "<p>【推介】日本成熱門關鍵字，建議推限時旅遊保險優惠</p>"
elif '紅雨' in weather:
    suggestion = "<p>【天氣提示】紅雨生效，推家居保險更有共鳴</p>"

# --- Chart (static for demo) ---
x = list(campaigns.keys())
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
<h2>2. Travel Promos</h2>{promo_html}
<h2>3. Insurance Campaigns</h2>{insurance_html}
<h2>4. Google Trends</h2>{trends_html}
<h2>5. LIHKG Posts</h2>{lihkg_html}
<h2>6. Weather</h2>{weather_html}
<h2>7. Suggestion</h2>{suggestion}
<h2>8. Insurance Buzz Chart</h2><img src="chart.png" width="600"/>
</body></html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
print("✅ Report saved to index.html")
