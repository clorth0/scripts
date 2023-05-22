import requests
from colorama import Fore, init

SECURITY_HEADERS = [
    'Strict-Transport-Security',
    'X-Frame-Options',
    'X-Content-Type-Options',
    'Content-Security-Policy',
    'X-Permitted-Cross-Domain-Policies',
    'Referrer-Policy',
    'Clear-Site-Data',
    'Cross-Origin-Embedder-Policy',
    'Cross-Origin-Opener-Policy',
    'Cross-Origin-Resource-Policy',
    'Cache-Control',
]

def check_headers(target):
    try:
        response = requests.get(target)
    except requests.exceptions.SSLError as e:
        print(Fore.RED + "Unable to make a request due to SSL Error: ")
        print(e)
        return
    
    headers = response.headers
    for header in SECURITY_HEADERS:
        print(Fore.GREEN + header, end=": ")
        if header in headers:
            print(Fore.GREEN + "Present")
        else:
            print(Fore.RED + "Missing")

if __name__ == "__main__":
    init(autoreset=True)  # initialize colorama
    target = 'https://example.com'  # replace with your target
    check_headers(target)
