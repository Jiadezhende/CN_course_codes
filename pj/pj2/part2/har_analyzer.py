"""
har_analyzer.py
Analyze HAR files collected by the crawler.

Outputs CSV summaries:
 - third_party_domains_top10.csv
 - third_party_cookies_top10.csv
 - third_party_cookies_full.csv
 - site_third_party_requests.csv

Usage: run `py har_analyzer.py` (expects `top100_harfiles/` directory).
"""

import json
import os
from collections import Counter, defaultdict
import tldextract
import csv


# Utility function: Extract SLD (e.g., "google.com")
def get_sld(url_or_domain):
    ext = tldextract.extract(url_or_domain)
    return f"{ext.domain}.{ext.suffix}"


# Load HAR file
def load_har(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# Analyze a single HAR file
# Returns:
#   - Counter of third-party domains with request counts
#   - Set of unique third-party cookie names
def analyze_har(har_data, site_url):
    site_sld = get_sld(site_url)

    third_party_domains = Counter()
    third_party_cookies = set()

    entries = har_data["log"]["entries"]

    for e in entries:
        # Request URL
        req_url = e["request"]["url"]
        req_sld = get_sld(req_url)

        # Count third-party domains
        if req_sld != site_sld:
            third_party_domains[req_sld] += 1

        # Request Cookies
        for c in e["request"].get("cookies", []):
            cookie_domain = c.get("domain", "")
            if cookie_domain:
                cookie_sld = get_sld(cookie_domain)
                if cookie_sld != site_sld:
                    third_party_cookies.add(c["name"])

        # Response Cookies
        for c in e["response"].get("cookies", []):
            cookie_domain = c.get("domain", "")
            if cookie_domain:
                cookie_sld = get_sld(cookie_domain)
                if cookie_sld != site_sld:
                    third_party_cookies.add(c["name"])

    return third_party_domains, third_party_cookies


# Iterate through all HAR files in a directory
def analyze_har_directory(har_dir):
    domain_counter = Counter()
    cookie_counter = Counter()
    site_request_counts = defaultdict(Counter)  # Track requests per site

    for filename in os.listdir(har_dir):
        if not filename.endswith(".har"):
            continue

        path = os.path.join(har_dir, filename)

        # Infer the website associated with the HAR file (assuming HAR filename = domain.har)
        site_url = "https://" + filename.replace(".har", "")

        try:
            har_data = load_har(path)
        except:
            print(f"[Error] Failed to parse HAR: {filename}")
            continue

        third_domains, third_cookies = analyze_har(har_data, site_url)

        # Update global counters
        domain_counter.update(third_domains)
        cookie_counter.update(third_cookies)

        # Track requests per site
        site_request_counts[site_url].update(third_domains)

        print(f"[OK] Processed: {filename}")

    return domain_counter, cookie_counter, site_request_counts


# Save Top-10 items to CSV
def save_top10_to_csv(counter, path):
    top10 = counter.most_common(10)
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["item", "count"])
        for item, count in top10:
            writer.writerow([item, count])
    print(f"[Saved] {path}")

# Save full items to CSV
def save_full_to_csv(counter, path):
    all_items = counter.most_common()
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["item", "count"])
        for item, count in all_items:
            writer.writerow([item, count])
    print(f"[Saved] {path}")


# Save per-site third-party domain requests to CSV
def save_site_requests_to_csv(site_request_counts, path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["site", "third_party_domain", "request_count"])
        for site, domain_counts in site_request_counts.items():
            for domain, count in domain_counts.items():
                writer.writerow([site, domain, count])
    print(f"[Saved] {path}")


# Main process
if __name__ == "__main__":
    HAR_FOLDER = "top100_harfiles"
    domain_counter, cookie_counter, site_request_counts = analyze_har_directory(HAR_FOLDER)

    save_top10_to_csv(domain_counter, "third_party_domains_top10.csv")
    save_top10_to_csv(cookie_counter, "third_party_cookies_top10.csv")
    save_full_to_csv(cookie_counter, "third_party_cookies_full.csv")
    save_site_requests_to_csv(site_request_counts, "site_third_party_requests.csv")
