import requests
from colorama import Fore, init
import argparse

# Define the security headers and their associated risks
SECURITY_HEADERS = {
    'Strict-Transport-Security': "Missing this header can expose the website to downgrade attacks, SSL stripping and cookie hijacking.",
    'X-Frame-Options': "Without this header, your website could be at risk of clickjacking attacks.",
    'X-Content-Type-Options': "Missing this header can lead to attacks such as MIME sniffing.",
    'Content-Security-Policy': "If this header is missing, your website is more susceptible to cross-site scripting (XSS) attacks.",
    'X-Permitted-Cross-Domain-Policies': "Missing this header can allow data loading from unknown sources, potentially leading to data theft.",
    'Referrer-Policy': "Without this header, browsers can send full URL of the previous page leading to possible data leakage.",
    'Clear-Site-Data': "Missing this header could allow data to persist in the browser, leading to data leakage.",
    'Cross-Origin-Embedder-Policy': "Without this header, the website may be vulnerable to attacks involving loading of resources.",
    'Cross-Origin-Opener-Policy': "Without this header, your website could be at risk of tab-nabbing attacks.",
    'Cross-Origin-Resource-Policy': "Missing this header can lead to unauthorized loading of resources.",
    'Cache-Control': "Without proper cache control, sensitive data can be stored by intermediaries or browser caches."
}

def check_headers(target):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(target, headers=headers, timeout=10)
    except requests.RequestException as e:
        print(Fore.RED + "Request failed: ", e)
        return

    # Print headers
    print(Fore.GREEN + "Full headers: ")
    for h, v in response.headers.items():
        print(Fore.GREEN + f"{h}: {v}")
    print(Fore.RESET)

    # Check for security headers
    for header, risk in SECURITY_HEADERS.items():
        print(Fore.GREEN + header, end=": ")
        if header in response.headers:
            print(Fore.GREEN + "Present")
        else:
            print(Fore.RED + "Missing")
            print(Fore.RED + "Risk: ", risk)

if __name__ == "__main__":
    init(autoreset=True)  # initialize colorama

    parser = argparse.ArgumentParser(description='Check security headers of a website.')
    parser.add_argument('url', help='URL of the website to check')
    args = parser.parse_args()

    check_headers(args.url)
