import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random
import string
from concurrent.futures import ThreadPoolExecutor

report_endpoint = "https://groupsor.link/data/addreport"
CUTOFF_TIME = datetime.strptime("2025-01-18 16:24:20", "%Y-%m-%d %H:%M:%S")  # Define the cutoff time


# List of real User-Agent strings (example)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.111 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.89 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-A536E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.65 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.133 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.49 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 12_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; vivo 1201 Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-A325F Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; POCO M5 Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; RMX3687 Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-M127G Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; M2010J19CI Build/RKQ1.201217.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-A037F Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; RMX3381 Build/RKQ1.211216.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; M2007J20CI Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-F711B Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Infinix X6813 Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Redmi Note 12 Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; A54 5G Build/RKQ1.211216.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; iQOO Z7 Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Galaxy A54 Build/RKQ1.211216.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; M2101K6I Build/RKQ1.201125.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; F103 Build/SKQ1.210830.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; 2201116SC Build/RKQ1.211101.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36"
    "Mozilla/5.0 (Linux; Android 12; M2101K6G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",  # Xiaomi Redmi Note 11
    "Mozilla/5.0 (Linux; Android 11; SM-M325F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",  # Samsung Galaxy M32
    "Mozilla/5.0 (Linux; Android 11; RMX3085) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",  # Realme 8
    "Mozilla/5.0 (Linux; Android 11; moto g stylus) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",  # Motorola Moto G Stylus (2021)
    "Mozilla/5.0 (Linux; Android 11; CPH2219) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",  # Oppo F19
    "Mozilla/5.0 (Linux; Android 12; SM-A325F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",  # Samsung Galaxy A32
    "Mozilla/5.0 (Linux; Android 11; V2111) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",  # Vivo V21e
    "Mozilla/5.0 (Linux; Android 11; M2010J19CG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",  # Xiaomi Poco M3
    "Mozilla/5.0 (Linux; Android 12; DE2111) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",  # OnePlus Nord CE 5G
    "Mozilla/5.0 (Linux; Android 11; RMX2151) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",  # Realme Narzo 30 Pro
    "Mozilla/5.0 (Linux; Android 12; SM-A528B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",  # Samsung Galaxy A52s
    "Mozilla/5.0 (Linux; Android 11; V2031) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",  # Vivo Y21
    "Mozilla/5.0 (Linux; Android 11; TA-1356) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",  # Nokia G20
    "Mozilla/5.0 (Linux; Android 11; X695) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",  # Infinix Note 10 Pro
    "Mozilla/5.0 (Linux; Android 13; AGNI 2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",  # Lava Agni 2
    "Mozilla/5.0 (Linux; Android 12; moto g play) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",  # Motorola Moto G Play (2023)
    "Mozilla/5.0 (Linux; Android 11; M2101K7AG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",  # Xiaomi Redmi Note 10
    "Mozilla/5.0 (Linux; Android 12; KSA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",  # Honor X30
    "Mozilla/5.0 (Linux; Android 12; 2201116PG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",  # Poco X4 Pro
    "Mozilla/5.0 (Linux; Android 11; Tecno-Camon 18) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"  # Tecno Camon 18
]

def generate_random_ip():
    return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

def generate_random_user_agent():
    """Select a random User-Agent string."""
    return random.choice(USER_AGENTS)

def generate_random_text(length=10):
    """Generates a random string of letters only."""
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def generate_random_reason():
    reasons = ["Group is Full", "Link Revoked", "Other", "Remove my Group", "Religious Hateful", "Group in Wrong Category", "Inappropriate", "Fake/Spam/Fraud", "Rape/Gang rape", "Child Pornography", "Group is Full", "Group is Full", "Group is Full", "Group is Full", "Remove my Group", "Link Revoked", "Other", "Link Revoked", "Remove my Group", "Link Revoked", "Other"]
    return random.choice(reasons)

def generate_random_rdesc():
    """Generates a random description with a sentence-like structure (letters only)."""
    return ' '.join(generate_random_text(random.randint(0, 2)) for _ in range(random.randint(0, 2)))

