print("Generating daily travel report...")

from datetime import datetime

html = f"""<!DOCTYPE html>
<html>
<head><meta charset='UTF-8'><title>Zurich Report</title></head>
<body>
<h1>Zurich Daily Travel Report</h1>
<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
<h2>Travel News</h2><p>Placeholder headline</p>
<h2>Promos</h2><p>HK Express $28 special</p>
<h2>Insurance</h2><p>AXA 10% Summer Promo</p>
</body></html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
    
print("Report saved to index.html")
