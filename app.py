import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

# === CONFIGURATION ===
WP_SITE = "https://yourwordpresssite.com"  # without trailing slash
USERNAME = "your_wp_username"
APP_PASSWORD = "your_generated_password"

YEAR = 2025
API_URL = f"https://astro-automatic.onrender.com/ekadashi?year={YEAR}-01-01"

# Optional: change to "posts" to create blog posts
WP_ENDPOINT = f"{WP_SITE}/wp-json/wp/v2/pages"
AUTH = HTTPBasicAuth(USERNAME, APP_PASSWORD)

# === MAIN SCRIPT ===
def create_wordpress_page(title, slug, content):
    data = {
        "title": title,
        "slug": slug,
        "content": content,
        "status": "publish"
    }
    res = requests.post(WP_ENDPOINT, json=data, auth=AUTH)

    if res.status_code == 201:
        print(f"✅ Created: {title}")
    else:
        print(f"❌ Failed: {title} | {res.status_code} | {res.text}")

def run():
    resp = requests.get(API_URL)
    ekadashis = resp.json()

    # Group by month
    month_map = {}
    for ek in ekadashis:
        month_name = datetime.strptime(ek["iso_date"], "%Y-%m-%d").strftime("%B").lower()
        month_map.setdefault(month_name, []).append(ek)

        # === Detail Page ===
        slug = f"{ek['slug']}-ekadashi-date-time"
        title = f"{ek['name']} {YEAR} Date, Time, Parana & Vrat Katha"
        content = f"""
        <h1>{ek['name']} {YEAR}</h1>
        <p><strong>Date:</strong> {ek['readable_date']}</p>
        <p><strong>Tithi:</strong> Ekadashi</p>
        <p><strong>Paksha:</strong> {ek['paksha']}</p>
        <p><strong>Month:</strong> {ek['month']}</p>
        <p><strong>Weekday:</strong> {ek['weekday']}</p>
        <h2>Parana Time</h2>
        <p>{ek['parana']['parana_date']} – Sunrise: {ek['parana']['sunrise']}</p>
        <p><strong>Description:</strong> {ek['name']} is a Hindu Ekadashi celebrated on {ek['readable_date']}.</p>
        """
        create_wordpress_page(title, slug, content)

    # === Year Page ===
    year_title = f"Ekadashi List {YEAR} - Dates and Festivals"
    year_slug = f"ekadashi-{YEAR}"
    year_content = f"<h2>All Ekadashi in {YEAR}</h2><ul>"
    for ek in ekadashis:
        ek_url = f"{WP_SITE}/{ek['slug']}-ekadashi-date-time?year={YEAR}"
        year_content += f"<li><a href='{ek_url}'>{ek['name']} - {ek['readable_date']}</a></li>"
    year_content += "</ul>"
    create_wordpress_page(year_title, year_slug, year_content)

    # === Month Pages ===
    for month, items in month_map.items():
        month_title = f"Ekadashi in {month.capitalize()} {YEAR}"
        month_slug = f"ekadashi-{month}-{YEAR}"
        month_content = f"<h2>{month.capitalize()} {YEAR} Ekadashi List</h2><ul>"
        for ek in items:
            url = f"{WP_SITE}/{ek['slug']}-ekadashi-date-time?year={YEAR}"
            month_content += f"<li><a href='{url}'>{ek['name']} - {ek['readable_date']}</a></li>"
        month_content += "</ul>"
        create_wordpress_page(month_title, month_slug, month_content)

if __name__ == "__main__":
    run()
