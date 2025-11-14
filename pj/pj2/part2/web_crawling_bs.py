from selenium import webdriver
from browsermobproxy import Server
import json, os, time
from util import csv_parser

SITE_LIST_PATH = 'top-1m.csv'
LOAD_TIMEOUT = 10  # seconds

# load page URL
domains = csv_parser(SITE_LIST_PATH)

# Create folder
har_folder = "top100_harfiles"
os.makedirs(har_folder, exist_ok=True)

# create a browsermob server instance
server = Server("browsermob-proxy/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy(params=dict(trustAllServers=True))

# create a new chromedriver instance
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'--proxy-server={proxy.proxy}')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument("--headless=new")   # run in headless mode to speed up
driver = webdriver.Chrome(options=chrome_options)
driver.set_page_load_timeout(LOAD_TIMEOUT)

# do crawling
collected = 0

for domain in domains:
    if collected >= 10:
        break

    url = "https://" + domain
    print(f"Visiting {url}")

    try:
        proxy.new_har(domain, options={'captureHeaders': True, 'captureContent': True})
        driver.get(url)
        time.sleep(3)  # allow background requests

        har_data = proxy.har
        if not har_data:
            print("HAR empty, skipping.")
            continue
        
        # save HAR file
        with open(f'{har_folder}/{domain}.har', 'w') as f:
            json.dump(har_data, f)

        collected += 1
        print(f"Saved HAR")

    except Exception as e:
        print(f"Failed: {e}")
        continue

# stop server and exit
server.stop()
driver.quit()
