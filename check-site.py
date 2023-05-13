import argparse
import subprocess
import sys
import pkg_resources
import requests
import ssl
import socket
from urllib.parse import urlparse
from datetime import datetime

REQUIRED_PACKAGES = [
    'requests',
    'beautifulsoup4',
    'colorama',
]

for package in REQUIRED_PACKAGES:
    try:
        dist = pkg_resources.get_distribution(package)
        print('{} ({}) is installed'.format(dist.key, dist.version))
    except pkg_resources.DistributionNotFound:
        print('{} is NOT installed'.format(package))
        subprocess.call([sys.executable, "-m", "pip", "install", package])

from colorama import Fore, Style

SECURITY_HEADERS = [
    'Strict-Transport-Security',
    'Content-Security-Policy',
    'X-Content-Type-Options',
    'X-Frame-Options',
    'X-XSS-Protection',
]

def check_ssl(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme != "https":
        print(Fore.RED + "The website is not using HTTPS. All websites should use HTTPS to ensure data integrity, confidentiality, and authenticity." + Style.RESET_ALL)
    else:
        hostname = parsed_url.hostname
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
            s.connect((hostname, 443))
            cert = s.getpeercert()

        # Check SSL expiration
        not_after = datetime.strptime(cert['notAfter'], r'%b %d %H:%M:%S %Y %Z')
        if datetime.now() > not_after:
            print(Fore.RED + "The SSL certificate has expired." + Style.RESET_ALL)

def check_headers(url):
    response = requests.get(url)
    headers = response.headers

    print("Checking headers:")
    for header, value in headers.items():
        print(f"{header}: {value}")
    
    missing_headers = [header for header in SECURITY_HEADERS if header not in headers]
    for header in missing_headers:
        if header == 'Strict-Transport-Security':
            print(Fore.RED + "The Strict-Transport-Security header is missing. This is a serious security risk as it allows connections over HTTP." + Style.RESET_ALL)
        else:
            print(Fore.RED + f"The header {header} is missing. This could potentially lead to security vulnerabilities." + Style.RESET_ALL)

def check_website(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = "https://" + url
    check_ssl(url)
    check_headers(url)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check the security of a website.")
    parser.add_argument("url", help="The URL of the website to check.")
    args = parser.parse_args()
    
    check_website(args.url)