def load_skipped_urls(file_path):
    try:
        with open(file_path, 'r') as file:
            skipped_urls = file.read().splitlines()
        return set(skipped_urls)
    except FileNotFoundError:
        return set()

def fetch_url(client, url, headers):
    try:
        response = client.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.HTTPError as e:
        print(f"HTTP error while fetching {url}: {e}")
    except requests.RequestException as e:
        print(f"Request error while fetching {url}: {e}")
    except Exception as e:
        print(f"Unexpected error while fetching {url}: {e}")
    return None

def get_group_post_time(html_content):
    """Extracts the group posting time from the HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    timestamp_span = soup.find('span', class_='cate')
    if timestamp_span:
        try:
            group_time = datetime.strptime(timestamp_span.text.strip(), "%Y-%m-%d %H:%M:%S")
            return group_time
        except ValueError:
            print(f"Error parsing time: {timestamp_span.text}")
    return None

def report_group(client, url):
    """Reports a group if it was posted after the cutoff time."""
    try:
        headers = {
            "X-Forwarded-For": generate_random_ip(),
            "X-Real-IP": generate_random_ip(),
            "User-Agent": generate_random_user_agent(),
        }

        # Extract form data for report submission
        html_content = fetch_url(client, url, headers)
        if html_content:
            group_time = get_group_post_time(html_content)

            if group_time and group_time <= CUTOFF_TIME:
                print(f"Skipping group {url} as it was posted before or at the cutoff time: {group_time}")
                return  # Skip reporting this group if it's too old

            soup = BeautifulSoup(html_content, 'html.parser')

            gpid = soup.find('input', {'name': 'gpid'}).get('value')
            code = soup.find('input', {'name': 'code'}).get('value')
            key = soup.find('input', {'name': 'key'}).get('value')
            val1 = int(soup.find('input', {'name': 'val1'}).get('value'))
            val2 = int(soup.find('input', {'name': 'val2'}).get('value'))
            expected_result = val1 + val2

            payload = {
                "gpid": gpid,
                "code": code,
                "key": key,
                "reason": generate_random_reason(),
                "rdesc": generate_random_rdesc(),
                "val1": val1,
                "val2": val2,
                "val3": expected_result
            }

            response = client.post(report_endpoint, data=payload, headers=headers)
            if response.status_code == 200:
                print(f"Report submitted successfully for {url}")
            else:
                print(f"Failed to submit report for {url}. Status code: {response.status_code}")
        else:
            print(f"Empty response received for {url}")

    except Exception as e:
        print(f"Error processing URL {url}: {e}")
import time

def scrape_and_report():
    url = "https://groupsor.link/group/invitemore"
    params = {
        'group_no': 0,
        'gcid': '7',
        'cid': '29',
        'lid': '11',
        'gpid': ''
    }

    try:
        start_time = time.time()
        while time.time() - start_time < 5:  # Run for 20 seconds
            response = requests.post(url, data=params)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            links = []
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and href.startswith('https://groupsor.link/group/invite/') and href not in links:
                    links.append(href)
                if len(links) == 2:
                    break

            skipped_urls = load_skipped_urls("not_to_report.txt")
            filtered_links = [link for link in links if link not in skipped_urls]

            # Use ThreadPoolExecutor to send reports concurrently
            with requests.Session() as client, ThreadPoolExecutor(max_workers=len(filtered_links)) as executor:
                futures = [executor.submit(report_group, client, link) for link in filtered_links]
                for future in futures:
                    future.result()  # Wait for each future to complete

            #print("Scraping and reporting cycle completed.")

        # Sleep for 10 seconds after the 20-second run
        print("Sleeping for 15 seconds...")
        time.sleep(0)

    except requests.HTTPError as e:
        print(f"HTTP error while fetching initial URL: {e}")
    except requests.RequestException as e:
        print(f"Request error while fetching initial URL: {e}")
    except Exception as e:
        print(f"Unexpected error while fetching initial URL: {e}")

if __name__ == "__main__":
    while True:
        scrape_and_report()
        print("Cycle complete. Starting the next cycle...")
