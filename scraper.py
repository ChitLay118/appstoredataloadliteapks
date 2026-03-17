import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_liteapks():
    url = "https://liteapks.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch data")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    apps_list = []

    # App တွေကို ရှာဖွေခြင်း (Latest Apps & Games Section)
    # HTML structure အရ class name တွေကို အခြေခံပြီး ယူထားပါတယ်
    for item in soup.select('a.flex.items-center.gap-4'):
        try:
            name = item.find('h3').get_text(strip=True)
            link = item['href']
            icon = item.find('img')['src']
            
            # Category ရှာခြင်း
            category_tag = item.select_one('.text-gray-3.truncate span:nth-of-type(3)')
            category = category_tag.get_text(strip=True) if category_tag else "App"

            # Mod Info ရှာခြင်း
            mod_info_tag = item.find('div', class_='text-orange')
            mod_info = mod_info_tag.get_text(strip=True) if mod_info_tag else "Original"

            app_data = {
                "name": name,
                "icon": icon,
                "link": link,
                "category": category,
                "mod_info": mod_info
            }
            apps_list.append(app_data)
        except Exception as e:
            continue

    # ရလာတဲ့ data ကို JSON file အနေနဲ့ သိမ်းမယ်
    with open('apps.json', 'w', encoding='utf-8') as f:
        json.dump(apps_list, f, ensure_ascii=False, indent=4)
    
    print(f"Successfully scraped {len(apps_list)} apps.")

if __name__ == "__main__":
    scrape_liteapks()
