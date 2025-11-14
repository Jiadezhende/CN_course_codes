# Web crawler using playwright
from playwright.sync_api import sync_playwright
import json, os, time
from util import csv_parser

SITE_LIST_PATH = "top-1m.csv"
LOAD_TIMEOUT = 10000  # ms
HAR_FOLDER = "top100_harfiles"
os.makedirs(HAR_FOLDER, exist_ok=True)

domains = csv_parser(SITE_LIST_PATH)

def save_har(har_path, har_data):
    with open(har_path, "w") as f:
        f.write(har_data)

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,  # 可改 False 调试
    )
    context = browser.new_context()
    page = context.new_page()

    collected = 0

    for domain in domains:
        if collected >= 10:
            break

        url = "https://" + domain
        print(f"Visiting {url}")

        har_path = f"{HAR_FOLDER}/{domain}.har"

        try:
            # Start HAR recording
            context = browser.new_context(
                record_har_path=har_path,
                record_har_content="embed",  # include full content
            )
            page = context.new_page()

            # load the page
            page.goto(url, timeout=LOAD_TIMEOUT)

            time.sleep(3)  # wait for background requests

            # Stop context → automatically writes HAR file
            context.close()
            collected += 1
            print(f"HAR saved: {har_path}")

        except Exception as e:
            print(f"Failed: {e}")
            continue

    browser.close()

print("Finished.")