import requests
from colorama import Fore, init

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
    try:
        response = requests.get(target)
    except requests.exceptions.SSLError as e:
        print(Fore.RED + "Unable to make a request due to SSL Error: ")
        print(e)
        return
    
    headers = response.headers
    print(Fore.GREEN + "Full headers: ")
    for h, v in headers.items():
        print(Fore.GREEN + f"{h}: {v}")
    print(Fore.RESET)

    for header, risk in SECURITY_HEADERS.items():
        print(Fore.GREEN + header, end=": ")
        if header in headers:
            print(Fore.GREEN + "Present")
        else:
            print(Fore.RED + "Missing")
            print(Fore.RED + "Risk: ", risk)

if __name__ == "__main__":
    init(autoreset=True)  # initialize colorama
    target = 'https://example.com'  # replace with your target
    check_headers(target)
