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

    # Check for Server and X-Powered-By headers
    for header in ['Server', 'X-Powered-By']:
        if header in headers:
            print(Fore.RED + f"The header {header} is present, which can reveal information about the server software and its version." + Style.RESET_ALL)

    # Check Content-Type header
    if 'Content-Type' not in headers or ';' not in headers['Content-Type']:
        print(Fore.RED + "The Content-Type header is missing or does not contain a charset. This could potentially lead to security vulnerabilities." + Style.RESET_ALL)

    # Check cookies for Secure and HttpOnly flags
    if 'Set-Cookie' in headers:
        if 'Secure' not in headers['Set-Cookie']:
            print(Fore.RED + "A Set-Cookie header lacks the 'Secure' flag. The Secure flag should be set to ensure that the cookie is only sent over HTTPS." + Style.RESET_ALL)
        if 'HttpOnly' not in headers['Set-Cookie']:
            print(Fore.RED + "A Set-Cookie header lacks the 'HttpOnly' flag. The HttpOnly flag should be set to prevent the cookie from being accessed through client-side scripts." + Style.RESET_ALL)
