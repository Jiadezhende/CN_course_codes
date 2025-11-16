"""
web_crawler_pw.py
Main web crawler using Playwright. Collects HAR files for a list of sites.

Usage: run `py web_crawler_pw.py`. Adjust `SITE_LIST_PATH`, `MAX_SITES`, and timeouts at top of file.
"""

from playwright.sync_api import sync_playwright, TimeoutError
import os, csv, time, logging

def csv_parser(file_path):
    domains = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 2:
                domains.append(row[1])  # second column is the domain
    return domains

SITE_LIST_PATH = "top-1m.csv"
HAR_FOLDER = "top100_harfiles"
LOAD_TIMEOUT = 10000  # ms - increased to allow more requests
BACKGROUND_TIMEOUT = 3000  # ms - increased to allow background requests
MAX_SITES = 100

os.makedirs(HAR_FOLDER, exist_ok=True)
domains = csv_parser(SITE_LIST_PATH)

# Configure logging
logging.basicConfig(
    filename='crawler.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    collected = 0

    try:
        for domain in domains:
            if collected >= MAX_SITES:
                break

            url = "https://" + domain   # default to https
            print(f"Visiting {url}")
            har_path = os.path.join(HAR_FOLDER, f"{domain}.har")

            context = browser.new_context(
                record_har_path=har_path,
                record_har_content="omit",  # omit to avoid embedding large content that causes hanging
                record_har_mode="full", # include large data
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
                ),
            )

            try:
                page = context.new_page()
                page.set_default_navigation_timeout(LOAD_TIMEOUT)
                # navigate; match spotify_test
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=LOAD_TIMEOUT)
                except TimeoutError:
                    print("Navigation timeout, but continuing...")

                # wait briefly for background requests
                page.wait_for_timeout(BACKGROUND_TIMEOUT)

                # force stop page load
                try:
                    page.close() # if not closed, may hang on SPA sites
                except Exception:
                    pass

                print(f"Stopping page load for {url}.")
                context.close()
                collected += 1
                print(f"HAR saved: {har_path}")

            except Exception as e:
                error_msg = f"Failed visiting {url}: {e}"
                print(error_msg)
                logger.error(error_msg)
                try:
                    if context:
                        context.close()
                except:
                    pass
                continue

    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        try:
            browser.close()
        except Exception:
            pass

print("Finished.")